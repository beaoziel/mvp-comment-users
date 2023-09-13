from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, User
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Comment!", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
user_tag = Tag(name="Usuario", description="Adição, visualização e remoção de usuários à base")

def get_duplicates(input:str):
    session = Session()
    list = []
    all = session.query(User).all()

    if input == "name":
        for i in all:
            value = i.name
            list.append(value)
    else:
        for i in all:
            value = i.mail
            list.append(value)

    return list

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#1 Adicionar usuário
@app.post('/user/new', tags=[user_tag],
          responses={"200": UserViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Adiciona um novo Usuário à base de dados

    Retorna uma representação dos usuários associados.
    """
    session = Session()
    names = get_duplicates("name")
    mails = get_duplicates("mail")

    if form.name in names:
        error_msg = "Usuário de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar usuário, {error_msg}")
        return {"mesage": error_msg}, 200
    elif form.mail in mails:
        error_msg = "Email já cadastrado na base :/"
        logger.warning(f"Erro ao adicionar usuário, {error_msg}")
        return {"mesage": error_msg}, 200
    else:
        user = User(
            name=form.name,
            mail=form.mail)
        logger.debug(f"Adicionando um novo usuário: '{user.name}'")
        try:
            session = Session()
            session.add(user)
            session.commit()
            logger.debug(f"Adicionando um novo usuário: '{user.name}'")
            return show_user(user), 200
        
        except IntegrityError as e:
            # como a duplicidade do nome é a provável razão do IntegrityError
            error_msg = "Usuário de mesmo nome já salvo na base :/"
            logger.warning(f"Erro ao adicionar usuário, {error_msg}")
            return {"mesage": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar nova usuário :/"
            logger.warning(f"Erro ao adicionar usuário, {error_msg}")
            return {"mesage": error_msg}, 400

#2 Pegar todos os usuários
@app.get('/user/all', tags=[user_tag],
         responses={"200": ListUsersSchema, "404": ErrorSchema})
def get_all_users():
    """Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da listagem de usuários.
    """
    logger.debug(f"Coletando todos os usuários")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    users = session.query(User).all()

    if not users:
        # se não há produtos cadastrados
        return {"usuários": []}, 200
    else:
        logger.debug(f"%d usuários econtrados" % len(users))
        # retorna a representação de produto
        print(users)
        return show_users(users), 200

#3 Deletar usuário
@app.delete('/user/delete', tags=[user_tag],
            responses={"200": UsereDelSchema, "404": ErrorSchema})
def del_user(query: UserSearchSchema):
    """Deleta um Usuário a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    user_name = unquote(unquote(query.name))
    print(user_name)
    logger.debug(f"Deletando dados sobre o usuário #{user_name}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(User).filter(User.name == user_name).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado usuário #{user_name}")
        return {"mesage": "Usuário deletado", "id": user_name}
    else:
        # se o usuário não foi encontrado
        error_msg = "Usuário não encontrada na base :/"
        logger.warning(f"Erro ao deletar usuário #'{user_name}', {error_msg}")
        return {"mesage": error_msg}, 404

#4 Buscar usuário pelo nome
@app.get('/user/get', tags=[user_tag],
         responses={"200": UserSearchSchema, "404": ErrorSchema})
def get_user(query: UserSearchSchema):
    """Faz a busca por nome do usuário
        Retorna uma representação do usuário
    """
    user_name = unquote(unquote(query.name))
    logger.debug(f"Coletando usuário {user_name}")
    # criando conexão com a base
    session = Session()
    #Fazendo busca geral
    user = session.query(User).filter(User.name == user_name).first()
    if not user:
        return "Nenhum usuário encontrado", 200
    else:
        user = session.query(User).filter(User.name == user_name).first()
        print(user)
        return show_user(user), 200

#5 Atualizar usuário
@app.put('/user/update', tags=[user_tag],
            responses={"200": UserSchema, "404": ErrorSchema})
def update_user(query: UserMailSearchSchema, form: UserSchema):
    """
    Faz update dos valores de um usuário
    """
    user_mail = unquote(unquote(query.mail))
    logger.debug(f"Coletando usuário {user_mail}")
    # criando conexão com a base
    session = Session()
    #Fazendo busca
    user = session.query(User).filter(User.mail == user_mail).first()
    if not user:
        return "Nenhum usuário encontrado", 200
    else:
        names = get_duplicates("name")
        mails = get_duplicates("mail")
        
        if form.name in names and user.mail != form.mail :
                #Verificar se email já existe
                if form.mail in mails:
                    return "Email já utlizado", 200
                else:
                    try:
                        user.mail = form.mail
                        user.name = user.name
                        session.commit()
                        logger.debug(f"Editando usuário: '{user.name}'")
                        return show_user(user), 200

                    except Exception as e:
                        # caso um erro fora do previsto
                        error_msg = "Não foi possível editar usuário :/"
                        logger.warning(f"Erro ao editar usuário, {error_msg}")
                        return {"mesage": error_msg}, 400
        elif form.mail in mails and user.name != form.name :
            #Verificar se nome já existe
            if form.name in names:
                return "Nome já utilizado", 200
            else: 
                 try:
                        user.mail = user.mail
                        user.name = form.name
                        session.commit()
                        logger.debug(f"Editando usuário: '{user.name}'")
                        return show_user(user), 200

                 except Exception as e:
                        # caso um erro fora do previsto
                        error_msg = "Não foi possível rditar usuário :/"
                        logger.warning(f"Erro ao editar usuário, {error_msg}")
                        return {"mesage": error_msg}, 400
        else:
                # caso um erro fora do previsto
                error_msg = "Não foi possível rditar usuário :/"
                logger.warning(f"Erro ao editar usuário, {error_msg}")
                return {"mesage": error_msg}, 400

#6 Pegar ID do usuário 
@app.get('/user/getID', tags=[user_tag],
         responses={"200": UserSearchSchema, "404": ErrorSchema})
def get_user_ID(query: UserSearchSchema):
    """Faz a busca por nome do usuário
        Retorna uma representação do usuário
    """
    user_name = unquote(unquote(query.name))
    logger.debug(f"Coletando usuário {user_name}")
    # criando conexão com a base
    session = Session()
    #Fazendo busca geral
    stmt=(f'SELECT pk_user FROM users WHERE name = "{user_name}"')
    user = session.execute(stmt)
    if not user:
        return "Nenhum usuário encontrado", 200
    else:
        user = session.query(User).filter(User.name == user_name).first()
        print(user)
        return show_userID(user), 200

    
    