import { z } from "zod";
import { SEARCH_CONFIG } from "./config";

/**
 * Search Form Validation Schema
 */

export const searchFormSchema = z.object({
  query: z
    .string()
    .min(SEARCH_CONFIG.MIN_QUERY_LENGTH, "Nhập ít nhất 1 ký tự")
    .max(SEARCH_CONFIG.MAX_QUERY_LENGTH, "Tối đa 500 ký tự"),
  limit: z
    .number()
    .int()
    .min(SEARCH_CONFIG.MIN_LIMIT)
    .max(SEARCH_CONFIG.MAX_LIMIT)
    .default(SEARCH_CONFIG.DEFAULT_LIMIT)
    .optional(),
  category_filter: z.string().optional(),
});

export type SearchFormValues = z.infer<typeof searchFormSchema>;
