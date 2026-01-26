"""Entry point for the Personalized News Curator application."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import validate_config, USE_MOCKS, USE_LLM_RERANK, USE_GROQ_RERANK
from datastore import ArticleDatastore
from agents.curator_agent import NewsCuratorAgent


def main():
    """Main entry point for the application."""
    try:
        # Validate configuration
        validate_config()
        
        if USE_MOCKS:
            print("⚙️  Using mock data (set USE_MOCKS=False to use real APIs)")
        elif USE_GROQ_RERANK:
            print("⚙️  Using real search with Groq reranking")
        elif USE_LLM_RERANK:
            print("⚙️  Using real search with OpenAI reranking")
        else:
            print("⚙️  Using real search with mock reranking (set USE_GROQ_RERANK=True or USE_LLM_RERANK=True for LLM rerank)")
        
        # Initialize datastore
        datastore = ArticleDatastore()
        
        # Create and run agent
        curator = NewsCuratorAgent(
            datastore,
            use_mocks=USE_MOCKS,
            use_llm_rerank=USE_LLM_RERANK,
            use_groq_rerank=USE_GROQ_RERANK,
        )
        curator.curate_session()
        
        # Print final statistics
        print("\n📊 Session Statistics:")
        print(f"   {datastore.summary()}")
        print(f"\n✅ Articles by rating:")
        print(f"   Liked: {len(datastore.get_articles_by_rating(1))}")
        print(f"   Neutral: {len([a for a in datastore.get_all_articles() if a.rating == 0])}")
        print(f"   Disliked: {len([a for a in datastore.get_articles_by_rating(-1)])}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Curator interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
