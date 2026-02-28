# -*- coding: utf-8 -*-
import json
import csv
import re
import asyncio
from pathlib import Path
from datetime import datetime
from collections import Counter
import statistics
import pandas as pd
import fastmcp
from mcp.types import TextContent
import sys
import io

# Enable UTF-8 output on Windows
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8') 

# Initialize FastMCP server with Netflix Data Analyzer
server = fastmcp.FastMCP("Netflix Data Analyzer")

# Configuration
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "netflix_data.csv"
CACHE_FILE = BASE_DIR / "netflix_cache.json"

def load_netflix_data() -> list[dict]:
    """Load Netflix CSV data with caching"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    data = []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        
        # Cache the data
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []
    
    return data

# Load data at startup
NETFLIX_DATA = load_netflix_data()

# ============= STYLING (DEFINE BEFORE TOOLS) =============
def format_response(content: str) -> TextContent:
    """Format MCP response with styling"""
    styled = f"""
    ╔════════════════════════════════════════════════════════════════╗
    ║           🎬 NETFLIX DATA ANALYZER - MCP SERVER 🎬             ║
    ╚════════════════════════════════════════════════════════════════╝
    
    {content}
    
    ╔════════════════════════════════════════════════════════════════╗
    ║                    Analysis Complete ✓                         ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    return TextContent(type="text", text=styled)

# ============= RESOURCES =============
@server.resource("netflix://data/overview")
def get_data_overview() -> str:
    """Overview of Netflix dataset"""
    if not NETFLIX_DATA:
        return "No data available"
    
    return f"""
    🎬 Netflix App Reviews Dataset Overview
    =======================================
    Total Reviews: {len(NETFLIX_DATA):,}
    Data Load Time: {datetime.now().isoformat()}
    Columns: reviewId, userName, content, score, thumbsUpCount, reviewCreatedVersion, at, appVersion
    Status: ✓ Ready for Analysis
    """

@server.resource("netflix://data/structure")
def get_data_structure() -> str:
    """Data structure and schema"""
    if not NETFLIX_DATA:
        return "No data available"
    
    sample = NETFLIX_DATA[0] if NETFLIX_DATA else {}
    schema_info = "\n".join([f"  - {key}: {type(sample.get(key, '')).__name__}" for key in sample.keys()])
    return f"""
    📋 Netflix Data Schema
    ======================
    {schema_info}
    
    Sample Record:
    {json.dumps(NETFLIX_DATA[0], ensure_ascii=False, indent=2)[:500]}...
    """

@server.resource("netflix://analysis/summary")
def get_analysis_summary() -> str:
    """Summary of all available analyses"""
    return """
    📊 Available Analysis Tools
    ============================
    1. review_score_distribution - Analyze review ratings distribution
    2. sentiment_analysis - Analyze sentiment of reviews
    3. top_reviewers - Identify most active reviewers
    4. version_analysis - Analyze app version adoption
    5. thumbs_up_analysis - Analyze engagement (thumbs up counts)
    6. content_length_analysis - Analyze review length patterns
    7. common_topics - Extract common topics from reviews
    8. rating_by_version - Compare ratings across app versions
    9. review_trends - Analyze review trends over time
    10. user_engagement_score - Calculate user engagement metrics
    11. review_completeness - Analyze data completeness
    12. keyword_sentiment_analysis - Analyze sentiment for specific keywords
    """

# ============= TOOLS =============

