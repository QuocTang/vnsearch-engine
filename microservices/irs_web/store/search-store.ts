import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { CategoryName } from "@/features/search/types";

/**
 * Global Search Store
 * State management cho search history và filters
 */

interface SearchHistoryItem {
  query: string;
  timestamp: number;
}

interface SearchFilters {
  category?: CategoryName;
  limit: number;
}

interface SearchStoreState {
  // History
  history: SearchHistoryItem[];
  addToHistory: (query: string) => void;
  removeFromHistory: (query: string) => void;
  clearHistory: () => void;

  // Filters
  filters: SearchFilters;
  setCategory: (category?: CategoryName) => void;
  setLimit: (limit: number) => void;
  resetFilters: () => void;
}

const DEFAULT_FILTERS: SearchFilters = {
  limit: 10,
};

const MAX_HISTORY = 10;

export const useSearchStore = create<SearchStoreState>()(
  persist(
    (set, get) => ({
      history: [],
      addToHistory: (query) => {
        const trimmed = query.trim();
        if (!trimmed) return;
        const state = get();
        const filtered = state.history.filter((item) => item.query !== trimmed);
        const newHistory = [
          { query: trimmed, timestamp: Date.now() },
          ...filtered,
        ].slice(0, MAX_HISTORY);
        set({ history: newHistory });
      },
      removeFromHistory: (query) => {
        set((state) => ({
          history: state.history.filter((item) => item.query !== query),
        }));
      },
      clearHistory: () => set({ history: [] }),

      filters: DEFAULT_FILTERS,
      setCategory: (category) =>
        set((state) => ({ filters: { ...state.filters, category } })),
      setLimit: (limit) =>
        set((state) => ({ filters: { ...state.filters, limit } })),
      resetFilters: () => set({ filters: DEFAULT_FILTERS }),
    }),
    {
      name: "search-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        history: state.history,
        filters: state.filters,
      }),
    },
  ),
);
