import { HttpClient } from "@/core/http/http-client";
import { API_ENDPOINTS } from "../config";
import type { SearchRequest, SearchResponse, HealthResponse } from "../types";

/**
 * Fetch Health Check Status
 */
export const fetchHealthCheck = async () => {
  const { data } = await HttpClient.get<HealthResponse>(API_ENDPOINTS.health);
  return data;
};

/**
 * Search Articles
 */
export const searchArticles = async (payload: SearchRequest) => {
  const { data } = await HttpClient.post<SearchResponse>(
    API_ENDPOINTS.search,
    payload,
  );
  return data;
};
