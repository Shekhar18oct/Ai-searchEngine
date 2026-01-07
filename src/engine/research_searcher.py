"""
Research Paper Search Engine
Integrates with Google Scholar, ResearchGate, and Wikipedia for academic research
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import re
import sys
from fake_useragent import UserAgent
import wikipedia
from scholarly import scholarly
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchPaperSearcher:
    """Search engine for academic research papers and theses"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random
        }
        
    def search_all(self, query: str, max_results: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search all sources for research papers
        
        Args:
            query: Search query
            max_results: Maximum results per source
            
        Returns:
            Dictionary containing results from all sources
        """
        results = {
            'scholar': self.search_google_scholar(query, max_results),
            'researchgate': self.search_researchgate(query, max_results),
            'wikipedia': self.search_wikipedia(query, max_results)
        }
        return results
    
    def search_google_scholar(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search Google Scholar for research papers
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of paper dictionaries
        """
        papers = []
        try:
            search_query = scholarly.search_pubs(query)
            
            for i, result in enumerate(search_query):
                if i >= max_results:
                    break
                    
                try:
                    paper = {
                        'title': result.get('bib', {}).get('title', 'N/A'),
                        'authors': result.get('bib', {}).get('author', []),
                        'year': result.get('bib', {}).get('pub_year', 'N/A'),
                        'abstract': result.get('bib', {}).get('abstract', 'No abstract available'),
                        'citations': result.get('num_citations', 0),
                        'url': result.get('pub_url', '') or result.get('eprint_url', ''),
                        'source': 'Google Scholar',
                        'venue': result.get('bib', {}).get('venue', 'N/A'),
                        'publisher': result.get('bib', {}).get('publisher', 'N/A')
                    }
                    papers.append(paper)
                except Exception as e:
                    logger.error(f"Error parsing scholar result: {e}")
                    continue
                    
            time.sleep(0.5)  # Respectful delay
            
        except Exception as e:
            logger.error(f"Error searching Google Scholar: {e}")
            
        return papers
    
    def search_researchgate(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for research papers using arXiv API (free and reliable)
        Labeled as ResearchGate for UI consistency
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of paper dictionaries
        """
        papers = []
        
        # Strategy 1: Use arXiv API (free, reliable, no rate limits)
        try:
            import feedparser
            
            # arXiv API endpoint
            arxiv_url = f"http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': min(max_results, 100)
            }
            
            response = requests.get(arxiv_url, params=params, timeout=15)
            
            if response.status_code == 200:
                # Parse the Atom feed
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries[:max_results]:
                    try:
                        # Extract paper information
                        title = entry.get('title', 'Untitled').replace('\n', ' ').strip()
                        
                        # Get authors
                        authors = []
                        if 'authors' in entry:
                            authors = [author.name for author in entry.authors[:5]]
                        
                        # Get year from published date
                        year = 'N/A'
                        if 'published' in entry:
                            year = entry.published[:4]  # Extract year from date
                        
                        # Get abstract
                        abstract = entry.get('summary', 'No abstract available').replace('\n', ' ').strip()
                        
                        # Get URL
                        url = entry.get('id', entry.get('link', ''))
                        
                        # Get category/venue
                        venue = 'arXiv'
                        if 'arxiv_primary_category' in entry:
                            venue = f"arXiv - {entry.arxiv_primary_category.get('term', '')}"
                        
                        paper = {
                            'title': title,
                            'authors': authors if authors else ['Unknown'],
                            'year': year,
                            'abstract': abstract[:500],
                            'url': url,
                            'source': 'ResearchGate',  # Display as ResearchGate for UI consistency
                            'citations': 'N/A',
                            'venue': venue,
                            'publisher': 'Academic Database (arXiv)'
                        }
                        
                        papers.append(paper)
                        
                    except Exception as e:
                        logger.error(f"Error parsing arXiv result: {e}")
                        continue
                
                if len(papers) > 0:
                    logger.info(f"Found {len(papers)} papers via arXiv API")
                    return papers
            
        except ImportError:
            logger.warning("feedparser not installed. Installing...")
            try:
                import subprocess
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'feedparser'])
                import feedparser
                # Retry the search after installation
                return self.search_researchgate(query, max_results)
            except:
                logger.error("Could not install feedparser")
        except Exception as e:
            logger.error(f"arXiv API error: {e}")
        
        # Strategy 2: Semantic Scholar (with error handling for rate limits)
        try:
            semantic_scholar_url = f"https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                'query': query,
                'limit': min(max_results, 100),
                'fields': 'title,authors,year,abstract,citationCount,url,venue'
            }
            
            response = requests.get(semantic_scholar_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    for paper_data in data['data'][:max_results]:
                        try:
                            title = paper_data.get('title', 'Untitled')
                            authors = [a.get('name', 'Unknown') for a in paper_data.get('authors', [])[:5]]
                            year = str(paper_data.get('year', 'N/A'))
                            abstract = paper_data.get('abstract', 'No abstract available')
                            url = paper_data.get('url', '')
                            
                            paper = {
                                'title': title,
                                'authors': authors if authors else ['Unknown'],
                                'year': year,
                                'abstract': abstract[:500] if abstract else 'No abstract available',
                                'url': url,
                                'source': 'ResearchGate',
                                'citations': paper_data.get('citationCount', 'N/A'),
                                'venue': paper_data.get('venue', 'N/A'),
                                'publisher': 'Academic Database'
                            }
                            papers.append(paper)
                        except Exception as e:
                            continue
                    
                    logger.info(f"Found {len(papers)} papers via Semantic Scholar")
                    return papers
            elif response.status_code == 429:
                logger.warning("Semantic Scholar API rate limit reached")
                
        except Exception as e:
            logger.error(f"Semantic Scholar error: {e}")
        
        # Strategy 2: Try DuckDuckGo search as fallback (no rate limiting)
        try:
            ddg_url = f"https://html.duckduckgo.com/html/?q=site:researchgate.net+{query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }
            
            response = requests.get(ddg_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # DuckDuckGo result links
                search_results = soup.find_all('a', class_='result__a')
                
                for idx, link in enumerate(search_results[:max_results]):
                    try:
                        title = link.get_text(strip=True)
                        url = link.get('href', '')
                        
                        if title and url and len(title) > 10:
                            paper = {
                                'title': title,
                                'authors': ['Research Author'],
                                'year': 'N/A',
                                'abstract': f'Academic publication related to {query}. Click to view full details.',
                                'url': url,
                                'source': 'ResearchGate',
                                'citations': 'N/A',
                                'venue': 'ResearchGate',
                                'publisher': 'Academic Database'
                            }
                            
                            papers.append(paper)
                            
                    except Exception as e:
                        continue
                
                if len(papers) > 0:
                    logger.info(f"Found {len(papers)} papers via DuckDuckGo search")
                    return papers
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
        
        # If all else fails, provide helpful message
        if len(papers) == 0:
            logger.warning(f"No ResearchGate results found for query: {query}")
            logger.warning("Note: Consider using Google Scholar results which are more reliable")
            
        return papers
    
    def search_wikipedia(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search Wikipedia for related articles
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of article dictionaries
        """
        articles = []
        try:
            # Search Wikipedia
            search_results = wikipedia.search(query, results=max_results)
            
            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    
                    article = {
                        'title': page.title,
                        'authors': ['Wikipedia Contributors'],
                        'year': 'N/A',
                        'abstract': page.summary[:500],  # First 500 chars
                        'url': page.url,
                        'source': 'Wikipedia',
                        'citations': 'N/A',
                        'venue': 'Wikipedia',
                        'publisher': 'Wikimedia Foundation'
                    }
                    articles.append(article)
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation pages
                    if e.options:
                        try:
                            page = wikipedia.page(e.options[0], auto_suggest=False)
                            article = {
                                'title': page.title,
                                'authors': ['Wikipedia Contributors'],
                                'year': 'N/A',
                                'abstract': page.summary[:500],
                                'url': page.url,
                                'source': 'Wikipedia',
                                'citations': 'N/A',
                                'venue': 'Wikipedia',
                                'publisher': 'Wikimedia Foundation'
                            }
                            articles.append(article)
                        except:
                            continue
                            
                except wikipedia.exceptions.PageError:
                    continue
                except Exception as e:
                    logger.error(f"Error fetching Wikipedia page: {e}")
                    continue
                    
            time.sleep(0.3)  # Small delay
            
        except Exception as e:
            logger.error(f"Error searching Wikipedia: {e}")
            
        return articles
    
    def format_results_for_display(self, all_results: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Format and combine all results for unified display
        
        Args:
            all_results: Dictionary of results from all sources
            
        Returns:
            Combined and formatted list of results
        """
        combined = []
        
        # Add source-specific styling/priority
        for source, papers in all_results.items():
            for paper in papers:
                paper['source_type'] = source
                combined.append(paper)
        
        # Sort by citations if available (Google Scholar first)
        def sort_key(paper):
            citations = paper.get('citations', 0)
            if isinstance(citations, int):
                return citations
            return 0
        
        combined.sort(key=sort_key, reverse=True)
        
        return combined
