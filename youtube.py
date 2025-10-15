# youtube.py
# This file contains the logic for interacting with the YouTube Data API v3.

import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from isodate import parse_duration

class YouTubeChannelAnalyser:
    """
    A class to fetch and analyze data for a given YouTube channel.
    """
    def __init__(self, api_key):
        """Initializes the YouTube API client."""
        try:
            self.youtube = build('youtube', 'v3', developerKey=api_key)
        except Exception as e:
            raise ValueError(f"Failed to build YouTube service. Check API key. Error: {e}")

    def _get_channel_id(self, channel_input):
        """
        Extracts channel ID from a URL, ID, or username.
        """
        # Regex for standard channel URLs
        channel_id_match = re.search(r'youtube\.com/channel/([^/]+)', channel_input)
        if channel_id_match:
            return channel_id_match.group(1)

        # Regex for custom URLs/usernames
        custom_url_match = re.search(r'youtube\.com/(?:c/|user/|@)?([^/]+)', channel_input)
        if custom_url_match:
            search_term = custom_url_match.group(1)
            try:
                # Search by username/custom URL
                request = self.youtube.channels().list(part='id', forUsername=search_term)
                response = request.execute()
                if response.get('items'):
                    return response['items'][0]['id']
            except HttpError as e:
                # Fallback to search if direct lookup fails
                pass

        # If it's not a URL, assume it's an ID or a username to be searched
        search_term = custom_url_match.group(1) if custom_url_match else channel_input
        try:
            search_request = self.youtube.search().list(part='id', q=search_term, type='channel', maxResults=1)
            search_response = search_request.execute()
            if search_response.get('items'):
                return search_response['items'][0]['id']['channelId']
            else:
                # Final attempt: Treat the input as a direct channel ID
                direct_request = self.youtube.channels().list(part='id', id=channel_input)
                direct_response = direct_request.execute()
                if direct_response.get('items'):
                    return direct_response['items'][0]['id']
        except HttpError as e:
            raise ValueError(f"API error while searching for channel. Details: {e}")

        raise ValueError("Could not find a valid YouTube channel for the given input.")


    def get_channel_data(self, channel_input):
        """
        Fetches all channel statistics and video data.
        Returns channel stats dictionary and a video details DataFrame.
        """
        channel_id = self._get_channel_id(channel_input)
        
        # 1. Get Channel Statistics
        try:
            request = self.youtube.channels().list(
                part="snippet,statistics,contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            # Defensive check if API returns no items for a valid-looking ID
            if not response.get("items"):
                raise ValueError("Could not retrieve channel details from the API.")
                
            channel_data = response["items"][0]
            
            stats = {
                "channel_id": channel_id,
                "channel_name": channel_data["snippet"]["title"],
                "description": channel_data["snippet"]["description"],
                "total_subscribers": int(channel_data["statistics"].get("subscriberCount", 0)),
                "total_views": int(channel_data["statistics"].get("viewCount", 0)),
                "total_videos": int(channel_data["statistics"].get("videoCount", 0)),
            }
            uploads_playlist_id = channel_data["contentDetails"]["relatedPlaylists"]["uploads"]

        except HttpError as e:
            raise ValueError(f"API Error fetching channel stats: {e}")
        except KeyError as e:
            raise ValueError(f"Unexpected API response structure for channel stats. Missing key: {e}")

        # 2. Get all Video IDs from the uploads playlist
        video_ids = self._get_video_ids(uploads_playlist_id)

        # If there are no videos, return stats and an empty DataFrame
        if not video_ids:
            return stats, pd.DataFrame()

        # 3. Get Video Details for all video IDs
        video_details = self._get_video_details(video_ids)

        # 4. Create DataFrame
        video_df = pd.DataFrame(video_details)

        # 5. Data Cleaning and Feature Engineering
        video_df = self._clean_and_process_df(video_df)

        return stats, video_df


    def _get_video_ids(self, uploads_playlist_id):
        """
        Paginates through the uploads playlist to get all video IDs.
        """
        video_ids = []
        request = self.youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50
        )

        while request:
            try:
                response = request.execute()
                # Use .get with a default empty list to prevent crashes on channels with no videos
                video_ids.extend([item['contentDetails']['videoId'] for item in response.get('items', [])])
                request = self.youtube.playlistItems().list_next(request, response)
            except HttpError as e:
                # If there's an error (e.g., playlist not found), stop and return what we have.
                print(f"Warning: Could not fetch all videos. API Error: {e}")
                break
                
        return video_ids

    def _get_video_details(self, video_ids):
        """
        Fetches detailed statistics and snippets for a list of video IDs in batches.
        """
        video_details = []
        # Process in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            try:
                request = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=",".join(batch_ids)
                )
                response = request.execute()
                # Use .get with a default empty list
                video_details.extend(response.get('items', []))
            except HttpError as e:
                print(f"Warning: Could not fetch details for a batch of videos. API Error: {e}")

        return video_details

    def _clean_and_process_df(self, df):
        """
        Cleans the raw video data and adds calculated columns.
        """
        # Extract relevant fields and convert types
        df['title'] = df['snippet'].apply(lambda x: x.get('title'))
        df['upload_date'] = pd.to_datetime(df['snippet'].apply(lambda x: x.get('publishedAt'))).dt.tz_localize(None)
        df['view_count'] = pd.to_numeric(df['statistics'].apply(lambda x: x.get('viewCount', 0)))
        df['like_count'] = pd.to_numeric(df['statistics'].apply(lambda x: x.get('likeCount', 0)))
        df['comment_count'] = pd.to_numeric(df['statistics'].apply(lambda x: x.get('commentCount', 0)))
        df['duration_seconds'] = df['contentDetails'].apply(lambda x: parse_duration(x.get('duration')).total_seconds())

        # Calculate Engagement Rate
        df['engagement_rate'] = ((df['like_count'] + df['comment_count']) / df['view_count']) * 100
        df['engagement_rate'] = df['engagement_rate'].fillna(0) # Handle division by zero for videos with 0 views

        # Add publish day and hour
        df['publish_day'] = df['upload_date'].dt.day_name()
        df['publish_hour'] = df['upload_date'].dt.hour
        
        return df

