import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useDebounceValue } from "usehooks-ts";
import { useSearchMutation } from "./use-search";
import { useFilters } from "./use-filters";
import { ArticleModel } from "../models/article.model";
import type { CategoryName } from "../types";

export function useSearchLogic() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [results, setResults] = useState<ArticleModel[]>([]);
  const [executionTime, setExecutionTime] = useState<number>(0);
  const [isSearched, setIsSearched] = useState(false);
  const [totalResults, setTotalResults] = useState(0);

  // Filters hook
  const { category, limit, setCategory, setLimit, clearFilters } = useFilters();

  // Debounce query to avoid spamming API
  const [debouncedQuery] = useDebounceValue(query, 300);

  // API Mutation
  const searchMutation = useSearchMutation();

  // Perform search
  const performSearch = async (
    searchQuery: string,
    currentLimit: number,
    currentCategory?: CategoryName,
  ) => {
    if (!searchQuery.trim()) {
      setResults([]);
      setIsSearched(false);
      return;
    }

    setIsSearched(true);

    try {
      const data = await searchMutation.mutateAsync({
        query: searchQuery,
        limit: currentLimit,
        category_filter: currentCategory,
      });

      // Transform raw results to ArticleModel
      const models = data.results.map((item) => new ArticleModel(item));
      setResults(models);
      setExecutionTime(data.execution_time_ms);
      setTotalResults(data.total_results);
    } catch (error) {
      console.error("Search failed:", error);
      setResults([]);
    }
  };

  // Sync URL with query
  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString());
    const currentQ = params.get("q") || "";

    // Only update URL if query has changed
    if (debouncedQuery !== currentQ) {
      if (debouncedQuery) {
        params.set("q", debouncedQuery);
      } else {
        params.delete("q");
      }
      router.replace(`?${params.toString()}`, { scroll: false });
    }
  }, [debouncedQuery, router, searchParams]);

  // Trigger search when debounced query or filters change
  useEffect(() => {
    if (debouncedQuery) {
      performSearch(debouncedQuery, limit, category);
    }
  }, [debouncedQuery, limit, category]);

  // Handle manual search (e.g. Enter key)
  const handleSearch = (newQuery: string) => {
    setQuery(newQuery);
  };

  const handleRetry = () => {
    if (query) {
      performSearch(query, limit, category);
    }
  };

  return {
    // State
    query,
    results,
    isSearched,
    isLoading: searchMutation.isPending,
    isError: searchMutation.isError,
    errorMessage: searchMutation.error?.message,
    executionTime,
    totalResults,

    // Filters
    category,
    limit,

    // Handlers
    handleSearch,
    handleCategoryChange: setCategory,
    handleLimitChange: setLimit,
    handleClearFilters: clearFilters,
    handleRetry,
  };
}
