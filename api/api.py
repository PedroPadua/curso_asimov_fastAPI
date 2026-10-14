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


class LivroPatch(BaseModel):

    autor : Optional[str] = None
    titulo: Optional[str] = None
    editora : Optional[str] = None
    ano : Optional[int] = None


class ConfirmaDelete(BaseModel):
    msg = str
    uuid : UUID

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


@app.put('/livros/{livro_id}', response_model=Livro, responses={404:{'description': 'Livro não encontrado.'}})
async def atualizar_livro(livro_id: UUID, livro_update: LivroPutPost) -> Livro:

    for index, livro in livros_db.items():
        if livro['uuid'] == livro_id:
            livros_db[index] = dict(
                uuid = livro_id,
                autor = livro_update.autor,
                titulo = livro_update.titulo,
                editora = livro_update.editora,
                ano = livro_update.ano
            )

            return Livro(**livros_db[index])

    raise HTTPException(status_code = 404, detail = 'Livro não encontrado.')


@app.patch('/Livros/{livro_id}', responde_model = Livro, 
           response = {404 : {'description': 'Livro não encontrado!'}})
async def atualizar_parcial(livro_id:UUID, livro_update: LivroPatch) -> Livro:
        for index, livro in livros_db.items():
            if livro['uuid'] == livro_id:
                for key, value in livro_update.model_dump(exclude_defaults= True).items():
                    livro[key] = value
            return Livro(**livros_db[index])

        raise HTTPException(status_code = 404, detail = 'Livro não encontrado.')

@app.delete('/Livros/{livro_id}', responde_model = Livro, response = {404 : {'description': 'Livro não encontrado!'}})
async def delete_livro(livro_id:UUID) -> ConfirmaDelete:

        for index, livro in livros_db.items():
            if livro['uuid'] == livro_id:
                del livros_db[index]

                return ConfirmaDelete(msg = f'Livro {livro_id} deletado.',uuid = livro_id) 

            raise HTTPException(status_code = 404, detail = 'Livro não encontrado.')