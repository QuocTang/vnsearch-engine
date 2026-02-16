import { Button } from "@/components/ui/button";

/**
 * Error State Component
 * Hiển thị khi có lỗi xảy ra trong quá trình search
 */
interface ErrorStateProps {
  onRetry?: () => void;
  message?: string;
}

export function ErrorState({ onRetry, message }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">⚠️</div>
      <h3 className="text-xl font-semibold mb-2">Có lỗi xảy ra</h3>
      <p className="text-muted-foreground mb-6 max-w-md">
        {message || "Không thể kết nối tới API. Vui lòng thử lại sau."}
      </p>
      {onRetry && (
        <Button onClick={onRetry} variant="outline">
          Thử lại
        </Button>
      )}
    </div>
  );
}
