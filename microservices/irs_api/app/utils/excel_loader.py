"""
Excel data loader utility.
Loads articles, categories, and comments from Excel files and merges them.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple


def load_excel_data(
    articles_path: str,
    categories_path: str,
    comments_path: str
) -> pd.DataFrame:
    """
    Load and merge data from Excel files.
    
    Args:
        articles_path: Path to articles.xlsx
        categories_path: Path to categories.xlsx
        comments_path: Path to comments.xlsx
        
    Returns:
        pd.DataFrame: Merged dataframe with columns:
            - article_id
            - title
            - summary
            - url
            - thumbnail_url
            - published_at
            - category_id
            - category_name
            - comment_count
            - full_text (title + summary)
            
    Raises:
        FileNotFoundError: If any Excel file doesn't exist
    """
    # Validate files exist
    for path_str, name in [
        (articles_path, "Articles"),
        (categories_path, "Categories"),
        (comments_path, "Comments")
    ]:
        if not Path(path_str).exists():
            raise FileNotFoundError(f"{name} file not found: {path_str}")
    
    # Load Excel files
    articles_df = pd.read_excel(articles_path)
    categories_df = pd.read_excel(categories_path)
    comments_df = pd.read_excel(comments_path)
    
    # Count comments per article
    comment_counts = comments_df.groupby('article_id').size().reset_index(name='comment_count')
    
    # Merge categories into articles
    merged_df = articles_df.merge(
        categories_df[['category_id', 'category_name']],
        on='category_id',
        how='left'
    )
    
    # Merge comment counts
    merged_df = merged_df.merge(
        comment_counts,
        on='article_id',
        how='left'
    )
    
    # Fill missing comment counts with 0
    merged_df['comment_count'] = merged_df['comment_count'].fillna(0).astype(int)
    
    # Create full_text field (title + summary)
    merged_df['full_text'] = (
        merged_df['title'].fillna('') + ' ' + merged_df['summary'].fillna('')
    ).str.strip()
    
    return merged_df


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate the merged dataframe has required columns.
    
    Args:
        df: Dataframe to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    required_columns = [
        'article_id', 'title', 'summary', 'url', 
        'category_name', 'comment_count', 'full_text'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {missing_columns}"
    
    # Check for empty full_text
    empty_text_count = df['full_text'].isna().sum() + (df['full_text'] == '').sum()
    if empty_text_count > 0:
        return False, f"Found {empty_text_count} articles with empty full_text"
    
    return True, ""
