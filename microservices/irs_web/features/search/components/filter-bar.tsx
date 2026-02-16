"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { CATEGORIES, UI_CONFIG } from "../config";
import type { CategoryName } from "../types";
import { X } from "lucide-react";

/**
 * Filter Bar Component
 * Category select và limit control
 */
interface FilterBarProps {
  category?: CategoryName;
  limit: number;
  onCategoryChange: (category?: CategoryName) => void;
  onLimitChange: (limit: number) => void;
  onClearFilters: () => void;
}

export function FilterBar({
  category,
  limit,
  onCategoryChange,
  onLimitChange,
  onClearFilters,
}: FilterBarProps) {
  const hasFilters = category !== undefined;

  return (
    <div className="flex flex-wrap items-center gap-4 p-4 border rounded-lg bg-muted/50">
      {/* Category Select */}
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium">Danh mục:</span>
        <Select
          value={category || "all"}
          onValueChange={(value) =>
            onCategoryChange(
              value === "all" ? undefined : (value as CategoryName),
            )
          }
        >
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Tất cả" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tất cả</SelectItem>
            {CATEGORIES.map((cat) => (
              <SelectItem key={cat} value={cat}>
                {cat}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Limit Select */}
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium">Kết quả:</span>
        <Select
          value={limit.toString()}
          onValueChange={(value) => onLimitChange(Number(value))}
        >
          <SelectTrigger className="w-[100px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {UI_CONFIG.RESULTS_PER_PAGE.map((num) => (
              <SelectItem key={num} value={num.toString()}>
                {num}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Clear Filters */}
      {hasFilters && (
        <Button
          variant="ghost"
          size="sm"
          onClick={onClearFilters}
          className="ml-auto"
        >
          <X className="h-4 w-4 mr-1" />
          Xóa bộ lọc
        </Button>
      )}
    </div>
  );
}
