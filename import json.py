import json
import csv
from pathlib import Path
from typing import Any
from datetime import datetime
import statistics
from collections import Counter
import mcp.server.stdio
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource, ResourceTemplate
import fastmcp

# Initialize FastMCP server
server = fastmcp.FastMCP("Netflix Data Analyzer")

# Load Netflix data
DATA_FILE = Path("netflix_data.csv")
CACHE_FILE = Path("netflix_cache.json")

def load_netflix_data() -> list[dict]:
    """Load Netflix CSV data"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    
    data = []
    try:
        with open(DATA_FILE, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        return []
    
    return data

# Load data at startup
NETFLIX_DATA = load_netflix_data()

# ============= RESOURCES =============
@server.resource("netflix://data/overview")
def get_data_overview() -> str:
    """Overview of Netflix dataset"""
    return f"""
    Netflix App Reviews Dataset
    ============================
    Total Reviews: {len(NETFLIX_DATA)}
    
    This dataset contains user reviews and ratings from the Netflix mobile app.
    Each review includes:
    - User ID and Name
    - Review Text
    - Rating (1-5 stars)
    - Flagged status
    - App Version
    - Timestamp
    """

@server.resource("netflix://stats/summary")
def get_stats_summary() -> str:
    """Statistical summary of the dataset"""
    if not NETFLIX_DATA:
        return "No data available"
    
    ratings = [int(row.get('Rating', 0)) for row in NETFLIX_DATA if row.get('Rating')]
    
    summary = f"""
    Dataset Statistics Summary
    ==========================
    Total Records: {len(NETFLIX_DATA)}
    Average Rating: {statistics.mean(ratings):.2f}
    Median Rating: {statistics.median(ratings):.2f}
    Std Deviation: {statistics.stdev(ratings):.2f}
    Min Rating: {min(ratings)}
    Max Rating: {max(ratings)}
    """
    return summary

# ============= ANALYSIS TOOLS =============

@server.tool()
def analyze_rating_distribution() -> str:
    """
    Analysis 1: Distribution of ratings across all reviews
    Shows count of each star rating (1-5)
    """
    ratings = [int(row.get('Rating', 0)) for row in NETFLIX_DATA if row.get('Rating')]
    distribution = Counter(ratings)
    
    result = "Rating Distribution:\n"
    for star in range(1, 6):
        count = distribution.get(star, 0)
        percentage = (count / len(ratings) * 100) if ratings else 0
        bar = "█" * int(percentage / 2)
        result += f"{star}⭐: {count:4d} ({percentage:5.1f}%) {bar}\n"
    
    return result

@server.tool()
def analyze_flagged_reviews() -> str:
    """
    Analysis 2: Identify flagged reviews and their characteristics
    Shows count and percentage of flagged reviews with rating breakdown
    """
    flagged = [row for row in NETFLIX_DATA if row.get('Flagged') == '1']
    
    flagged_ratings = Counter([int(row.get('Rating', 0)) for row in flagged if row.get('Rating')])
    
    result = f"""
Flagged Reviews Analysis:
========================
Total Flagged: {len(flagged)} out of {len(NETFLIX_DATA)} ({len(flagged)/len(NETFLIX_DATA)*100:.1f}%)

