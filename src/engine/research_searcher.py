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
        try:
            # Use more robust search approach
            search_url = f"https://www.researchgate.net/search/publication?q={query.replace(' ', '%20')}"
            
            # Rotate user agents to avoid blocking
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Multiple selector strategies
                results = []
                
                # Strategy 1: Look for article/research items
                results = soup.find_all('div', {'data-testid': re.compile('publication|research')})
                
                if not results:
                    # Strategy 2: Search result items
                    results = soup.find_all('div', class_=re.compile('search-box__result-item|research-item'))
                
                if not results:
                    # Strategy 3: Generic containers with links
                    results = soup.find_all('div', class_=re.compile('nova-legacy-o-stack__item'))
                
                logger.info(f"Found {len(results)} ResearchGate results")
                
                for idx, result in enumerate(results[:max_results]):
                    try:
                        # Find title with multiple strategies
                        title_elem = (result.find('a', class_=re.compile('nova-legacy-e-link.*nova-legacy-e-link--theme-bare')) or
                                    result.find('a', href=re.compile('/publication/')) or
                                    result.find('h3') or
                                    result.find('div', class_=re.compile('nova-legacy-e-text.*nova-legacy-e-text--size-l')))
                        
                        if not title_elem:
                            continue
                            
                        title = title_elem.get_text(strip=True) if title_elem else f"Research Paper {idx+1}"
                        url = ''
                        
                        if title_elem.name == 'a':
                            url = title_elem.get('href', '')
                        elif title_elem.find_parent('a'):
                            url = title_elem.find_parent('a').get('href', '')
                        
                        if url and not url.startswith('http'):
                            url = 'https://www.researchgate.net' + url
                        
                        # Extract authors
                        authors = []
                        author_links = result.find_all('a', href=re.compile('/profile/'))
                        if author_links:
                            authors = [a.get_text(strip=True) for a in author_links[:5]]
                        
                        if not authors:
                            # Fallback: look for author text
                            author_elem = result.find('div', class_=re.compile('nova-legacy-v-person-list-item'))
                            if author_elem:
                                authors = [author_elem.get_text(strip=True)]
                        
                        # Extract year
                        year = 'N/A'
                        date_text = result.get_text()
                        year_match = re.search(r'\b(19|20)\d{2}\b', date_text)
                        if year_match:
                            year = year_match.group(0)
                        
                        # Extract abstract/snippet
                        abstract = 'No abstract available'
                        abstract_elem = (result.find('div', class_=re.compile('nova-legacy-e-text.*nova-legacy-e-text--color-grey-700')) or
                                       result.find('div', class_=re.compile('publication-preview|research-snippet')))
                        if abstract_elem:
                            abstract = abstract_elem.get_text(strip=True)[:500]
                        
                        # Only add if we have a valid title
                        if title and len(title) > 3:
                            paper = {
                                'title': title,
                                'authors': authors if authors else ['Unknown'],
                                'year': year,
                                'abstract': abstract,
                                'url': url if url else f"https://www.researchgate.net/search/publication?q={query.replace(' ', '+')}",
                                'source': 'ResearchGate',
                                'citations': 'N/A',
                                'venue': 'N/A',
                                'publisher': 'ResearchGate'
                            }
                            papers.append(paper)
                            logger.info(f"Successfully parsed ResearchGate paper: {title[:50]}...")
                        
                    except Exception as e:
                        logger.error(f"Error parsing ResearchGate result {idx}: {e}")
                        continue
                        
            time.sleep(1)  # Respectful delay
            
        except Exception as e:
            logger.error(f"Error searching ResearchGate: {e}")
            
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
