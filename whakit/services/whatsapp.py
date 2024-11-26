# whakit/services/whatsapp_service.py

import logging

import httpx

from whakit.config.settings import settings

logger = logging.getLogger(__name__)


class WhatsAppService:
    def __init__(self):
        self.base_url = f"{settings.BASE_URL}/{settings.API_VERSION}/{settings.BUSINESS_PHONE}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.API_TOKEN}",
            "Content-Type": "application/json",
        }

    async def send_message(self, to: str, body: str):
        data = {"messaging_product": "whatsapp", "to": to, "text": {"body": body}}
        await self._send_request(data)

    async def send_interactive_message(self, to: str, body_text: str, buttons: list):
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": buttons},
            },
        }
        await self._send_request(data)

    async def send_media_message(
        self,
        to: str,
        media_type: str,
        media_url: str,
        caption: str = None,
        filename: str = None,
    ):
        media_object = {}
        if media_type == "image":
            media_object["image"] = {"link": media_url, "caption": caption}
        elif media_type == "audio":
            media_object["audio"] = {"link": media_url}
        elif media_type == "video":
            media_object["video"] = {"link": media_url, "caption": caption}
        elif media_type == "document":
            media_object["document"] = {
                "link": media_url,
                "caption": caption,
                "filename": filename,
            }
        else:
            raise ValueError("Unsupported media type")

        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": media_type,
            **media_object,
        }
        await self._send_request(data)

    async def send_contact_message(self, to: str, contact: dict):
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "contacts",
            "contacts": [contact],
        }
        await self._send_request(data)

    async def send_location_message(
        self, to: str, latitude: float, longitude: float, name: str, address: str
    ):
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "location",
            "location": {
                "latitude": str(latitude),
                "longitude": str(longitude),
                "name": name,
                "address": address,
            },
        }
        await self._send_request(data)

    async def mark_as_read(self, message_id: str):
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        await self._send_request(data)

    async def _send_request(self, data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url, json=data, headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Message sent successfully: {data}")
        except httpx.HTTPStatusError as exc:
            print(f"Error sending message: {exc.response.status_code} - {exc.response.text}")
            logger.error(
                f"Error sending message: {exc.response.status_code} - {exc.response.text}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
