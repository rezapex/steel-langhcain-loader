from typing import List, Optional
import logging
import asyncio
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from playwright.async_api import async_playwright

from .session_manager import SteelSessionManager

class SteelWebLoader(BaseLoader):
    """
    Async Web page loader using Steel session management
    """
    
    def __init__(
        self, 
        url: str, 
        steel_api_key: Optional[str] = None,
        extract_strategy: str = 'text',
        timeout: int = 30000
    ):
        """
        Initialize the Steel Web Loader
        
        :param url: Web page URL to load
        :param steel_api_key: Steel API key
        :param extract_strategy: Content extraction method
        :param timeout: Navigation timeout in milliseconds
        """
        self.url = url
        self.steel_api_key = steel_api_key
        self.extract_strategy = extract_strategy
        self.timeout = timeout
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Validate extract strategy
        valid_strategies = ['text', 'markdown', 'html']
        if extract_strategy not in valid_strategies:
            raise ValueError(
                f"Invalid extract_strategy. Must be one of {valid_strategies}"
            )
    
    async def aload(self) -> List[Document]:
        """
        Async load method for web page content
        
        :return: List of Documents
        """
        # Use session manager to handle session lifecycle
        with SteelSessionManager(steel_api_key=self.steel_api_key) as session_manager:
            # Create session and get details
            session_info = session_manager.create_session()
            self.logger.info(f"Created session: {session_info['id']}")
            
            # Initialize Playwright
            playwright = await async_playwright().start()
            
            try:
                # Connect to Steel session
                browser = await playwright.chromium.connect_over_cdp(
                    f"wss://connect.steel.dev?apiKey={self.steel_api_key}&sessionId={session_info['id']}"
                )
                
                # Create new page
                context = browser.contexts[0]
                page = await context.new_page()
                
                # Navigate to URL
                await page.goto(
                    self.url, 
                    wait_until="networkidle", 
                    timeout=self.timeout
                )
                
                # Extract content based on strategy
                if self.extract_strategy == 'text':
                    content = await page.inner_text('body')
                elif self.extract_strategy == 'markdown':
                    content = await page.inner_text('body')  # Simplified
                else:  # html
                    content = await page.content()
                
                # Create and return document
                return [
                    Document(
                        page_content=content,
                        metadata={
                            'source': self.url,
                            'steel_session_id': session_info['id'],
                            'steel_session_viewer_url': session_info['viewer_url'],
                            'extract_strategy': self.extract_strategy
                        }
                    )
                ]
            
            except Exception as e:
                self.logger.error(f"Error loading {self.url}: {e}")
                return []
            
            finally:
                # Ensure Playwright is stopped
                await playwright.stop()
    
    def load(self) -> List[Document]:
        """
        Synchronous load method that runs the async load
        
        :return: List of Documents
        """
        return asyncio.run(self.aload())