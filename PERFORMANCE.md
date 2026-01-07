# ScholarSphere - Performance Tips

## Search Speed Optimization

### Current Performance (Optimized):
- **Parallel searching**: All 3 sources run simultaneously
- **Smart timeouts**: 30 seconds max per source, 60 seconds total
- **Progress logging**: See which sources complete first

### Expected Search Times:
- **10 results** (all sources): ~15-40 seconds
- **20 results** (all sources): ~30-60 seconds
- **Single source**: ~5-15 seconds

### Speed by Source:
1. **arXiv (ResearchGate)**: ⚡ **Fastest** (~2-5 seconds)
2. **Wikipedia**: ⚡⚡ **Fast** (~3-8 seconds)
3. **Google Scholar**: 🐌 **Slowest** (~15-40 seconds)

### Tips for Faster Searches:
1. **Select specific sources** instead of "All Sources"
2. **Use smaller result counts** (10-20 instead of 100+)
3. **arXiv is fastest** for scientific papers
4. **Google Scholar has best metadata** but is slowest

### Why is Google Scholar Slow?
- Uses web scraping (not official API)
- Rate limiting to avoid blocks
- Fetches detailed metadata
- Multiple HTTP requests

### Recommendations:
- For **quick results**: Use arXiv (ResearchGate) only
- For **comprehensive search**: Use All Sources with 10-20 results
- For **large datasets**: Be patient or use arXiv with 100+ results
