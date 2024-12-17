# Steel Browser Automation Toolkit

## Overview
A Python toolkit for web automation using Steel.dev and Playwright.

## Features
- Managed Steel browser sessions
- Web page loading with LangChain integration
- Easy session and browser management

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/steel-browser.git
cd steel-browser

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -e .
```

## Configuration
1. Create a `.env` file in the project root
2. Add your Steel API key:
```
STEEL_API_KEY=your_steel_api_key_here
```

## Usage Examples

### Basic Session Management
```python
from steel_browser.session_manager import SteelSessionManager

with SteelSessionManager() as session:
    browser = session.connect_playwright()
    # Perform browser operations
```

### Web Page Loading
```python
from steel_browser.web_loader import SteelWebLoader

loader = SteelWebLoader('https://www.example.com')
documents = loader.load()
```

## Running Examples
```bash
python examples/web_loader_example.py
```

## Testing
```bash
pytest tests/
```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Your License Here]