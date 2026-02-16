"""
Search endpoint - Core functionality for semantic search.
"""

import time
from fastapi import APIRouter, Depends, HTTPException
from app.models.request import SearchRequest
from app.models.response import SearchResponse, ArticleResult
from app.core.config import get_settings
from app.services.qdrant_service import QdrantService
from app.api.v1.dependencies import get_tfidf_service, get_nlp_processor

router = APIRouter()


@router.post("/search", response_model=SearchResponse, tags=["Search"])
async def search_articles(
    request: SearchRequest,
    tfidf_service = Depends(get_tfidf_service),
    nlp_processor = Depends(get_nlp_processor)
):
    """
    Search for articles using semantic similarity.
    
    Args:
        request: Search request with query, limit, and optional category filter
        
    Returns:
        SearchResponse: Search results with articles and execution time
    """
    start_time = time.time()
    settings = get_settings()
    
    try:
        # Step 1: Preprocess query with NLP
        processed_query = nlp_processor.preprocess(request.query)
        
        if not processed_query or not processed_query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query không có từ khóa hợp lệ sau khi xử lý (có thể toàn stopwords)"
            )
        
        # Step 2: Transform to vector using TF-IDF
        if not tfidf_service.is_fitted:
            raise HTTPException(
                status_code=503,
                detail="TF-IDF model chưa được train. Vui lòng chạy ingestion trước."
            )
        
        query_vector = tfidf_service.transform([processed_query])[0]
        
        # Step 3: Search in Qdrant
        qdrant = QdrantService(settings.qdrant_host, settings.qdrant_port)
        
        search_results = qdrant.search(
            collection_name=settings.qdrant_collection_name,
            query_vector=query_vector,
            limit=request.limit,
            category_filter=request.category_filter
        )
        
        # Step 4: Format results
        articles = [
            ArticleResult(
                id=result["id"],
                score=result["score"],
                article_id=result["article_id"],
                title=result["title"],
                summary=result["summary"],
                url=result["url"],
                category_name=result["category_name"],
                comment_count=result["comment_count"]
            )
            for result in search_results
        ]
        
        # Calculate execution time
        execution_time_ms = (time.time() - start_time) * 1000
        
        return SearchResponse(
            query=request.query,
            processed_query=processed_query,
            total_results=len(articles),
            results=articles,
            execution_time_ms=round(execution_time_ms, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi tìm kiếm: {str(e)}"
        )
