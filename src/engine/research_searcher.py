"""
Research Paper Search Engine
Integrates with Google Scholar, ResearchGate, and Wikipedia for academic research
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
import re
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
        Search ResearchGate for research papers
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of paper dictionaries
        """
        papers = []
        
        # IMPORTANT: ResearchGate has strong anti-scraping measures
        # This implementation provides a fallback approach
        
        try:
            # Attempt to use Google search with site:researchgate.net
            google_search_url = f"https://www.google.com/search?q=site:researchgate.net+{query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(google_search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract Google search results that link to ResearchGate
                search_results = soup.find_all('div', class_='g')
                
                for idx, result in enumerate(search_results[:max_results]):
                    try:
                        # Get title
                        title_elem = result.find('h3')
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        # Get URL
                        link_elem = result.find('a', href=True)
                        url = link_elem['href'] if link_elem else ''
                        
                        # Extract from citation text
                        snippet_elem = result.find('div', class_=re.compile('VwiC3b|s3v9rd'))
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else 'No description available'
                        
                        # Try to extract authors and year from snippet
                        authors = []
                        year = 'N/A'
                        
                        # Look for patterns like "Author Name, Year"
                        author_year_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(19|20)\d{2}', snippet)
                        if author_year_match:
                            authors = [author_year_match.group(1)]
                            year = author_year_match.group(2)
                        
                        if not authors:
                            authors = ['ResearchGate Author']
                        
                        paper = {
                            'title': title,
                            'authors': authors,
                            'year': year,
                            'abstract': snippet[:500],
                            'url': url if 'researchgate.net' in url else f"https://www.researchgate.net/search/publication?q={query.replace(' ', '+')}",
                            'source': 'ResearchGate',
                            'citations': 'N/A',
                            'venue': 'ResearchGate',
                            'publisher': 'ResearchGate'
                        }
                        
                        papers.append(paper)
                        logger.info(f"Found ResearchGate paper via Google: {title[:50]}...")
                        
                    except Exception as e:
                        logger.error(f"Error parsing Google result {idx}: {e}")
                        continue
            
            # If Google approach didn't work or got no results, use direct search with simplified parsing
            if len(papers) == 0:
                logger.warning("Google search failed, trying direct ResearchGate search...")
                direct_url = f"https://www.researchgate.net/search/publication?q={query.replace(' ', '%20')}"
                
                try:
                    response = requests.get(direct_url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for any links that might be publications
                        all_links = soup.find_all('a', href=re.compile('/publication/'))
                        
                        seen_titles = set()
                        for link in all_links[:max_results * 2]:  # Get more to filter duplicates
                            try:
                                title = link.get_text(strip=True)
                                
                                # Skip if empty or duplicate
                                if not title or len(title) < 10 or title in seen_titles:
                                    continue
                                
                                seen_titles.add(title)
                                url = link.get('href', '')
                                
                                if url and not url.startswith('http'):
                                    url = 'https://www.researchgate.net' + url
                                
                                paper = {
                                    'title': title,
                                    'authors': ['ResearchGate Author'],
                                    'year': 'N/A',
                                    'abstract': f'Research publication related to {query}. Click to view full details on ResearchGate.',
                                    'url': url,
                                    'source': 'ResearchGate',
                                    'citations': 'N/A',
                                    'venue': 'ResearchGate',
                                    'publisher': 'ResearchGate'
                                }
                                
                                papers.append(paper)
                                
                                if len(papers) >= max_results:
                                    break
                                    
                            except Exception as e:
                                continue
                        
                        logger.info(f"Direct search found {len(papers)} ResearchGate papers")
                        
                except Exception as e:
                    logger.error(f"Direct ResearchGate search failed: {e}")
            
            time.sleep(1)  # Respectful delay
            
        except Exception as e:
            logger.error(f"Error searching ResearchGate: {e}")
        
        # If still no results, log a warning
        if len(papers) == 0:
            logger.warning(f"No ResearchGate results found for query: {query}")
            logger.warning("Note: ResearchGate has anti-scraping measures that may prevent data access")
            
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
