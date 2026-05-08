import pandas as pd
import numpy as np
from textblob import TextBlob
import os

class AudioMatchmaker:
    def __init__(self, csv_path='trending_audio_dataset.csv'):
        self.csv_path = csv_path
        self.dataset = self.load_audio_dataset()

    def load_audio_dataset(self):
        """Loads the audio dataset using Pandas."""
        if os.path.exists(self.csv_path):
            return pd.read_csv(self.csv_path)
        else:
            # Fallback empty dataframe
            return pd.DataFrame(columns=['audio_name', 'artist', 'category', 'mood', 'duration', 'trend_score', 'usage_count', 'popularity_level'])

    def detect_content_category(self, caption, niche):
        """Infers category from niche or keywords."""
        if niche and niche != "General":
            return niche.lower()
        
        # Simple keyword fallback
        caption_lower = caption.lower()
        if any(w in caption_lower for w in ['workout', 'gym', 'run']): return 'fitness'
        if any(w in caption_lower for w in ['trip', 'beach', 'mountain']): return 'travel'
        if any(w in caption_lower for w in ['outfit', 'style', 'dress']): return 'fashion'
        if any(w in caption_lower for w in ['code', 'gadget', 'app']): return 'tech'
        
        return 'lifestyle'

    def detect_mood(self, caption, tone):
        """Detects mood from tone or sentiment analysis."""
        if tone and tone != "Casual":
            mapping = {
                "Motivational": "motivational",
                "Funny": "funny",
                "Aesthetic": "aesthetic",
                "Professional": "energetic",
                "Hype": "energetic"
            }
            return mapping.get(tone, "aesthetic")

        # Sentiment fallback
        blob = TextBlob(caption)
        sentiment = blob.sentiment.polarity
        if sentiment > 0.3: return 'energetic'
        if sentiment < -0.1: return 'emotional'
        return 'calm'

    def calculate_match_score(self, audio, target_cat, target_mood, target_dur):
        """Calculates the 0-100 match score with a Variety Pulse."""
        cat_match = 1.0 if audio['category'] == target_cat else 0.0
        mood_match = 1.0 if audio['mood'] == target_mood else 0.0
        
        # Duration match (closeness)
        dur_diff = abs(audio['duration'] - target_dur)
        dur_match = max(0, 1.0 - (dur_diff / 60.0))
        
        norm_trend = audio['trend_score'] / 100.0
        
        # --- NEW: VARIETY PULSE (RANDOM NOISE) ---
        # Adds 0-5% variation to prevent repeating the same songs
        noise = np.random.uniform(0, 0.05)
        
        score = (0.35 * cat_match) + (0.3 * mood_match) + (0.2 * dur_match) + (0.1 * norm_trend) + noise
        return round(score * 100, 1)

    def recommend_trending_audio(self, caption, niche, tone, duration):
        """Main recommendation engine with Diversity Shuffling."""
        target_cat = self.detect_content_category(caption, niche)
        target_mood = self.detect_mood(caption, tone)
        
        if self.dataset.empty:
            return []

        # Calculate scores for all
        self.dataset['match_score'] = self.dataset.apply(
            lambda x: self.calculate_match_score(x, target_cat, target_mood, duration), 
            axis=1
        )
        
        # Sort and take top 10 (more variety)
        top_pool = self.dataset.sort_values(by='match_score', ascending=False).head(10)
        
        # Randomly sample 5 from the top 10 for diversity
        recommendations = top_pool.sample(min(5, len(top_pool)))
        recommendations = recommendations.sort_values(by='match_score', ascending=False)
        
        results = []
        for _, row in recommendations.iterrows():
            results.append({
                "audio_name": row['audio_name'],
                "artist": row['artist'],
                "trend_score": row['trend_score'],
                "match_score": row['match_score'],
                "popularity": row['popularity_level'],
                "why": f"Matches your {target_cat} niche and {target_mood} mood perfectly.",
                "tip": "Use for transitions" if duration < 30 else "Sync with text overlays"
            })
            
        return results
