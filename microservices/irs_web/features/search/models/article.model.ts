import type { ArticleResult as ArticleResultDto } from "../types";

/**
 * Article Model
 * Transform từ API DTO sang Domain Model
 */

export class ArticleModel {
  id: number;
  articleId: number;
  title: string;
  summary: string;
  url: string;
  category: string;
  commentCount: number;
  score: number; // 0-1

  constructor(data: ArticleResultDto) {
    this.id = data.id;
    this.articleId = data.article_id;
    this.title = data.title;
    this.summary = data.summary;
    this.url = data.url;
    this.category = data.category_name;
    this.commentCount = data.comment_count;
    this.score = data.score;
  }

  // Computed properties
  get scorePercentage(): string {
    return `${Math.round(this.score * 100)}%`;
  }

  get hasComments(): boolean {
    return this.commentCount > 0;
  }

  get commentText(): string {
    if (this.commentCount === 0) return "Chưa có bình luận";
    return `${this.commentCount} bình luận`;
  }

  // Static factory
  static fromAPI(data: ArticleResultDto): ArticleModel {
    return new ArticleModel(data);
  }
}
