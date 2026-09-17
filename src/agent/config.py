import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-large-latest")
    SIMULATED_NOW: str = os.getenv("SIMULATED_NOW", "2026-09-24T17:00:00")

config = Config()