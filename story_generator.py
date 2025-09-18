import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set. Please set it in your environment or .env.")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # default to a supported model

    def generate_story(self, name: str, age: int, genre: str) -> str:
        prompt = (
            f"Write a short, engaging bedtime story for a {age}-year-old child named {name}. "
            f"The story should be in the {genre} genre, written in simple, friendly language, "
            f"and should end with a positive, calming message for bedtime."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a friendly  story generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=300
        )

        return response.choices[0].message.content.strip()
