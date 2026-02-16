"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { X, Search, Loader2 } from "lucide-react";

/**
 * Search Bar Component
 * Input tìm kiếm chính với validation và character counter
 */
interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
  defaultValue?: string;
}

export function SearchBar({
  onSearch,
  isLoading = false,
  defaultValue = "",
}: SearchBarProps) {
  const [query, setQuery] = useState(defaultValue);
  const charCount = query.length;
  const maxChars = 500;
  const isValid = charCount >= 1 && charCount <= maxChars;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isValid && !isLoading) {
      onSearch(query.trim());
    }
  };

  const handleClear = () => {
    setQuery("");
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
      <div className="relative">
        <div className="relative">
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Tìm kiếm bài viết..."
            className="h-14 pr-24 text-lg"
            disabled={isLoading}
          />

          {/* Clear Button */}
          {query && !isLoading && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={handleClear}
              className="absolute right-16 top-1/2 -translate-y-1/2"
            >
              <X className="h-4 w-4" />
            </Button>
          )}

          {/* Search/Loading Button */}
          <Button
            type="submit"
            size="sm"
            disabled={!isValid || isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Search className="h-4 w-4" />
            )}
          </Button>
        </div>

        {/* Character Counter */}
        <div className="flex items-center justify-between mt-2 px-1">
          <div className="text-sm text-muted-foreground">
            {!isValid && charCount > 0 && (
              <span className="text-destructive">
                {charCount < 1 ? "Nhập ít nhất 1 ký tự" : "Vượt quá 500 ký tự"}
              </span>
            )}
          </div>
          <div
            className={`text-sm ${
              charCount > maxChars
                ? "text-destructive"
                : "text-muted-foreground"
            }`}
          >
            {charCount}/{maxChars}
          </div>
        </div>
      </div>
    </form>
  );
}
