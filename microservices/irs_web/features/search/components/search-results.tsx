import { ArticleModel } from "../models/article.model";
import { ArticleCard } from "./article-card";
import { LoadingState } from "./loading-state";
import { EmptyState } from "./empty-state";
import { ErrorState } from "./error-state";
import { motion } from "framer-motion";

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
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid gap-4 md:grid-cols-2 lg:grid-cols-3"
    >
      {results.map((article) => (
        <motion.div key={article.id} variants={item}>
          <ArticleCard article={article} />
        </motion.div>
      ))}
    </motion.div>
  );
}
