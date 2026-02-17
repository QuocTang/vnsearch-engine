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

export const CATEGORY_COLORS: Record<CategoryName, string> = {
  "Khoa học":
    "bg-blue-500/10 text-blue-700 border-blue-200 dark:text-blue-400 dark:border-blue-800",
  "Ý kiến":
    "bg-purple-500/10 text-purple-700 border-purple-200 dark:text-purple-400 dark:border-purple-800",
  "Giáo dục":
    "bg-green-500/10 text-green-700 border-green-200 dark:text-green-400 dark:border-green-800",
  "Sức khỏe":
    "bg-red-500/10 text-red-700 border-red-200 dark:text-red-400 dark:border-red-800",
  "Thời sự":
    "bg-orange-500/10 text-orange-700 border-orange-200 dark:text-orange-400 dark:border-orange-800",
  "Giải trí":
    "bg-pink-500/10 text-pink-700 border-pink-200 dark:text-pink-400 dark:border-pink-800",
  "Đời sống":
    "bg-yellow-500/10 text-yellow-700 border-yellow-200 dark:text-yellow-400 dark:border-yellow-800",
};

export const DEFAULT_CATEGORY_COLOR =
  "bg-gray-500/10 text-gray-700 border-gray-200 dark:text-gray-400 dark:border-gray-800";

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
