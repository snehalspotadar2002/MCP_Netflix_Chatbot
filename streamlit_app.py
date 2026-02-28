import streamlit as st
import json
import requests
from typing import Any, Optional
import pandas as pd
from datetime import datetime
import os
import sys

# Configure Streamlit page
st.set_page_config(
    page_title="Netflix Data Analyzer Chatbot",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Netflix Data Analyzer Chatbot - Powered by MCP"
    }
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
        border-left: 4px solid #1f77b4;
    }
    .assistant-message {
        background-color: #f0f0f0;
        margin-right: 2rem;
        border-left: 4px solid #2ca02c;
    }
    .analysis-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff6b6b;
        margin: 0.5rem 0;
    }
    .tool-button {
        margin: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============= HELPER FUNCTIONS =============

def load_netflix_csv():
    """Load Netflix CSV data"""
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(BASE_DIR, "netflix_data.csv")
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Error loading Netflix data: {e}")
        return None

def get_score_distribution():
    """Get score distribution analysis"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    score_counts = df['score'].value_counts().sort_index()
    
    analysis = "📊 Review Score Distribution\n"
    analysis += "=" * 50 + "\n"
    for score, count in score_counts.items():
        percentage = (count / len(df)) * 100
        analysis += f"⭐ {score} stars: {count:,} reviews ({percentage:.1f}%)\n"
    
    analysis += f"\nAverage Score: {df['score'].mean():.2f}\n"
    analysis += f"Median Score: {df['score'].median():.0f}\n"
    
    return analysis

def get_sentiment_analysis():
    """Get sentiment analysis"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    positive_words = ['love', 'great', 'excellent', 'amazing', 'perfect', 'good', 'best', 'awesome', 'wonderful', 'fantastic']
    negative_words = ['hate', 'bad', 'terrible', 'awful', 'worst', 'poor', 'horrible', 'useless', 'broken', 'garbage']
    
    df['content_lower'] = df['content'].fillna('').str.lower()
    
    df['sentiment'] = df['content_lower'].apply(lambda x: 
        'positive' if any(w in x for w in positive_words) and not any(w in x for w in negative_words)
        else 'negative' if any(w in x for w in negative_words) and not any(w in x for w in positive_words)
        else 'neutral'
    )
    
    sentiment_counts = df['sentiment'].value_counts()
    
    analysis = "💬 Sentiment Analysis\n"
    analysis += "=" * 50 + "\n"
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        analysis += f"{sentiment.upper()}: {count:,} ({percentage:.1f}%)\n"
    
    return analysis

def get_top_reviewers():
    """Get top reviewers"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    top_users = df['userName'].value_counts().head(10)
    
    analysis = "👥 Top 10 Most Active Reviewers\n"
    analysis += "=" * 50 + "\n"
    for i, (user, count) in enumerate(top_users.items(), 1):
        analysis += f"{i}. {user}: {count:,} reviews\n"
    
    return analysis

def get_version_analysis():
    """Get version analysis"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    top_versions = df['appVersion'].value_counts().head(10)
    
    analysis = "📱 Top App Versions\n"
    analysis += "=" * 50 + "\n"
    for version, count in top_versions.items():
        percentage = (count / len(df)) * 100
        analysis += f"v{version}: {count:,} reviews ({percentage:.1f}%)\n"
    
    return analysis

def get_thumbs_up_analysis():
    """Get thumbs up analysis"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    df['thumbsUpCount'] = pd.to_numeric(df['thumbsUpCount'], errors='coerce')
    
    total_thumbs = df['thumbsUpCount'].sum()
    avg_thumbs = df['thumbsUpCount'].mean()
    max_thumbs = df['thumbsUpCount'].max()
    reviews_with_thumbs = (df['thumbsUpCount'] > 0).sum()
    
    analysis = "👍 Engagement Analysis\n"
    analysis += "=" * 50 + "\n"
    analysis += f"Total Thumbs Up: {total_thumbs:,.0f}\n"
    analysis += f"Average per Review: {avg_thumbs:.2f}\n"
    analysis += f"Maximum Thumbs Up: {max_thumbs:.0f}\n"
    analysis += f"Reviews with Thumbs Up: {reviews_with_thumbs:,} ({reviews_with_thumbs/len(df)*100:.1f}%)\n"
    
    return analysis

def get_content_length_analysis():
    """Get content length analysis"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    df['content_length'] = df['content'].fillna('').str.len()
    df['word_count'] = df['content'].fillna('').str.split().str.len()
    
    analysis = "📝 Review Content Analysis\n"
    analysis += "=" * 50 + "\n"
    analysis += f"Average Content Length: {df['content_length'].mean():.0f} characters\n"
    analysis += f"Median Content Length: {df['content_length'].median():.0f} characters\n"
    analysis += f"Average Word Count: {df['word_count'].mean():.0f} words\n"
    analysis += f"Longest Review: {df['content_length'].max()} characters\n"
    analysis += f"Empty Reviews: {(df['content_length'] == 0).sum():,}\n"
    
    return analysis

def get_common_topics():
    """Get common topics"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'it', 'to', 'of', 'in', 'for', 'on', 'with'}
    
    all_words = []
    for content in df['content'].fillna(''):
        words = content.lower().split()
        all_words.extend([w for w in words if len(w) > 3 and w not in stopwords])
    
    from collections import Counter
    word_freq = Counter(all_words).most_common(15)
    
    analysis = "🔑 Common Keywords\n"
    analysis += "=" * 50 + "\n"
    for i, (word, count) in enumerate(word_freq, 1):
        analysis += f"{i}. '{word}': {count:,} occurrences\n"
    
    return analysis

def get_rating_by_version():
    """Get rating by version"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    
    version_ratings = df.groupby('appVersion')['score'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(10)
    
    analysis = "⭐ Rating by App Version\n"
    analysis += "=" * 50 + "\n"
    for version, row in version_ratings.iterrows():
        analysis += f"v{version}: {row['mean']:.2f} avg ({row['count']:.0f} reviews)\n"
    
    return analysis

def get_review_trends():
    """Get review trends"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    df['date'] = pd.to_datetime(df['at'], errors='coerce').dt.date
    daily_reviews = df.groupby('date').size().sort_index().tail(10)
    
    analysis = "📅 Review Trends (Last 10 Days)\n"
    analysis += "=" * 50 + "\n"
    for date, count in daily_reviews.items():
        analysis += f"{date}: {count:,} reviews\n"
    
    return analysis

def get_user_engagement_score():
    """Get user engagement score"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['thumbsUpCount'] = pd.to_numeric(df['thumbsUpCount'], errors='coerce')
    
    user_stats = df.groupby('userName').agg({
        'reviewId': 'count',
        'thumbsUpCount': 'sum',
        'score': 'mean'
    }).rename(columns={'reviewId': 'reviews'})
    
    user_stats['engagement'] = (user_stats['reviews'] * 0.4) + (user_stats['thumbsUpCount'] * 0.3) + (user_stats['score'] * 0.3)
    top_users = user_stats.nlargest(10, 'engagement')
    
    analysis = "🎯 Top Engaged Users\n"
    analysis += "=" * 50 + "\n"
    for i, (user, row) in enumerate(top_users.iterrows(), 1):
        analysis += f"{i}. {user}: Score {row['engagement']:.2f} ({row['reviews']:.0f} reviews)\n"
    
    return analysis

def get_review_completeness():
    """Get review completeness"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    analysis = "✓ Data Completeness\n"
    analysis += "=" * 50 + "\n"
    
    for col in df.columns:
        non_null = df[col].notna().sum()
        percentage = (non_null / len(df)) * 100
        analysis += f"{col}: {non_null:,}/{len(df):,} ({percentage:.1f}%)\n"
    
    return analysis

def get_keyword_sentiment(keyword):
    """Get keyword sentiment analysis"""
    df = load_netflix_csv()
    if df is None:
        return "Unable to load data"
    
    if not keyword:
        keyword = "netflix"
    
    mask = df['content'].fillna('').str.lower().str.contains(keyword.lower())
    matching = df[mask]
    
    if len(matching) == 0:
        return f"No reviews found containing '{keyword}'"
    
    analysis = f"🔍 Sentiment for '{keyword}'\n"
    analysis += "=" * 50 + "\n"
    analysis += f"Total Mentions: {len(matching):,}\n"
    
    positive_words = ['love', 'great', 'excellent', 'amazing', 'perfect', 'good', 'best']
    negative_words = ['hate', 'bad', 'terrible', 'awful', 'worst', 'poor', 'horrible']
    
    positive = matching['content'].fillna('').str.lower().apply(lambda x: any(w in x for w in positive_words)).sum()
    negative = matching['content'].fillna('').str.lower().apply(lambda x: any(w in x for w in negative_words)).sum()
    
    analysis += f"Positive: {positive} ({positive/len(matching)*100:.1f}%)\n"
    analysis += f"Negative: {negative} ({negative/len(matching)*100:.1f}%)\n"
    
    return analysis

def extract_keyword(text):
    """Extract keyword from text"""
    words = text.split()
    for word in words:
        if len(word) > 3 and word not in ['what', 'about', 'show', 'tell', 'give']:
            return word
    return "netflix"

def provide_general_response(user_input):
    """Provide general response"""
    response = f"📢 Available Analysis Tools:\n"
    response += "=" * 50 + "\n"
    response += "1. Score Distribution - Review ratings\n"
    response += "2. Sentiment Analysis - Positive/Negative reviews\n"
    response += "3. Top Reviewers - Most active users\n"
    response += "4. Version Analysis - App version stats\n"
    response += "5. Thumbs Up Analysis - Engagement metrics\n"
    response += "6. Content Length - Review length analysis\n"
    response += "7. Common Topics - Popular keywords\n"
    response += "8. Rating by Version - Version ratings\n"
    response += "9. Review Trends - Temporal patterns\n"
    response += "10. User Engagement - Engagement scores\n"
    response += "11. Data Completeness - Missing values\n"
    response += "12. Keyword Sentiment - Sentiment for keywords\n"
    
    response += f"\n💬 Your Question: {user_input}\n"
    response += "Please select one of the analyses above or use keywords like 'sentiment', 'score', 'reviewer', etc."
    
    return response

# ============= SESSION STATE INITIALIZATION =============

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "mcp_connected" not in st.session_state:
    st.session_state.mcp_connected = False

if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = {}

# ============= HEADER =============
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.image("https://a.slack-edge.com/prod-client-apps/netflix-0b9df9/ffc82ba2e3e9_512.png", width=100)

with col2:
    st.title("🎬 Netflix Data Analyzer Chatbot")
    st.markdown("#### Interactive AI Assistant for Netflix Reviews Analysis")

with col3:
    status = st.empty()

# ============= SIDEBAR =============
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("MCP Server Settings")
    mcp_host = st.text_input("MCP Host", value="http://localhost:8000", key="mcp_host")
    mcp_timeout = st.slider("Timeout (seconds)", 5, 60, 30, key="timeout")
    
    st.divider()
    
    st.subheader("📊 Available Analysis Tools")
    tools_list = [
        "review_score_distribution",
        "sentiment_analysis",
        "top_reviewers",
        "version_analysis",
        "thumbs_up_analysis",
        "content_length_analysis",
        "common_topics",
        "rating_by_version",
        "review_trends",
        "user_engagement_score",
        "review_completeness",
        "keyword_sentiment_analysis"
    ]
    
    for tool in tools_list:
        st.caption(f"✓ {tool}")
    
    st.divider()
    
    st.subheader("📚 Available Resources")
    resources = [
        "netflix://data/overview",
        "netflix://data/structure",
        "netflix://analysis/summary"
    ]
    
    for resource in resources:
        st.caption(f"📄 {resource}")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.analysis_cache = {}
        st.rerun()
    
    if st.button("🔄 Refresh MCP Connection", use_container_width=True):
        st.session_state.mcp_connected = False
        st.rerun()

# ============= MAIN CONTENT =============

st.subheader("🚀 Quick Analysis")
quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)

with quick_col1:
    if st.button("📊 Score Distribution", use_container_width=True):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Run review_score_distribution analysis"
        })

with quick_col2:
    if st.button("💬 Sentiment Analysis", use_container_width=True):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Run sentiment_analysis"
        })

with quick_col3:
    if st.button("👥 Top Reviewers", use_container_width=True):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Run top_reviewers analysis"
        })

with quick_col4:
    if st.button("📱 Version Analysis", use_container_width=True):
        st.session_state.chat_history.append({
            "role": "user",
            "content": "Run version_analysis"
        })

st.divider()

st.subheader("💬 Chat Conversation")

chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant:</strong>
                <pre>{message['content']}</pre>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.subheader("📝 Ask a Question")

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Enter your analysis request or question about Netflix data:",
        placeholder="e.g., 'Show me the sentiment analysis' or 'What are the top reviewers?'",
        key="user_input"
    )

with col2:
    submit_button = st.button("Send", use_container_width=True, type="primary")

if submit_button and user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    with st.spinner("🔄 Processing your request..."):
        try:
            input_lower = user_input.lower()
            
            tool_mapping = {
                "score": "review_score_distribution",
                "sentiment": "sentiment_analysis",
                "reviewer": "top_reviewers",
                "version": "version_analysis",
                "thumbs": "thumbs_up_analysis",
                "length": "content_length_analysis",
                "topic": "common_topics",
                "rating": "rating_by_version",
                "trend": "review_trends",
                "engagement": "user_engagement_score",
                "complete": "review_completeness",
                "keyword": "keyword_sentiment_analysis"
            }
            
            response_text = ""
            
            matched_tool = None
            for keyword, tool in tool_mapping.items():
                if keyword in input_lower:
                    matched_tool = tool
                    break
            
            if matched_tool:
                if matched_tool == "review_score_distribution":
                    response_text = get_score_distribution()
                elif matched_tool == "sentiment_analysis":
                    response_text = get_sentiment_analysis()
                elif matched_tool == "top_reviewers":
                    response_text = get_top_reviewers()
                elif matched_tool == "version_analysis":
                    response_text = get_version_analysis()
                elif matched_tool == "thumbs_up_analysis":
                    response_text = get_thumbs_up_analysis()
                elif matched_tool == "content_length_analysis":
                    response_text = get_content_length_analysis()
                elif matched_tool == "common_topics":
                    response_text = get_common_topics()
                elif matched_tool == "rating_by_version":
                    response_text = get_rating_by_version()
                elif matched_tool == "review_trends":
                    response_text = get_review_trends()
                elif matched_tool == "user_engagement_score":
                    response_text = get_user_engagement_score()
                elif matched_tool == "review_completeness":
                    response_text = get_review_completeness()
                elif matched_tool == "keyword_sentiment_analysis":
                    keyword_extract = extract_keyword(input_lower)
                    response_text = get_keyword_sentiment(keyword_extract)
            else:
                response_text = provide_general_response(user_input)
            
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            st.rerun()
        
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            st.error(error_msg)

st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8rem;'>
    🎬 Netflix Data Analyzer v1.0 | Powered by FastMCP & Streamlit | Built with ❤️
    </div>
""", unsafe_allow_html=True)

