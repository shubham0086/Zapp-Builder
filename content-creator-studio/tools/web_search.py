import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import time
from urllib.parse import quote_plus
from loguru import logger

class WebSearchTool:
    """Web search tool for research agents"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_duckduckgo(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo (no API key required)"""
        try:
            # DuckDuckGo instant answer API
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            results = []
            
            # Process abstract if available
            if data.get('Abstract'):
                results.append({
                    'title': data.get('Heading', 'DuckDuckGo Summary'),
                    'content': data['Abstract'],
                    'url': data.get('AbstractURL', ''),
                    'source': 'DuckDuckGo'
                })
            
            # Process related topics
            for topic in data.get('RelatedTopics', [])[:max_results-1]:
                if isinstance(topic, dict) and topic.get('Text'):
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'content': topic['Text'],
                        'url': topic.get('FirstURL', ''),
                        'source': 'DuckDuckGo'
                    })
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {str(e)}")
            return []
    
    def scrape_content(self, url: str) -> Dict[str, Any]:
        """Scrape content from a URL"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title = title.text.strip() if title else 'No title'
            
            # Extract main content
            content = ''
            
            # Try to find main content areas
            main_selectors = [
                'main', 'article', '.content', '.post-content', 
                '.entry-content', '.article-body', '#content'
            ]
            
            for selector in main_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    # Extract text from paragraphs
                    paragraphs = main_content.find_all('p')
                    content = ' '.join([p.get_text().strip() for p in paragraphs[:10]])
                    break
            
            # Fallback to all paragraphs if no main content found
            if not content:
                paragraphs = soup.find_all('p')[:10]
                content = ' '.join([p.get_text().strip() for p in paragraphs])
            
            return {
                'title': title,
                'content': content[:2000],  # Limit content length
                'url': url,
                'word_count': len(content.split()),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Content scraping failed for {url}: {str(e)}")
            return {
                'title': 'Scraping failed',
                'content': f'Could not scrape content: {str(e)}',
                'url': url,
                'word_count': 0,
                'success': False
            }
    
    def search_and_scrape(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for content and scrape the results"""
        search_results = self.search_duckduckgo(query, max_results)
        
        enriched_results = []
        
        for result in search_results:
            if result.get('url'):
                # Add a small delay to be respectful
                time.sleep(1)
                
                scraped = self.scrape_content(result['url'])
                
                # Combine search result with scraped content
                enriched_result = {
                    **result,
                    'scraped_title': scraped['title'],
                    'full_content': scraped['content'],
                    'word_count': scraped['word_count'],
                    'scrape_success': scraped['success']
                }
                
                enriched_results.append(enriched_result)
            else:
                enriched_results.append(result)
        
        return enriched_results
    
    def analyze_trends(self, query: str) -> Dict[str, Any]:
        """Analyze trends for a given query (mock implementation)"""
        # This would integrate with Google Trends API or similar
        # For now, return mock trend data
        
        return {
            'query': query,
            'trend_score': 0.75,  # Mock score between 0-1
            'growth_rate': 0.15,  # Mock growth rate
            'related_queries': [
                f"{query} tools",
                f"{query} trends 2024",
                f"best {query}",
                f"{query} guide",
                f"{query} tips"
            ],
            'peak_interest': "High interest in technology and business sectors",
            'geographic_interest': ["United States", "United Kingdom", "Canada"],
            'temporal_interest': "Peak interest during business hours"
        }