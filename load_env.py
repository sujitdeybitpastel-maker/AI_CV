import os
from pathlib import Path
from dotenv import load_dotenv

# Get absolute project root path
ROOT_DIR = Path(__file__).resolve().parent

# Construct env path
ENV_PATH = ROOT_DIR / "env" / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    raise FileNotFoundError(f" Could not find .env file at: {ENV_PATH}")
