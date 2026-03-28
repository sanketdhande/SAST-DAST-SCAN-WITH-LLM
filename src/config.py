"""Configuration module for DevSecOps LLM integration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
