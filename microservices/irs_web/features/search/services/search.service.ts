import { HttpClient } from "@/core/http/http-client";
import { SEARCH_APIS } from "../config";
import type { SearchRequest, SearchResponse, HealthResponse } from "../types";

/**
 * Search Feature Services
 * Pure IO layer - no logic, no transformation
 */

// ============================================
// Health Check
// ============================================

export const fetchHealth = async (): Promise<HealthResponse> => {
  const response = await HttpClient.get(SEARCH_APIS.health);
  return response.data; // Return RAW data
};

// ============================================
// Search
// ============================================

export const fetchSearchResults = async (
  request: SearchRequest,
): Promise<SearchResponse> => {
  const response = await HttpClient.post(SEARCH_APIS.search, request);
  return response.data; // Return RAW data
};
