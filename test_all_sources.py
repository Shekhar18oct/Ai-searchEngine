"""
ScholarSphere - Source Testing Script
Tests all three research sources individually
"""
import sys
import time
from src.engine.research_searcher import ResearchPaperSearcher

def test_source(searcher, source_name, search_func, query, max_results=5):
    """Test a single source"""
    print(f"\n{'='*70}")
    print(f"Testing: {source_name}")
    print(f"Query: '{query}' | Max Results: {max_results}")
    print('='*70)
    
    start_time = time.time()
    
    try:
        results = search_func(query, max_results)
        elapsed = time.time() - start_time
        
        if results and len(results) > 0:
            print(f"✅ SUCCESS - Found {len(results)} results in {elapsed:.1f}s")
            print("\nSample Results:")
            for i, paper in enumerate(results[:3], 1):
                print(f"\n{i}. {paper.get('title', 'No title')[:70]}")
                authors = paper.get('authors', [])
                if isinstance(authors, list):
                    authors_str = ', '.join(authors[:3])
                else:
                    authors_str = str(authors)
                print(f"   Authors: {authors_str[:60]}")
                print(f"   Year: {paper.get('year', 'N/A')}")
                print(f"   Source: {paper.get('source', 'Unknown')}")
                if paper.get('url'):
                    print(f"   URL: {paper.get('url')[:60]}...")
            return True
        else:
            print(f"❌ FAILED - No results returned (Time: {elapsed:.1f}s)")
            return False
            
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ ERROR - {str(e)} (Time: {elapsed:.1f}s)")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*70)
    print("SCHOLARSPHERE - SOURCE VALIDATION TEST")
    print("="*70)
    
    searcher = ResearchPaperSearcher()
    query = "machine learning"
    max_results = 5
    
    results = {}
    
    # Test 1: Google Scholar
    results['Google Scholar'] = test_source(
        searcher,
        "Google Scholar",
        searcher.search_google_scholar,
        query,
        max_results
    )
    
    # Test 2: ResearchGate (arXiv)
    results['ResearchGate (arXiv)'] = test_source(
        searcher,
        "ResearchGate (arXiv API)",
        searcher.search_researchgate,
        query,
        max_results
    )
    
    # Test 3: Wikipedia
    results['Wikipedia'] = test_source(
        searcher,
        "Wikipedia",
        searcher.search_wikipedia,
        query,
        max_results
    )
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    all_passed = True
    for source, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {source}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED - All sources are working!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - Check output above for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())
