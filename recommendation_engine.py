class RecommendationEngine:
    def generate_ai_captions(self, mood, post_type, style_pref="Balanced"):
        """Generates 3 viral caption options based on mood, type, and user style preference."""
        
        # Style modifiers
        style_mods = {
            "Hype Beast": " 🔥 FAST. LOUD. VIRAL.",
            "Minimalist": " ✨ Simple. Clean.",
            "Storyteller": " 📖 A story to tell...",
            "Educational": " 🧠 Learn this today.",
            "Balanced": ""
        }
        mod = style_mods.get(style_pref, "")

        templates = {
            "🔥 Energetic": [
                f"POV: You found the energy you needed today. ⚡️{mod}",
                f"Don't wait for opportunity. Create it. 🔥{mod}",
                f"Leveling up, one step at a time. 🚀{mod}"
            ],
            "🤝 Engaging & Friendly": [
                f"Which one is your favorite? Let me know in the comments! 👇{mod}",
                f"Tag someone who needs to see this today. ✨{mod}",
                f"Small moments, big memories. 💛{mod}"
            ],
            "🌑 Moody & Aesthetic": [
                f"Silence speaks louder than words. 🌑{mod}",
                f"Current mood: Aesthetic. ✨ #minimalist{mod}",
                f"Lost in the right direction.{mod}"
            ],
            "✨ Bright & Professional": [
                f"The secret to growth? Consistency. 📈{mod}",
                f"Professional vibes only. 💼 #success{mod}",
                f"Swipe to see the process! ➡️{mod}"
            ],
            "🌈 Neutral & Clean": [
                f"A clean start to the week. 🌿{mod}",
                f"Simple is the new significant.{mod}",
                f"Happy days are here. ☀️{mod}"
            ]
        }
        
        options = templates.get(mood, templates["🌈 Neutral & Clean"])
        return {
            "The Hook": options[0],
            "The Story": options[1],
            "The Minimalist": options[2]
        }

    def get_recommendations(self, features, metadata, virality_score, style_pref="Balanced"):
        """
        Generates a 3-point strategy plan (Visual, Text, Timing).
        """
        recs = []
        nlp = metadata['nlp']
        
        # 1. VISUAL RECOMMENDATION (The "Eye")
        if features.get('brightness_score', 120) < 100:
            recs.append({'category': '👁️ Visual Pulse', 'suggestion': "Lighting is too low for a viral hit. Boost the 'Exposure' or use a 'High-Contrast' filter to stop the scroll.", 'impact': 'High'})
        elif features.get('face_count', 0) == 0:
            recs.append({'category': '👁️ Visual Pulse', 'suggestion': "Human connection drives saves! If possible, add a face or hands in the first 3 seconds of the reel.", 'impact': 'Medium'})
        else:
            recs.append({'category': '👁️ Visual Pulse', 'suggestion': "Visual DNA looks solid! Maintain this high-clarity aesthetic for brand consistency.", 'impact': 'Stable'})

        # 2. TEXT RECOMMENDATION (The "Brain")
        if nlp['hook_strength'] < 6:
            recs.append({'category': '✍️ Hook Mastery', 'suggestion': "Your first sentence is too passive. Start with a 'How To' or a 'Controversial Opinion' to spike retention.", 'impact': 'High'})
        elif nlp['caption_length'] > 200 and style_pref == "Minimalist":
            recs.append({'category': '✍️ Hook Mastery', 'suggestion': "Caption is too wordy for a Minimalist vibe. Trim the middle and use more line breaks.", 'impact': 'Medium'})
        else:
            recs.append({'category': '✍️ Hook Mastery', 'suggestion': "Caption flow is excellent. Your sentiment matches your viral profile perfectly.", 'impact': 'Stable'})

        # 3. ALGO TIMING (The "Clock")
        if virality_score > 70:
            recs.append({'category': '⏰ Algo Timing', 'suggestion': "This is a 'Power Post'! Upload this between 6:00 PM and 8:30 PM for maximum algorithm push.", 'impact': 'Critical'})
        else:
            recs.append({'category': '⏰ Algo Timing', 'suggestion': "Standard post detected. Best to share this during the 'Lunch Break' window (12:00 PM - 1:30 PM).", 'impact': 'Medium'})

        # Final Strategy Summary
        if virality_score < 50:
            strategy = f"Strategy: Your content is 'Safe' but lacks 'Spark'. Apply the 3 boosters above to push your score over 75%."
        else:
            strategy = f"Strategy: You've matched the {style_pref} DNA! Focus on rapid engagement in the first 15 minutes of posting."

        return recs, strategy

    def get_growth_sim(self, expected_engagement):
        """Returns engagement growth data based on requested percentages."""
        times = ['1h', '6h', '12h', '24h']
        engagement = [
            round(expected_engagement * 0.20),
            round(expected_engagement * 0.50),
            round(expected_engagement * 0.75),
            round(expected_engagement * 1.00)
        ]
        
        return {'times': times, 'engagement': engagement}

