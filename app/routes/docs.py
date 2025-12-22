from scalar_fastapi import get_scalar_api_reference
from fastapi import APIRouter

router = APIRouter(prefix='/docs', tags=['Docs'])
@router.get("/scalar", include_in_schema=True, summary="Scalar API Reference")
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url="/openapi.json",
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
    )