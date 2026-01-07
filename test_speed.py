import time
from src.engine.research_searcher import ResearchPaperSearcher

searcher = ResearchPaperSearcher()

print("Testing parallel search speed...")
print("-" * 50)

start = time.time()
results = searcher.search_all('machine learning', 10)
elapsed = time.time() - start

total = sum(len(v) for v in results.values())

print(f"\n✓ Search completed in {elapsed:.1f} seconds")
print(f"✓ Total results: {total}")
print(f"  - Google Scholar: {len(results['scholar'])} papers")
print(f"  - ResearchGate (arXiv): {len(results['researchgate'])} papers")
print(f"  - Wikipedia: {len(results['wikipedia'])} articles")
print("-" * 50)
