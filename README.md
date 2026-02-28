# 🎬 Netflix Data Analyzer - MCP Chatbot

A comprehensive MCP (Model Context Protocol) server with a Streamlit chatbot interface for analyzing Netflix app reviews data.

## Features

### 🔧 FastMCP Server (main.py)
- **12 Analysis Tools** for Netflix data insights
- **3 Resource Endpoints** for data structure and overview
- **Cached Data Loading** for performance optimization
- **Professional Styling** with formatted output

### 📊 Analysis Tools Included

1. **review_score_distribution** - Distribution of review ratings (1-5 stars)
2. **sentiment_analysis** - Positive/Negative/Neutral review classification
3. **top_reviewers** - Most active reviewers on the platform
4. **version_analysis** - App version adoption and distribution
5. **thumbs_up_analysis** - User engagement through thumbs up counts
6. **content_length_analysis** - Review length patterns and statistics
7. **common_topics** - Frequently mentioned keywords in reviews
8. **rating_by_version** - Average ratings for different app versions
9. **review_trends** - Review volume trends over time
10. **user_engagement_score** - Comprehensive engagement metrics
11. **review_completeness** - Data quality and missing values analysis
12. **keyword_sentiment_analysis** - Sentiment analysis for specific keywords

### 💬 Streamlit Chatbot (streamlit_app.py)
- Interactive chat interface with history
- Quick-action buttons for common analyses
- Real-time data processing
- Beautiful UI with custom styling
- Chat history management
- MCP configuration panel

### 📚 Resources
- `netflix://data/overview` - Dataset overview
- `netflix://data/structure` - Data schema and structure
- `netflix://analysis/summary` - Available analysis summary

## Installation

1. **Create Virtual Environment** (Windows):
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the MCP Server
```bash
python main.py
```

### Running the Streamlit Chatbot
In a new terminal:
```bash
streamlit run streamlit_app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## Project Structure

```
Netflix/
├── main.py                 # FastMCP server with 12 analysis tools
├── streamlit_app.py       # Streamlit chatbot interface
├── netflix_data.csv       # Netflix reviews dataset (~145,892 reviews)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Data Structure

The Netflix dataset contains the following columns:
- `reviewId` - Unique review identifier
- `userName` - Reviewer username
- `content` - Review text content
- `score` - Review rating (1-5)
- `thumbsUpCount` - Number of thumbs up
- `reviewCreatedVersion` - App version when review was created
- `at` - Timestamp of review
- `appVersion` - Current app version

## Key Features

### MCP Server
- ✅ 12 comprehensive analysis tools
- ✅ 3 information resources
- ✅ JSON caching for performance
- ✅ Error handling and validation
- ✅ Professional formatted output

### Streamlit Interface
- ✅ Real-time chat conversation
- ✅ Quick analysis buttons
- ✅ Chat history management
- ✅ Beautiful custom styling
- ✅ Data visualization support
- ✅ Configuration panel
- ✅ Clear chat history

## Example Queries

### Sentiment Analysis
```
"Show me sentiment analysis"
"What's the sentiment in reviews?"
"Analyze sentiment of reviews"
```

### Score Distribution
```
"Display score distribution"
"How are reviews rated?"
"Show rating statistics"
```

### Top Reviewers
```
"Show top reviewers"
"Who are the most active reviewers?"
"List top 10 reviewers"
```

### Keyword Analysis
```
"Analyze sentiment for 'streaming'"
"What do people say about Netflix?"
"Sentiment for 'content' keyword"
```

## API Endpoints

### Tools
Each tool can be called with the format:
```
/tool/{tool_name}
```

### Resources
Each resource can be accessed with:
```
/resource/{resource_uri}
```

## Performance

- **Data Loading**: ~1-2 seconds (first load)
- **Cached Loading**: <100ms
- **Analysis Processing**: 1-5 seconds depending on analysis
- **Cache File**: netflix_cache.json (~15-20MB)

## Customization

### Adding New Tools
Edit `main.py` and add new `@server.tool()` decorated functions.

### Styling
Modify the CSS in `streamlit_app.py` under the custom CSS section.

### Analysis Logic
Each analysis tool in `main.py` can be customized by editing the respective function.

## Requirements

- Python 3.8+
- pandas
- fastmcp
- streamlit
- requests

## Troubleshooting

### Data Not Loading
- Ensure `netflix_data.csv` is in the same directory
- Check file encoding (UTF-8)
- Verify CSV format

### Streamlit Connection Issues
- Check if MCP server is running
- Verify localhost and port settings
- Clear browser cache

### Memory Issues
- CSV cache is stored in `netflix_cache.json`
- Clear cache file to free space

## License

MIT License - Feel free to use and modify

## Author

Netflix Data Analyzer v1.0
Built with FastMCP & Streamlit

---

**Note**: This is a demonstration project for Netflix app review analysis. For production use, consider adding authentication, rate limiting, and database optimization.
