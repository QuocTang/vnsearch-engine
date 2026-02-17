"use client";

import { History, X, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
} from "@/components/ui/command";

interface HistoryListProps {
  history: { query: string; timestamp: number }[];
  onSelect: (query: string) => void;
  onDelete: (query: string) => void;
  onClear: () => void;
}

export function HistoryList({
  history,
  onSelect,
  onDelete,
  onClear,
}: HistoryListProps) {
  if (history.length === 0) return null;

  return (
    <div className="absolute top-full left-0 right-0 z-50 mt-1 bg-popover text-popover-foreground rounded-md border shadow-md animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 duration-200">
      <div className="flex items-center justify-between px-3 py-2 border-b">
        <span className="text-xs font-medium text-muted-foreground flex items-center gap-1">
          <History className="h-3 w-3" />
          Lịch sử tìm kiếm
        </span>
        <Button
          variant="ghost"
          size="sm"
          className="h-6 px-2 text-xs text-muted-foreground hover:text-destructive"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            onClear();
          }}
        >
          <Trash2 className="h-3 w-3 mr-1" />
          Xóa tất cả
        </Button>
      </div>

      <Command className="border-none bg-transparent">
        <CommandList className="max-h-[300px] overflow-y-auto p-1">
          <CommandGroup>
            {history.map((item) => (
              <CommandItem
                key={`${item.query}-${item.timestamp}`}
                value={item.query}
                onSelect={() => onSelect(item.query)}
                className="flex items-center justify-between cursor-pointer aria-selected:bg-accent aria-selected:text-accent-foreground"
              >
                <div className="flex items-center gap-2 flex-1 overflow-hidden">
                  <span className="truncate">{item.query}</span>
                </div>
                <div
                  role="button"
                  tabIndex={0}
                  className="ml-2 h-6 w-6 flex items-center justify-center rounded-sm hover:bg-destructive/10 hover:text-destructive transition-colors"
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    onDelete(item.query);
                  }}
                >
                  <X className="h-3 w-3" />
                  <span className="sr-only">Xóa</span>
                </div>
              </CommandItem>
            ))}
          </CommandGroup>
        </CommandList>
      </Command>
    </div>
  );
}
