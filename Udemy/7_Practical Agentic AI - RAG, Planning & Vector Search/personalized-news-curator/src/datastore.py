"""In-memory datastore for articles and user preferences."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import uuid


@dataclass
class Article:
    """Represents a news article."""
    
    title: str
    url: str
    content: str
    topic: str
    summary: str = ""
    tags: List[str] = field(default_factory=list)
    rating: int = 0  # -1 (dislike), 0 (neutral), 1 (like)
    fetched_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self):
        return f"[{self.id}] {self.title}\n    Topic: {self.topic}\n    URL: {self.url}\n    Rating: {self.rating}"


class ArticleDatastore:
    """In-memory storage for articles with preference tracking."""
    
    def __init__(self):
        self.articles: Dict[str, Article] = {}
        self.user_preferences: Dict[str, float] = {}  # topic -> preference score
        self.article_queue: List[str] = []  # Article IDs in order
        self.interaction_count = 0
    
    def add_article(self, article: Article) -> str:
        """Add an article to the datastore and queue.
        
        Args:
            article: Article object to add
            
        Returns:
            Article ID
        """
        self.articles[article.id] = article
        self.article_queue.append(article.id)
        return article.id
    
    def get_article(self, article_id: str) -> Optional[Article]:
        """Retrieve an article by ID."""
        return self.articles.get(article_id)
    
    def get_articles_by_topic(self, topic: str) -> List[Article]:
        """Get all articles for a specific topic."""
        return [a for a in self.articles.values() if a.topic == topic]
    
    def update_rating(self, article_id: str, rating: int) -> None:
        """Update article rating and user preferences.
        
        Args:
            article_id: ID of the article
            rating: -1 (dislike), 0 (neutral), 1 (like)
        """
        if article_id not in self.articles:
            raise ValueError(f"Article {article_id} not found")
        
        article = self.articles[article_id]
        article.rating = rating
        self._update_preferences(article.topic, rating)
        self.interaction_count += 1
    
    def _update_preferences(self, topic: str, rating: int) -> None:
        """Update user preference score for a topic (linear update).
        
        Args:
            topic: Topic name
            rating: -1, 0, or 1
        """
        from config import PREFERENCE_UPDATE_FACTOR
        
        if topic not in self.user_preferences:
            self.user_preferences[topic] = 0.0
        self.user_preferences[topic] += rating * PREFERENCE_UPDATE_FACTOR
    
    def get_preferences(self) -> Dict[str, float]:
        """Get current user preference scores."""
        return self.user_preferences.copy()
    
    def get_all_articles(self) -> List[Article]:
        """Get all articles in the datastore."""
        return list(self.articles.values())
    
    def get_articles_by_rating(self, min_rating: int = None) -> List[Article]:
        """Get articles filtered by minimum rating."""
        articles = self.articles.values()
        if min_rating is not None:
            articles = [a for a in articles if a.rating >= min_rating]
        return sorted(articles, key=lambda a: a.rating, reverse=True)
    
    def get_queue(self) -> List[Article]:
        """Get articles in queue order."""
        return [self.articles[aid] for aid in self.article_queue if aid in self.articles]
    
    def pop_from_queue(self) -> Optional[Article]:
        """Remove and return the first article from the queue."""
        if self.article_queue:
            article_id = self.article_queue.pop(0)
            return self.articles.get(article_id)
        return None
    
    def clear(self) -> None:
        """Clear all data from the datastore."""
        self.articles.clear()
        self.user_preferences.clear()
        self.article_queue.clear()
        self.interaction_count = 0
    
    def summary(self) -> str:
        """Get a summary of the datastore state."""
        return (
            f"Articles: {len(self.articles)} | "
            f"Topics tracked: {len(self.user_preferences)} | "
            f"Interactions: {self.interaction_count} | "
            f"Queue length: {len(self.article_queue)}"
        )
