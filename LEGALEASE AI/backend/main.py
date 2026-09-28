from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .config import APP_NAME, APP_VERSION
    from .routes import router
except ImportError:  # pragma: no cover
    from config import APP_NAME, APP_VERSION
    from routes import router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered legal document generation API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():

    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "message": "LegalEase Backend API is running."
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


app.include_router(router)
