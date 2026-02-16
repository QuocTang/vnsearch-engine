"""
Ingestion Service - Orchestrates full data ingestion pipeline.
Load Excel -> Preprocess -> Train TF-IDF -> Index to Qdrant
"""

import logging
from typing import Dict, Any
from pathlib import Path

from app.utils.excel_loader import load_excel_data, validate_dataframe
from app.utils.stopwords_loader import load_stopwords
from app.services.nlp_processor import create_nlp_processor
from app.services.tfidf_service import TFIDFService
from app.services.qdrant_service import QdrantService
from app.core.config import get_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngestionService:
    """
    Orchestrates the complete data ingestion pipeline.
    """
    
    def __init__(self):
        """Initialize ingestion service with configuration."""
        self.settings = get_settings()
        self.tfidf_service = TFIDFService()
        self.qdrant_service = QdrantService(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port
        )
        self.nlp_processor = None
        self.stats: Dict[str, Any] = {}
    
    def run_full_ingestion(self) -> Dict[str, Any]:
        """
        Run complete ingestion pipeline.
        
        Returns:
            Dict: Ingestion statistics and results
        """
        try:
            logger.info("=" * 60)
            logger.info("Starting Full Data Ingestion Pipeline")
            logger.info("=" * 60)
            
            # Step 1: Load stopwords
            logger.info("Step 1/6: Loading Vietnamese stopwords...")
            stopwords = load_stopwords(self.settings.stopwords_path)
            self.nlp_processor = create_nlp_processor(stopwords)
            logger.info(f"✅ Loaded {len(stopwords)} stopwords")
            
            # Step 2: Load Excel data
            logger.info("\nStep 2/6: Loading Excel data...")
            df = load_excel_data(
                articles_path=self.settings.excel_articles_path,
                categories_path=self.settings.excel_categories_path,
                comments_path=self.settings.excel_comments_path
            )
            logger.info(f"✅ Loaded {len(df)} articles")
            
            # Validate dataframe
            is_valid, error_msg = validate_dataframe(df)
            if not is_valid:
                raise ValueError(f"Data validation failed: {error_msg}")
            logger.info("✅ Data validation passed")
            
            # Step 3: NLP Preprocessing
            logger.info("\nStep 3/6: Preprocessing text with NLP...")
            preprocessed_texts = self.nlp_processor.preprocess_batch(
                df['full_text'].tolist()
            )
            logger.info(f"✅ Preprocessed {len(preprocessed_texts)} texts")
            
            # Step 4: Train TF-IDF
            logger.info("\nStep 4/6: Training TF-IDF model...")
            self.tfidf_service.train(
                texts=preprocessed_texts,
                max_features=5000,
                min_df=2,
                max_df=0.8
            )
            vector_dim = self.tfidf_service.get_vector_dimension()
            logger.info(f"✅ TF-IDF trained with {vector_dim} features")
            
            # Save model
            self.tfidf_service.save(self.settings.tfidf_model_path)
            logger.info(f"✅ Model saved to {self.settings.tfidf_model_path}")
            
            # Step 5: Transform to vectors
            logger.info("\nStep 5/6: Transforming texts to vectors...")
            vectors = self.tfidf_service.transform(preprocessed_texts)
            logger.info(f"✅ Generated {len(vectors)} vectors of dimension {vector_dim}")
            
            # Step 6: Index to Qdrant
            logger.info("\nStep 6/6: Indexing to Qdrant...")
            
            # Create collection
            self.qdrant_service.create_collection(
                collection_name=self.settings.qdrant_collection_name,
                vector_dimension=vector_dim
            )
            logger.info(f"✅ Created collection '{self.settings.qdrant_collection_name}'")
            
            # Prepare payloads
            payloads = []
            for _, row in df.iterrows():
                payload = {
                    "article_id": int(row['article_id']),
                    "title": str(row['title']),
                    "summary": str(row['summary']) if row['summary'] else "",
                    "url": str(row['url']) if row['url'] else "",
                    "category_name": str(row['category_name']) if row['category_name'] else "",
                    "comment_count": int(row['comment_count']),
                    "full_text": str(row['full_text'])
                }
                payloads.append(payload)
            
            # Upsert vectors - use index as ID (0-based, always positive)
            ids = list(range(len(df)))  # Use sequential IDs instead of article_id
            self.qdrant_service.upsert_vectors(
                collection_name=self.settings.qdrant_collection_name,
                ids=ids,
                vectors=vectors,
                payloads=payloads
            )
            logger.info(f"✅ Indexed {len(vectors)} vectors to Qdrant")
            
            # Get collection info
            collection_info = self.qdrant_service.get_collection_info(
                self.settings.qdrant_collection_name
            )
            
            # Compile stats
            self.stats = {
                "status": "success",
                "articles_count": len(df),
                "stopwords_count": len(stopwords),
                "vector_dimension": vector_dim,
                "qdrant_collection": self.settings.qdrant_collection_name,
                "qdrant_points": collection_info['points_count'],
                "model_path": self.settings.tfidf_model_path,
                "categories": df['category_name'].nunique()
            }
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ INGESTION COMPLETED SUCCESSFULLY")
            logger.info("=" * 60)
            logger.info(f"Articles indexed: {self.stats['articles_count']}")
            logger.info(f"Vector dimension: {self.stats['vector_dimension']}")
            logger.info(f"Qdrant points: {self.stats['qdrant_points']}")
            logger.info(f"Categories: {self.stats['categories']}")
            logger.info("=" * 60)
            
            return self.stats
            
        except Exception as e:
            logger.error(f"❌ Ingestion failed: {str(e)}")
            self.stats = {
                "status": "failed",
                "error": str(e)
            }
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get ingestion statistics."""
        return self.stats