@server.tool()
def review_score_distribution() -> TextContent:
    """Analyze the distribution of review scores (ratings)"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    scores = []
    for item in NETFLIX_DATA:
        try:
            score = int(item.get('score', 0))
            scores.append(score)
        except (ValueError, TypeError):
            continue
    
    if not scores:
        return format_response("No valid scores found")
    
    score_counts = Counter(scores)
    distribution = "\n".join([
        f"  ⭐ {score} stars: {score_counts[score]:,} reviews ({score_counts[score]/len(scores)*100:.1f}%)"
        for score in sorted(score_counts.keys())
    ])
    
    avg_score = statistics.mean(scores)
    median_score = statistics.median(scores)
    
    result = f"""
    📊 Review Score Distribution
    =============================
    {distribution}
    
    Statistics:
    - Average Score: {avg_score:.2f}
    - Median Score: {median_score}
    - Total Reviews Analyzed: {len(scores):,}
    - Score Range: {min(scores)} to {max(scores)}
    """
    return format_response(result)

@server.tool()
def sentiment_analysis() -> TextContent:
    """Analyze sentiment from review content"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    positive_words = ['love', 'great', 'excellent', 'amazing', 'perfect', 'good', 'best', 'awesome', 'wonderful', 'fantastic']
    negative_words = ['hate', 'bad', 'terrible', 'awful', 'worst', 'poor', 'horrible', 'useless', 'broken', 'garbage']
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for item in NETFLIX_DATA:
        review_content = item.get('content', '').lower()
        if not review_content:
            neutral_count += 1
            continue
        
        pos_found = any(word in review_content for word in positive_words)
        neg_found = any(word in review_content for word in negative_words)
        
        if pos_found and not neg_found:
            positive_count += 1
        elif neg_found and not pos_found:
            negative_count += 1
        else:
            neutral_count += 1
    
    total = len(NETFLIX_DATA)
    
    result = f"""
    💬 Sentiment Analysis
    =====================
    Positive Reviews: {positive_count:,} ({positive_count/total*100:.1f}%)
    Negative Reviews: {negative_count:,} ({negative_count/total*100:.1f}%)
    Neutral Reviews: {neutral_count:,} ({neutral_count/total*100:.1f}%)
    
    Analysis based on keyword detection in review content.
    """
    return format_response(result)

@server.tool()
def top_reviewers(limit: int = 10) -> TextContent:
    """Identify the most active reviewers"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    user_counts = Counter()
    for item in NETFLIX_DATA:
        username = item.get('userName', 'Unknown')
        user_counts[username] += 1
    
    top_users = user_counts.most_common(limit)
    top_list = "\n".join([
        f"  {i+1}. {user}: {count:,} reviews" 
        for i, (user, count) in enumerate(top_users)
    ])
    
    result = f"""
    👥 Top {limit} Most Active Reviewers
    ====================================
    {top_list}
    
    Total Unique Reviewers: {len(user_counts):,}
    """
    return format_response(result)

@server.tool()
def version_analysis() -> TextContent:
    """Analyze app version adoption and distribution"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    versions = Counter()
    for item in NETFLIX_DATA:
        version = item.get('appVersion', 'Unknown')
        if version:
            versions[version] += 1
    
    # Get top 10 versions
    top_versions = versions.most_common(10)
    version_list = "\n".join([
        f"  📱 v{version}: {count:,} reviews ({count/len(NETFLIX_DATA)*100:.1f}%)"
        for version, count in top_versions
    ])
    
    result = f"""
    📱 App Version Distribution
    ============================
    {version_list}
    
    Total Unique Versions: {len(versions)}
    Most Common: {top_versions[0][0] if top_versions else 'N/A'} ({top_versions[0][1]:,} reviews)
    """
    return format_response(result)

@server.tool()
def thumbs_up_analysis() -> TextContent:
    """Analyze engagement through thumbs up counts"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    thumbs_up_counts = []
    for item in NETFLIX_DATA:
        try:
            count = int(item.get('thumbsUpCount', 0))
            thumbs_up_counts.append(count)
        except (ValueError, TypeError):
            continue
    
    if not thumbs_up_counts:
        return format_response("No thumbs up data available")
    
    total_thumbs = sum(thumbs_up_counts)
    avg_thumbs = statistics.mean(thumbs_up_counts)
    max_thumbs = max(thumbs_up_counts)
    reviews_with_thumbs = sum(1 for c in thumbs_up_counts if c > 0)
    
    result = f"""
    👍 Engagement Analysis (Thumbs Up)
    ==================================
    Total Thumbs Up: {total_thumbs:,}
    Average per Review: {avg_thumbs:.2f}
    Maximum Thumbs Up: {max_thumbs}
    Reviews with Thumbs Up: {reviews_with_thumbs:,} ({reviews_with_thumbs/len(thumbs_up_counts)*100:.1f}%)
    
    Total Reviews Analyzed: {len(thumbs_up_counts):,}
    """
    return format_response(result)

@server.tool()
def content_length_analysis() -> TextContent:
    """Analyze review content length patterns"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    lengths = []
    word_counts = []
    empty_reviews = 0
    
    for item in NETFLIX_DATA:
        review_content = item.get('content', '')
        if not review_content:
            empty_reviews += 1
            continue
        lengths.append(len(review_content))
        word_counts.append(len(review_content.split()))
    
    if not lengths:
        return format_response(f"All {empty_reviews:,} reviews are empty")
    
    avg_length = statistics.mean(lengths)
    median_length = statistics.median(lengths)
    avg_words = statistics.mean(word_counts)
    
    result = f"""
    📝 Review Content Analysis
    ==========================
    Average Content Length: {avg_length:.0f} characters
    Median Content Length: {median_length} characters
    Average Word Count: {avg_words:.0f} words
    Longest Review: {max(lengths)} characters
    Shortest Review: {min(lengths)} characters
    
    Empty Reviews: {empty_reviews:,}
    Total Analyzed: {len(lengths):,}
    """
    return format_response(result)

