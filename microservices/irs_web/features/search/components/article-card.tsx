import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArticleModel } from "../models/article.model";

/**
 * Article Card Component
 * Hiển thị một article result v với đầy đủ thông tin
 */
interface ArticleCardProps {
  article: ArticleModel;
}

// Category colors mapping
const CATEGORY_COLORS: Record<string, string> = {
  "Khoa học": "bg-blue-500/10 text-blue-700 border-blue-200",
  "Ý kiến": "bg-purple-500/10 text-purple-700 border-purple-200",
  "Giáo dục": "bg-green-500/10 text-green-700 border-green-200",
  "Sức khỏe": "bg-red-500/10 text-red-700 border-red-200",
  "Thời sự": "bg-orange-500/10 text-orange-700 border-orange-200",
  "Giải trí": "bg-pink-500/10 text-pink-700 border-pink-200",
  "Đời sống": "bg-yellow-500/10 text-yellow-700 border-yellow-200",
};

export function ArticleCard({ article }: ArticleCardProps) {
  const categoryColor =
    CATEGORY_COLORS[article.category] ||
    "bg-gray-500/10 text-gray-700 border-gray-200";

  return (
    <motion.div
      whileHover={{ y: -5 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <Card className="group relative overflow-hidden p-6 transition-all hover:shadow-lg">
        {/* Header: Category Badge + Score */}
        <div className="flex items-start justify-between mb-3">
          <Badge variant="outline" className={categoryColor}>
            {article.category}
          </Badge>
          <div className="text-sm font-medium text-muted-foreground">
            {article.scorePercentage}
          </div>
        </div>

        {/* Title - max 2 lines */}
        <h3 className="text-lg font-semibold line-clamp-2 mb-2 group-hover:text-primary transition-colors">
          {article.title}
        </h3>

        {/* Summary - max 3-4 lines */}
        <p className="text-sm text-muted-foreground line-clamp-3 mb-4">
          {article.summary}
        </p>

        {/* Footer: Comments + CTA */}
        <div className="flex items-center justify-between pt-4 border-t">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>📝</span>
            <span>{article.commentText}</span>
          </div>

          <Button
            variant="ghost"
            size="sm"
            asChild
            className="group-hover:bg-primary group-hover:text-primary-foreground"
          >
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              Đọc thêm →
            </a>
          </Button>
        </div>
      </Card>
    </motion.div>
  );
}
