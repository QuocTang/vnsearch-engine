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

// Components
export { SearchBar } from "./components/search-bar";
export { SearchResults } from "./components/search-results";
export { ArticleCard } from "./components/article-card";
export { FilterBar } from "./components/filter-bar";
export { ResultsHeader } from "./components/results-header";
export { LoadingState } from "./components/loading-state";
export { EmptyState } from "./components/empty-state";
export { ErrorState } from "./components/error-state";

// Main Component
export { SearchFeature } from "./components/search-feature";

// Hooks
export * from "./hooks/use-search-logic";
export * from "./hooks/use-filters";
// export { useSearch } from "./hooks/use-search";
