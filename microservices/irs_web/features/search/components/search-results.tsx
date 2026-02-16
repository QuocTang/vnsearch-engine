import { ArticleModel } from "../models/article.model";
import { ArticleCard } from "./article-card";
import { LoadingState } from "./loading-state";
import { EmptyState } from "./empty-state";
import { ErrorState } from "./error-state";

/**
 * Search Results Component
 * Container cho danh sách article cards
 */
interface SearchResultsProps {
  results: ArticleModel[];
  isLoading?: boolean;
  isError?: boolean;
  onRetry?: () => void;
  errorMessage?: string;
}

export function SearchResults({
  results,
  isLoading,
  isError,
  onRetry,
  errorMessage,
}: SearchResultsProps) {
  // Loading state
  if (isLoading) {
    return <LoadingState count={6} />;
  }

  // Error state
  if (isError) {
    return <ErrorState onRetry={onRetry} message={errorMessage} />;
  }

  // Empty state
  if (results.length === 0) {
    return <EmptyState />;
  }

  // Results grid
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {results.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
}
