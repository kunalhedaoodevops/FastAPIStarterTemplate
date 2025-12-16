from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from starlette_exporter import handle_metrics

router = APIRouter(prefix='/health', tags=['health'])

@router.get('/', response_class=JSONResponse)
async def health_check():
    # Perform checks (e.g., database connection, external services)
    all_systems_operational = True
    if all_systems_operational:
        return JSONResponse(content={"status": "healthy"}, status_code=200)
    else:
        return JSONResponse(content={"status": "unhealthy"}, status_code=503)

# Prometheus metrics under /health/metrics
@router.get('/metrics', include_in_schema=True)
def metrics(request: Request):
    return handle_metrics(request)