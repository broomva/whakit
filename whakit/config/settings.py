# whakit/config/settings.py

import logging.config
import os
from typing import Dict, List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    WEBHOOK_VERIFY_TOKEN: str = Field(default=os.environ.get("WEBHOOK_VERIFY_TOKEN", ""), description="Webhook verify token")
    API_TOKEN: str = Field(default=os.environ.get("API_TOKEN", ""), description="API token")
    BUSINESS_PHONE: str = Field(default=os.environ.get("BUSINESS_PHONE", ""), description="Business phone number")
    API_VERSION: str = Field(default="v1", description="API version")
    PORT: int = Field(default=os.environ.get("PORT", 8000), description="Port number")
    BASE_URL: str = Field(default=os.environ.get("BASE_URL", "https://graph.facebook.com"), description="Base URL")
    OPENAI_API_KEY: str = Field(default=os.environ.get("OPENAI_API_KEY", ""), description="OpenAI API key")

    # Customizable settings
    GREETINGS: List[str] = Field(default=["hello", "hi", "hola"], description="List of greetings")
    WELCOME_MESSAGE: str = "Hello {name}, welcome to our service. How can I assist you today?"
    MENU_MESSAGE: str = Field(default="Please choose an option:")
    MENU_BUTTONS: List[Dict] = Field(default=[
        {
            "type": "reply",
            "reply": {"id": "option_1", "title": "Schedule Appointment"}
        },
        {
            "type": "reply",
            "reply": {"id": "option_2", "title": "Ask Assistant"}
        },
        {
            "type": "reply",
            "reply": {"id": "option_3", "title": "Send Location"}
        }
    ])
    # AI Assistant Configuration
    AI_SYSTEM_PROMPT: str = Field(default="You are a helpful assistant.", description="System prompt for the AI assistant")

    # Logging Configuration
    LOGGING_CONFIG: Dict = Field(default_factory=lambda: {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[{asctime}] [{levelname}] {name}: {message}",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "level": "DEBUG",
                "filename": "whakit/logs/app.log",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
        "loggers": {
            "whakit": {
                "level": "DEBUG",
                "propagate": True,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            # ... other loggers ...
        },
    })

    # class Config:
    #     env_file = ".env"

settings = Settings()
