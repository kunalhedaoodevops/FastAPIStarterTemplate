from scalar_fastapi import get_scalar_api_reference
from fastapi import APIRouter
from scalar_fastapi import Theme


router = APIRouter(prefix='/docs', tags=['📄 Documentation'])
@router.get("/scalar", include_in_schema=True, summary="Scalar API Modern UI")
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url="/openapi.json",
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",

        # ---- UI CONFIG ----
        theme=Theme.DEEP_SPACE,
        show_sidebar=True,
        hide_client_button=False,
        hide_search=False,
        hide_dark_mode_toggle=False,
        with_default_fonts=True,
        default_open_all_tags=False,
        expand_all_model_sections=False,
        expand_all_responses=False,
        order_required_properties_first=True,

    )