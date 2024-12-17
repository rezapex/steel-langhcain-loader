import os
from dotenv import load_dotenv

from steel import Steel
from playwright.sync_api import sync_playwright

from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader

class SteelWebLoader(BaseLoader):
    """
    Web page loader using Steel and Playwright for Langchain
    """
    def __init__(
        self, 
        url: str, 
        steel_api_key: str = None,
        timeout: int = 30000
    ):
        """
        Initialize the Steel Web Loader
        
        :param url: Web page URL to load
        :param steel_api_key: Steel API key
        :param timeout: Navigation timeout in milliseconds
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.steel_api_key = steel_api_key or os.getenv('STEEL_API_KEY')
        if not self.steel_api_key:
            raise ValueError("STEEL_API_KEY must be set in .env file")
        
        self.url = url
        self.timeout = timeout

    def load(self):
        """
        Load web page content using Steel and Playwright
        
        :return: List of Documents
        """
        # Initialize Steel client
        client = Steel(steel_api_key=self.steel_api_key)
        
        # Create Steel session
        session = client.sessions.create(
            use_proxy=True,    # Use Steel's proxy network
            solve_captcha=True # Enable CAPTCHA solving if needed
        )
        
        try:
            # Connect Playwright to the Steel session
            with sync_playwright() as playwright:
                browser = playwright.chromium.connect_over_cdp(
                    f"wss://connect.steel.dev?apiKey={self.steel_api_key}&sessionId={session.id}"
                )
                
                # Create a new page
                context = browser.contexts[0]
                page = context.new_page()
                
                # Navigate to the URL
                page.goto(self.url, wait_until="networkidle")
                
                # Extract page content
                content = page.inner_text('body')
                
                # Create Langchain Document
                document = Document(
                    page_content=content,
                    metadata={
                        'source': self.url,
                        'steel_session_id': session.id,
                        'steel_session_url': session.session_viewer_url
                    }
                )
                
                return [document]
        
        except Exception as e:
            print(f"Error loading {self.url}: {e}")
            return []
        
        finally:
            # Always release the session
            client.sessions.release(session.id)

def main():
    # URL to load
    url = 'https://www.example.com'
    
    # Create loader
    loader = SteelWebLoader(url)
    
    # Load documents
    documents = loader.load()
    
    # Print document details
    for doc in documents:
        print("\n--- Document Details ---")
        print(f"Source: {doc.metadata['source']}")
        print(f"Steel Session ID: {doc.metadata['steel_session_id']}")
        print(f"Steel Session URL: {doc.metadata['steel_session_url']}")
        print("\nContent Preview:")
        print(doc.page_content[:500] + "...")

if __name__ == '__main__':
    main()