from sqlmodel import create_engine, Session, SQLModel, select
from pathlib import Path
from uuid import UUID
from api.models import Livro

database_path = Path('database.db')
database_url = f'sqlite:///{database_path}'
connect_args = {'check_same_thread': False}

engine = create_engine(database_url , connect_args= connect_args)


def criar_db_tabelas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

livros_default_data = [
    {
        "uuid": UUID('7abb8a2b-4f2d-4d0e-8aaf-32a639954e96'),
        "autor": "George Orwell",
        "titulo": "1984",
        "editora": "Companhia das Letras",
        "ano": 1949
    },
    {
        "uuid": UUID('f8afdc1e-be9a-474b-9a12-607c5c7d8882'),
        "autor": "J. K. Rowling",
        "titulo": "Harry Potter e a Pedra Filosofal",
        "editora": "Rocco",
        "ano": 1997
    }
]


def adicionar_livros_default():
    with Session(engine) as session:

        if not session.exec(select(Livro)).first():
            for data in livros_default_data:
                livro = Livro(
                        uuid = data.get('uuid'),
                        autor = data.get('autor'),
                        titulo = data.get('titulo'),
                        editora = data.get('editora'),
                        ano = data.get('ano')
                )
                session.add(livro)
                session.commit()