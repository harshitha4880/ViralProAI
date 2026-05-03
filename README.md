# 🚀 AI-Driven Instagram Content Virality Predictor

A premium Streamlit web application that uses Machine Learning, NLP, and Computer Vision to predict the virality of Instagram posts before you publish them.

## ✨ Features
- **Multi-Modal Analysis**: Analyzes text (captions/hashtags) and media (images/reels/carousels).
- **Computer Vision**: Extracts brightness, face count, and motion scores using OpenCV.
- **NLP Engine**: Evaluates sentiment, hook strength, and hashtag quality.
- **Virality Prediction**: Predicts a score (0-100), expected likes, comments, and engagement rate.
- **Growth Simulator**: Interactive charts showing engagement projection over 24 hours.
- **AI Recommendation Engine**: Actionable suggestions to improve reach.
- **PDF Reports**: Professional downloadable analysis summaries.
- **Premium UI**: Futuristic dark theme with glassmorphism and modern aesthetics.

## 🛠️ Tech Stack
- **Frontend**: Streamlit + Custom CSS
- **Machine Learning**: Scikit-Learn (RandomForest)
- **Computer Vision**: OpenCV, Pillow
- **NLP**: TextBlob
- **Visualizations**: Plotly
- **Data**: Pandas, NumPy
- **Reports**: FPDF

## 📦 Installation & Setup

1. **Clone the project** or navigate to the directory:
   ```bash
   cd instagram_virality_predictor
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure
- `app.py`: Main Streamlit dashboard with custom UI.
- `dataset_generator.py`: Generates synthetic data for training.
- `train_model.py`: Trains the RandomForest virality model.
- `feature_extraction.py`: Unifies text and media features.
- `media_analysis.py`: OpenCV logic for image/video analysis.
- `nlp_analysis.py`: TextBlob logic for sentiment and hooks.
- `recommendation_engine.py`: Logic for growth tips and simulations.
- `report_generator.py`: PDF generation logic.

---
Built for creators and social media managers who want to data-drive their growth. 🚀
