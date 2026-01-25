"""LangChain-based curator agent."""

from typing import List, Dict, Optional
from datastore import ArticleDatastore
from agents import CuratorTools
from config import USE_MOCKS, USE_LLM_RERANK, USE_GROQ_RERANK


class NewsCuratorAgent:
    """Agentic news curator using LangChain patterns."""
    
    def __init__(self, datastore: ArticleDatastore, use_mocks: bool = None, use_llm_rerank: bool = None, use_groq_rerank: bool = None):
        self.datastore = datastore
        self.use_mocks = use_mocks if use_mocks is not None else USE_MOCKS
        llm_flag = use_llm_rerank if use_llm_rerank is not None else USE_LLM_RERANK
        groq_flag = use_groq_rerank if use_groq_rerank is not None else USE_GROQ_RERANK
        self.tools = CuratorTools(datastore, use_mocks=use_mocks, use_llm_rerank=llm_flag, use_groq_rerank=groq_flag)
        self.topics = []
    
    def initialize_topics(self, topics: List[str]) -> None:
        """Initialize user topics of interest.
        
        Args:
            topics: List of topics the user is interested in
        """
        self.topics = topics
        print(f"\n📌 Initialized topics: {', '.join(topics)}")
    
    def fetch_initial_articles(self) -> None:
        """Fetch initial articles for all topics.
        
        This is the first interaction - one article per topic.
        """
        if not self.topics:
            raise ValueError("Topics not initialized. Call initialize_topics first.")
        
        print(f"\n🚀 Fetching initial articles (one per topic)...")
        
        for topic in self.topics:
            # Search for articles
            articles = self.tools.search_articles(topic, num_articles=1)
            
            if articles:
                # Rerank articles
                reranked = self.tools.rerank_articles(articles, topic)
                
                # Store in datastore
                self.tools.store_articles(reranked, topic)
    
    def fetch_next_article(self, topic: str) -> None:
        """Fetch one more article for a topic after feedback.
        
        Args:
            topic: Topic to fetch article for
        """
        print(f"\n➕ Fetching next article for topic '{topic}'...")
        
        # Search for articles
        articles = self.tools.search_articles(topic, num_articles=1)
        
        if articles:
            # Rerank based on current preferences
            reranked = self.tools.rerank_articles(articles, topic)
            
            # Store in datastore
            self.tools.store_articles(reranked, topic)
    
    def curate_session(self) -> None:
        """Run a complete curation session.
        
        1. Get user topics
        2. Fetch initial articles
        3. Loop: display article, get feedback, fetch next
        """
        # Initialize topics
        print("\n" + "="*60)
        print("🗞️  PERSONALIZED NEWS CURATOR")
        print("="*60)
        
        topics = self._get_user_topics()
        self.initialize_topics(topics)
        
        # Fetch initial articles
        self.fetch_initial_articles()
        
        # Feedback loop
        self._feedback_loop()
    
    def _get_user_topics(self) -> List[str]:
        """Get 3 topics from user.
        
        Returns:
            List of topics
        """
        topics = []
        print("\n📝 Please enter 3 topics you're interested in:")
        
        for i in range(3):
            while True:
                topic = input(f"   Topic {i+1}: ").strip()
                if topic:
                    topics.append(topic)
                    break
                print("   Please enter a valid topic")
        
        return topics
    
    def _feedback_loop(self) -> None:
        """Main feedback loop for article rating and fetching.
        
        User rates articles, preferences are updated, new articles are fetched.
        """
        while True:
            # Get queue of articles
            queue = self.datastore.get_queue()
            
            if not queue:
                print("\n❌ No articles in queue. Fetching more...")
                for topic in self.topics:
                    self.fetch_next_article(topic)
                queue = self.datastore.get_queue()
            
            if not queue:
                print("\n⚠️  Unable to fetch articles")
                break
            
            # Display next article
            article = queue[0]
            print("\n" + "="*60)
            print(f"📰 {article.title}")
            print(f"   Topic: {article.topic}")
            print(f"   URL: {article.url}")
            print(f"   Summary: {article.summary}")
            print("="*60)
            
            # Get user feedback
            rating = self._get_article_rating()
            
            if rating is None:
                # User wants to change topic or quit
                action = input("\nWhat would you like to do?\n  1. Continue with current topics\n  2. Add a new topic\n  3. Exit\n\nChoice (1-3): ").strip()
                
                if action == "2":
                    new_topic = input("Enter new topic: ").strip()
                    if new_topic:
                        self.topics.append(new_topic)
                        self.fetch_next_article(new_topic)
                elif action == "3":
                    print("\n👋 Thank you for using the News Curator!")
                    break
                else:
                    # Continue with current topics
                    pass
            else:
                # Update rating
                self.datastore.update_rating(article.id, rating)
                print(f"✅ Rating saved: {'👍' if rating > 0 else '👎' if rating < 0 else '😐'}")
                
                # Remove from queue
                self.datastore.pop_from_queue()
                
                # Fetch next article for this topic
                self.fetch_next_article(article.topic)
                
                # Show preferences
                prefs = self.datastore.get_preferences()
                if prefs:
                    print(f"\n📊 Current preferences: {prefs}")
    
    def _get_article_rating(self) -> Optional[int]:
        """Get user's rating for an article.
        
        Returns:
            1 (like), -1 (dislike), 0 (neutral), or None (skip/menu)
        """
        while True:
            response = input("\nRate this article:\n  1 = Like 👍\n  0 = Neutral 😐\n  -1 = Dislike 👎\n  m = Menu\n\nYour choice: ").strip().lower()
            
            if response in ['1', '0', '-1']:
                return int(response)
            elif response == 'm':
                return None
            else:
                print("Please enter 1, 0, -1, or m")
