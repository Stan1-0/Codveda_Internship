import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from typing import List, Tuple, Set
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WebScraper:
    """Efficient web scraper for extracting headlines from websites."""
    
    def __init__(self, delay: float = 1.0, timeout: int = 10, max_retries: int = 3):
        """
        Initialize the scraper with configuration.
        
        Args:
            delay: Delay between requests in seconds
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.delay = delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
    
    def _make_request(self, url: str) -> requests.Response:
        """Make a request with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.delay * (attempt + 1))  # Exponential backoff
    
    def _extract_headlines_from_soup(self, soup: BeautifulSoup, base_url: str) -> Set[Tuple[str, str]]:
        """Extract headlines from parsed HTML using efficient selectors."""
        headlines = set()
        
        # Single pass through the HTML with comprehensive selectors
        selectors = [
            # Article headlines
            "article h1, article h2, article h3",
            # Standalone headlines
            "h1, h2",
            # Headlines in common containers
            ".headline, .title, .post-title, .article-title",
            # Links that might be headlines
            "a[class*='head'], a[class*='title'], a[class*='post']"
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10:  # Filter out very short text
                    # Get link if it's an anchor tag or find parent link
                    link = None
                    if element.name == 'a' and element.get('href'):
                        link = urljoin(base_url, element.get('href'))
                    else:
                        parent_link = element.find_parent('a')
                        if parent_link and parent_link.get('href'):
                            link = urljoin(base_url, parent_link.get('href'))
                    
                    headlines.add((text, link or ""))
        
        return headlines
    
    def scrape_website(self, url: str, max_pages: int = 10, min_headlines: int = 10) -> List[Tuple[str, str]]:
        """
        Scrape headlines from a website.
        
        Args:
            url: Base URL to scrape
            max_pages: Maximum number of pages to scrape
            min_headlines: Minimum number of headlines to collect before stopping
            
        Returns:
            List of (headline, link) tuples
        """
        all_headlines = set()
        page = 1
        
        logger.info(f"Starting to scrape {url}")
        
        while page <= max_pages:
            try:
                page_url = f"{url}?page={page}" if page > 1 else url
                logger.info(f"Scraping page {page}: {page_url}")
                
                response = self._make_request(page_url)
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract headlines from current page
                page_headlines = self._extract_headlines_from_soup(soup, url)
                all_headlines.update(page_headlines)
                
                logger.info(f"Found {len(page_headlines)} headlines on page {page}")
                
                # Stop if we have enough headlines or no new headlines found
                if len(page_headlines) == 0 or len(all_headlines) >= min_headlines:
                    break
                
                time.sleep(self.delay)
                page += 1
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to scrape page {page}: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error on page {page}: {e}")
                break
        
        # Convert set to list and sort by headline length (longer headlines are usually more informative)
        result = list(all_headlines)
        result.sort(key=lambda x: len(x[0]), reverse=True)
        
        logger.info(f"Scraping completed. Total headlines found: {len(result)}")
        return result
    
    def close(self):
        """Close the session."""
        self.session.close()


def main():
    """Main function to run the scraper."""
    try:
        url = input("Enter the website URL: ").strip()
        if not url:
            print("No URL provided. Exiting.")
            return
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        scraper = WebScraper(delay=1.0, timeout=10, max_retries=3)
        
        try:
            headlines = scraper.scrape_website(url, max_pages=5, min_headlines=10)
            
            print(f"\nFound {len(headlines)} headlines:")
            print("-" * 50)
            
            for i, (headline, link) in enumerate(headlines[:10], 1):
                link_text = f" [{link}]" if link else ""
                print(f"{i}. {headline}{link_text}")
            
            if len(headlines) > 10:
                print(f"\n... and {len(headlines) - 10} more headlines")
                
        finally:
            scraper.close()
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()