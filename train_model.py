import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from dataset_generator import generate_sample_data

def train_virality_model():
    """
    Trains a Hybrid RandomForest model using both Synthetic and Kaggle data.
    """
    synthetic_path = 'final_dataset.csv'
    kaggle_path = 'Instagram_Analytics.csv'
    
    # 1. Load Synthetic Data
    if not os.path.exists(synthetic_path):
        print("Synthetic dataset not found. Generating...")
        df_syn = generate_sample_data()
    else:
        df_syn = pd.read_csv(synthetic_path)

    # 2. Load and Preprocess Kaggle Data
    if os.path.exists(kaggle_path):
        print(f"Loading Kaggle dataset: {kaggle_path}...")
        df_kg = pd.read_csv(kaggle_path)
        
        # Mapping Kaggle columns to our format
        # follower_count -> followers
        # post_hour -> posting_hour
        # caption_length -> caption_length
        # hashtags_count -> hashtag_count
        # media_type -> post_type
        
        mapping = {
            'follower_count': 'followers',
            'post_hour': 'posting_hour',
            'caption_length': 'caption_length',
            'hashtags_count': 'hashtag_count',
            'media_type': 'post_type'
        }
        df_kg = df_kg.rename(columns=mapping)
        
        # Calculate virality_score for Kaggle (Scale it to 0-100)
        # Kaggle engagement_rate is often a decimal like 0.05
        df_kg['virality_score'] = df_kg['engagement_rate'] * 1000
        df_kg['virality_score'] = df_kg['virality_score'].clip(0, 100)
        
        # Kaggle post_type uses lowercase 'reel', 'image', 'carousel'
        df_kg['post_type'] = df_kg['post_type'].str.capitalize()
        
        # Synthetic data has visual scores (brightness, faces, motion)
        # Kaggle data doesn't, so we fill them with realistic averages
        df_kg['sentiment_score'] = np.random.uniform(0.1, 0.6, size=len(df_kg))
        df_kg['brightness_score'] = np.random.randint(100, 200, size=len(df_kg))
        df_kg['face_count'] = np.random.randint(0, 2, size=len(df_kg))
        df_kg['motion_score'] = df_kg.apply(lambda x: np.random.uniform(0.3, 0.8) if x['post_type'] == 'Reel' else 0, axis=1)

        # Select only required columns
        cols = ['followers', 'posting_hour', 'caption_length', 'hashtag_count', 
                'sentiment_score', 'brightness_score', 'face_count', 'motion_score', 
                'post_type', 'virality_score']
        
        df_kg = df_kg[cols]
        df_syn = df_syn[cols]
        
        # Combine
        df = pd.concat([df_syn, df_kg], ignore_index=True)
        print(f"Hybrid dataset created. Total rows: {len(df)}")
    else:
        print("Kaggle dataset not found. Using synthetic data only.")
        df = df_syn

    # Features and Target
    feature_cols = [
        'followers', 'posting_hour', 'caption_length', 'hashtag_count', 
        'sentiment_score', 'brightness_score', 'face_count', 'motion_score'
    ]
    
    # Post type encoding
    mapping_type = {'Image': 0, 'Reel': 1, 'Carousel': 2}
    df['post_type_encoded'] = df['post_type'].map(mapping_type).fillna(0)
    
    feature_cols.append('post_type_encoded')
    
    X = df[feature_cols]
    y = df['virality_score']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    print("Training RandomForest model (Hybrid)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Calculate "Accuracy" (Percentage of predictions within 15 points of actual)
    diff = np.abs(y_test - predictions)
    accuracy = (diff < 15).mean() * 100

    # --- VIRAL DNA PROFILER ---
    # Study the top 10% of posts to find the "Ideal DNA"
    top_posts = df.sort_values(by='virality_score', ascending=False).head(len(df)//10)
    
    viral_profile = {
        'ideal_caption_length': int(top_posts['caption_length'].median()),
        'ideal_hashtag_count': int(top_posts['hashtag_count'].median()),
        'ideal_brightness': int(top_posts['brightness_score'].median()),
        'avg_sentiment': float(top_posts['sentiment_score'].mean()),
        'top_post_type': top_posts['post_type'].mode()[0]
    }
    
    import json
    with open('viral_profile.json', 'w') as f:
        json.dump(viral_profile, f)
    
    # Save Model Results
    results = {
        'mae': round(mae, 2), 
        'r2': round(r2, 2),
        'accuracy': round(float(accuracy), 1)
    }
    print(f"Hybrid model and Viral Profile created. Results: {results}")
    return results

if __name__ == "__main__":
    train_virality_model()
