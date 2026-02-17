"use client";

import { useState } from "react";
import {
  SearchBar,
  SearchResults,
  FilterBar,
  ResultsHeader,
  ArticleModel,
} from "@/features/search";
import { HeroBackground } from "@/components/three/hero-background";
import type { CategoryName } from "@/features/search";

/**
 * Home Page - IRS Search
 * Demo page để test các components đã tạo
 */

// Mock data để demo
const MOCK_ARTICLES: ArticleModel[] = [
  new ArticleModel({
    id: 1,
    score: 0.85,
    article_id: 123456,
    title: "Những chính sách khoa học công nghệ được kỳ vọng năm 2025",
    summary:
      "Năm 2025, Chính phủ, Bộ Khoa học và Công nghệ xác định ưu tiên phát triển các ngành công nghiệp mũi nhọn, đẩy mạnh đổi mới sáng tạo...",
    url: "https://vnexpress.net/",
    category_name: "Khoa học",
    comment_count: 12,
  }),
  new ArticleModel({
    id: 2,
    score: 0.75,
    article_id: 234567,
    title: "Trái đắng kiếm sống nhờ xe ôm công nghệ",
    summary:
      "Cứ nghĩ chạy xe ôm công nghệ dễ kiếm tiền nhưng nhiều tài xế nhận ra thu nhập không ổn định...",
    url: "https://vnexpress.net/",
    category_name: "Ý kiến",
    comment_count: 36,
  }),
  new ArticleModel({
    id: 3,
    score: 0.92,
    article_id: 345678,
    title: "Giáo dục STEM - xu hướng tất yếu trong kỷ nguyên số",
    summary:
      "Giáo dục STEM (Khoa học, Công nghệ, Kỹ thuật, Toán học) đang trở thành xu hướng giáo dục hiện đại...",
    url: "https://vnexpress.net/",
    category_name: "Giáo dục",
    comment_count: 8,
  }),
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<ArticleModel[]>([]);
  const [category, setCategory] = useState<CategoryName>();
  const [limit, setLimit] = useState(10);
  const [isSearched, setIsSearched] = useState(false);

  const handleSearch = (searchQuery: string) => {
    setQuery(searchQuery);
    setIsSearched(true);
    // Mock search - filter articles by query
    const filtered = MOCK_ARTICLES.filter((article) =>
      article.title.toLowerCase().includes(searchQuery.toLowerCase()),
    );
    setResults(filtered);
  };

  const handleCategoryChange = (newCategory?: CategoryName) => {
    setCategory(newCategory);
  };

  const handleLimitChange = (newLimit: number) => {
    setLimit(newLimit);
  };

  const handleClearFilters = () => {
    setCategory(undefined);
    setLimit(10);
  };

  return (
    <div className="container py-8">
      {/* Hero Section với Search Bar */}
      {/* Hero Section với Search Bar */}
      <section className="relative py-12 text-center">
        <HeroBackground />
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-4">IRS Search</h1>
          <p className="text-lg text-muted-foreground mb-8">
            Tìm kiếm semantic cho bài viết tiếng Việt
          </p>
          <SearchBar onSearch={handleSearch} isLoading={false} />
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
              totalResults={results.length}
              executionTime={125}
            />
          )}

          {/* Results Grid */}
          <SearchResults results={results} isLoading={false} isError={false} />
        </section>
      )}

      {/* Initial State - Before Search */}
      {!isSearched && (
        <section className="py-12 text-center text-muted-foreground">
          <p>Nhập từ khóa để bắt đầu tìm kiếm...</p>
        </section>
      )}
    </div>
  );
}
