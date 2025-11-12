# from load_env import *
# import os
# from google import genai

# class GeminiClient:

#     @staticmethod
#     def generate_text(prompt: str) -> str:

#         api_key = os.getenv("GEMINI_API_KEY")
#         if not api_key:
#             raise Exception("❌ GEMINI_API_KEY missing in env/.env")

#         client = genai.Client(api_key=api_key)

#         response = client.models.generate_content(
#             model="gemini-1.5-flash",   # ✅ CORRECT MODEL
#             contents=prompt
#         )

#         return response.text
