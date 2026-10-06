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

@app.get('/')
async def root():
    return {'message': 'Biblioteca de Livros'} 


# Método GET - listar livros

@app.get(path="/livros", response_model= list[Livro])
async def listar_livros():
    return [Livro(**dados)for dados in livros_db.values()]