# youtube.py
# Enhanced YouTube Data Extraction with Maximum Accuracy + VALIDATION

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import re
from datetime import datetime, timezone
import isodate
import time


class YouTubeChannelAnalyser:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)


    def extract_channel_id(self, channel_identifier):
        """Extract channel ID with improved accuracy"""
        channel_identifier = channel_identifier.strip()
        
        # Direct channel ID
        if channel_identifier.startswith('UC') and len(channel_identifier) == 24:
            return channel_identifier
        
        # Handle @username
        if channel_identifier.startswith('@'):
            username = channel_identifier[1:]
            try:
                request = self.youtube.channels().list(
                    part='id',
                    forHandle=username
                )
                response = request.execute()
                if response.get('items'):
                    return response['items'][0]['id']
            except:
                pass
            
            # Fallback to search
            try:
                request = self.youtube.search().list(
                    part='snippet',
                    q=username,
                    type='channel',
                    maxResults=5
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    if item['snippet'].get('channelTitle', '').lower() == username.lower():
                        return item['snippet']['channelId']
                
                if response.get('items'):
                    return response['items'][0]['snippet']['channelId']
            except HttpError:
                pass
        
        # Extract from URL patterns
        patterns = [
            r'youtube\.com/channel/([^/?&]+)',
            r'youtube\.com/c/([^/?&]+)',
            r'youtube\.com/user/([^/?&]+)',
            r'youtube\.com/@([^/?&]+)',
            r'youtube\.com/([^/?&]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, channel_identifier)
            if match:
                identifier = match.group(1)
                
                if identifier.startswith('UC') and len(identifier) == 24:
                    return identifier
                
                try:
                    request = self.youtube.channels().list(
                        part='id',
                        forHandle=identifier
                    )
                    response = request.execute()
                    if response.get('items'):
                        return response['items'][0]['id']
                except:
                    pass
                
                try:
                    request = self.youtube.search().list(
                        part='snippet',
                        q=identifier,
                        type='channel',
                        maxResults=5
                    )
                    response = request.execute()
                    
                    for item in response.get('items', []):
                        if item['snippet'].get('channelTitle', '').lower().replace(' ', '') == identifier.lower().replace(' ', ''):
                            return item['snippet']['channelId']
                    
                    if response.get('items'):
                        return response['items'][0]['snippet']['channelId']
                except HttpError:
                    pass
        
        # Last resort: Direct search
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=channel_identifier,
                type='channel',
                maxResults=5
            )
            response = request.execute()
            
            for item in response.get('items', []):
                if item['snippet'].get('channelTitle', '').lower() == channel_identifier.lower():
                    return item['snippet']['channelId']
            
            if response.get('items'):
                return response['items'][0]['snippet']['channelId']
        except HttpError:
            pass
        
        raise ValueError(f"Could not extract channel ID from: {channel_identifier}")


    def get_channel_statistics(self, channel_id):
        """Get ACTUAL channel stats from YouTube API"""
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics,contentDetails,brandingSettings',
                id=channel_id
            )
            response = request.execute()
            
            if not response.get('items'):
                raise ValueError("Channel not found")
            
            item = response['items'][0]
            stats = item.get('statistics', {})
            snippet = item.get('snippet', {})
            
            # RETURN ACTUAL CHANNEL STATS
            return {
                'channel_id': channel_id,
                'channel_name': snippet.get('title', 'Unknown'),
                'description': snippet.get('description', ''),
                'published_at': snippet.get('publishedAt', ''),
                'total_subscribers': int(stats.get('subscriberCount', 0)),
                'total_views': int(stats.get('viewCount', 0)),  # ACTUAL VIEWS
                'total_videos': int(stats.get('videoCount', 0)),  # ACTUAL VIDEO COUNT
                'uploads_playlist_id': item['contentDetails']['relatedPlaylists']['uploads'],
                'hidden_subscriber_count': stats.get('hiddenSubscriberCount', False),
                'custom_url': snippet.get('customUrl', ''),
                'country': snippet.get('country', 'Unknown')
            }
        except HttpError as e:
            raise ValueError(f"API Error: {str(e)}")


    def get_video_ids_from_playlist(self, playlist_id, max_results=500):
        """Fetch ALL video IDs with proper pagination"""
        video_ids = []
        next_page_token = None
        
        print(f"📥 Fetching video IDs...")
        
        while len(video_ids) < max_results:
            try:
                request = self.youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=playlist_id,
                    maxResults=min(50, max_results - len(video_ids)),
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    video_ids.append(item['contentDetails']['videoId'])
                
                print(f"  ✓ Fetched {len(video_ids)} videos so far...")
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                
                time.sleep(0.1)
                    
            except HttpError as e:
                print(f"⚠️ Error fetching playlist: {str(e)}")
                break
        
        return video_ids


    def get_video_details(self, video_ids):
        """Get detailed video statistics"""
        all_video_data = []
        total_batches = (len(video_ids) + 49) // 50
        
        print(f"📊 Fetching details for {len(video_ids)} videos in {total_batches} batches...")
        
        for batch_num, i in enumerate(range(0, len(video_ids), 50), 1):
            batch = video_ids[i:i+50]
            
            try:
                request = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails,status',
                    id=','.join(batch)
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    # Only public videos
                    if item['status']['privacyStatus'] != 'public':
                        continue
                    
                    snippet = item['snippet']
                    stats = item.get('statistics', {})
                    content_details = item['contentDetails']
                    
                    try:
                        duration = isodate.parse_duration(content_details['duration'])
                        duration_seconds = int(duration.total_seconds())
                    except:
                        duration_seconds = 0
                    
                    try:
                        upload_date = datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00'))
                    except:
                        upload_date = datetime.now(timezone.utc)
                    
                    view_count = int(stats.get('viewCount', 0))
                    like_count = int(stats.get('likeCount', 0))
                    comment_count = int(stats.get('commentCount', 0))
                    
                    engagement_rate = ((like_count + comment_count) / view_count * 100) if view_count > 0 else 0.0
                    
                    video_data = {
                        'video_id': item['id'],
                        'title': snippet['title'],
                        'upload_date': upload_date,
                        'view_count': view_count,
                        'like_count': like_count,
                        'comment_count': comment_count,
                        'engagement_rate': round(engagement_rate, 4),
                        'duration_seconds': duration_seconds,
                        'tags': snippet.get('tags', []),
                        'category_id': snippet.get('categoryId', ''),
                        'publish_day': upload_date.strftime('%A'),
                        'publish_hour': upload_date.hour,
                        'description': snippet.get('description', '')[:500],
                    }
                    
                    all_video_data.append(video_data)
                
                print(f"  ✓ Batch {batch_num}/{total_batches} complete ({len(all_video_data)} videos processed)")
                time.sleep(0.1)
                    
            except HttpError as e:
                print(f"⚠️ Error in batch {batch_num}: {str(e)}")
                continue
        
        return all_video_data


    def get_channel_data(self, channel_identifier, max_videos=500):
        """Main method - Returns ACTUAL channel stats + video data"""
        print(f"\n🔍 Analyzing: {channel_identifier}")
        print("=" * 60)
        
        # Step 1: Get channel ID
        channel_id = self.extract_channel_id(channel_identifier)
        print(f"✅ Channel ID: {channel_id}")
        
        # Step 2: Get ACTUAL channel statistics
        channel_stats = self.get_channel_statistics(channel_id)
        print(f"\n📊 OFFICIAL CHANNEL STATISTICS:")
        print(f"   Channel: {channel_stats['channel_name']}")
        print(f"   Subscribers: {channel_stats['total_subscribers']:,}")
        print(f"   Total Views: {channel_stats['total_views']:,}")
        print(f"   Total Videos: {channel_stats['total_videos']}")
        print(f"   Created: {channel_stats['published_at'][:10]}")
        
        # Step 3: Fetch video data
        actual_limit = min(max_videos, channel_stats['total_videos'])
        print(f"\n📥 Fetching up to {actual_limit} most recent videos...")
        
        video_ids = self.get_video_ids_from_playlist(
            channel_stats['uploads_playlist_id'],
            max_results=actual_limit
        )
        
        if not video_ids:
            raise ValueError("No videos found")
        
        print(f"✅ Retrieved {len(video_ids)} video IDs")
        
        # Step 4: Get video details
        video_data = self.get_video_details(video_ids)
        
        if not video_data:
            raise ValueError("Could not fetch video details")
        
        print(f"✅ Processed {len(video_data)} public videos\n")
        
        # Step 5: Create DataFrame
        df = pd.DataFrame(video_data)
        
        df['view_count'] = df['view_count'].astype('int64')
        df['like_count'] = df['like_count'].astype('int64')
        df['comment_count'] = df['comment_count'].astype('int64')
        df['engagement_rate'] = df['engagement_rate'].astype('float64')
        df['duration_seconds'] = df['duration_seconds'].astype('int64')
        
        df = df.sort_values('upload_date', ascending=False).reset_index(drop=True)
        df['view_rank'] = df['view_count'].rank(ascending=False, method='dense').astype(int)
        df['days_since_upload'] = (datetime.now(timezone.utc) - df['upload_date']).dt.days
        df['views_per_day'] = (df['view_count'] / df['days_since_upload'].replace(0, 1)).round(2)
        
        # CRITICAL: Add validation
        fetched_views = df['view_count'].sum()
        print(f"📊 VALIDATION:")
        print(f"   Videos Fetched: {len(df)} / {channel_stats['total_videos']}")
        print(f"   Views from Fetched Videos: {fetched_views:,}")
        print(f"   Total Channel Views (API): {channel_stats['total_views']:,}")
        print(f"   Coverage: {(fetched_views / channel_stats['total_views'] * 100):.1f}%")
        print("=" * 60)
        
        return channel_stats, df
