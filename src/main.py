from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from constants import project_constants as project
import logging
logger = logging.getLogger(__name__)

app = FastAPI()


@asynccontextmanager
async def lifespan_event(app: FastAPI):
    logger.info("Application startup")
    yield
    app.state.prompt_manager = None
    logger.info("Application shutdown")

app.router.lifespan_context = lifespan_event

def create_app() -> FastAPI:
    from src.routers import eval, chat

    app = FastAPI(
        title=project.PROJECT_NAME,
        version=project.API_VERSION,
        docs_url=f"{project.RAG_API_BASE_URL}/docs",
        lifespan=lifespan_event
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(eval.router)
    app.include_router(chat.router)
    return app


app = create_app()

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "server is up and running..."}