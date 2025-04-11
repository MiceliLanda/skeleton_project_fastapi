from fastapi import FastAPI
from middleware import HttpErrorHandler, TokenValidationMiddleware
from controllers import router as api_router
from lifespan import get_lifespan

app = FastAPI(
    title="InitialJwt Services",
    version="0.0.1",
    lifespan=get_lifespan
)

app.add_middleware(HttpErrorHandler)
app.add_middleware(TokenValidationMiddleware)
app.include_router(api_router)