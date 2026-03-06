import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import {
  CATEGORY_COLORS,
  DEFAULT_CATEGORY_COLOR,
} from "@/features/search/config";
import type { ArticleModel } from "@/features/search/models/article.model";

/**
 * Article Card Component
 * Hiển thị một article result v với đầy đủ thông tin
 */

export function ArticleCard({ article }: { article: ArticleModel }) {
  // Get color or default
  const categoryColor =
    CATEGORY_COLORS[article.category as keyof typeof CATEGORY_COLORS] ||
    DEFAULT_CATEGORY_COLOR;

  return (
    <motion.div
      whileHover={{ y: -5 }}
      transition={{ type: "spring", stiffness: 300 }}
      className="h-full"
    >
      <Card className="group relative overflow-hidden p-4 md:p-6 transition-all hover:shadow-lg h-full flex flex-col">
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
        <p className="text-sm text-muted-foreground line-clamp-3 mb-4 flex-1">
          {article.summary}
        </p>

        {/* Footer: Comments + CTA */}
        <div className="flex items-center justify-between pt-4 border-t mt-auto">
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
