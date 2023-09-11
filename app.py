from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Funcionario, Pessoa

from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Cadastro de funcionarios. Autor: Daniel Leite", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Documentação da API com a ferramenta Swagger",
)
funcionario_tag = Tag(
    name="Funcionario",
    description="Adição, visualização e remoção de funcionarios da base",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela de documentação."""
    return redirect("/openapi/swagger#/")


@app.post(
    "/funcionario",
    tags=[funcionario_tag],
    responses={"200": FuncionarioViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_funcionario(form: FuncionarioSchema):
    """Adiciona um novo funcionario à base de dados

    Retorna uma representação dos funcionario, em caso de sucesso, ou uma mensagem de erro, em caso de falha.
    Ao criar um funcionário, o campo senha sempre será preenchido com o valor padrão = "123456" e um flag para
    reset da senha será ligado.
    """

    funcionario = Funcionario(
        cpf=form.cpf,
        funcao=form.funcao,
        email=form.email,
        login=form.login,
        matricula=form.matricula,
    )
    logger.debug(f"Tentativa de adicionar funcionario de cpf: '{funcionario.cpf}'")
    logger.warning(apresenta_funcionario(funcionario))
    try:
        # criando conexão com a base
        session = Session()

        # adicionando produto
        session.add(funcionario)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado funcionario de nome: '{funcionario.cpf}'")
        return apresenta_funcionario(funcionario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Funcionario de mesmo nome já salvo na base :/"
        logger.warning(f"Erro tentar cadastrar: '{funcionario.cpf}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao tentar cadastrar o funcionario: '{funcionario.cpf}', {error_msg}"
        )
        return {"message": error_msg}, 400


@app.get(
    "/funcionarios",
    tags=[funcionario_tag],
    responses={"200": ListagemFuncionariosSchema, "404": ErrorSchema},
)
def get_funcionarios():
    """Faz a busca por todos os funcionarios cadastrados

    Retorna uma representação da listagem de funcionários, em caso de sucesso.
    """

    logger.debug(f"Coletando funcionaros do banco ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionarios = session.query(Funcionario).all()

    if not funcionarios:
        # se não há produtos cadastrados
        return {"funcionarios": []}, 200
    else:
        logger.debug(f"%d funcionarios econtrados" % len(funcionarios))
        # retorna a representação de produto
        print(funcionarios)
        return apresenta_funcionarios(funcionarios), 200


@app.post(
    "/ficha",
    tags=[funcionario_tag],
    responses={"200": FuncionarioViewSchema, "404": ErrorSchema},
)
def get_funcionario(form: FuncionarioBuscaSchema):
    """Realiza a leitura dos dados cadastrais de um dado funcionário

    Utiliza como campo de busca, o login do funcionário
    Retorna os dados do funcionário, em casso de sucesso, ou uma mensagem de erro, em caso de falha,

    """

    logger.debug(f"Validando login do funcionario:  #{form.login}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionario = (
        session.query(Funcionario).filter(Funcionario.login == form.login).first()
    )

    if not funcionario:
        # se o produto não foi encontrado
        error_msg = "Funcionario não encontrado na base :/"
        logger.warning(f"Erro ao buscar login '{form.login}', {error_msg}")
        return {"message": error_msg}, 404

    else:
        # logger.warning(f"Login realizado com sucesso'{form.login}' e senha '{form.senha}', {error_msg}")
        logger.warning(f"Carregando funcionario: '{funcionario.login}'")
        # retorna a representação de produto
        return apresenta_funcionario(funcionario), 200


# @app.get(
#     "/senha",
#     tags=[funcionario_tag],
#     responses={"200": InterfaceParaSenha, "404": ErrorSchema},
# )
# def get_senha(query: FuncionarioBuscaSchema):
#     """Busca a senha do usuario, dado a informacao de login

#     Retorna uma string com a senha do usiario.
#     """

#     funcionario_login = query.login
#     funcionario = busca_por_login(funcionario_login)

#     if not funcionario:
#         # se o produto não foi encontrado
#         error_msg = "Funcionario não encontrado na base :/"
#         logger.warning(f"Erro ao buscar login '{funcionario_login}', {error_msg}")
#         return {"message": error_msg}, 404
#     else:
#         logger.debug(f"Senha: '{funcionario.senha}'")
#         # retorna a representação de produto
#         return apresenta_senha(funcionario), 200


# @app.post(
#     "/login",
#     tags=[funcionario_tag],
#     responses={"200": RetornoLoginValido, "204": RetornoLoginNaoValido},
# )
# def get_login(form: InterfaceParaLogin):
#     """Envia os dados de login e senha do usuário, para validação com a interface.

#     Retorna um dicionário com a informação de login realizado e o status de reset de senha.
#     """

#     logger.debug(f"Validando login do funcionario:  #{form.login}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     funcionario = (
#         session.query(Funcionario)
#         .filter(Funcionario.login == form.login)
#         .filter(Funcionario.senha == form.senha)
#         .first()
#     )

#     if not funcionario:
#         # se o produto não foi encontrado
#         error_msg = "Funcionario não encontrado na base :/"
#         logger.warning(
#             f"Erro ao buscar login '{form.login}' e senha '{form.senha}', {error_msg}"
#         )
#         return {"logado": False, "alterar_senha": funcionario.alterar_senha}, 204

#     else:
#         # logger.warning(f"Login realizado com sucesso'{form.login}' e senha '{form.senha}', {error_msg}")
#         logger.warning(f"Logado: '{funcionario.login}'")
#         # retorna a representação de produto
#         return {"logado": True, "alterar_senha": funcionario.alterar_senha}, 200


# @app.put(
#     "/senha",
#     tags=[funcionario_tag],
#     responses={
#         "200": FuncionarioViewSchema,
#         "404": ErrorSchema,
#         "400": ErrorSchema,
#     },
# )
# def altera_senha(form: FuncionarioSenhaNovaSchema):
#     """Altera a senha de um dado funcioanrio, a partir da informação de login do mesmo.
#       Caso a flag de reset esteja ativa, o senha colocada será a senha padrão '123456'

#     Retorna uma representação dos funcionarios.
#     """

#     funcionario_login = form.login
#     funcionario = busca_por_login(funcionario_login)
#     nova_senha = form.senha
#     if form.alterar_senha:
#         nova_senha = "123456"

#     if not funcionario:
#         # se o produto não foi encontrado
#         error_msg = "Funcionario não encontrado na base :/"
#         logger.warning(f"Erro ao buscar login '{funcionario_login}', {error_msg}")
#         return {"message": error_msg}, 404

#     try:
#         # criando conexão com a base
#         session = Session()
#         session.query(Funcionario).filter(
#             Funcionario.login == funcionario_login
#         ).update(
#             {
#                 Funcionario.senha: nova_senha,
#                 Funcionario.alterar_senha: form.alterar_senha,
#             }
#         )
#         session.commit()
#         logger.debug(f"Alterada a senha do funcionario: '{funcionario.nome}'")
#         return apresenta_funcionario(funcionario), 200

#     except IntegrityError as e:
#         # como a duplicidade do nome é a provável razão do IntegrityError
#         error_msg = "Nao foi possivel alterar a senha do funcionario. Verifique se o campo login está correto.:/"
#         logger.warning(
#             f"Erro ao alterar senha do funcionario: '{funcionario.nome}', {error_msg}"
#         )
#         return {"message": error_msg}, 404

#     except Exception as e:
#         # caso um erro fora do previsto
#         error_msg = "Erro ao atualizar a senha :/"
#         logger.warning(f"Erro ao alterar a senha do '{funcionario.nome}', {error_msg}")
#         return {"message": error_msg}, 400


@app.put(
    "/atualiza",
    tags=[funcionario_tag],
    responses={
        "200": FuncionarioViewSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
    },
)
def altera_dados(form: FuncionarioSchema):
    """Altera os dados cadastrais do funcionário.

    Recebe os dados de funcionário e utiliza o campo login para busca do funcionário.
    
    Para alterar o login, é necessário excluir o cadastro do funcionário e criar um novo.

    Retorna uma representação do funcionario.
    """

    funcionario_login = form.login
    funcionario = busca_por_login(funcionario_login)

    if not funcionario:
        # se o produto não foi encontrado
        error_msg = "Funcionario não encontrado na base :/"
        logger.warning(f"Erro ao buscar login '{funcionario_login}', {error_msg}")
        return {"mesage": error_msg}, 404

    try:
        # Salva o CPF do funcionario para fazer a relaçaõ entra a tebela pessoa e a tabela funcionario
        cpf = funcionario.cpf

        # criando conexão com a base
        session = Session()

        # realiza o reset da senha, se o flag estiver ativo


        session.query(Funcionario).filter(Funcionario.cpf == cpf).update(
            {
                Funcionario.matricula: form.matricula,
                Funcionario.funcao: form.funcao,
                Funcionario.cpf: form.cpf,
                Funcionario.email: form.email,
                Funcionario.login: form.login
                # Funcionario.cadastrado_por: form.cadastrado_por,
                # Funcionario.alterar_senha: form.alterar_senha,
            }
        )

        # session.query(Pessoa).filter(Pessoa.cpf == cpf).update(
        #     {
        #         Pessoa.nome: form.nome,
        #         Pessoa.cpf: form.cpf,
        #         Pessoa.endereco: form.endereco,
        #     }
        # )

        session.commit()

        # Faz uma nova busca no banco para imprimir o resultado atualzado
        funcionario_atualizado = busca_por_login(funcionario_login)
        logger.debug(
            f"Alterados os dados o funcionario: '{funcionario_atualizado.nome}'"
        )
        return apresenta_funcionario(funcionario_atualizado), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi possivel alterar os dados do funcionario. Verifique se o campo login está correto.:/"
        logger.warning(
            f"Erro ao alterar dados do funcionario: '{funcionario.nome}', {error_msg}"
        )
        return {"mesage": error_msg}, 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar os dados do funcionario :/"
        logger.warning(
            f"Erro ao dados do funcionario: '{funcionario.nome}', {error_msg}"
        )
        return {"mesage": error_msg}, 400


@app.delete(
    "/excluir",
    tags=[funcionario_tag],
    responses={
        "200": ErrorSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
    },
)
def exclui_funcionario(query: FuncionarioBuscaSchema):
    """Apaga o funcionario da base de dados

    Utiliza o campo login como filtro para busca do funcionário que será excluído

    Retorna uma mensagem com a confirmação da exclusão ou informação do erro
    """

    funcionario_login = query.login
    funcionario = busca_por_login(funcionario_login)

    if not funcionario:
        # se o produto não foi encontrado
        error_msg = f"Funcionario não encontrado na base: '{query.login}'"
        logger.warning(f"Erro ao buscar login '{funcionario_login}', {error_msg}")
        return {"message": error_msg}, 404

    try:
        # Salva o CPF do funcionario para fazer a relaçaõ entra a tebela pessoa e a tabela funcionario
        cpf = funcionario.cpf
        # criando conexão com a base
        session = Session()

        session.query(Funcionario).filter(Funcionario.cpf == cpf).delete()
        # session.query(Pessoa).filter(Pessoa.cpf == cpf).delete()

        session.commit()

        logger.debug(f"Funcionario excluido com sucesso: '{funcionario.login}'")
        error_msg = f"Funcionario exlcuido com sucesso: '{funcionario.login}'"
        return {"message": error_msg}, 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = (
            "Nao foi excluir o funcionario. Verifique se o campo login está correto.:/"
        )
        logger.warning(
            f"Erro ao excluir o funcionario: '{funcionario.login}', {error_msg}"
        )
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar os dados do funcionario :/"
        logger.warning(
            f"Erro ao dados do funcionario: '{funcionario.login}', {error_msg}"
        )
        return {"message": error_msg}, 400


# Função auxiliar para buscar funcionário
def busca_por_login(login: str) -> Funcionario:
    logger.debug(f"Procurando senha do funcionario de login:  #{login}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionario = session.query(Funcionario).filter(Funcionario.login == login).first()
    return funcionario
