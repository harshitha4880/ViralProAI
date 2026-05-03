import random
from textblob import TextBlob
import re

class CaptionGenerator:
    def __init__(self):
        # 1. Template Library: Hooks based on Tone
        self.hooks = {
            "Motivational": [
                "No excuses. Just results 💪",
                "This changed everything 🔥",
                "Your future self will thank you for starting today 🚀",
                "Dream big, work harder ✨"
            ],
            "Funny": [
                "POV: You said just one more 😅",
                "I’m not lazy, I’m just on energy-saving mode 🔋😂",
                "My life is basically a series of 'oops' and 'it worked' 🤷‍♂️",
                "Expectation vs Reality: This post 🤡"
            ],
            "Aesthetic": [
                "Golden hour hits different ✨",
                "Little moments, big memories 🕊️",
                "Soul full of sunshine ☀️",
                "Whispers of elegance 💎"
            ],
            "Professional": [
                "The secret to scaling your business 📈",
                "Why consistency is your greatest asset 🤝",
                "Industry insights you can't ignore 🧠",
                "Redefining excellence in the industry 💼"
            ],
            "Casual": [
                "Just another day in paradise 🌴",
                "Weekend vibes only ✨",
                "Keeping it real today ✌️",
                "Current status: Relaxed 🧘‍♂️"
            ]
        }

        # 2. Template Library: CTAs
        self.ctas = [
            "Save this post for later 🔖",
            "Follow for more viral tips 🚀",
            "Tag a friend who needs to see this 👇",
            "Drop a ❤️ if you agree!",
            "Click the link in bio to learn more 🔗"
        ]

        # 3. Template Library: Hashtags based on Niche
        self.hashtags_map = {
            "Fitness": ["#fitness", "#gym", "#workout", "#fitlife", "#healthylifestyle", "#gains"],
            "Travel": ["#travel", "#wanderlust", "#explore", "#adventure", "#travelgram", "#vacation"],
            "Fashion": ["#fashion", "#ootd", "#styleinspo", "#fashionblogger", "#outfit", "#lookbook"],
            "Tech": ["#tech", "#gadgets", "#innovation", "#coding", "#ai", "#software"],
            "Food": ["#foodie", "#instafood", "#recipe", "#yummy", "#cooking", "#foodstagram"],
            "Lifestyle": ["#lifestyle", "#dailyvibe", "#mindfulness", "#aesthetic", "#homedecor"]
        }

    def generate_hook(self, tone):
        """Generates a strong first line."""
        return random.choice(self.hooks.get(tone, self.hooks["Casual"]))

    def generate_cta(self):
        """Generates a call to action."""
        return random.choice(self.ctas)

    def generate_hashtags(self, niche, keywords="", count=10):
        """Generates a mix of niche and keyword hashtags."""
        base_tags = self.hashtags_map.get(niche, ["#trending", "#viral"])
        
        # Add keyword-based hashtags
        extra_tags = []
        if keywords:
            words = re.findall(r'\w+', keywords.lower())
            extra_tags = [f"#{w}" for w in words]

        combined = list(set(base_tags + extra_tags))
        random.shuffle(combined)
        return " ".join(combined[:count])

    def improve_caption(self, existing_caption):
        """Enhances an existing caption with sentiment and emojis."""
        if not existing_caption:
            return ""

        blob = TextBlob(existing_caption)
        sentiment = blob.sentiment.polarity
        
        improved = existing_caption
        # If sentiment is low, add positive boosters
        if sentiment < 0.2:
            boosters = [" Honestly, it's been a game-changer! ✨", " So grateful for this journey. 🕊️", " Loving every second! ❤️"]
            improved += random.choice(boosters)
        
        # Add engagement phrases
        engagement = [" What do you think? 👇", " Can you relate? 💭", " Let me know in the comments! 🗣️"]
        improved += random.choice(engagement)
        
        return improved

    def generate_caption(self, keywords, niche, tone, post_type, existing_caption=None, style_pref="Balanced"):
        """Full caption generation logic tailored by style preference."""
        hook = self.generate_hook(tone)
        cta = self.generate_cta()
        hashtags = self.generate_hashtags(niche, keywords)
        
        # Style modifiers
        style_mods = {
            "Hype Beast": " 🔥 THIS IS NEXT LEVEL. DON'T BLINK.",
            "Minimalist": " ✨ Clean and simple.",
            "Storyteller": " 📖 Here's a story you won't forget...",
            "Educational": " 🧠 Quick tip for you today.",
            "Balanced": ""
        }
        style_mod = style_mods.get(style_pref, "")

        if existing_caption:
            body = self.improve_caption(existing_caption)
        else:
            # Generate body from keywords
            body = f"Discovering the best of {keywords if keywords else niche} today. {tone} vibes all around! 🌟{style_mod}"
            if post_type == "Reel":
                body += " This reel captures the essence of it perfectly. 🎬"
            elif post_type == "Carousel":
                body += " Swipe left to see the full story! 📸"

        if style_pref == "Minimalist":
            full_caption = f"{hook}\n\n{body}\n\n{hashtags}" # No CTA for minimalist
        elif style_pref == "Storyteller":
            full_caption = f"📖 {hook}\n\n{body}\n\nI've been thinking a lot about this lately, and I wanted to share it with you all. What are your thoughts?\n\n👉 {cta}\n\n{hashtags}"
        else:
            full_caption = f"🔥 {hook}\n\n{body}\n\n👉 {cta}\n\n{hashtags}"
        
        return {
            "full": full_caption,
            "hook": hook,
            "body": body,
            "cta": cta,
            "hashtags": hashtags
        }

