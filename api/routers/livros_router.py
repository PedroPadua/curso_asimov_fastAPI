from fastapi import APIRouter, Depends
from api.models import Livro, LivroResposta
from sqlmodel import Session, select
from api.database import get_session
from typing import Annotated

router = APIRouter(prefix = '/livros', tags = ['livros'])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get(path = '/', response_model = list[LivroResposta])
async def listar_livros(session: SessionDep) -> list[LivroResposta]:
    livros =  session.exec(select(Livro)).all()

    return [LivroResposta.model_validate(livro) for livro in livros]
