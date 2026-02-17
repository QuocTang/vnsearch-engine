"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState, useRef, useEffect } from "react";
import { X, Search, Loader2 } from "lucide-react";
import { HistoryList } from "./history-list";
import { useOnClickOutside } from "usehooks-ts";

/**
 * Search Bar Component
 * Input tìm kiếm chính với validation và character counter
 */
interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
  defaultValue?: string;
  history?: { query: string; timestamp: number }[];
  onClearHistory?: () => void;
  onRemoveHistoryItem?: (query: string) => void;
}

export function SearchBar({
  onSearch,
  isLoading = false,
  defaultValue = "",
  history = [],
  onClearHistory,
  onRemoveHistoryItem,
}: SearchBarProps) {
  const [query, setQuery] = useState(defaultValue);
  const [isFocused, setIsFocused] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const charCount = query.length;
  const maxChars = 500;
  const isValid = charCount >= 1 && charCount <= maxChars;

  useOnClickOutside(containerRef as React.RefObject<HTMLElement>, () =>
    setIsFocused(false),
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isValid && !isLoading) {
      onSearch(query.trim());
      setIsFocused(false);
    }
  };

  const handleClear = () => {
    setQuery("");
    setIsFocused(true);
  };

  const handleHistorySelect = (selectedQuery: string) => {
    setQuery(selectedQuery);
    onSearch(selectedQuery);
    setIsFocused(false);
  };

  return (
    <div ref={containerRef} className="w-full max-w-3xl mx-auto relative">
      <form onSubmit={handleSubmit} className="relative z-20">
        <div className="relative">
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsFocused(true)}
            placeholder="Tìm kiếm bài viết..."
            className="h-14 pr-24 text-lg bg-background"
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
      </form>

      {/* History Dropdown */}
      {isFocused && history.length > 0 && !query && (
        <HistoryList
          history={history}
          onSelect={handleHistorySelect}
          onDelete={(q) => onRemoveHistoryItem?.(q)}
          onClear={() => onClearHistory?.()}
        />
      )}

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
            charCount > maxChars ? "text-destructive" : "text-muted-foreground"
          }`}
        >
          {charCount}/{maxChars}
        </div>
      </div>
    </div>
  );
}
