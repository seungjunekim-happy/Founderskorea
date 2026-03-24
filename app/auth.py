import json
from fastapi import Header, HTTPException
from app.config import settings


def _parse_api_keys() -> dict[str, str]:
    """Parse ARTICLE_API_KEYS setting. Format: JSON {"name": "secret"}"""
    try:
        return json.loads(settings.ARTICLE_API_KEYS)
    except (json.JSONDecodeError, TypeError):
        return {}


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Verify API key and return the key name for audit."""
    keys = _parse_api_keys()
    for name, secret in keys.items():
        if secret == x_api_key:
            return name
    raise HTTPException(status_code=401, detail="Invalid API key")
