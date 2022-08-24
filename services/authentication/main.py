from fastapi import FastAPI, Depends,Response,Request
from functools import lru_cache
from pythonjsonlogger import jsonlogger
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import pendulum

# in-built
import json
from uuid import uuid4

from api.api_v1.api import api_router
from core.config import PROJECT_NAME, API_V1_STR, logger, TZ

app = FastAPI(title=PROJECT_NAME)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=API_V1_STR)
handler = Mangum(app, enable_lifespan=False)

@app.middleware("http")
async def log_http_request_attributes(request: Request, call_next):
    received_at = pendulum.now(tz=TZ)
    request_id = uuid4().hex
    request.state.__setattr__("x_request_id", request_id)
    response = await call_next(request)
    responded_at = pendulum.now(tz=TZ)
    response.headers["request-id"] = request_id
    response_time = responded_at - received_at
    response_time_ms = response_time._to_microseconds() / 1000
    response.headers["X-Process-Time"] = f'{response_time_ms} ms'

    content = b''
    async for chunk in response.body_iterator:
        content += chunk

    response_data = json.loads(content)

    request_attrs = {
            'request': {
                'request_id': request_id,
                "method": request.method,
                "path": request.url.path,
                'params': dict(request.query_params),
                'headers': dict(request.headers),
                'origin': request.client.host,
                'port': request.client.port,
                'received_at': received_at.to_iso8601_string(),
            },
            'response': {
                'responded_at': responded_at.to_iso8601_string(),
                'response_time_ms': response_time_ms,
                'response_time_sec': response_time.total_seconds(),
                'response_status': response.status_code,
                'response_headers': dict(response.headers),
                'response_media_type': response.media_type,
                'response_background': response.background,
                'data': response_data
            }
        }
    all_attrs = {'log_type': 'request', 'context': request_attrs}
    logger.info('Responded', extra=all_attrs)
    return Response(
        content=content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
