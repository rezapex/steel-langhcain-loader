import os
from dotenv import load_dotenv
from steel import Steel
from playwright.sync_api import sync_playwright

def main():
    # Load environment variables
    load_dotenv()

    # Get Steel API key
    steel_api_key = os.getenv('STEEL_API_KEY')
    if not steel_api_key:
        raise ValueError("STEEL_API_KEY must be set in .env file")

    # Initialize Steel client
    client = Steel(steel_api_key=steel_api_key)

    # Create a Steel session
    try:
        # Create session with basic configuration
        session = client.sessions.create(
            use_proxy=True,    # Use Steel's proxy network
            solve_captcha=True # Enable CAPTCHA solving if needed
        )

        print(f"Session created successfully!")
        print(f"Session ID: {session.id}")
        print(f"Session Viewer URL: {session.session_viewer_url}")

        # Connect Playwright to the Steel session
        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(
                f"wss://connect.steel.dev?apiKey={steel_api_key}&sessionId={session.id}"
            )

            # Create a new page
            context = browser.contexts[0]
            page = context.new_page()

            # Navigate to a website
            page.goto('https://www.example.com')

            # Extract page title as a simple interaction
            print(f"Page Title: {page.title()}")

            # Optional: Take a screenshot
            page.screenshot(path='example_screenshot.png')
            print("Screenshot saved as example_screenshot.png")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Always release the session
        try:
            client.sessions.release(session.id)
            print("Session released successfully!")
        except Exception as release_error:
            print(f"Error releasing session: {release_error}")

if __name__ == '__main__':
    main()