import cv2
import numpy as np
from PIL import Image
import os

class MediaAnalyzer:
    def __init__(self):
        # Load Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def get_mood(self, brightness, motion, face_count):
        """Determines content mood based on visual properties."""
        if motion > 0.6: return "🔥 Energetic"
        if face_count > 0 and brightness > 160: return "🤝 Engaging & Friendly"
        if brightness < 80: return "🌑 Moody & Aesthetic"
        if brightness > 180: return "✨ Bright & Professional"
        return "🌈 Neutral & Clean"

    def analyze_image(self, image_path):
        """Analyzes a single image and returns features."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return self.get_default_features()

            # 1. Brightness Score
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            brightness = hsv[:, :, 2].mean()

            # 2. Face Count
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            face_count = len(faces)

            # 3. Clarity/Quality Score (Laplacian variance)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            clarity = cv2.Laplacian(gray, cv2.CV_64F).var()

            # 4. Neural Emotion Heuristics (Smile/Energy detection)
            emotion = "Neutral"
            if face_count > 0:
                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    # Check for higher pixel intensity in the lower half of the face (smile heuristic)
                    mouth_area = roi_gray[int(h*0.65):h, int(w*0.2):int(w*0.8)]
                    if mouth_area.mean() > 100:
                        emotion = "😊 Happy/Engaging"
                    else:
                        emotion = "😐 Serious/Aesthetic"

            return {
                "brightness": round(float(brightness), 1),
                "face_count": face_count,
                "clarity": round(float(clarity), 1),
                "emotion": emotion
            }

            return {
                'brightness_score': round(float(brightness), 2),
                'face_count': int(face_count),
                'clarity_score': round(float(clarity), 2),
                'motion_score': 0.0 # Images have no motion
            }
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return self.get_default_features()

    def analyze_video(self, video_path):
        """Analyzes a video/reel and returns average features."""
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return self.get_default_features()

            frame_count = 0
            brightness_list = []
            face_counts = []
            prev_frame = None
            motion_scores = []

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or frame_count > 100: # Limit to 100 frames for speed
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Brightness
                brightness_list.append(np.mean(frame))

                # Face detection (every 10th frame for speed)
                if frame_count % 10 == 0:
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    face_counts.append(len(faces))

                # Motion detection
                if prev_frame is not None:
                    diff = cv2.absdiff(gray, prev_frame)
                    motion_scores.append(np.mean(diff))
                
                prev_frame = gray
                frame_count += 1

            cap.release()

            return {
                'brightness_score': round(float(np.mean(brightness_list)), 2) if brightness_list else 120,
                'face_count': int(max(face_counts)) if face_counts else 0,
                'clarity_score': 100.0, # Placeholder for videos
                'motion_score': round(float(np.mean(motion_scores)), 2) if motion_scores else 0.5
            }
        except Exception as e:
            print(f"Error analyzing video: {e}")
            return self.get_default_features()

    def analyze_carousel(self, image_paths):
        """Analyzes multiple images for carousels."""
        all_features = [self.analyze_image(p) for p in image_paths]
        
        avg_brightness = np.mean([f['brightness_score'] for f in all_features])
        avg_faces = np.mean([f['face_count'] for f in all_features])
        avg_clarity = np.mean([f['clarity_score'] for f in all_features])

        return {
            'brightness_score': round(float(avg_brightness), 2),
            'face_count': int(round(avg_faces)),
            'clarity_score': round(float(avg_clarity), 2),
            'motion_score': 0.0,
            'image_count': len(image_paths)
        }

    def get_default_features(self):
        return {
            'brightness_score': 120.0,
            'face_count': 0,
            'clarity_score': 50.0,
            'motion_score': 0.0
        }
