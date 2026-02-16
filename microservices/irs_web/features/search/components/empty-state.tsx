/**
 * Empty State Component
 * Hiển thị khi không tìm thấy kết quả
 */
export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="text-6xl mb-4">🔍</div>
      <h3 className="text-xl font-semibold mb-2">Không tìm thấy kết quả</h3>
      <p className="text-muted-foreground mb-4 max-w-md">
        Không tìm thấy bài viết nào phù hợp với từ khóa của bạn.
      </p>
      <div className="text-sm text-muted-foreground space-y-1">
        <p className="font-medium">Gợi ý:</p>
        <ul className="list-disc list-inside space-y-1 text-left">
          <li>Thử từ khóa khác</li>
          <li>Kiểm tra chính tả</li>
          <li>Giảm số lượng filters</li>
          <li>Sử dụng từ khóa tổng quát hơn</li>
        </ul>
      </div>
    </div>
  );
}
