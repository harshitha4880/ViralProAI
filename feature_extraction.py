from media_analysis import MediaAnalyzer
from nlp_analysis import NLPAnalyzer

class FeatureExtractor:
    def __init__(self):
        self.media_analyzer = MediaAnalyzer()
        self.nlp_analyzer = NLPAnalyzer()

    def extract_all(self, caption, hashtags, post_type, followers, posting_hour, media_path=None):
        """
        Combines all analysis into one feature dictionary.
        """
        # NLP Analysis
        nlp_res = self.nlp_analyzer.analyze_caption(caption)
        hash_res = self.nlp_analyzer.analyze_hashtags(hashtags)

        # Media Analysis
        if media_path:
            if post_type == 'Reel':
                media_res = self.media_analyzer.analyze_video(media_path)
            elif post_type == 'Carousel':
                # For carousel, we expect media_path to be a list of paths
                if isinstance(media_path, list):
                    media_res = self.media_analyzer.analyze_carousel(media_path)
                else:
                    media_res = self.media_analyzer.analyze_image(media_path)
            else:
                media_res = self.media_analyzer.analyze_image(media_path)
        else:
            media_res = self.media_analyzer.get_default_features()

        # Combine into ML compatible format
        features = {
            'followers': followers,
            'posting_hour': posting_hour,
            'caption_length': nlp_res['caption_length'],
            'hashtag_count': hash_res['count'],
            'sentiment_score': nlp_res['sentiment_score'],
            'brightness_score': media_res['brightness_score'],
            'face_count': media_res['face_count'],
            'motion_score': media_res['motion_score'],
            # Mapping post type to numeric
            'post_type_encoded': self._encode_post_type(post_type)
        }

        # Detailed breakdown for dashboard
        metadata = {
            'nlp': nlp_res,
            'hashtags': hash_res,
            'media': media_res
        }

        return features, metadata

    def analyze_text(self, text):
        """Standalone NLP analysis for the Creative Studio."""
        return self.nlp_analyzer.analyze_caption(text)

    def _encode_post_type(self, ptype):
        mapping = {'Image': 0, 'Reel': 1, 'Carousel': 2}
        return mapping.get(ptype, 0)
