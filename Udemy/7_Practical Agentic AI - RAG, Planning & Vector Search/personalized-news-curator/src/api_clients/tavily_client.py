"""Tavily Search API client with mock support."""

from typing import List, Dict, Any
import json
from config import USE_MOCKS, TAVILY_API_KEY


class TavilySearchClient:
    """Client for Tavily Search API with mock support."""
    
    def __init__(self, use_mocks: bool = None):
        self.use_mocks = use_mocks if use_mocks is not None else USE_MOCKS
        if not self.use_mocks and not TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not set and mocks disabled")
        
        if not self.use_mocks:
            try:
                from tavily import TavilyClient
                self.client = TavilyClient(api_key=TAVILY_API_KEY)
            except ImportError:
                raise ImportError("tavily-python not installed. Install with: pip install tavily-python")
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for articles using Tavily Search or mock data.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of article dictionaries with keys: title, url, content, score
        """
        if self.use_mocks:
            return self._mock_search(query, max_results)
        
        try:
            response = self.client.search(query, max_results=max_results)
            results = response.get('results', [])
            
            # Normalize response format
            normalized = []
            for result in results:
                normalized.append({
                    'title': result.get('title', 'Untitled'),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0.5)
                })
            return normalized
        except Exception as e:
            print(f"Error searching Tavily: {e}")
            return []
    
    def _mock_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Generate mock search results for testing.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of mock articles
        """
        mock_articles = {
            "artificial intelligence": [
                {
                    "title": "Latest Breakthroughs in AI and Machine Learning 2026",
                    "url": "https://example.com/ai-breakthroughs-2026",
                    "content": "Explore the latest advancements in artificial intelligence including neural networks, transformers, and deep learning applications.",
                    "score": 0.95
                },
                {
                    "title": "How AI is Revolutionizing Healthcare",
                    "url": "https://example.com/ai-healthcare",
                    "content": "Discover how artificial intelligence is transforming medical diagnosis, drug discovery, and patient care.",
                    "score": 0.89
                },
                {
                    "title": "AI Ethics: Ensuring Responsible AI Development",
                    "url": "https://example.com/ai-ethics",
                    "content": "Understanding the ethical implications of AI and ensuring responsible development practices.",
                    "score": 0.85
                }
            ],
            "climate change": [
                {
                    "title": "Climate Change: 2026 Global Impact Report",
                    "url": "https://example.com/climate-2026",
                    "content": "Annual report on climate change impacts, carbon emissions, and environmental policy updates.",
                    "score": 0.92
                },
                {
                    "title": "Renewable Energy Surpasses Fossil Fuels",
                    "url": "https://example.com/renewable-energy",
                    "content": "Breaking news: Renewable energy sources now generate more electricity than fossil fuels globally.",
                    "score": 0.88
                },
                {
                    "title": "Ocean Conservation Initiatives Show Promise",
                    "url": "https://example.com/ocean-conservation",
                    "content": "New marine protection policies and conservation efforts are making a positive impact.",
                    "score": 0.81
                }
            ],
            "technology": [
                {
                    "title": "Quantum Computing Reaches New Milestone",
                    "url": "https://example.com/quantum-computing",
                    "content": "Major advancement in quantum computing with practical applications in cryptography and optimization.",
                    "score": 0.94
                },
                {
                    "title": "5G Networks Expand Global Coverage",
                    "url": "https://example.com/5g-networks",
                    "content": "5G infrastructure continues to expand, enabling faster internet and IoT applications worldwide.",
                    "score": 0.87
                },
                {
                    "title": "Cybersecurity Threats and Defense Strategies",
                    "url": "https://example.com/cybersecurity",
                    "content": "Latest cybersecurity threats and best practices for protecting digital infrastructure.",
                    "score": 0.83
                }
            ],
            "sports": [
                {
                    "title": "Champions League Finals: Historical Performance Analysis",
                    "url": "https://example.com/champions-league",
                    "content": "Analysis of Champions League performance and predictions for upcoming tournaments.",
                    "score": 0.90
                },
                {
                    "title": "Olympic Games 2026: Host City and Events",
                    "url": "https://example.com/olympics-2026",
                    "content": "Everything you need to know about the 2026 Olympic Games and featured sports.",
                    "score": 0.86
                },
                {
                    "title": "Rising Stars in Professional Football",
                    "url": "https://example.com/football-stars",
                    "content": "Spotlight on emerging talent in professional football leagues around the world.",
                    "score": 0.82
                }
            ]
        }
        
        # Find matching articles based on query keywords
        query_lower = query.lower()
        results = []
        
        for topic, articles in mock_articles.items():
            if topic in query_lower or any(word in query_lower for word in topic.split()):
                results.extend(articles)
        
        # If no exact match, return generic articles
        if not results:
            results = [
                {
                    "title": f"News about {query}",
                    "url": f"https://example.com/{query.replace(' ', '-')}",
                    "content": f"Article discussing recent developments in {query}.",
                    "score": 0.85
                },
                {
                    "title": f"The Future of {query}",
                    "url": f"https://example.com/future-{query.replace(' ', '-')}",
                    "content": f"Exploring upcoming trends and innovations in {query}.",
                    "score": 0.78
                }
            ]
        
        # Sort by score and return top results
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        return results[:max_results]
