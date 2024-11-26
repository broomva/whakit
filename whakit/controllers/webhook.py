# whakit/controllers/webhook_controller.py

import logging

from fastapi import APIRouter, HTTPException, Request, Response

from whakit.config.settings import settings
from whakit.services.message_handler import BaseMessageHandler, DefaultMessageHandler

logger = logging.getLogger(__name__)

logger.info(f"Logger {logger.name} effective level: {logging.getLevelName(logger.getEffectiveLevel())}")

router = APIRouter()

# Instantiate the default message handler
message_handler: BaseMessageHandler = DefaultMessageHandler()


@router.post("/webhook")
async def handle_incoming(request: Request):
    body = await request.json()
    # Extract message and sender_info from the webhook payload
    message = (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("messages", [{}])[0]
    )
    sender_info = (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("contacts", [{}])[0]
    )
    if message:
        await message_handler.handle_incoming_message(message, sender_info)
    else:
        logger.warning("Received webhook without message.")
    return Response(status_code=200)


@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully.")
        return Response(content=challenge, media_type="text/plain")
    else:
        logger.warning("Webhook verification failed.")
        raise HTTPException(status_code=403)
