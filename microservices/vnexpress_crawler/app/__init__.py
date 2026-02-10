"""VnExpress Crawler API Application"""

import json
import logging
from pathlib import Path
from fastapi import FastAPI
from .routers import categories, articles, health

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="VnExpress Crawler API",
        description="API to crawl data from VnExpress",
        version="0.1.0",
    )
    
    # Register routers
    app.include_router(health.router)
    app.include_router(categories.router, prefix="/api/v1/categories")
    app.include_router(articles.router, prefix="/api/v1/articles")
    
    # Generate endpoints list on startup
    @app.on_event("startup")
    def generate_endpoints_list():
        """Generate and save endpoints list to endpoints.txt"""
        endpoints_text = "VnExpress Crawler API - Endpoints\n"
        endpoints_text += "=" * 50 + "\n\n"
        
        # Get routes from app
        routes = []
        for route in app.routes:
            if hasattr(route, "methods") and hasattr(route, "path"):
                methods = ", ".join(sorted(route.methods - {"HEAD", "OPTIONS"}))
                if methods:
                    routes.append((route.path, methods))
        
        # Sort and format
        routes.sort()
        for path, methods in routes:
            endpoints_text += f"[{methods}] {path}\n"
        
        endpoints_text += "\n" + "=" * 50 + "\n"
        endpoints_text += f"Total endpoints: {len(routes)}\n\n"
        endpoints_text += "Documentation:\n"
        endpoints_text += "- Interactive Docs: http://localhost:8000/docs\n"
        endpoints_text += "- ReDoc: http://localhost:8000/redoc\n"
        
        endpoints_path = Path(__file__).parent.parent / "endpoints.txt"
        with open(endpoints_path, "w", encoding="utf-8") as f:
            f.write(endpoints_text)
        
        logger.info(f"Endpoints list generated: {endpoints_path}")
    
    return app