@server.tool()
def common_topics() -> TextContent:
    """Extract common topics and keywords from reviews"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    # Common words to exclude
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'it', 'to', 'of', 'in', 'for', 'on', 'with', 'i', 'you', 'he', 'she', 'this', 'that', 'be', 'have', 'has', 'are', 'was', 'were', 'very', 'so', 'as', 'from', 'by', 'at', 'my', 'me', 'if', 'can', 'get', 'got', 'really', 'just', 'more', 'one', 'two', 'like', 'love', 'good', 'bad'}
    
    all_words = Counter()
    
    for item in NETFLIX_DATA:
        review_content = item.get('content', '').lower()
        if review_content:
            # Extract words
            words = re.findall(r'\b[a-z]+\b', review_content)
            for word in words:
                if word not in stopwords and len(word) > 3:
                    all_words[word] += 1
    
    top_keywords = all_words.most_common(15)
    keywords_list = "\n".join([
        f"  {i+1}. '{keyword}': {count:,} occurrences"
        for i, (keyword, count) in enumerate(top_keywords)
    ])
    
    result = f"""
    🔑 Common Topics & Keywords
    =============================
    {keywords_list}
    
    Unique Keywords: {len(all_words):,}
    """
    return format_response(result)

@server.tool()
def rating_by_version() -> TextContent:
    """Compare average ratings across different app versions"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    version_ratings = {}
    
    for item in NETFLIX_DATA:
        version = item.get('appVersion', 'Unknown')
        try:
            score = int(item.get('score', 0))
            if version not in version_ratings:
                version_ratings[version] = []
            version_ratings[version].append(score)
        except (ValueError, TypeError):
            continue
    
    # Calculate averages for top versions
    version_avg = {}
    for version, ratings in version_ratings.items():
        if ratings:
            version_avg[version] = statistics.mean(ratings)
    
    # Sort by average rating
    sorted_versions = sorted(version_avg.items(), key=lambda x: x[1], reverse=True)[:10]
    version_list = "\n".join([
        f"  📱 v{version}: ⭐ {avg:.2f} avg ({len(version_ratings[version]):,} reviews)"
        for version, avg in sorted_versions
    ])
    
    result = f"""
    ⭐ Rating Analysis by App Version
    ==================================
    {version_list}
    
    Total Versions: {len(version_ratings)}
    """
    return format_response(result)

@server.tool()
def review_trends() -> TextContent:
    """Analyze review trends over time"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    date_reviews = Counter()
    dates = []
    
    for item in NETFLIX_DATA:
        date_str = item.get('at', '')
        if date_str:
            try:
                # Extract just the date part (YYYY-MM-DD)
                date_only = date_str.split()[0]
                date_reviews[date_only] += 1
                dates.append(date_only)
            except:
                continue
    
    if not date_reviews:
        return format_response("No date information available")
    
    # Get recent dates
    recent_dates = sorted(date_reviews.items())[-10:]
    trends_list = "\n".join([
        f"  {date}: {count:,} reviews"
        for date, count in recent_dates
    ])
    
    avg_per_day = statistics.mean(date_reviews.values())
    
    result = f"""
    📅 Review Trends Over Time
    ============================
    Last 10 Days:
    {trends_list}
    
    Average Reviews per Day: {avg_per_day:.0f}
    Total Days with Reviews: {len(date_reviews)}
    """
    return format_response(result)

@server.tool()
def user_engagement_score() -> TextContent:
    """Calculate comprehensive user engagement metrics"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    engagement_data = {}
    
    for item in NETFLIX_DATA:
        user = item.get('userName', 'Unknown')
        if user not in engagement_data:
            engagement_data[user] = {
                'review_count': 0,
                'total_thumbs': 0,
                'avg_rating': []
            }
        
        engagement_data[user]['review_count'] += 1
        try:
            engagement_data[user]['total_thumbs'] += int(item.get('thumbsUpCount', 0))
            engagement_data[user]['avg_rating'].append(int(item.get('score', 0)))
        except:
            pass
    
    # Calculate engagement scores
    engagement_scores = []
    for user, data in engagement_data.items():
        reviews = data['review_count']
        thumbs = data['total_thumbs']
        avg_rating = statistics.mean(data['avg_rating']) if data['avg_rating'] else 0
        engagement_score = (reviews * 0.4) + (thumbs * 0.3) + (avg_rating * 0.3)
        engagement_scores.append((user, engagement_score, reviews, thumbs))
    
    # Sort by engagement score
    top_engaged = sorted(engagement_scores, key=lambda x: x[1], reverse=True)[:10]
    engaged_list = "\n".join([
        f"  {i+1}. {user}: Score {score:.2f} ({reviews} reviews, {thumbs} thumbs up)"
        for i, (user, score, reviews, thumbs) in enumerate(top_engaged)
    ])
    
    result = f"""
    🎯 User Engagement Score
    ==========================
    Top 10 Engaged Users:
    {engaged_list}
    
    Total Active Users: {len(engagement_data):,}
    Engagement Score = (Reviews × 0.4) + (Thumbs Up × 0.3) + (Avg Rating × 0.3)
    """
    return format_response(result)

