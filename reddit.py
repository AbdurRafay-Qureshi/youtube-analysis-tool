# reddit.py
# Reddit Analytics Engine - FIXED VERSION
# Accurate engagement calculations: (Upvotes + Comments) / Members × 100

import praw
from praw.exceptions import PRAWException, RedditAPIException
import pandas as pd
from datetime import datetime, timezone
import re


class RedditAnalyser:
    """
    Professional Reddit analytics with accurate engagement metrics.
    
    Engagement Rate Formula:
    - Subreddit: (Total Upvotes + Total Comments) / Members × 100
    - Individual Posts: (Post Upvotes + Post Comments) / Members × 100
    """
    
    def __init__(self, client_id, client_secret, user_agent):
        """Initialize Reddit API connection."""
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                check_for_async=False,
                timeout=30
            )
            # Test connection
            self.reddit.user.me()
            print("✅ Reddit API connected successfully")
        except Exception as e:
            print(f"❌ Reddit API connection failed: {str(e)}")
            raise
    
    
    @staticmethod
    def clean_identifier(identifier, prefix='r/'):
        """
        Clean subreddit/user identifier.
        Handles: 'python', 'r/python', 'https://reddit.com/r/python'
        """
        identifier = identifier.strip()
        
        # Handle full Reddit URLs
        if 'reddit.com' in identifier:
            match = re.search(r'/(r|u)/([^/]+)', identifier)
            if match:
                identifier = match.group(2)
        
        # Remove r/ or u/ prefix
        identifier = identifier.replace(prefix, '').strip()
        
        return identifier
    
    
    def analyze_subreddit(self, subreddit_name, limit=200):
        """
        Analyze a subreddit with ACCURATE engagement metrics.
        
        Engagement Rate = (Upvotes + Comments) / Members × 100
        """
        # Clean input
        clean_name = self.clean_identifier(subreddit_name, 'r/')
        
        print(f"\n📊 Analyzing r/{clean_name}...")
        
        try:
            # Get subreddit object
            subreddit = self.reddit.subreddit(clean_name)
            
            # Force refresh for accurate subscriber count
            subreddit._fetch()
            
            # Fetch info and posts
            stats = self._get_subreddit_info(subreddit)
            posts_df = self._fetch_subreddit_posts(subreddit, limit, stats['members'])
            
            # Calculate engagement metrics using CORRECT formula
            engagement_stats = self._calculate_subreddit_engagement(posts_df, stats['members'])
            
            # Merge stats
            stats.update(engagement_stats)
            stats['posts_analyzed'] = len(posts_df)
            
            print(f"✅ Successfully analyzed r/{clean_name}")
            print(f"📝 Fetched {len(posts_df)} posts")
            print(f"👥 Members: {stats['members']:,}")
            print(f"📊 Engagement Rate: {stats['avg_engagement_rate']:.2f}%")
            
            return {
                'stats': stats,
                'posts': posts_df,
                'type': 'subreddit',
                'name': clean_name
            }
            
        except Exception as e:
            print(f"❌ Error analyzing subreddit: {str(e)}")
            raise
    
    
    def analyze_user(self, username, limit=200):
        """Analyze a Reddit user."""
        # Clean input
        clean_name = self.clean_identifier(username, 'u/')
        
        print(f"\n👤 Analyzing u/{clean_name}...")
        
        try:
            # Get user object
            user = self.reddit.redditor(clean_name)
            
            # Fetch info, posts, and comments
            stats = self._get_user_info(user)
            posts_df = self._fetch_user_posts(user, limit)
            comments_df = self._fetch_user_comments(user, limit)
            
            # Calculate engagement metrics
            engagement_stats = self._calculate_user_engagement(posts_df, comments_df)
            
            # Merge stats
            stats.update(engagement_stats)
            stats['posts_analyzed'] = len(posts_df)
            stats['comments_analyzed'] = len(comments_df)
            
            print(f"✅ Successfully analyzed u/{clean_name}")
            print(f"📝 Fetched {len(posts_df)} posts, {len(comments_df)} comments")
            
            return {
                'stats': stats,
                'posts': posts_df,
                'comments': comments_df,
                'type': 'user',
                'name': clean_name
            }
            
        except Exception as e:
            print(f"❌ Error analyzing user: {str(e)}")
            raise
    
    
    # ==================== SUBREDDIT METHODS ====================
    
    def _get_subreddit_info(self, subreddit):
        """Get subreddit info with forced refresh."""
        try:
            # Force refresh for accurate subscriber count
            subreddit._fetch()
            
            return {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.public_description[:200] if subreddit.public_description else "No description",
                'members': subreddit.subscribers,
                'active_users': getattr(subreddit, 'accounts_active', 0) or 0,
                'created_utc': datetime.fromtimestamp(subreddit.created_utc, tz=timezone.utc),
                'is_nsfw': subreddit.over18,
                'url': f"https://www.reddit.com/r/{subreddit.display_name}/",
            }
        except Exception as e:
            print(f"⚠️ Error fetching subreddit info: {str(e)}")
            return {'members': 1}  # Prevent division by zero
    
    
    def _fetch_subreddit_posts(self, subreddit, limit, member_count):
        """
        Fetch posts with CORRECT engagement rate calculation.
        
        Engagement Rate = ((Upvotes + Comments) / Members) × 100
        """
        posts_list = []
        
        try:
            print(f"🔄 Fetching up to {limit} posts from r/{subreddit.display_name}...")
            
            # Fetch hot posts
            for post in subreddit.hot(limit=limit):
                try:
                    # CORRECT FORMULA: (Upvotes + Comments) / Members × 100
                    engagement = ((post.score + post.num_comments) / member_count) * 100
                    
                    posts_list.append({
                        'post_id': post.id,
                        'title': post.title,
                        'author': str(post.author) if post.author else '[deleted]',
                        'created_utc': datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                        'upvotes': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'engagement_rate': round(engagement, 4),  # More precision
                        'permalink': f"https://reddit.com{post.permalink}",
                        'url': post.url,
                        'is_self': post.is_self,
                        'selftext': post.selftext[:300] if post.is_self else '',
                        'link_flair_text': post.link_flair_text or 'None',
                        'num_awards': post.total_awards_received,
                        'is_video': post.is_video,
                        'domain': post.domain,
                    })
                except Exception as e:
                    print(f"⚠️ Skipping post: {str(e)}")
                    continue
            
            df = pd.DataFrame(posts_list)
            
            if not df.empty:
                # Add time-based features
                df['hour'] = df['created_utc'].dt.hour
                df['day_of_week'] = df['created_utc'].dt.day_name()
                df['day_name'] = df['created_utc'].dt.day_name()
                df['date'] = df['created_utc'].dt.date
            
            return df
            
        except Exception as e:
            print(f"❌ Error fetching posts: {str(e)}")
            return pd.DataFrame()
    
    
    def _calculate_subreddit_engagement(self, df, member_count):
        """
        Calculate ACCURATE engagement metrics.
        
        Total Engagement Rate = (Total Upvotes + Total Comments) / Members × 100
        """
        if df.empty:
            return {
                'total_upvotes': 0,
                'total_comments': 0,
                'total_awards': 0,
                'avg_upvotes': 0.0,
                'avg_comments': 0.0,
                'avg_engagement_rate': 0.0,
                'total_engagement_rate': 0.0,  # NEW: Overall engagement
                'comment_rate': 0.0,  # NEW: Comment rate
                'max_engagement_rate': 0.0,
                'avg_upvote_ratio': 0.0,
                'total_posts_fetched': 0,
            }
        
        total_upvotes = int(df['upvotes'].sum())
        total_comments = int(df['num_comments'].sum())
        
        # CORRECT FORMULAS
        total_engagement_rate = ((total_upvotes + total_comments) / member_count) * 100
        comment_rate = (total_comments / member_count) * 100
        
        return {
            'total_upvotes': total_upvotes,
            'total_comments': total_comments,
            'total_awards': int(df['num_awards'].sum()),
            'avg_upvotes': round(df['upvotes'].mean(), 1),
            'avg_comments': round(df['num_comments'].mean(), 1),
            'avg_engagement_rate': round(df['engagement_rate'].mean(), 2),
            'total_engagement_rate': round(total_engagement_rate, 2),  # NEW
            'comment_rate': round(comment_rate, 2),  # NEW
            'max_engagement_rate': round(df['engagement_rate'].max(), 2),
            'avg_upvote_ratio': round(df['upvote_ratio'].mean() * 100, 1),
            'total_posts_fetched': len(df),
        }
    
    
    # ==================== USER METHODS ====================
    
    def _get_user_info(self, user):
        """Get user info."""
        try:
            return {
                'username': user.name,
                'created_utc': datetime.fromtimestamp(user.created_utc, tz=timezone.utc),
                'link_karma': user.link_karma,
                'comment_karma': user.comment_karma,
                'total_karma': user.link_karma + user.comment_karma,
                'is_employee': user.is_employee,
                'is_gold': user.is_gold,
                'is_mod': user.is_mod,
                'has_verified_email': user.has_verified_email,
            }
        except Exception as e:
            print(f"⚠️ Error fetching user info: {str(e)}")
            return {}
    
    
    def _fetch_user_posts(self, user, limit):
        """Fetch user posts."""
        posts_list = []
        
        try:
            print(f"🔄 Fetching up to {limit} posts from u/{user.name}...")
            
            for post in user.submissions.new(limit=limit):
                try:
                    # Simplified engagement for user posts
                    engagement = ((post.num_comments + post.total_awards_received) / max(post.score, 1)) * 100
                    
                    posts_list.append({
                        'post_id': post.id,
                        'title': post.title,
                        'subreddit': str(post.subreddit),
                        'created_utc': datetime.fromtimestamp(post.created_utc, tz=timezone.utc),
                        'upvotes': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'engagement_rate': round(engagement, 2),
                        'permalink': f"https://reddit.com{post.permalink}",
                        'is_self': post.is_self,
                        'num_awards': post.total_awards_received,
                    })
                except Exception as e:
                    print(f"⚠️ Skipping post: {str(e)}")
                    continue
            
            df = pd.DataFrame(posts_list)
            
            if not df.empty:
                df['hour'] = df['created_utc'].dt.hour
                df['day_of_week'] = df['created_utc'].dt.day_name()
                df['day_name'] = df['created_utc'].dt.day_name()
            
            return df
            
        except Exception as e:
            print(f"❌ Error fetching user posts: {str(e)}")
            return pd.DataFrame()
    
    
    def _fetch_user_comments(self, user, limit):
        """Fetch user comments."""
        comments_list = []
        
        try:
            print(f"🔄 Fetching up to {limit} comments from u/{user.name}...")
            
            for comment in user.comments.new(limit=limit):
                try:
                    comments_list.append({
                        'comment_id': comment.id,
                        'body': comment.body[:200],
                        'subreddit': str(comment.subreddit),
                        'created_utc': datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                        'upvotes': comment.score,
                        'permalink': f"https://reddit.com{comment.permalink}",
                    })
                except Exception as e:
                    print(f"⚠️ Skipping comment: {str(e)}")
                    continue
            
            return pd.DataFrame(comments_list)
            
        except Exception as e:
            print(f"❌ Error fetching user comments: {str(e)}")
            return pd.DataFrame()
    
    
    def _calculate_user_engagement(self, posts_df, comments_df):
        """Calculate user engagement metrics."""
        stats = {}
        
        if not posts_df.empty:
            stats['total_post_upvotes'] = int(posts_df['upvotes'].sum())
            stats['total_post_comments'] = int(posts_df['num_comments'].sum())
            stats['avg_post_upvotes'] = round(posts_df['upvotes'].mean(), 1)
            stats['avg_post_engagement'] = round(posts_df['engagement_rate'].mean(), 2)
        else:
            stats.update({
                'total_post_upvotes': 0,
                'total_post_comments': 0,
                'avg_post_upvotes': 0.0,
                'avg_post_engagement': 0.0
            })
        
        if not comments_df.empty:
            stats['total_comment_upvotes'] = int(comments_df['upvotes'].sum())
            stats['avg_comment_upvotes'] = round(comments_df['upvotes'].mean(), 1)
        else:
            stats.update({
                'total_comment_upvotes': 0,
                'avg_comment_upvotes': 0.0
            })
        
        return stats
    
    
    # ==================== UTILITY METHODS ====================
    
    def get_top_posts(self, df, metric='upvotes', n=10):
        """Get top N posts by specified metric."""
        if df.empty:
            return pd.DataFrame()
        
        return df.nlargest(n, metric)[['title', 'upvotes', 'num_comments', 'engagement_rate', 'permalink']]
    
    
    def format_large_number(self, num):
        """Format large numbers with K/M suffix."""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(int(num))
