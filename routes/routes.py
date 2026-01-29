from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from models.models import ShortenRequest, ShortenResponse
from service.service import create_short_url, get_long_url
from config.env import settings

url_shortener_routes = APIRouter()


@url_shortener_routes.get("/{url_id}")
async def redirect_url(url_id: str):
    long_url = get_long_url(url_id)

    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url=long_url)


@url_shortener_routes.post("/shorten", response_model=ShortenResponse)
async def shorten_url(request: ShortenRequest):
    long_url = str(request.url)

    url_mapping = create_short_url(long_url)

    return ShortenResponse(
        short_url=f"{settings.BASE_URL}/{url_mapping.url_id}",
        url_id=url_mapping.url_id,
        original_url=url_mapping.long_url
    )