from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Funcionario

import requests, json, os

from logger import logger
from schemas import *
from flask_cors import CORS


if os.getenv("DOCKER_ENV") == "true":
    HOST_LOGIN = "api_login_ip"
    HOST_PESSOA = "api_pessoas_ip"
    print("\nHost login docker")
else:
    HOST_LOGIN = "127.0.0.1"
    HOST_PESSOA = "127.0.0.1"
    print("\nHost local")


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
        error_msg = "Funcionario de mesmo nome já salvo na base"
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
    """Realiza a leitura dos dados cadastrais de um dado funcionário, apenas dados da tabela funcionário

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


@app.post(
    "/ficha_completa",
    tags=[funcionario_tag],
    responses={"200": FuncionarioCompletoViewSchema, "404": ErrorSchema},
)
def get_funcionario_completo(form: FuncionarioBuscaSchema):
    """Realiza a leitura dos dados cadastrais de um dado funcionário.

    Se conecta a API pessoas, para fazer a busca dos dados pessoais do funcionário

     Utiliza como campo de busca, o login do funcionário
     Retorna os dados do funcionário + dados pessoais, em casso de sucesso, ou uma mensagem de erro, em caso de falha,

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
        url_pessoa = f"http://{HOST_PESSOA}:5001/pessoa?cpf={funcionario.cpf}"
        logger.warning("Fazendo busca por dados pessoais: " + url_pessoa)
        response = requests.get(url_pessoa)
        if response.status_code == 200:
            pessoa = json.loads(response.text)

            url_login = f"http://{HOST_LOGIN}:5000/login"
            formdata = {"login": funcionario.login}
            r_post = requests.post(url_login, json=formdata)

            if r_post.status_code == 200:
                login = json.loads(r_post.text)
                # logger.warning(f"Login realizado com sucesso'{form.login}' e senha '{form.senha}', {error_msg}")
                logger.warning(f"Carregando funcionario: '{funcionario.login}'")

                logger.warning(f"\n\\ Campo Login buscado: '{login}'")

                return apresenta_funcionario_completo(funcionario, pessoa, login), 200
            else:
                error_msg = "Não foi possível buscar a base de login do funcionario:/"
                return {"message": error_msg}, 404
        else:
            error_msg = "Não foi possível buscar a base de dados pessoais:/"
            return {"message": error_msg}, 404


@app.put(
    "/atualiza",
    tags=[funcionario_tag],
    responses={
        "200": FuncionarioViewSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
    },
)
def altera_dados(query: FuncionarioBuscaCpfSchema, form: FuncionarioSchema):
    """Altera os dados cadastrais do funcionário.

    Recebe os dados de funcionário e utiliza o campo login para busca do funcionário.

    Para alterar o login, é necessário excluir o cadastro do funcionário e criar um novo.

    Retorna uma representação do funcionario.
    """

    funcionario_cpf = query.cpf
    funcionario = busca_por_cpf(funcionario_cpf)

    if not funcionario:
        # se o produto não foi encontrado
        error_msg = "Funcionario não encontrado na base"
        logger.warning(f"Erro ao buscar cpf '{funcionario_cpf}', {error_msg}")
        return {"mesage": error_msg}, 404

    try:
        # criando conexão com a base
        session = Session()

        # realiza o reset da senha, se o flag estiver ativo

        session.query(Funcionario).filter(Funcionario.cpf == funcionario_cpf).update(
            {
                Funcionario.matricula: form.matricula,
                Funcionario.funcao: form.funcao,
                Funcionario.email: form.email,
                Funcionario.login: form.login,
            }
        )

        session.commit()

        # Faz uma nova busca no banco para imprimir o resultado atualzado
        funcionario_atualizado = busca_por_cpf(funcionario_cpf)
        logger.debug(
            f"Alterados os dados o funcionario: '{funcionario_atualizado.login}'"
        )
        return apresenta_funcionario(funcionario_atualizado), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi possivel alterar os dados do funcionario. Verifique se o campo login está correto.:/"
        logger.warning(
            f"Erro ao alterar dados do funcionario: '{funcionario.cpf}', {error_msg}"
        )
        return {"mesage": error_msg}, 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar os dados do funcionario :/"
        logger.warning(
            f"Erro ao dados do funcionario: '{funcionario.cpf}', {error_msg}"
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
    logger.debug(f"Procurando funcionario de login:  #{login}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionario = session.query(Funcionario).filter(Funcionario.login == login).first()
    return funcionario


# Função auxiliar para buscar funcionário
def busca_por_cpf(cpf: str) -> Funcionario:
    logger.debug(f"Procurando funcionário de cpf:  #{cpf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionario = session.query(Funcionario).filter(Funcionario.cpf == cpf).first()
    return funcionario
