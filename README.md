# ScholarSphere - Academic Research Discovery Platform

ScholarSphere is a comprehensive research paper and thesis search engine that aggregates results from Google Scholar, ResearchGate, and Wikipedia. Built with a modern, responsive design featuring glass-morphism effects and smooth animations.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Local Development](#local-development)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Multi-Source Search**: Simultaneously search Google Scholar, ResearchGate, and Wikipedia
🎨 **Modern UI**: Glass-morphism design with animated particles and gradient backgrounds
📱 **Fully Responsive**: Mobile-first design that works on all devices
⚡ **Fast Results**: Efficient aggregation and display of research papers
🔍 **Smart Filtering**: Filter by source, citations, year, and more

## Installation

Follow these steps to set up ScholarSphere locally:

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Ai-searchEngine
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate your virtual environment:
   ```bash
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. Run the application:
   ```bash
   python src/main.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

4. Start searching for research papers!
   - Enter your search query (e.g., "machine learning", "quantum computing")
   - Select your preferred sources (All, Scholar, ResearchGate, or Wikipedia)
   - Browse through beautifully formatted results with citations, abstracts, and direct links

## API Endpoints

- `GET /` - Main application interface
- `GET /research/search?q={query}&source={source}&max={max}` - Search research papers
  - Parameters:
    - `q`: Search query (required)
    - `source`: Source filter (all/scholar/researchgate/wikipedia, default: all)
    - `max`: Maximum results per source (default: 10)

## Technology Stack

**Backend:**
- Flask - Web framework
- BeautifulSoup4 - Web scraping
- Scholarly - Google Scholar API
- Wikipedia API - Wikipedia integration
- scikit-learn - Text similarity and ranking

**Frontend:**
- Modern vanilla JavaScript with ES6+
- TailwindCSS - Utility-first CSS framework
- Custom CSS3 animations and glass-morphism effects
- Canvas API for particle animations
- Font Awesome icons

## Local Development

- Debug mode is enabled by default in `main.py`
- The application auto-reloads on file changes
- Check `src/engine/research_searcher.py` for search logic
- Modify `src/static/css/style.css` for styling changes
- Update `src/static/js/app.js` for frontend functionality

## Contributing

Explain how others can contribute to your project (fork, branch, PRs, etc.)

## License

State the license under which your project is released, for example:

This project is licensed under the MIT License - see the LICENSE file for details.


To activate the virtual environment and run the application:

