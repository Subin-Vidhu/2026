"""Quick test to verify project setup."""

import sys
sys.path.insert(0, 'src')

from config import USE_MOCKS
print('✅ Config loaded')
print(f'USE_MOCKS: {USE_MOCKS}')

from api_clients.tavily_client import TavilySearchClient
client = TavilySearchClient()
results = client.search('artificial intelligence', max_results=2)
print(f'✅ Found {len(results)} articles')
print(f'First article: {results[0]["title"]}')

from datastore import Article, ArticleDatastore
store = ArticleDatastore()
print(f'✅ Datastore initialized: {store.summary()}')

print('\n✅ All imports and basic functionality working!')
