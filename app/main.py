import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.core.scheduler import setup_scheduler, scheduler, groq_service, telegram_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Lifecycle
    logger.info("Starting Ayno Assistant background services...")
    app_scheduler = setup_scheduler()
    app_scheduler.start()
    yield
    # Shutdown Lifecycle
    logger.info("Shutting down background services...")
    app_scheduler.shutdown(wait=False)

app = FastAPI(title="Ayno Assistant", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": "Ayno Assistant"})

@app.get("/health")
async def health_check():
    groq_ok = await groq_service.check_health()
    telegram_ok = await telegram_service.check_health()
    scheduler_running = scheduler.running

    status_ok = groq_ok and telegram_ok and scheduler_running

    return {
        "status": "ok" if status_ok else "degraded",
        "app": "Ayno Assistant",
        "telegram": telegram_ok,
        "groq": groq_ok,
        "scheduler": scheduler_running
    }
