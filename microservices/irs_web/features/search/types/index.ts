/**
 * Search Feature TypeScript Types
 * Based on IRS API v1.0.0
 */

// ============================================
// Health Check
// ============================================

export interface HealthResponse {
  status: "healthy" | "unhealthy";
  qdrant_connected: boolean;
  model_loaded: boolean;
}

// ============================================
// Search Request/Response
// ============================================

export interface SearchRequest {
  query: string;
  limit?: number;
  category_filter?: string;
}

export interface SearchResponse {
  query: string;
  processed_query: string;
  total_results: number;
  execution_time_ms: number;
  results: ArticleResult[];
}

export interface ArticleResult {
  id: number;
  score: number;
  article_id: number;
  title: string;
  summary: string;
  url: string;
  category_name: string;
  comment_count: number;
}

// ============================================
// Categories
// ============================================

export type CategoryName =
  | "Khoa học"
  | "Ý kiến"
  | "Giáo dục"
  | "Sức khỏe"
  | "Thời sự"
  | "Giải trí"
  | "Đời sống";

// ============================================
// Search Criteria (Client-side)
// ============================================

export interface SearchCriteria {
  query: string;
  limit: number;
  category?: CategoryName;
}
