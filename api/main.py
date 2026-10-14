from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.database import criar_db_tabelas, adicionar_livros_default
from api.routers import livros_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    criar_db_tabelas()
    adicionar_livros_default()
    yield

app = FastAPI(title = 'API de livros', lifespan = lifespan)

app.include_router(livros_router.router)