Rating Distribution of Flagged Reviews:
"""
    for rating, count in sorted(flagged_ratings.items()):
        result += f"  {rating}⭐: {count}\n"
    
    return result

@server.tool()
def analyze_sentiment_keywords() -> str:
    """
    Analysis 3: Extract common positive and negative keywords from reviews
    Identifies frequently used words indicating sentiment
    """
    positive_words = ['good', 'great', 'love', 'amazing', 'excellent', 'best', 'awesome', 'perfect', 'wonderful', 'nice']
    negative_words = ['bad', 'worst', 'hate', 'terrible', 'poor', 'waste', 'garbage', 'useless', 'pathetic', 'horrible']
    
    positive_count = Counter()
    negative_count = Counter()
    
    for row in NETFLIX_DATA:
        review = row.get('Review', '').lower()
        for word in positive_words:
            if word in review:
                positive_count[word] += 1
        for word in negative_words:
            if word in review:
                negative_count[word] += 1
    
    result = "Sentiment Keywords Analysis:\n"
    result += "\nTop Positive Keywords:\n"
    for word, count in positive_count.most_common(5):
        result += f"  '{word}': {count} mentions\n"
    
    result += "\nTop Negative Keywords:\n"
    for word, count in negative_count.most_common(5):
        result += f"  '{word}': {count} mentions\n"
    
    return result

@server.tool()
def analyze_review_length() -> str:
    """
    Analysis 4: Analyze review text length and its correlation with ratings
    Shows average length for each rating tier
    """
    review_lengths = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    for row in NETFLIX_DATA:
        review = row.get('Review', '')
        rating = int(row.get('Rating', 0))
        if rating in review_lengths:
            review_lengths[rating].append(len(review))
    
    result = "Review Length Analysis by Rating:\n"
    for rating in range(1, 6):
        lengths = review_lengths[rating]
        if lengths:
            avg_len = statistics.mean(lengths)
            max_len = max(lengths)
            result += f"{rating}⭐: Avg={avg_len:.0f} chars, Max={max_len}, Count={len(lengths)}\n"
    
    return result

@server.tool()
def analyze_app_versions() -> str:
    """
    Analysis 5: Identify most common app versions and their associated ratings
    Shows top versions and average rating for each
    """
    version_data = {}
    
    for row in NETFLIX_DATA:
        version = row.get('App_Version', 'Unknown')
        rating = row.get('Rating', '0')
        
        if version not in version_data:
            version_data[version] = []
        if rating:
            try:
                version_data[version].append(int(rating))
            except ValueError:
                pass
    
    result = "Top App Versions by Review Count:\n"
    sorted_versions = sorted(version_data.items(), key=lambda x: len(x[1]), reverse=True)
    
    for version, ratings in sorted_versions[:10]:
        if ratings:
            avg_rating = statistics.mean(ratings)
            result += f"{version}: {len(ratings)} reviews, Avg Rating: {avg_rating:.2f}⭐\n"
    
    return result

@server.tool()
def analyze_common_issues() -> str:
    """
    Analysis 6: Identify most common issues and problems mentioned
    Extracts problem keywords and their frequency
    """
    issues = ['crashing', 'freezing', 'error', 'bug', 'slow', 'loading', 'cast', 'chromecast', 
              'payment', 'login', 'sign in', 'buffering', 'ads', 'expensive', 'cancel', 'removed']
    
    issue_count = Counter()
    
    for row in NETFLIX_DATA:
        review = row.get('Review', '').lower()
        for issue in issues:
            if issue in review:
                issue_count[issue] += 1
    
    result = "Most Common Issues Mentioned:\n"
    for issue, count in issue_count.most_common(15):
        percentage = (count / len(NETFLIX_DATA)) * 100
        result += f"'{issue}': {count} ({percentage:.1f}%)\n"
    
    return result

@server.tool()
def analyze_temporal_trends() -> str:
    """
    Analysis 7: Analyze review trends over time by month
    Shows rating trends across different time periods
    """
    monthly_data = {}
    
    for row in NETFLIX_DATA:
        timestamp = row.get('Timestamp', '')
        rating = row.get('Rating', '0')
        
        if timestamp and rating:
            try:
                date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                month_key = date.strftime('%Y-%m')
                
                if month_key not in monthly_data:
                    monthly_data[month_key] = []
                monthly_data[month_key].append(int(rating))
            except (ValueError, AttributeError):
                pass
    
    result = "Monthly Rating Trends:\n"
    for month in sorted(monthly_data.keys())[-12:]:  # Last 12 months
        ratings = monthly_data[month]
        avg_rating = statistics.mean(ratings)
        result += f"{month}: Avg={avg_rating:.2f}⭐ ({len(ratings)} reviews)\n"
    
    return result

@server.tool()
def analyze_rating_vs_engagement() -> str:
    """
    Analysis 8: Compare ratings with flagged status and engagement
    Shows if flagged reviews have different rating patterns
    """
    flagged_ratings = []
    unflagged_ratings = []
    
    for row in NETFLIX_DATA:
        rating = row.get('Rating', '')
        if rating:
            try:
                rating = int(rating)
                if row.get('Flagged') == '1':
                    flagged_ratings.append(rating)
                else:
                    unflagged_ratings.append(rating)
            except ValueError:
                pass
    
    result = "Rating vs Flagged Status Analysis:\n\n"
    result += f"Flagged Reviews: {len(flagged_ratings)}\n"
    if flagged_ratings:
        result += f"  Average Rating: {statistics.mean(flagged_ratings):.2f}⭐\n"
        result += f"  Median Rating: {statistics.median(flagged_ratings):.1f}⭐\n"
    
    result += f"\nUnflagged Reviews: {len(unflagged_ratings)}\n"
    if unflagged_ratings:
        result += f"  Average Rating: {statistics.mean(unflagged_ratings):.2f}⭐\n"
        result += f"  Median Rating: {statistics.median(unflagged_ratings):.1f}⭐\n"
    
    return result

@server.tool()
def analyze_user_sentiment_by_rating() -> str:
    """
    Analysis 9: Classify reviews as positive/negative/neutral based on rating
    Shows sentiment distribution
    """
    positive = []  # 4-5 stars
    neutral = []   # 3 stars
    negative = []  # 1-2 stars
    
    for row in NETFLIX_DATA:
        rating = row.get('Rating', '')
        review = row.get('Review', '')
        
        if rating and review:
            try:
                r = int(rating)
                if r >= 4:
                    positive.append(review)
                elif r == 3:
                    neutral.append(review)
                else:
                    negative.append(review)
            except ValueError:
                pass
    
    result = "User Sentiment Distribution:\n"
    total = len(positive) + len(neutral) + len(negative)
    result += f"Positive (4-5⭐): {len(positive):4d} ({len(positive)/total*100:5.1f}%)\n"
    result += f"Neutral (3⭐):    {len(neutral):4d} ({len(neutral)/total*100:5.1f}%)\n"
    result += f"Negative (1-2⭐): {len(negative):4d} ({len(negative)/total*100:5.1f}%)\n"
    
    return result

@server.tool()
def analyze_feature_mentions() -> str:
    """
    Analysis 10: Track mentions of specific features in reviews
    Shows which features are most discussed
    """
    features = {
        'casting/chromecast': ['cast', 'chromecast'],
        'ads': ['ads', 'advertisement', 'commercial'],
        'games': ['games', 'gaming'],
        'password sharing': ['password', 'sharing', 'household'],
        'ui/ux': ['ui', 'ux', 'interface', 'design'],
        'content': ['movie', 'series', 'show', 'content'],
        'performance': ['crash', 'freeze', 'lag', 'slow', 'loading'],
        'pricing': ['price', 'expensive', 'cost', 'subscription'],
        'downloads': ['download', 'offline'],
        'subtitles': ['subtitle', 'language', 'translation']
    }
    
    feature_mentions = {feature: 0 for feature in features}
    
    for row in NETFLIX_DATA:
        review = row.get('Review', '').lower()
        for feature, keywords in features.items():
            for keyword in keywords:
                if keyword in review:
                    feature_mentions[feature] += 1
                    break
    
    result = "Feature Mentions in Reviews:\n"
    for feature, count in sorted(feature_mentions.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(NETFLIX_DATA)) * 100
        result += f"{feature:20s}: {count:4d} mentions ({percentage:5.1f}%)\n"
    
    return result

@server.tool()
def generate_comprehensive_report() -> str:
    """
    Analysis 11: Generate comprehensive summary report
    Combines key metrics and insights
    """
    if not NETFLIX_DATA:
        return "No data available for analysis"
    
    ratings = [int(row.get('Rating', 0)) for row in NETFLIX_DATA if row.get('Rating')]
    flagged = sum(1 for row in NETFLIX_DATA if row.get('Flagged') == '1')
    
    report = f"""
