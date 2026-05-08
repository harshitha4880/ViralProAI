import requests
import json
import os

class InstagramAPIHandler:
    def __init__(self, credentials_path='credentials.json'):
        with open(credentials_path, 'r') as f:
            self.creds = json.load(f)
        self.base_url = "https://graph.facebook.com/v20.0/"
        self.access_token = self.creds['access_token']
        self.ig_user_id = None 
        self.facebook_page_id = None
        self.last_error = None # Track the latest API error
        
        # Auto-discover on init to ensure 'Spy' works immediately
        self.discover_ids()

    def discover_ids(self):
        """Automatically finds the Page and IG ID for the current token."""
        try:
            self.get_facebook_page_id()
            self.get_instagram_business_account_id()
        except Exception as e:
            self.last_error = str(e)

    def get_facebook_page_id(self):
        """Fetches the Facebook Page ID linked to the account."""
        url = f"{self.base_url}me/accounts?access_token={self.access_token}"
        response = requests.get(url).json()
        if 'error' in response:
            self.last_error = response['error'].get('message', 'Unknown Meta Error')
            return None
        if 'data' in response and len(response['data']) > 0:
            self.facebook_page_id = response['data'][0]['id']
            return self.facebook_page_id
        return None

    def get_instagram_business_account_id(self):
        """Fetches the Instagram Business Account ID linked to the Facebook Page."""
        if not self.facebook_page_id:
            self.get_facebook_page_id()
        
        if self.facebook_page_id:
            url = f"{self.base_url}{self.facebook_page_id}?fields=instagram_business_account&access_token={self.access_token}"
            response = requests.get(url).json()
            if 'error' in response:
                self.last_error = response['error'].get('message', 'Unknown Meta Error')
                return None
            if 'instagram_business_account' in response:
                self.ig_user_id = response['instagram_business_account']['id']
                return self.ig_user_id
        return None

    def get_profile_info(self):
        """Fetches follower count and profile details."""
        if not self.ig_user_id:
            self.get_instagram_business_account_id()
        
        if self.ig_user_id:
            url = f"{self.base_url}{self.ig_user_id}?fields=name,username,followers_count,media_count,profile_picture_url&access_token={self.access_token}"
            response = requests.get(url).json()
            if 'error' in response:
                self.last_error = response['error'].get('message', 'Unknown Meta Error')
                return None
            return response
        return None

    def get_recent_media(self, limit=10):
        """Fetches the most recent media posts with engagement metrics."""
        if not self.ig_user_id:
            self.get_instagram_business_account_id()
        
        if self.ig_user_id:
            # Removed 'engagement' as it's an insights field, added 'thumbnail_url' for reels
            url = f"{self.base_url}{self.ig_user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count&limit={limit}&access_token={self.access_token}"
            try:
                return requests.get(url).json()
            except:
                return None
        return None

    def get_competitor_info(self, username):
        """Uses Business Discovery API to fetch public stats and recent media of a competitor."""
        if not self.ig_user_id:
            self.get_instagram_business_account_id()
        
        if self.ig_user_id:
            # Clean username (remove @)
            username = username.replace("@", "").strip()
            
            # Meta Business Discovery Query (Added thumbnail_url for Reels)
            query = f"business_discovery.username({username}){{followers_count,media_count,id,username,name,media.limit(10){{id,caption,like_count,comments_count,media_type,timestamp,media_url,thumbnail_url}}}}"
            url = f"{self.base_url}{self.ig_user_id}?fields={query}&access_token={self.access_token}"
            
            try:
                response = requests.get(url)
                data = response.json()
                if 'business_discovery' in data:
                    return data['business_discovery']
                else:
                    print(f"Discovery Error: {data}")
                    return None
            except Exception as e:
                print(f"API Request Failed: {e}")
                return None
        return None

    def get_media_insights(self, media_id):
        """Fetches detailed insights for a specific post (reach, impressions, saved)."""
        url = f"{self.base_url}{media_id}/insights?metric=impressions,reach,saved&access_token={self.access_token}"
        return requests.get(url).json()

# API Integration Ready! 🚀
