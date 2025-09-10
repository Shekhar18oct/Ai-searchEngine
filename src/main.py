from flask import Flask, jsonify, request, render_template # pyright: ignore[reportMissingImports]
from engine.indexer import Indexer
from engine.searcher import Searcher
from models.document import Document
import uuid
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
import json

# Load environment variables
load_dotenv()

# API Keys configuration
class APIConfig:
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    STACKOVERFLOW_KEY = os.getenv('STACKOVERFLOW_KEY')
    GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

    @staticmethod
    def check_api_keys():
        missing_keys = []
        if not APIConfig.YOUTUBE_API_KEY:
            missing_keys.append("YouTube API Key")
        if not APIConfig.GITHUB_TOKEN:
            missing_keys.append("GitHub Token")
        if not APIConfig.STACKOVERFLOW_KEY:
            missing_keys.append("Stack Overflow API Key")
        
        if missing_keys:
            print("Warning: The following API keys are missing:")
            for key in missing_keys:
                print(f"- {key}")
            print("Some search features may be limited.")
        
        return len(missing_keys) == 0

# Check API keys on startup
api_keys_valid = APIConfig.check_api_keys()

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Initialize the search engine components
indexer = Indexer()
searcher = Searcher(indexer)

@app.route('/')
def index():
    return render_template('index.html')

# Sample documents for testing
sample_docs = [
    Document(
        id=str(uuid.uuid4()),
        title="Introduction to AI",
        content="Artificial Intelligence (AI) is the simulation of human intelligence by machines. It involves creating systems that can learn, reason, and solve problems.",
        url="https://example.com/ai-intro",
        created_at=datetime.now()
    ),
    Document(
        id=str(uuid.uuid4()),
        title="Machine Learning Basics",
        content="Machine Learning is a subset of AI that focuses on training models to learn from data. It includes supervised, unsupervised, and reinforcement learning approaches.",
        url="https://example.com/ml-basics",
        created_at=datetime.now()
    ),
]

# Index sample documents
for doc in sample_docs:
    indexer.index_document(doc)

@app.route('/search', methods=['GET'])
def search():
    """Universal search endpoint"""
    query = request.args.get('q', '')
    source = request.args.get('source', 'local')  # 'local', 'youtube', 'stackoverflow', 'github'
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
        
    if source == 'youtube':
        return redirect(f'https://www.youtube.com/results?search_query={query}') # pyright: ignore[reportUndefinedVariable]
    elif source == 'stackoverflow':
        return redirect(f'https://stackoverflow.com/search?q={query}') # pyright: ignore[reportUndefinedVariable]
    elif source == 'github':
        return redirect(f'https://github.com/search?q={query}') # pyright: ignore[reportUndefinedVariable]
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = {
        "query": query,
        "local_results": [],
        "web_results": [],
        "youtube_results": [],
        "stackoverflow_results": [],
        "github_results": []
    }

    # Local search
    if 'local' in sources: # type: ignore
        local_results = searcher.search(query, top_k=5)
        results["local_results"] = local_results

    # YouTube search
    if 'youtube' in sources and APIConfig.YOUTUBE_API_KEY: # type: ignore
        youtube_url = f"https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': query,
            'key': APIConfig.YOUTUBE_API_KEY,
            'maxResults': 5,
            'type': 'video'
        }
        try:
            response = requests.get(youtube_url, params=params)
            if response.status_code == 200:
                results["youtube_results"] = response.json().get('items', [])
        except Exception as e:
            print(f"YouTube API error: {e}")

    # Stack Overflow search
    if 'stackoverflow' in sources and APIConfig.STACKOVERFLOW_KEY: # type: ignore
        stackoverflow_url = f"https://api.stackexchange.com/2.3/search"
        params = {
            'intitle': query,
            'site': 'stackoverflow',
            'key': APIConfig.STACKOVERFLOW_KEY,
            'pagesize': 5,
            'order': 'desc',
            'sort': 'relevance'
        }
        try:
            response = requests.get(stackoverflow_url, params=params)
            if response.status_code == 200:
                results["stackoverflow_results"] = response.json().get('items', [])
        except Exception as e:
            print(f"Stack Overflow API error: {e}")

    # GitHub search
    if 'github' in sources and APIConfig.GITHUB_TOKEN: # pyright: ignore[reportUndefinedVariable]
        github_url = "https://api.github.com/search/repositories"
        headers = {'Authorization': f'token {APIConfig.GITHUB_TOKEN}'}
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 5
        }
        try:
            response = requests.get(github_url, headers=headers, params=params)
            if response.status_code == 200:
                results["github_results"] = response.json().get('items', [])
        except Exception as e:
            print(f"GitHub API error: {e}")

    return jsonify(results)

@app.route('/documents', methods=['POST'])
def add_document():
    """Add a new document to the index"""
    data = request.json
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400
    
    doc = Document(
        id=str(uuid.uuid4()),
        title=data['title'],
        content=data['content'],
        url=data.get('url'),
        created_at=datetime.now()
    )
    
    indexer.index_document(doc)
    return jsonify(doc.to_dict()), 201

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get all indexed documents"""
    return jsonify(searcher.get_results())

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)