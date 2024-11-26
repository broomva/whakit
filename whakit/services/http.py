# whakit/services/http_client.py

import logging

import httpx

logger = logging.getLogger(__name__)


class HttpClient:
    async def post(self, url: str, data: dict, headers: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP error: {exc.response.status_code} - {exc.response.text}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
