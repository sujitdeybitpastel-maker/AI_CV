from load_env import *
import os
from openai import OpenAI

class OpenAIClient:

    @staticmethod
    def generate_text(prompt: str) -> str:

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise Exception("❌ OPENAI_API_KEY is missing. Check env/.env")

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content
    def generate_cv_link(prompt: str) -> str:

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise Exception("❌ OPENAI_API_KEY is missing. Check env/.env")

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content
