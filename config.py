"""
Configuration file for Netflix Data Analyzer
Customize these settings as needed
"""

import os
from pathlib import Path

# ============= FILE CONFIGURATION =============
DATA_FILE = Path("netflix_data.csv")
CACHE_FILE = Path("netflix_cache.json")

# ============= SERVER CONFIGURATION =============
MCP_SERVER_NAME = "Netflix Data Analyzer"
MCP_PORT = 8000
MCP_HOST = "localhost"

# ============= ANALYSIS CONFIGURATION =============
# Number of results to return for top-k analyses
TOP_K_RESULTS = 10

# Stopwords for keyword analysis
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'is', 'it', 'to', 'of', 'in', 'for', 'on', 'with',
    'i', 'you', 'he', 'she', 'this', 'that', 'be', 'have', 'has', 'are', 'was', 'were',
    'very', 'so', 'as', 'from', 'by', 'at', 'my', 'me', 'if', 'can', 'get', 'got', 'really',
    'just', 'more', 'one', 'two', 'like', 'love', 'good', 'bad', 'netflix'
}

# Sentiment analysis keywords
POSITIVE_KEYWORDS = {
    'love', 'great', 'excellent', 'amazing', 'perfect', 'good', 'best', 'awesome',
    'wonderful', 'fantastic', 'awesome', 'great', 'cool', 'nice', 'brilliant',
    'superb', 'outstanding', 'incredible', 'wonderful', 'marvelous'
}

NEGATIVE_KEYWORDS = {
    'hate', 'bad', 'terrible', 'awful', 'worst', 'poor', 'horrible', 'useless',
    'broken', 'garbage', 'terrible', 'awful', 'disappointing', 'waste', 'pathetic',
    'disgusting', 'appalling', 'abysmal', 'dreadful', 'rubbish'
}

# ============= STREAMLIT CONFIGURATION =============
STREAMLIT_THEME = "light"  # "light" or "dark"
CHAT_HISTORY_LIMIT = 100  # Maximum messages to keep in history

# ============= UI CONFIGURATION =============
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#2ca02c"
ERROR_COLOR = "#d62728"

# App title and description
APP_TITLE = "🎬 Netflix Data Analyzer Chatbot"
APP_DESCRIPTION = "Interactive AI Assistant for Netflix Reviews Analysis"

# ============= RESOURCE URIS =============
RESOURCES = {
    "netflix://data/overview": "Dataset overview",
    "netflix://data/structure": "Data schema and structure",
    "netflix://analysis/summary": "Available analysis summary"
}

# ============= TOOLS =============
TOOLS = {
    "review_score_distribution": "Analyze the distribution of review scores",
    "sentiment_analysis": "Analyze sentiment from review content",
    "top_reviewers": "Identify the most active reviewers",
    "version_analysis": "Analyze app version adoption",
    "thumbs_up_analysis": "Analyze engagement through thumbs up",
    "content_length_analysis": "Analyze review content length patterns",
    "common_topics": "Extract common topics and keywords",
    "rating_by_version": "Compare ratings across app versions",
    "review_trends": "Analyze review trends over time",
    "user_engagement_score": "Calculate user engagement metrics",
    "review_completeness": "Analyze data completeness",
    "keyword_sentiment_analysis": "Analyze sentiment for keywords"
}

# ============= CSV COLUMNS =============
CSV_COLUMNS = [
    'reviewId',
    'userName',
    'content',
    'score',
    'thumbsUpCount',
    'reviewCreatedVersion',
    'at',
    'appVersion'
]

# ============= ENCODING =============
CSV_ENCODING = 'utf-8'
JSON_ENCODING = 'utf-8'

# ============= CACHE SETTINGS =============
ENABLE_CACHE = True
CACHE_EXPIRY_HOURS = 24  # Cache expires after 24 hours

# ============= LOGGING =============
LOG_LEVEL = "INFO"  # "DEBUG", "INFO", "WARNING", "ERROR"
LOG_FILE = "netflix_analyzer.log"

# ============= PERFORMANCE =============
MAX_RESULTS_PER_QUERY = 1000  # Limit results to prevent memory issues
BATCH_SIZE = 1000  # Process data in batches

# ============= DATABASE (Optional - for future use) =============
USE_DATABASE = False
DATABASE_URL = "sqlite:///netflix_analyzer.db"

# ============= API KEYS (Optional) =============
# Add any API keys here for future enhancements
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# ============= FEATURE FLAGS =============
ENABLE_ADVANCED_NLP = False  # Set to True to enable advanced NLP features
ENABLE_VISUALIZATION = True  # Enable chart generation
ENABLE_EXPORT = True  # Enable result export

# ============= TIMEZONE =============
TIMEZONE = "UTC"

# ============= REGEX PATTERNS =============
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
URL_PATTERN = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'

# ============= VALIDATION =============
MIN_REVIEW_LENGTH = 1  # Minimum characters in a review
MAX_REVIEW_LENGTH = 50000  # Maximum characters in a review
VALID_SCORES = [1, 2, 3, 4, 5]  # Valid review scores

# ============= QUICK SHORTCUTS =============
TOOL_KEYWORDS = {
    "score": "review_score_distribution",
    "rating": "review_score_distribution",
    "sentiment": "sentiment_analysis",
    "mood": "sentiment_analysis",
    "reviewer": "top_reviewers",
    "user": "top_reviewers",
    "version": "version_analysis",
    "app": "version_analysis",
    "thumbs": "thumbs_up_analysis",
    "engagement": "user_engagement_score",
    "length": "content_length_analysis",
    "topic": "common_topics",
    "keyword": "common_topics",
    "trend": "review_trends",
    "time": "review_trends",
    "complete": "review_completeness",
    "quality": "review_completeness"
}

# ============= DEFAULT VALUES =============
DEFAULT_LIMIT = 10
DEFAULT_KEYWORD = "netflix"
DEFAULT_TIMEOUT = 30  # seconds

# ============= MESSAGES =============
MESSAGES = {
    "welcome": "Welcome to Netflix Data Analyzer! 🎬",
    "error": "An error occurred: {}",
    "no_data": "No data available for this query",
    "loading": "Loading analysis...",
    "complete": "Analysis complete!"
}

# ============= NOTEPAD++ OPENING INSTRUCTIONS =============
NOTEPAD_PLUS_PLUS_INSTRUCTIONS = """
1. Open Notepad++
2. File → Open → Navigate to:
   C:\\Users\\91952\\Documents\\Projects\\GenAi\\McpProject\\Netflix\\
3. Open:
   - streamlit_app.py (to customize chatbot)
   - main.py (to modify analysis tools)
   - config.py (to change settings)
4. Edit and save
5. Restart servers to see changes
"""
