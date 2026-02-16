"""
Qdrant vector database service.
Handles connection, indexing, and searching in Qdrant.
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
import numpy as np


class QdrantService:
    """
    Qdrant vector database service for vector storage and search.
    """
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        """
        Initialize Qdrant client.
        
        Args:
            host: Qdrant server host
            port: Qdrant server port
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name: Optional[str] = None
    
    def health_check(self) -> bool:
        """
        Check if Qdrant server is healthy.
        
        Returns:
            bool: True if healthy
        """
        try:
            # Try to list collections
            self.client.get_collections()
            return True
        except Exception:
            return False
    
    def create_collection(
        self,
        collection_name: str,
        vector_dimension: int,
        distance: Distance = Distance.COSINE
    ) -> None:
        """
        Create Qdrant collection.
        
        Args:
            collection_name: Name of collection
            vector_dimension: Dimension of vectors
            distance: Distance metric (COSINE, EUCLID, DOT)
        """
        # Delete if exists
        if self.client.collection_exists(collection_name):
            self.client.delete_collection(collection_name)
        
        # Create new collection
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_dimension,
                distance=distance
            )
        )
        
        self.collection_name = collection_name
    
    def upsert_vectors(
        self,
        collection_name: str,
        ids: List[int],
        vectors: np.ndarray,
        payloads: List[Dict[str, Any]]
    ) -> None:
        """
        Upsert vectors with payloads to collection.
        
        Args:
            collection_name: Name of collection
            ids: List of point IDs
            vectors: Array of vectors (N x D)
            payloads: List of payload dictionaries
        """
        points = [
            PointStruct(
                id=int(point_id),
                vector=vector.tolist(),
                payload=payload
            )
            for point_id, vector, payload in zip(ids, vectors, payloads)
        ]
        
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=collection_name,
                points=batch
            )
    
    def search(
        self,
        collection_name: str,
        query_vector: np.ndarray,
        limit: int = 10,
        category_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in collection.
        
        Args:
            collection_name: Name of collection
            query_vector: Query vector (1D array)
            limit: Number of results to return
            category_filter: Optional category name to filter by
            
        Returns:
            List[Dict]: List of search results with score and payload
        """
        # Build filter if category specified
        query_filter = None
        if category_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category_name",
                        match=MatchValue(value=category_filter)
                    )
                ]
            )
        
        # Query points using new API
        search_results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector.tolist(),
            limit=limit,
            query_filter=query_filter
        )
        
        # Format results
        results = []
        for hit in search_results.points:
            result = {
                "id": hit.id,
                "score": hit.score,
                **hit.payload
            }
            results.append(result)
        
        return results
    
    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Get collection information.
        
        Args:
            collection_name: Name of collection
            
        Returns:
            Dict: Collection info
        """
        info = self.client.get_collection(collection_name)
        return {
            "points_count": info.points_count if hasattr(info, 'points_count') else 0,
            "status": info.status if hasattr(info, 'status') else "unknown"
        }
