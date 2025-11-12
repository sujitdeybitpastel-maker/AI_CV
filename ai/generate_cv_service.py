
from .openai_client import OpenAIClient
# from .gemini_client import GeminiClient
# from .claude_client import ClaudeClient

# services/cv_ai_service.py
from pathlib import Path
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import os, re

ROOT_DIR = Path(__file__).resolve().parent.parent  # project_root
PROMPT_DIR = ROOT_DIR / "prompts"

# PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(filename):
    """Load prompt template from prompts folder."""
    file_path = PROMPT_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def fill_prompt(template: str, context: dict) -> str:
    """Replace {{variables}} inside the prompt."""
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template


def generate_summary(provider: str, user_data: dict) -> str:
    """
    Generate professional summary using selected AI model.

    provider: "openai"
    user_data: dictionary with full_name, job_role, years_experience, skills , project_name
    """

    # 1. Load prompt
    base_prompt = load_prompt("cv_prompt.txt")

    # 2. Fill prompt with user data
    final_prompt = fill_prompt(base_prompt, user_data)

    # 3. Select AI provider
    if provider == "openai":
        response_text = OpenAIClient.generate_text(final_prompt)

    # elif provider == "gemini":
    #     response_text = GeminiClient.generate_text(final_prompt)

    # elif provider == "claude":
    #     response_text = ClaudeClient.generate_text(final_prompt)

    else:
        raise ValueError("Invalid provider. Use: openai, gemini, claude")

    # 4. Clean and return AI output
    return response_text.strip()



def generate_cv_pdf(provider: str, project_data: dict) -> dict:
    """
    Generate AI-enhanced CV text and create a real downloadable PDF on the server.
    Returns a dict with { "link": <absolute_download_url> }.
    """
    base_prompt = load_prompt("cv_pdf_prompt.txt")
    final_prompt = fill_prompt(base_prompt, project_data)

    # STEP 1 — get CV text
    if provider == "openai":
        response_text = OpenAIClient.generate_cv_link(final_prompt)
    # elif provider == "gemini":
    #     response_text = GeminiClient.generate_text(final_prompt)
    else:
        raise ValueError("Invalid provider. Use: openai or gemini")

    # Remove any sandbox references
    clean_text = re.sub(r"\[Download.*?\]\(sandbox:[^)]+\)", "", response_text).strip()

    # STEP 2 — make a real PDF
    filename = f"{project_data['full_name'].replace(' ', '_')}_CV.pdf"
    media_dir = Path(settings.MEDIA_ROOT)
    media_dir.mkdir(exist_ok=True)
    pdf_path = media_dir / filename

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    story = []
    for line in clean_text.split("\n"):
        if line.strip():
            story.append(Paragraph(line.strip(), styles["Normal"]))
            story.append(Spacer(1, 8))
    doc.build(story)

    # STEP 3 — build public URL for download
    download_url = os.path.join(settings.MEDIA_URL, filename)
    full_link = f"{settings.SITE_URL.rstrip('/')}{download_url}"

    return {"link": full_link}

