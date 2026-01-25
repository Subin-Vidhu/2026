"""Agent tools for the news curator."""

from typing import List, Dict, Any
from api_clients.tavily_client import TavilySearchClient
from api_clients.openai_client import ArticleReranker
from config import USE_LLM_RERANK, USE_GROQ_RERANK
from datastore import Article, ArticleDatastore


class CuratorTools:
    """Collection of tools for the curator agent."""
    
    def __init__(self, datastore: ArticleDatastore, use_mocks: bool = None, use_llm_rerank: bool = None, use_groq_rerank: bool = None):
        self.datastore = datastore
        llm_flag = use_llm_rerank if use_llm_rerank is not None else USE_LLM_RERANK
        groq_flag = use_groq_rerank if use_groq_rerank is not None else USE_GROQ_RERANK
        self.search_client = TavilySearchClient(use_mocks=use_mocks)
        self.reranker = ArticleReranker(use_mocks=use_mocks, use_llm=llm_flag, use_groq=groq_flag)
    
    def search_articles(self, topic: str, num_articles: int = 3) -> List[Dict[str, Any]]:
        """Search for articles on a specific topic.
        
        Args:
            topic: Topic to search for
            num_articles: Number of articles to fetch
            
        Returns:
            List of article dictionaries
        """
        print(f"🔍 Searching for articles on '{topic}'...")
        results = self.search_client.search(topic, max_results=num_articles)
        print(f"   Found {len(results)} articles")
        return results
    
    def rerank_articles(
        self,
        articles: List[Dict[str, Any]],
        topic: str = None
    ) -> List[Dict[str, Any]]:
        """Rerank articles based on current user preferences.
        
        Args:
            articles: Articles to rerank
            topic: Optional topic context
            
        Returns:
            Reranked articles
        """
        prefs = self.datastore.get_preferences()
        if not prefs and topic:
            # If no preferences yet, use the current topic
            prefs = {topic: 0.5}
        
        print(f"📊 Reranking {len(articles)} articles...")
        reranked = self.reranker.rerank(articles, prefs, topic)
        return reranked
    
    def store_articles(self, articles: List[Dict[str, Any]], topic: str) -> List[str]:
        """Store articles in the datastore.
        
        Args:
            articles: Articles to store
            topic: Topic classification
            
        Returns:
            List of stored article IDs
        """
        article_ids = []
        for article in articles:
            # Create tags from title
            tags = self._extract_tags(article.get('title', ''))
            
            article_obj = Article(
                title=article.get('title', 'Untitled'),
                url=article.get('url', ''),
                content=article.get('content', ''),
                topic=topic,
                summary=article.get('content', '')[:200],  # Use first 200 chars as summary
                tags=tags,
                rating=0
            )
            
            article_id = self.datastore.add_article(article_obj)
            article_ids.append(article_id)
        
        print(f"💾 Stored {len(article_ids)} articles")
        return article_ids
    
    def _extract_tags(self, text: str) -> List[str]:
        """Simple tag extraction from text.
        
        Args:
            text: Text to extract tags from
            
        Returns:
            List of tags
        """
        # Simple approach: use capitalized words as potential tags
        words = text.split()
        tags = []
        for word in words:
            if word[0].isupper() and len(word) > 3:
                tags.append(word.lower())
        
        return tags[:3]  # Max 3 tags
