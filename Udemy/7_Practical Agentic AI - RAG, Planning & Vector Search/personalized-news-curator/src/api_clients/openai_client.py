"""OpenAI API client for article reranking with mock support."""

from typing import List, Dict, Any
import json
from config import (
    USE_MOCKS,
    USE_LLM_RERANK,
    USE_GROQ_RERANK,
    OPENAI_API_KEY,
    GROQ_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
)


class ArticleReranker:
    """Rerank articles based on user preferences using OpenAI or mock."""
    
    def __init__(self, use_mocks: bool = None, use_llm: bool = None, use_groq: bool = None):
        self.use_mocks = use_mocks if use_mocks is not None else USE_MOCKS
        self.use_llm = use_llm if use_llm is not None else USE_LLM_RERANK
        self.use_groq = use_groq if use_groq is not None else USE_GROQ_RERANK
        self.llm = None

        # If mocks are on or no LLM rerank requested, skip client setup
        if self.use_mocks or (not self.use_llm and not self.use_groq):
            return

        if self.use_groq:
            if not GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not set and Groq rerank requested")
            try:
                from langchain_groq import ChatGroq

                self.llm = ChatGroq(
                    groq_api_key=GROQ_API_KEY,
                    model_name=LLM_MODEL,
                    temperature=TEMPERATURE,
                )
            except ImportError:
                raise ImportError("langchain-groq not installed. Install with: pip install langchain-groq")
        elif self.use_llm:
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set and LLM rerank requested")
            try:
                from langchain_openai import ChatOpenAI

                self.llm = ChatOpenAI(
                    model=LLM_MODEL,
                    temperature=TEMPERATURE,
                    api_key=OPENAI_API_KEY,
                )
            except ImportError:
                raise ImportError("langchain-openai not installed. Install with: pip install langchain-openai")
    
    def rerank(
        self,
        articles: List[Dict[str, Any]],
        user_preferences: Dict[str, float],
        topic: str = None
    ) -> List[Dict[str, Any]]:
        """Rerank articles based on user preferences.
        
        Args:
            articles: List of article dictionaries
            user_preferences: Dictionary of topic -> preference score
            topic: Optional topic to focus reranking on
            
        Returns:
            Reranked list of articles with adjusted scores
        """
        if self.use_mocks or (not self.use_llm and not self.use_groq) or not self.llm:
            return self._mock_rerank(articles, user_preferences, topic)
        
        try:
            return self._llm_rerank(articles, user_preferences, topic)
        except Exception as e:
            print(f"Error reranking with LLM: {e}")
            return self._mock_rerank(articles, user_preferences, topic)
    
    def _mock_rerank(
        self,
        articles: List[Dict[str, Any]],
        user_preferences: Dict[str, float],
        topic: str = None
    ) -> List[Dict[str, Any]]:
        """Mock reranking based on simple heuristics.
        
        Uses preference scores and article content matching to adjust rankings.
        """
        if not articles:
            return articles
        
        reranked = []
        for article in articles:
            score = article.get('score', 0.5)
            
            # Boost score based on user preferences
            if user_preferences:
                # Calculate preference boost
                pref_score = sum(user_preferences.values()) / len(user_preferences) if user_preferences else 0
                # Clamp preference score between 0.8 and 1.2
                pref_boost = max(0.8, min(1.2, 1.0 + (pref_score * 0.2)))
                score = score * pref_boost
            
            # Check if article content matches known topics
            title_lower = article.get('title', '').lower()
            content_lower = article.get('content', '').lower()
            
            for pref_topic, pref_value in user_preferences.items():
                if pref_topic.lower() in title_lower or pref_topic.lower() in content_lower:
                    score += pref_value * 0.1
            
            # Clamp score between 0 and 1
            score = max(0.0, min(1.0, score))
            
            reranked_article = article.copy()
            reranked_article['reranked_score'] = score
            reranked.append(reranked_article)
        
        # Sort by reranked score
        reranked = sorted(reranked, key=lambda x: x['reranked_score'], reverse=True)
        return reranked
    
    def _llm_rerank(
        self,
        articles: List[Dict[str, Any]],
        user_preferences: Dict[str, float],
        topic: str = None
    ) -> List[Dict[str, Any]]:
        """Rerank using LangChain and OpenAI.
        
        Args:
            articles: List of articles
            user_preferences: User preference scores
            topic: Optional focus topic
            
        Returns:
            Reranked articles
        """
        try:
            # Preferred import for modern LangChain
            from langchain_core.prompts import ChatPromptTemplate
        except ImportError:
            # Fallback for older LangChain versions
            from langchain.prompts import ChatPromptTemplate
        
        # Format articles for the prompt
        articles_text = "\n".join([
            f"{i+1}. {a.get('title', 'N/A')}\n"
            f"   Content: {a.get('content', 'N/A')[:200]}...\n"
            f"   URL: {a.get('url', 'N/A')}\n"
            f"   Score: {a.get('score', 0.5)}"
            for i, a in enumerate(articles)
        ])
        
        prompt = ChatPromptTemplate.from_template("""You are an expert news curator. 
Rerank the following articles based on the user's interests and preferences.

User Preferences (topic -> score):
{preferences}

Articles to rerank:
{articles}

Return a JSON array with the articles reranked (1-10 scale where 10 is best match).
Format: [{{"index": 1, "title": "...", "new_score": 0.95}}, ...]

Only return the JSON, no additional text.""")
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "preferences": json.dumps(user_preferences, indent=2),
                "articles": articles_text
            })
            
            # Parse the response
            response_text = result.content
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                rankings = json.loads(json_str)
                
                # Map rankings back to articles
                reranked = []
                for ranking in rankings:
                    idx = ranking.get('index', 1) - 1
                    if 0 <= idx < len(articles):
                        article = articles[idx].copy()
                        article['reranked_score'] = ranking.get('new_score', 0.5) / 10.0
                        reranked.append(article)
                
                return reranked
        except Exception as e:
            print(f"Error parsing LLM rerank response: {e}")
        
        # Fallback to mock reranking on error
        return self._mock_rerank(articles, user_preferences, topic)
