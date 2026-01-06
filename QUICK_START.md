# ScholarSphere - Quick Start Guide

## 🎯 What is ScholarSphere?

**ScholarSphere** is your comprehensive academic research discovery platform. It simultaneously searches:
- **Google Scholar** - Academic papers and citations
- **ResearchGate** - Research publications and preprints  
- **Wikipedia** - Encyclopedia articles and summaries

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate     # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python src/main.py
```

### 3. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## 🎨 Features Overview

### Modern Glass-Morphism Design
- Animated gradient background with floating orbs
- Particle system with connected nodes
- Glass-morphism cards with blur effects
- Smooth transitions and hover animations

### Advanced Search Capabilities
- **Universal Search**: Search all sources at once
- **Source Filtering**: Focus on specific databases
- **Result Limiting**: Control number of results per source
- **Quick Searches**: One-click popular topics

### Rich Result Display
- **Paper Cards** with:
  - Title and authors
  - Publication year and venue
  - Abstract preview
  - Citation count (Google Scholar)
  - Direct link to full paper
  - Source badges

## 🔍 How to Use

### Basic Search
1. Enter your research topic in the search box
2. Click "Search" or press Enter
3. View results from all sources

### Advanced Filtering
- **Sources Tab**: Select "All Sources", "Scholar", "ResearchGate", or "Wikipedia"
- **Results Dropdown**: Choose 5, 10, 15, or 20 results per source

### Quick Topics
Click any popular topic tag:
- Machine Learning
- Quantum Computing
- Climate Change
- Artificial Intelligence
- Neuroscience

## 📱 Responsive Design

ScholarSphere works perfectly on:
- 🖥️ Desktop (1920px+)
- 💻 Laptop (1366px-1920px)
- 📱 Tablet (768px-1366px)
- 📱 Mobile (320px-768px)

## 🛠️ Project Structure

```
Ai-searchEngine/
├── src/
│   ├── main.py                      # Flask application
│   ├── engine/
│   │   ├── research_searcher.py     # Multi-source search engine
│   │   ├── indexer.py               # Document indexing
│   │   └── searcher.py              # Local search
│   ├── templates/
│   │   └── index.html               # Main UI
│   └── static/
│       ├── css/
│       │   └── style.css            # Glass-morphism styling
│       └── js/
│           └── app.js               # Dynamic search & particles
├── requirements.txt                  # Python dependencies
└── README.md                        # Full documentation
```

## 🎨 Design Features

### Color Palette
- **Primary**: Indigo (#6366f1)
- **Secondary**: Pink (#ec4899)
- **Accent**: Amber (#f59e0b)
- **Success**: Green (#10b981)

### Typography
- **Headings**: Playfair Display (Serif)
- **Body**: Inter (Sans-serif)

### Animations
- Gradient background shift (15s loop)
- Floating orbs (20s loop)
- Particle connections
- Card hover effects
- Button transitions

## 🔧 Customization

### Change Colors
Edit `src/static/css/style.css`:
```css
:root {
    --primary: #6366f1;
    --secondary: #ec4899;
    /* ... modify as needed */
}
```

### Modify Particle Count
Edit `src/static/js/app.js`:
```javascript
this.particleCount = 50; // Change this number
```

### Adjust Search Results
Edit `src/engine/research_searcher.py`:
```python
def search_all(self, query: str, max_results: int = 10):
    # Modify search logic here
```

## 🚨 Troubleshooting

### Issue: No results appearing
- Check your internet connection
- Some sources may be rate-limited - try again in a few minutes
- Try different search terms

### Issue: Slow search
- Reduce `max_results` parameter
- Select specific source instead of "All"
- Scholarly API can be slow - this is normal

### Issue: CSS not loading
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors
- Ensure Flask is serving static files correctly

## 📊 Performance Tips

1. **Start with specific queries** - "machine learning optimization" vs "AI"
2. **Use source filtering** - Faster than searching all sources
3. **Limit results** - 5-10 results are usually sufficient
4. **Cache results** - Browser caches responses automatically

## 🌟 Best Practices

### For Best Results:
- ✅ Use specific, academic terminology
- ✅ Include author names if known
- ✅ Add year ranges for recent work
- ✅ Combine multiple keywords

### Avoid:
- ❌ Very broad terms ("science", "research")
- ❌ Too many search terms (keep it focused)
- ❌ Special characters in queries

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Scholar** for academic paper database
- **ResearchGate** for research community
- **Wikipedia** for knowledge base
- **Scholarly** Python library
- **Flask** web framework

---

**Happy Researching! 🎓✨**

For issues or questions, check the main README.md or open an issue on GitHub.