╔════════════════════════════════════════════════════════════╗
║        NETFLIX APP REVIEWS - COMPREHENSIVE REPORT         ║
╚════════════════════════════════════════════════════════════╝

📊 DATASET OVERVIEW
───────────────────
Total Reviews Analyzed: {len(NETFLIX_DATA)}
Date Range: Analysis of historical review data
Flagged Reviews: {flagged} ({flagged/len(NETFLIX_DATA)*100:.1f}%)

⭐ RATING METRICS
─────────────────
Average Rating: {statistics.mean(ratings):.2f}/5.0
Median Rating: {statistics.median(ratings):.1f}/5.0
Standard Deviation: {statistics.stdev(ratings):.2f}
Most Common Rating: {Counter(ratings).most_common(1)[0][0]}

📈 SENTIMENT DISTRIBUTION
──────────────────────────
"""
    
    # Quick sentiment analysis
    positive = sum(1 for r in ratings if r >= 4)
    neutral = sum(1 for r in ratings if r == 3)
    negative = sum(1 for r in ratings if r <= 2)
    
    report += f"""
Positive (4-5⭐): {positive:4d} reviews ({positive/len(ratings)*100:5.1f}%)
Neutral (3⭐):    {neutral:4d} reviews ({neutral/len(ratings)*100:5.1f}%)
Negative (1-2⭐): {negative:4d} reviews ({negative/len(ratings)*100:5.1f}%)

🔍 KEY INSIGHTS
────────────────
• Dataset contains diverse user feedback
• Use analyze_* functions for detailed insights
• Track trends across app versions and time periods
• Identify common issues for prioritization

For detailed analysis, use individual analysis tools.
"""
    
    return report

# Style configuration
STYLES = {
    "analysis": {
        "color": "#00ff00",
        "font-weight": "bold"
    },
    "metric": {
        "color": "#0099ff",
        "font-style": "italic"
    },
    "warning": {
        "color": "#ff6600",
        "background": "#ffe6cc"
    }
}

if __name__ == "__main__":
    import sys
    
    # Print available analyses
    print("Netflix Data Analysis MCP Bot - Available Analyses:")
    print("=" * 60)
    print("1. analyze_rating_distribution - Rating breakdown")
    print("2. analyze_flagged_reviews - Flagged content analysis")
    print("3. analyze_sentiment_keywords - Sentiment word frequency")
    print("4. analyze_review_length - Review length correlation")
    print("5. analyze_app_versions - App version performance")
    print("6. analyze_common_issues - Problem identification")
    print("7. analyze_temporal_trends - Time-based trends")
    print("8. analyze_rating_vs_engagement - Engagement metrics")
    print("9. analyze_user_sentiment_by_rating - Sentiment classification")
    print("10. analyze_feature_mentions - Feature discussion tracking")
    print("11. generate_comprehensive_report - Full summary report")
    print("=" * 60)
    print(f"\nData loaded: {len(NETFLIX_DATA)} reviews")
    
    # Run server
    mcp.server.stdio.stdio_server(server)