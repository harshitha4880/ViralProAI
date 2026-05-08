import requests
import json
import os

class InstagramAPIHandler:
    def __init__(self, credentials_path='credentials.json', cache_path='id_cache.json'):
        with open(credentials_path, 'r') as f:
            self.creds = json.load(f)
        self.cache_path = cache_path
        self.base_url = "https://graph.facebook.com/v20.0/"
        self.access_token = self.creds['access_token']
        self.ig_user_id = None 
        self.facebook_page_id = None
        self.last_error = None 

        # Try loading from cache first
        self.load_cache()
        
        # If cache is empty or we hit an error, attempt discovery
        if not self.ig_user_id:
            self.discover_ids()

    def load_cache(self):
        """Loads IDs from local cache to avoid API rate limits."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as f:
                    cache = json.load(f)
                self.ig_user_id = cache.get('ig_user_id')
                self.facebook_page_id = cache.get('facebook_page_id')
            except:
                pass

    def save_cache(self):
        """Saves discovered IDs to local cache."""
        with open(self.cache_path, 'w') as f:
            json.dump({
                'ig_user_id': self.ig_user_id,
                'facebook_page_id': self.facebook_page_id
            }, f)

    def discover_ids(self):
        """Automatically finds the Page and IG ID for the current token by scanning all pages."""
        try:
            # 1. Fetch all Facebook Pages linked to this token
            url = f"{self.base_url}me/accounts?access_token={self.access_token}"
            response = requests.get(url).json()
            
            if 'error' in response:
                self.last_error = response['error'].get('message', 'Unknown Meta Error')
                return
            
            pages = response.get('data', [])
            if not pages:
                self.last_error = "No Facebook Pages found linked to this token."
                return

            # 2. Iterate through each page to find the linked Instagram Business Account
            for page in pages:
                page_id = page.get('id')
                if page_id:
                    # Probe this specific page for an IG link
                    url_ig = f"{self.base_url}{page_id}?fields=instagram_business_account&access_token={self.access_token}"
                    res_ig = requests.get(url_ig).json()
                    
                    if 'instagram_business_account' in res_ig:
                        self.facebook_page_id = page_id
                        self.ig_user_id = res_ig['instagram_business_account']['id']
                        self.save_cache() # Persist for future sessions
                        return # Success! Exit early
            
            self.last_error = "None of your Facebook Pages are linked to an Instagram Business account."
        except Exception as e:
            self.last_error = str(e)

    def get_profile_info(self):
        """Fetches follower count and profile details."""
        if not self.ig_user_id:
            self.discover_ids()
        
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
            self.discover_ids()
        
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
            self.discover_ids()
        
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
