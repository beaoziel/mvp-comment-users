from pydantic import BaseModel
from typing import List
from model.user import User

class UserSchema(BaseModel):
    """ Define como um novo usuario a ser inserido deve ser representado
    """
    name: str = "Maria"
    mail: str = "Maria.empresa@email.com"

class UserSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do usuario.
    """
    name: str = "Maria"

class UserMailSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no email do usuario.
    """
    mail: str = "Maria.empresa@gmail.com"

class ListUsersSchema(BaseModel):
    """ Define como uma listagem de usuarios será retornada.
    """
    name:List[UserSchema]

def show_users(users: List[User]):
    """ Retorna uma representação do usuario seguindo o schema definido em
        UserViewSchema.
    """
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "mail": u.mail
        })

    return {"users": result}

class UsereDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    name: str

class UserViewSchema(BaseModel):
    """ Define como um usuario será retornado: nome + comentários.
    """
    id: int = 1
    name: str = "Maria"
    mail: str = "Maria.empresa@email.com"

def show_user(user: User):
    """ Retorna uma representação do usuario seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": user.id,
        "name": user.name,
        "mail": user.mail
    }

def show_userID(user: User):
    """ Retorna uma representação do usuario seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": user.id
    }