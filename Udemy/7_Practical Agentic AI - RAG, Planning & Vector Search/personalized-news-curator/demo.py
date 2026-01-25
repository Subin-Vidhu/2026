"""
Demo script showing how the Personalized News Curator works.
This demonstrates the core functionality without requiring user interaction.
"""

import sys
sys.path.insert(0, 'src')

from datastore import Article, ArticleDatastore
from api_clients.tavily_client import TavilySearchClient
from api_clients.openai_client import ArticleReranker

def demo():
    """Run a demonstration of the curator system."""
    
    print("\n" + "="*70)
    print("🗞️  PERSONALIZED NEWS CURATOR - DEMO")
    print("="*70)
    
    # Initialize components
    print("\n1️⃣  Initializing datastore and tools...")
    datastore = ArticleDatastore()
    search_client = TavilySearchClient(use_mocks=True)
    reranker = ArticleReranker(use_mocks=True)
    
    # Demo topics
    topics = ["artificial intelligence", "climate change", "technology"]
    print(f"   Topics: {', '.join(topics)}")
    
    # Search for articles on each topic
    print("\n2️⃣  Searching for initial articles...")
    for topic in topics:
        print(f"\n   📍 Topic: {topic}")
        results = search_client.search(topic, max_results=1)
        
        for result in results:
            # Create article object
            article = Article(
                title=result['title'],
                url=result['url'],
                content=result['content'],
                topic=topic,
                summary=result['content'][:150],
                tags=[topic.split()[0]]
            )
            
            article_id = datastore.add_article(article)
            print(f"      ✓ Added: {article.title[:50]}...")
            print(f"        ID: {article_id}")
    
    # Show articles in datastore
    print("\n3️⃣  Articles in datastore:")
    for article in datastore.get_all_articles():
        print(f"      • [{article.id}] {article.title[:40]}... (Topic: {article.topic})")
    
    # Simulate user ratings
    print("\n4️⃣  Simulating user feedback (ratings)...")
    articles = datastore.get_all_articles()
    ratings = [1, -1, 1]  # Like, Dislike, Like
    
    for article, rating in zip(articles, ratings):
        datastore.update_rating(article.id, rating)
        rating_str = "👍 Like" if rating > 0 else "👎 Dislike" if rating < 0 else "😐 Neutral"
        print(f"      • {article.id}: {rating_str}")
    
    # Show updated preferences
    print("\n5️⃣  Updated user preferences:")
    prefs = datastore.get_preferences()
    for topic, score in prefs.items():
        bar = "█" * max(1, int((score + 1) * 10))
        print(f"      • {topic:20s}: {score:6.2f} {bar}")
    
    # Demonstrate reranking
    print("\n6️⃣  Demonstrating reranking with preferences...")
    new_results = search_client.search("AI news", max_results=3)
    print(f"      Original articles ({len(new_results)}):")
    for i, r in enumerate(new_results, 1):
        score = r.get('score', 0.5)
        print(f"        {i}. {r['title'][:40]}... (score: {score:.2f})")
    
    reranked = reranker.rerank(new_results, prefs, "artificial intelligence")
    print(f"\n      Reranked (based on preferences):")
    for i, r in enumerate(reranked, 1):
        new_score = r.get('reranked_score', r.get('score', 0.5))
        print(f"        {i}. {r['title'][:40]}... (score: {new_score:.2f})")
    
    # Show final statistics
    print("\n7️⃣  Final statistics:")
    print(f"      {datastore.summary()}")
    
    articles_by_rating = {
        1: len([a for a in datastore.get_all_articles() if a.rating == 1]),
        0: len([a for a in datastore.get_all_articles() if a.rating == 0]),
        -1: len([a for a in datastore.get_all_articles() if a.rating == -1])
    }
    print(f"      Articles by rating:")
    print(f"        • Liked (👍):    {articles_by_rating[1]}")
    print(f"        • Neutral (😐):  {articles_by_rating[0]}")
    print(f"        • Disliked (👎): {articles_by_rating[-1]}")
    
    print("\n" + "="*70)
    print("✅ Demo complete! Ready to run: python main.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    demo()
