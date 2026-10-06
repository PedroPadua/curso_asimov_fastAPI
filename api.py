from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI(title='API de Livros')

livros_db = {
    1: {
        "uuid": uuid4(),
        "autor": "George Orwell",
        "titulo": "1984",
        "editora": "Companhia das Letras",
        "ano": 1949
    },
    2: {
        "uuid": uuid4(),
        "autor": "J. K. Rowling",
        "titulo": "Harry Potter e a Pedra Filosofal",
        "editora": "Rocco",
        "ano": 1997
    }
}

class Livro(BaseModel):

    uuid: UUID
    autor : str
    titulo: str
    editora : str
    ano : int

class LivroPutPost(BaseModel):

    autor : str
    titulo: str
    editora : str
    ano : int

@app.get('/')
async def root():
    return {'message': 'Biblioteca de Livros'} 


# Método GET - listar livros

@app.get(path="/livros", response_model= list[Livro])
async def listar_livros() -> List[Livro]:
    return [Livro(**dados)for dados in livros_db.values()]


@app.get(path='/livros/{livro_id}', response_model = Livro, responses = {404: {'description': 'Livro não encontrado'}})
async def obter_livro(livro_id:UUID) -> Livro:

    for livro in livros_db.values():
        if livro['uuid'] == livro_id:
            return Livro(**livro)

    raise HTTPException(status_code= 404, detail = 'Livro não encontrado')

@app.post('/livros', response_model= Livro)
async def add_livro(livro: LivroPutPost) ->Livro:

    novo_uuid = uuid4()
    novo_id = max(livros_db.keys()) + 1 if livros_db else 1

    livro_gravado = Livro(
        uuid = novo_uuid,
        autor = livro.autor,
        titulo = livro.titulo,
        editora= livro.editora,
        ano = livro.ano
    )

    livros_db[novo_id] = livro_gravado.model_dump()
    return livro_gravado