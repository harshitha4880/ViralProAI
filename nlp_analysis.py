from textblob import TextBlob
import re

class NLPAnalyzer:
    def analyze_caption(self, caption):
        """Analyzes caption text for sentiment, length, and quality."""
        if not caption:
            return {
                'sentiment_score': 0.0,
                'caption_length': 0,
                'hook_strength': 0,
                'caption_quality': 0,
                'emotions': self._get_default_emotions(),
                'sentiment_flow': "Neutral"
            }

        blob = TextBlob(caption)
        sentiment = blob.sentiment.polarity # Range [-1, 1]
        
        # Length
        length = len(caption)
        caption_lower = caption.lower()
        
        # Hook strength & Power Words
        power_words = [
            'secret', 'hacks', 'viral', 'best', 'unbelievable', 'magic', 'luxury', 
            'must-have', 'finally', 'exposed', 'stop', 'warning', 'actually'
        ]
        power_count = sum(1 for word in power_words if word in caption_lower)
        
        # Hook Strength Calculation
        first_part = caption[:50].lower()
        hook_score = 0
        if '?' in first_part: hook_score += 3
        if '!' in first_part: hook_score += 2
        if any(char for char in first_part if ord(char) > 127): hook_score += 2 # Emojis
        if any(word in first_part for word in ['how to', 'why', 'top', 'new']): hook_score += 3
        hook_score += (power_count * 1.5)

        # Advanced Emotion Detection
        emotions = {
            "Hype": min(1.0, (caption.count('!') + power_count) / 8),
            "Joy": max(0.0, min(1.0, (sentiment + 0.5))),
            "Curiosity": (power_count + (2 if '?' in caption else 0)) / 6,
            "Luxury": 1.0 if any(w in caption_lower for w in ['luxury', 'exclusive', 'premium', 'aesthetic']) else 0.2,
            "Trust": 1.0 if any(w in caption_lower for w in ['guide', 'tips', 'how', 'learned', 'truth']) else 0.3,
            "Personal": 1.0 if any(w in caption_lower for w in ['i ', 'my', 'me ', 'we ', 'our']) else 0.4
        }
        
        # Sentiment Flow (Beginning vs End)
        sentences = blob.sentences
        if len(sentences) >= 2:
            start_sent = sentences[0].sentiment.polarity
            end_sent = sentences[-1].sentiment.polarity
            if start_sent < 0 and end_sent > 0:
                flow = "Redemption (Neg -> Pos)"
            elif start_sent > 0 and end_sent < 0:
                flow = "Warning (Pos -> Neg)"
            elif start_sent > 0.5 and end_sent > 0.5:
                flow = "Pure Hype"
            else:
                flow = "Stable"
        else:
            flow = "Short/Consistent"

        # Quality score based on sentiment and length balance
        quality = 50 + (sentiment * 20)
        if 80 < length < 250:
            quality += 20
        elif length > 600:
            quality -= 15

        return {
            'sentiment_score': round(float(sentiment), 2),
            'caption_length': length,
            'hook_strength': min(round(hook_score, 1), 10),
            'caption_quality': round(min(quality, 100), 2),
            'emotions': emotions,
            'sentiment_flow': flow,
            'readability': "High" if length < 150 else ("Medium" if length < 400 else "Dense")
        }

    def _get_default_emotions(self):
        return {
            "Hype": 0.0, "Joy": 0.5, "Curiosity": 0.0, 
            "Luxury": 0.0, "Trust": 0.0, "Personal": 0.0
        }

    def analyze_hashtags(self, hashtags_text):
        """Analyzes hashtag string."""
        if not hashtags_text:
            return {'count': 0, 'quality_score': 0, 'tags': []}

        tags = re.findall(r'#\w+', hashtags_text)
        count = len(tags)
        
        # Quality based on count (Ideal is usually 7-15)
        quality = 0
        if 7 <= count <= 15:
            quality = 95
        elif 1 <= count < 7:
            quality = 70
        elif count > 20:
            quality = 40
            
        return {
            'count': count,
            'quality_score': quality,
            'tags': tags
        }

