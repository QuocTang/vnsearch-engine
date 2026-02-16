/**
 * Search Feature Public API
 * Exports for other modules to use
 */

// Types
export type {
  SearchRequest,
  SearchResponse,
  ArticleResult,
  CategoryName,
} from "./types";

// Models
export { ArticleModel } from "./models/article.model";

// Config & Constants
export {
  CATEGORIES,
  SEARCH_CONFIG,
  UI_CONFIG,
  SEARCH_QUERY_KEYS,
} from "./config";

// Services (nếu cần expose)
export * from "./services/search.service";

// Hooks (sẽ export sau khi tạo)
// export { useSearch } from "./hooks/use-search";
