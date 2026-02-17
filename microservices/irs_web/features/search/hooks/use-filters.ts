import { useState, useEffect, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import type { CategoryName } from "../types";

export interface SearchFilters {
  category?: CategoryName;
  limit: number;
}

export interface UseFiltersReturn extends SearchFilters {
  setCategory: (category?: CategoryName) => void;
  setLimit: (limit: number) => void;
  clearFilters: () => void;
}

export function useFilters(): UseFiltersReturn {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Initialize state from URL params
  const [category, setCategoryState] = useState<CategoryName | undefined>(
    (searchParams.get("category") as CategoryName) || undefined,
  );
  const [limit, setLimitState] = useState<number>(
    Number(searchParams.get("limit")) || 10,
  );

  // Sync URL when state changes
  const updateUrl = useCallback(
    (newCategory?: CategoryName, newLimit?: number) => {
      const params = new URLSearchParams(searchParams.toString());

      if (newCategory) {
        params.set("category", newCategory);
      } else {
        params.delete("category");
      }

      if (newLimit && newLimit !== 10) {
        params.set("limit", String(newLimit));
      } else {
        params.delete("limit");
      }

      router.push(`?${params.toString()}`, { scroll: false });
    },
    [router, searchParams],
  );

  const setCategory = (newCategory?: CategoryName) => {
    setCategoryState(newCategory);
    updateUrl(newCategory, limit);
  };

  const setLimit = (newLimit: number) => {
    setLimitState(newLimit);
    updateUrl(category, newLimit);
  };

  const clearFilters = () => {
    setCategoryState(undefined);
    setLimitState(10);
    // Remove params from URL
    const params = new URLSearchParams(searchParams.toString());
    params.delete("category");
    params.delete("limit");
    router.push(`?${params.toString()}`, { scroll: false });
  };

  return {
    category,
    limit,
    setCategory,
    setLimit,
    clearFilters,
  };
}
