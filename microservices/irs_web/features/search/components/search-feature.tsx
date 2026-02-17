"use client";

import { useSearchLogic } from "../hooks/use-search-logic";
import { SearchBar } from "./search-bar";
import { FilterBar } from "./filter-bar";
import { ResultsHeader } from "./results-header";
import { SearchResults } from "./search-results";
import { HeroBackground } from "@/components/three/hero-background";

export function SearchFeature() {
  const {
    query,
    results,
    isSearched,
    isLoading,
    isError,
    errorMessage,
    executionTime,
    totalResults,
    category,
    limit,
    handleSearch,
    handleCategoryChange,
    handleLimitChange,
    handleClearFilters,
    handleRetry,
  } = useSearchLogic();

  return (
    <>
      <section className="relative py-12 text-center">
        <HeroBackground />
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-4">IRS Search</h1>
          <p className="text-lg text-muted-foreground mb-8">
            Tìm kiếm semantic cho bài viết tiếng Việt
          </p>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </section>

      {/* Results Section */}
      {isSearched && (
        <section className="py-8 space-y-6">
          {/* Filters */}
          <FilterBar
            category={category}
            limit={limit}
            onCategoryChange={handleCategoryChange}
            onLimitChange={handleLimitChange}
            onClearFilters={handleClearFilters}
          />

          {/* Results Header */}
          {results.length > 0 && (
            <ResultsHeader
              query={query}
              totalResults={totalResults}
              executionTime={executionTime}
            />
          )}

          {/* Results Grid */}
          <SearchResults
            results={results}
            isLoading={isLoading}
            isError={isError}
            errorMessage={errorMessage}
            onRetry={handleRetry}
          />
        </section>
      )}

      {/* Initial State - Before Search */}
      {!isSearched && (
        <section className="py-12 text-center text-muted-foreground">
          <p>Nhập từ khóa để bắt đầu tìm kiếm...</p>
        </section>
      )}
    </>
  );
}
