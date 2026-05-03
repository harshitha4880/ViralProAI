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
        Generates conversational, ChatGPT-style insights based on style preference.
        """
        recs = []
        nlp = metadata['nlp']
        
        # 1. Style-Specific Checks
        if style_pref == "Minimalist" and nlp['caption_length'] > 150:
            recs.append({'category': '🎨 Style Match', 'suggestion': "Since you prefer a Minimalist style, I'd suggest cutting this caption by 50%. Less is more for your aesthetic.", 'impact': 'Medium'})
        elif style_pref == "Hype Beast" and nlp['hook_strength'] < 7:
            recs.append({'category': '🎨 Style Match', 'suggestion': "For a Hype Beast vibe, your hook needs more punch! Use more 'Power Words' or emojis in the first line.", 'impact': 'High'})
        elif style_pref == "Storyteller" and nlp['caption_length'] < 300:
            recs.append({'category': '🎨 Style Match', 'suggestion': "Storytellers usually thrive on depth. Try expanding this into a 'Micro-Blog' style post to increase Save rates.", 'impact': 'Medium'})

        # 2. General NLP Suggestions
        if nlp['hook_strength'] < 5:
            recs.append({'category': '🧠 AI Insight', 'suggestion': "I noticed your hook is a bit weak. ChatGPT-style tip: Try starting with a 'cliffhanger' sentence to keep them reading.", 'impact': 'High'})
        
        if nlp['sentiment_flow'] == "Warning (Pos -> Neg)":
            recs.append({'category': '🎭 Emotional Flow', 'suggestion': "Your caption ends on a negative note. Consider flipping it to end with a positive Call-To-Action (CTA) for better engagement.", 'impact': 'Medium'})

        # 3. Score-based Strategy
        if virality_score < 40:
            strategy = f"Based on my analysis for the {style_pref} style, your content is 'Safe' but lacks 'Spark'. To fix this, I recommend boosting the visual contrast and using one of the 'Hook' captions below."
        elif 40 <= virality_score <= 70:
            strategy = f"You're on the right track for a {style_pref} creator! This content has high engagement potential. If you post this between 6-8 PM tonight, my data suggests you'll hit peak reach."
        else:
            strategy = f"Incredible! This content matches the DNA of {style_pref} viral hits perfectly. Don't change a thing—just hit post and engage with every comment in the first 30 minutes."

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

