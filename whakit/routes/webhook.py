# whakit/routes/webhook_routes.py

from fastapi import APIRouter

from whakit.controllers.webhook import router as webhook_router

router = APIRouter()
router.include_router(webhook_router)
