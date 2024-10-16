import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from redis import asyncio as aioredis

from infrastructure.api_services.common.cors import setup_cors
from infrastructure.database import setup as database
from tg_api.src import settings
from tg_api.src.tgusers.api.v1.user import router as tg_user_router


@asynccontextmanager
async def lifespan(App: FastAPI):  # noqa
    database.redis = aioredis.from_url(settings.redis.dsn, encoding="utf-8")
    await FastAPILimiter.init(database.redis)
    FastAPICache.init(RedisBackend(database.redis), prefix="fastapi-cache")
    database.init_database(settings)
    logging.info("Application initialized")
    yield
    await database.redis.close()
    await FastAPILimiter.close()


app = FastAPI(
    lifespan=lifespan,
    title="Users API",
    description="API для выполнения операций с пользователями.",
    docs_url="/tg/api/openapi",
    openapi_url="/tg/api/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.service.app_version,
)


@app.get("/tg/ping")
async def pong() -> dict[str, str]:
    return {"ping": "pong!"}


@app.get("/tg/version")
@cache(expire=600)
def get_version() -> dict[str, str]:
    return {"version": settings.service.app_version}


app.include_router(tg_user_router, prefix="/tg/api/v1/users", tags=["Users"])

setup_cors(app, settings)
add_pagination(app)