@server.tool()
def review_completeness() -> TextContent:
    """Analyze data completeness and missing values"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    columns = ['reviewId', 'userName', 'content', 'score', 'thumbsUpCount', 'reviewCreatedVersion', 'at', 'appVersion']
    completeness = {col: 0 for col in columns}
    
    for item in NETFLIX_DATA:
        for col in columns:
            if item.get(col) and str(item.get(col)).strip():
                completeness[col] += 1
    
    total = len(NETFLIX_DATA)
    completeness_list = "\n".join([
        f"  {col}: {completeness[col]:,}/{total:,} ({completeness[col]/total*100:.1f}%)"
        for col in columns
    ])
    
    result = f"""
    ✓ Data Completeness Analysis
    =============================
    {completeness_list}
    
    Total Records: {total:,}
    """
    return format_response(result)

@server.tool()
def keyword_sentiment_analysis(keyword: str) -> TextContent:
    """Analyze sentiment for specific keywords"""
    if not NETFLIX_DATA:
        return format_response("No data available")
    
    keyword_lower = keyword.lower()
    positive_words = ['love', 'great', 'excellent', 'amazing', 'perfect', 'good', 'best', 'awesome', 'wonderful', 'fantastic']
    negative_words = ['hate', 'bad', 'terrible', 'awful', 'worst', 'poor', 'horrible', 'useless', 'broken', 'garbage']
    
    matching_reviews = []
    positive = 0
    negative = 0
    neutral = 0
    
    for item in NETFLIX_DATA:
        review_content = item.get('content', '').lower()
        if keyword_lower in review_content:
            matching_reviews.append(item)
            
            pos_found = any(word in review_content for word in positive_words)
            neg_found = any(word in review_content for word in negative_words)
            
            if pos_found and not neg_found:
                positive += 1
            elif neg_found and not pos_found:
                negative += 1
            else:
                neutral += 1
    
    if not matching_reviews:
        return format_response(f"No reviews found containing keyword: '{keyword}'")
    
    total_matching = len(matching_reviews)
    
    sample_reviews = json.dumps([
        {"userName": r.get("userName"), "content": r.get("content", "")[:100]} 
        for r in matching_reviews[:3]
    ], ensure_ascii=False, indent=2)
    
    result = f"""
    🔍 Sentiment Analysis for Keyword: '{keyword}'
    ================================================
    Total Mentions: {total_matching:,}
    
    Sentiment Breakdown:
    - Positive: {positive:,} ({positive/total_matching*100:.1f}%)
    - Negative: {negative:,} ({negative/total_matching*100:.1f}%)
    - Neutral: {neutral:,} ({neutral/total_matching*100:.1f}%)
    
    Sample Reviews with '{keyword}':
    {sample_reviews}
    """
    return format_response(result)

if __name__ == "__main__":
    # Only log to stderr to avoid interfering with MCP JSON-RPC protocol on stdout
    sys.stderr.write("[SERVER] Starting Netflix Data Analyzer MCP Server...\n")
    sys.stderr.write(f"[DATA] Loaded {len(NETFLIX_DATA):,} reviews from Netflix dataset\n")
    sys.stderr.write("[OK] Server ready. Use MCP client to connect.\n")
    sys.stderr.flush()
    
    # Run the server
    asyncio.run(server.run())
