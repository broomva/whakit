# whakit/main.py

import logging
import logging.config

import uvicorn
from fastapi import FastAPI

from whakit.config.settings import settings
from whakit.routes.webhook import router as webhook_router


def setup_logging():
    # Configure logging
    logging.config.dictConfig(settings.LOGGING_CONFIG)

# Call the setup_logging function before creating the app
setup_logging()

logger = logging.getLogger(__name__)
logger.info("Starting WhaKit application.")

app = FastAPI()
app.include_router(webhook_router)


@app.get("/")
async def root():
    return {"message": "Nothing to see here. Checkout README.md to start."}


if __name__ == "__main__":
    uvicorn.run("whakit.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
