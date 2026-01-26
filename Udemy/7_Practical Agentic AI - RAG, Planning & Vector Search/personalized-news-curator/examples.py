"""
Example usage patterns for the Personalized News Curator.
Shows how to use the components programmatically.
"""

import sys
sys.path.insert(0, 'src')

from datastore import Article, ArticleDatastore
from api_clients.tavily_client import TavilySearchClient
from api_clients.openai_client import ArticleReranker
from agents.curator_agent import NewsCuratorAgent


def example_1_basic_search():
    """Example 1: Basic article search."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Article Search")
    print("="*70)
    
    client = TavilySearchClient(use_mocks=True)
    
    # Search for articles
    results = client.search("machine learning", max_results=3)
    
    print(f"\nFound {len(results)} articles on 'machine learning':")
    for i, article in enumerate(results, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   Relevance: {article['score']:.2f}")
        print(f"   Preview: {article['content'][:100]}...")


def example_2_datastore_operations():
    """Example 2: Working with the article datastore."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Datastore Operations")
    print("="*70)
    
    store = ArticleDatastore()
    
    # Create articles
    article1 = Article(
        title="AI Breakthroughs",
        url="https://example.com/ai",
        content="Latest AI developments",
        topic="artificial intelligence",
        summary="Recent advances in AI",
        tags=["ai", "ml", "tech"]
    )
    
    article2 = Article(
        title="Climate Action",
        url="https://example.com/climate",
        content="Climate change initiatives",
        topic="climate",
        summary="New climate policies",
        tags=["climate", "environment"]
    )
    
    # Add to store
    id1 = store.add_article(article1)
    id2 = store.add_article(article2)
    
    print(f"\n✓ Added article 1: {id1}")
    print(f"✓ Added article 2: {id2}")
    
    # Get articles by topic
    ai_articles = store.get_articles_by_topic("artificial intelligence")
    print(f"\n✓ Found {len(ai_articles)} articles on AI")
    
    # Rate articles
    store.update_rating(id1, 1)  # Like
    store.update_rating(id2, -1)  # Dislike
    
    print(f"\n✓ Rated articles")
    print(f"  Preferences: {store.get_preferences()}")
    
    # Show statistics
    print(f"\n✓ {store.summary()}")


def example_3_reranking():
    """Example 3: Reranking articles based on preferences."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Article Reranking")
    print("="*70)
    
    # Setup
    search_client = TavilySearchClient(use_mocks=True)
    reranker = ArticleReranker(use_mocks=True)
    
    # Simulate user preferences
    user_prefs = {
        "artificial intelligence": 0.8,  # Strong interest
        "technology": 0.3,                # Mild interest
        "sports": -0.5                    # Not interested
    }
    
    print(f"\nUser Preferences: {user_prefs}")
    
    # Search
    articles = search_client.search("AI and technology", max_results=3)
    
    print(f"\nOriginal Rankings:")
    for i, a in enumerate(articles, 1):
        print(f"  {i}. {a['title']} (score: {a['score']:.2f})")
    
    # Rerank
    reranked = reranker.rerank(articles, user_prefs)
    
    print(f"\nReranked (based on preferences):")
    for i, a in enumerate(reranked, 1):
        score = a.get('reranked_score', a.get('score'))
        print(f"  {i}. {a['title']} (score: {score:.2f})")


def example_4_preference_learning():
    """Example 4: How preferences evolve with feedback."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Preference Learning Over Time")
    print("="*70)
    
    store = ArticleDatastore()
    topic = "artificial intelligence"
    
    print(f"\nScenario: User rates {topic} articles")
    print("-" * 70)
    
    # Create and rate articles
    for i in range(1, 6):
        article = Article(
            title=f"AI Article {i}",
            url=f"https://example.com/ai{i}",
            content=f"Content about AI {i}",
            topic=topic
        )
        article_id = store.add_article(article)
        
        rating = 1  # User likes AI articles
        store.update_rating(article_id, rating)
        
        prefs = store.get_preferences()
        ai_pref = prefs.get(topic, 0)
        
        print(f"Interaction {i}:")
        print(f"  Rating: {'👍 Like' if rating > 0 else '👎 Dislike'}")
        print(f"  Topic preference: {ai_pref:.2f}")
        print(f"  Preference bar: {'█' * max(1, int((ai_pref + 1) * 10))}")


def example_5_queue_management():
    """Example 5: Managing the article queue."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Article Queue Management")
    print("="*70)
    
    store = ArticleDatastore()
    
    # Add articles to queue
    for i in range(5):
        article = Article(
            title=f"Article {i+1}",
            url=f"https://example.com/{i}",
            content=f"Content of article {i+1}",
            topic="test"
        )
        store.add_article(article)
    
    print(f"\nQueue length: {len(store.get_queue())}")
    print("Queue contents:")
    for i, article in enumerate(store.get_queue(), 1):
        print(f"  {i}. {article.title}")
    
    # Process queue
    print("\nProcessing queue:")
    while True:
        article = store.pop_from_queue()
        if not article:
            break
        print(f"  Popped: {article.title}")
        print(f"  Remaining: {len(store.get_queue())}")


def main():
    """Run all examples."""
    print("\n🗞️  PERSONALIZED NEWS CURATOR - USAGE EXAMPLES")
    
    try:
        example_1_basic_search()
        example_2_datastore_operations()
        example_3_reranking()
        example_4_preference_learning()
        example_5_queue_management()
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70)
        print("\nFor interactive use, run: python main.py")
        print("For automated demo, run: python demo.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
