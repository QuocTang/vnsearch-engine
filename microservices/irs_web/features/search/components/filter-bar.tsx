"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { CATEGORIES, UI_CONFIG } from "../config";
import type { CategoryName } from "../types";
import { X, Filter } from "lucide-react";
import { useState } from "react";

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
  const [open, setOpen] = useState(false);

  // Common Filter Content
  const FilterContent = () => (
    <div className="flex flex-col md:flex-row gap-4">
      {/* Category Select */}
      <div className="flex flex-col md:flex-row md:items-center gap-2">
        <span className="text-sm font-medium">Danh mục:</span>
        <Select
          value={category || "all"}
          onValueChange={(value) =>
            onCategoryChange(
              value === "all" ? undefined : (value as CategoryName),
            )
          }
        >
          <SelectTrigger className="w-full md:w-[180px]">
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
      <div className="flex flex-col md:flex-row md:items-center gap-2">
        <span className="text-sm font-medium">Kết quả:</span>
        <Select
          value={limit.toString()}
          onValueChange={(value) => onLimitChange(Number(value))}
        >
          <SelectTrigger className="w-full md:w-[100px]">
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

      {/* Clear Filters (Desktop only here, Mobile has its own) */}
      {hasFilters && (
        <Button
          variant="ghost"
          size="sm"
          onClick={onClearFilters}
          className="ml-auto hidden md:flex"
        >
          <X className="h-4 w-4 mr-1" />
          Xóa bộ lọc
        </Button>
      )}
    </div>
  );

  return (
    <div className="flex items-center justify-between p-4 border rounded-lg bg-muted/50">
      {/* Desktop View */}
      <div className="hidden md:block w-full">
        <FilterContent />
      </div>

      {/* Mobile View */}
      <div className="md:hidden flex items-center justify-between w-full">
        <span className="text-sm font-medium text-muted-foreground">
          {hasFilters ? "Đang lọc kết quả" : "Tùy chọn tìm kiếm"}
        </span>
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Bộ lọc
              {hasFilters && (
                <span className="ml-1 flex h-2 w-2 rounded-full bg-primary" />
              )}
            </Button>
          </SheetTrigger>
          <SheetContent side="bottom">
            <SheetHeader className="mb-4">
              <SheetTitle>Bộ lọc tìm kiếm</SheetTitle>
              <SheetDescription>
                Tùy chỉnh kết quả tìm kiếm theo nhu cầu của bạn.
              </SheetDescription>
            </SheetHeader>
            <div className="space-y-6 px-4 pb-4">
              <FilterContent />
              {hasFilters && (
                <Button
                  variant="destructive"
                  className="w-full"
                  onClick={() => {
                    onClearFilters();
                    setOpen(false);
                  }}
                >
                  Xóa tất cả bộ lọc
                </Button>
              )}
              <Button className="w-full" onClick={() => setOpen(false)}>
                Áp dụng
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </div>
  );
}
