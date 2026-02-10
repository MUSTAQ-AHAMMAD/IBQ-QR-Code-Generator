"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import qr_routes
from app.config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready QR code generator for business cards",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(qr_routes.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with QR code generator UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/info")
async def get_api_info():
    """Get API information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "QR Code Generator API for Business Cards",
        "endpoints": {
            "generate": "/api/v1/generate",
            "generate_with_logo": "/api/v1/generate-with-logo",
            "download": "/api/v1/download/{filename}",
            "batch_generate": "/api/v1/batch-generate",
            "health": "/api/v1/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
