#!/usr/bin/env python3
"""
Initial Data Ingestion Script
Run this script to perform initial data ingestion into Qdrant.

Usage:
    python scripts/initial_ingest.py
    
    or with uv:
    uv run python scripts/initial_ingest.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.ingestion_service import IngestionService


def main():
    """Run initial data ingestion."""
    print("\n" + "=" * 70)
    print("IRS API - Initial Data Ingestion")
    print("=" * 70 + "\n")
    
    try:
        # Create ingestion service
        ingestion_service = IngestionService()
        
        # Run full ingestion
        stats = ingestion_service.run_full_ingestion()
        
        # Print summary
        print("\n" + "=" * 70)
        print("INGESTION SUMMARY")
        print("=" * 70)
        print(f"Status: {stats['status']}")
        print(f"Articles indexed: {stats['articles_count']}")
        print(f"Vector dimension: {stats['vector_dimension']}")
        print(f"Qdrant collection: {stats['qdrant_collection']}")
        print(f"Qdrant points: {stats['qdrant_points']}")
        print(f"Unique categories: {stats['categories']}")
        print(f"Model saved to: {stats['model_path']}")
        print("=" * 70 + "\n")
        
        print("✅ Ingestion completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
