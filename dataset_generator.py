import pandas as pd
import numpy as np
import os

def generate_sample_data(num_rows=600):
    """
    Generates a realistic synthetic dataset for Instagram virality prediction.
    """
    np.random.seed(42)
    
    post_types = ['Image', 'Reel', 'Carousel']
    captions = [
        "Check out this amazing view! #nature #travel",
        "Morning workout routine. #fitness #goals",
        "New recipe alert! 🍲 #cooking #foodie",
        "Throwback to the best summer. #vibes #memory",
        "AI is changing the world. #tech #ai",
        "Productivity hacks for 2024. #success #work",
        "Night out with friends! ✨ #party #weekend",
        "Cozy rainy day mood. #aesthetic #home",
        "Just launched my new website! #business #startup",
        "Life is better when you're laughing. #happy #life"
    ]
    
    data = []
    for _ in range(num_rows):
        post_type = np.random.choice(post_types)
        followers = np.random.randint(500, 100000)
        posting_hour = np.random.randint(0, 24)
        
        # Simulating correlation: Reels generally get more reach
        base_virality = np.random.randint(30, 80)
        if post_type == 'Reel':
            base_virality += 15
        elif post_type == 'Carousel':
            base_virality += 5
            
        caption = np.random.choice(captions)
        hashtag_count = np.random.randint(2, 25)
        
        # NLP Features (Simulated for dataset generation)
        sentiment_score = np.random.uniform(-0.1, 0.9)
        caption_length = len(caption)
        
        # Visual Features (Simulated)
        brightness_score = np.random.randint(50, 255)
        face_count = np.random.randint(0, 4)
        motion_score = np.random.uniform(0, 1) if post_type == 'Reel' else 0
        
        # Virality Score Calculation (Target)
        # Weighting factors
        v_score = (
            (sentiment_score * 10) + 
            (brightness_score / 25) + 
            (face_count * 2) + 
            (motion_score * 15) + 
            (10 if 18 <= posting_hour <= 21 else 0) + # Peak hours
            np.random.normal(0, 5)
        )
        
        # Normalize to 0-100
        v_score = max(min(v_score + base_virality, 100), 10)
        
        # engagement metrics
        likes = int(followers * (v_score / 1000) * np.random.uniform(0.5, 1.5))
        comments = int(likes * np.random.uniform(0.02, 0.08))
        shares = int(likes * np.random.uniform(0.01, 0.05))
        
        data.append({
            'caption': caption,
            'hashtags': "#tag" + str(np.random.randint(1,100)),
            'post_type': post_type,
            'followers': followers,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'posting_hour': posting_hour,
            'caption_length': caption_length,
            'hashtag_count': hashtag_count,
            'sentiment_score': sentiment_score,
            'brightness_score': brightness_score,
            'face_count': face_count,
            'motion_score': motion_score,
            'virality_score': round(v_score, 2)
        })
        
    df = pd.DataFrame(data)
    df.to_csv('final_dataset.csv', index=False)
    print("Dataset generated successfully: final_dataset.csv")
    return df

if __name__ == "__main__":
    generate_sample_data()
