# Steel Web Loader for LangChain

## Overview
This custom document loader uses Steel.dev's browser automation to load web pages for LangChain document processing.

## Features
- Uses Steel.dev for robust web page loading
- Supports different content extraction strategies
- Handles dynamic web content
- Provides metadata about the source and extraction method

## Installation

```bash
pip install steel-sdk langchain-community
```

## Usage

```python
from steel_web_loader import SteelWebLoader

# Basic usage
loader = SteelWebLoader(
    url='https://www.example.com',
    extract_strategy='text'  # Options: 'text', 'html', 'markdown'
)

# Load documents
documents = loader.load()

# Process documents in a LangChain pipeline
```

## Configuration

### Extract Strategies
- `text`: Plain text extraction
- `html`: Full HTML content
- `markdown`: Markdown conversion (simplified in current version)

### Environment Variables
Set your Steel API key:
```
STEEL_API_KEY=your_steel_api_key_here
```

## Advanced Usage with RAG

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load documents
loader = SteelWebLoader('https://www.example.com')
documents = loader.load()

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Perform similarity search
results = vectorstore.similarity_search("Your query")
```

## Limitations
- Requires active Steel.dev API key
- Performance depends on Steel.dev session and network conditions
- Some complex web pages might require additional parsing

## Contributing
Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.