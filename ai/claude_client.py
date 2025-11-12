# import os
# import anthropic

# client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

# class ClaudeClient:

#     @staticmethod
#     def generate_text(prompt: str) -> str:
#         response = client.messages.create(
#             model="claude-3-haiku-20240307",
#             max_tokens=300,
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return response.content[0].text
