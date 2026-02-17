import { environment } from "@/core/environment";
import type { CategoryName } from "./types/index";

/**
 * Search Feature Configuration
 * Constants, API endpoints, và config cho search module
 */

// ============================================
// Categories
// ============================================

export const CATEGORIES: CategoryName[] = [
  "Khoa học",
  "Ý kiến",
  "Giáo dục",
  "Sức khỏe",
  "Thời sự",
  "Giải trí",
  "Đời sống",
];

// ============================================
// API Endpoints
// ============================================

export const API_ENDPOINTS = {
  search: `${environment.API_BASE_URL}/api/v1/search`,
  health: `${environment.API_BASE_URL}/`,
} as const;

// ============================================
// Search Config
// ============================================

export const SEARCH_CONFIG = {
  MIN_QUERY_LENGTH: 1,
  MAX_QUERY_LENGTH: 500,
  MIN_LIMIT: 1,
  MAX_LIMIT: 100,
  DEFAULT_LIMIT: 10,
  DEBOUNCE_MS: 300,
} as const;

// ============================================
// UI Config
// ============================================

export const UI_CONFIG = {
  RESULTS_PER_PAGE: [5, 10, 20, 50] as const,
  CARD_TITLE_MAX_LINES: 2,
  CARD_SUMMARY_MAX_LINES: 4,
} as const;

// ============================================
// React Query Keys
// ============================================

export const SEARCH_QUERY_KEYS = {
  health: () => ["search", "health"] as const,
  search: (query: string, filters?: Record<string, unknown>) =>
    ["search", "results", query, filters] as const,
} as const;
