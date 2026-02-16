/**
 * Results Header Component
 * Hiển thị metadata của search results
 */
interface ResultsHeaderProps {
  query: string;
  totalResults: number;
  executionTime?: number;
}

export function ResultsHeader({
  query,
  totalResults,
  executionTime,
}: ResultsHeaderProps) {
  return (
    <div className="flex items-center justify-between py-4">
      <div className="text-sm text-muted-foreground">
        Tìm thấy{" "}
        <span className="font-semibold text-foreground">{totalResults}</span>{" "}
        kết quả cho{" "}
        <span className="font-semibold text-foreground">"{query}"</span>
        {executionTime && (
          <span className="ml-2">({Math.round(executionTime)}ms)</span>
        )}
      </div>
    </div>
  );
}
