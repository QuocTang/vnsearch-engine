import { useQuery, useMutation } from "@tanstack/react-query";
import { fetchHealthCheck, searchArticles } from "../services/search.service";
import { SEARCH_QUERY_KEYS } from "../config";
import type { SearchRequest } from "../types";

/**
 * Hook to check API Health Status
 */
export const useHealthCheck = () => {
  return useQuery({
    queryKey: SEARCH_QUERY_KEYS.health(),
    queryFn: fetchHealthCheck,
    refetchInterval: 30000,
    retry: 1,
  });
};

/**
 * Hook to search articles
 */
export const useSearchMutation = () => {
  return useMutation({
    mutationFn: (payload: SearchRequest) => searchArticles(payload),
  });
};
