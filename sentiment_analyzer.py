# sentiment_analyzer.py
# Sentiment analysis module for YouTube comments

from googleapiclient.errors import HttpError
import pandas as pd
import re
from collections import Counter
import streamlit as st

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    st.warning("⚠️ Install vaderSentiment for sentiment analysis: pip install vaderSentiment")


class SentimentAnalyzer:
    """Analyze sentiment from YouTube comments"""
    
    def __init__(self, youtube_client):
        self.youtube = youtube_client
        if VADER_AVAILABLE:
            self.analyzer = SentimentIntensityAnalyzer()
        else:
            self.analyzer = None
    
    def fetch_video_comments(self, video_id, max_comments=100):
        """Fetch comments from a specific video"""
        comments = []
        
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_comments),
                order="relevance",
                textFormat="plainText"
            )
            
            while request and len(comments) < max_comments:
                response = request.execute()
                
                for item in response.get('items', []):
                    comment_data = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'author': comment_data['authorDisplayName'],
                        'text': comment_data['textDisplay'],
                        'like_count': comment_data['likeCount'],
                        'published_at': comment_data['publishedAt'],
                        'reply_count': item['snippet']['totalReplyCount']
                    })
                
                # Get next page
                if 'nextPageToken' in response and len(comments) < max_comments:
                    request = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=min(100, max_comments - len(comments)),
                        pageToken=response['nextPageToken'],
                        order="relevance",
                        textFormat="plainText"
                    )
                else:
                    request = None
            
            return comments
        
        except HttpError as e:
            st.error(f"Could not fetch comments: {e}")
            return []
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of a single text"""
        if not self.analyzer:
            return {'compound': 0, 'category': 'Neutral'}
        
        scores = self.analyzer.polarity_scores(text)
        
        # Categorize based on compound score
        if scores['compound'] >= 0.05:
            category = 'Positive'
        elif scores['compound'] <= -0.05:
            category = 'Negative'
        else:
            category = 'Neutral'
        
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'category': category
        }
    
    def analyze_comments(self, comments):
        """Analyze sentiment for all comments"""
        if not self.analyzer:
            return pd.DataFrame()
        
        results = []
        
        for comment in comments:
            sentiment = self.analyze_sentiment(comment['text'])
            results.append({
                'author': comment['author'],
                'text': comment['text'][:100] + '...' if len(comment['text']) > 100 else comment['text'],
                'full_text': comment['text'],
                'likes': comment['like_count'],
                'replies': comment['reply_count'],
                'sentiment_score': sentiment['compound'],
                'sentiment_category': sentiment['category'],
                'positive_score': sentiment['positive'],
                'negative_score': sentiment['negative'],
                'neutral_score': sentiment['neutral']
            })
        
        return pd.DataFrame(results)
    
    def get_sentiment_summary(self, sentiment_df):
        """Generate sentiment summary statistics"""
        if sentiment_df.empty:
            return {}
        
        total = len(sentiment_df)
        positive = len(sentiment_df[sentiment_df['sentiment_category'] == 'Positive'])
        negative = len(sentiment_df[sentiment_df['sentiment_category'] == 'Negative'])
        neutral = len(sentiment_df[sentiment_df['sentiment_category'] == 'Neutral'])
        
        return {
            'total_comments': total,
            'positive_count': positive,
            'negative_count': negative,
            'neutral_count': neutral,
            'positive_percentage': (positive / total) * 100,
            'negative_percentage': (negative / total) * 100,
            'neutral_percentage': (neutral / total) * 100,
            'average_sentiment': sentiment_df['sentiment_score'].mean(),
            'most_positive': sentiment_df.nlargest(1, 'sentiment_score')['full_text'].values[0] if not sentiment_df.empty else "",
            'most_negative': sentiment_df.nsmallest(1, 'sentiment_score')['full_text'].values[0] if not sentiment_df.empty else ""
        }
    
    def extract_keywords(self, comments, top_n=20):
        """Extract most common keywords from comments"""
        # Combine all comment texts
        all_text = ' '.join([c['text'].lower() for c in comments])
        
        # Remove special characters and split into words
        words = re.findall(r'\b[a-z]{3,}\b', all_text)
        
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 
                     'can', 'has', 'was', 'one', 'our', 'out', 'this', 'that',
                     'with', 'have', 'from', 'they', 'been', 'will', 'what',
                     'about', 'which', 'when', 'more', 'your', 'like', 'just'}
        
        filtered_words = [w for w in words if w not in stop_words]
        
        # Count frequencies
        word_freq = Counter(filtered_words)
        
        return word_freq.most_common(top_n)
    
    def analyze_emoji_usage(self, comments):
        """Analyze emoji usage in comments"""
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        all_emojis = []
        
        for comment in comments:
            emojis = emoji_pattern.findall(comment['text'])
            all_emojis.extend(emojis)
        
        emoji_freq = Counter(all_emojis)
        
        return emoji_freq.most_common(10)
