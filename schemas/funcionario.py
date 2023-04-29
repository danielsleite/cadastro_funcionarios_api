from pydantic import BaseModel
from typing import Optional, List
from model import Funcionario


class FuncionarioSchema(BaseModel):
    """Define como um novo funcionario a ser inserido deve ser representado"""

    nome: str = "Joao da Silva"
    cpf: str = "123456789-10"
    endereco: str = "Rua Alguma coisa, 22 Baixo: Qualquer Cidade: Alguma"
    funcao: str = "Operador"
    matricula: int = 12345
    email: str = "joao.silva@empresa.com"
    login: str = "jsilva"
    alterar_senha: bool = True
    cadastrado_por: str = "Admin"


class FuncionarioBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca do funcinário.
    
    A busca é feita baseada no login do funcionario
    """

    login: str = "jsilva"


class FuncionarioSenhaNovaSchema(BaseModel):
    """Define a estrutura para envio de uma nova senha. 
    Além do usuário, para a busca, e a senha para a atualização, também é enviado o flag de reset.
    Caso o flag de reset seja verdadeiro, o valor da senha padrão = "123456", é utlizado, no lugar 
    do valor do campo senha
    
    """

    login: str = "jsilva"
    senha: str = "******"
    alterar_senha: bool = False


class ListagemFuncionariosSchema(BaseModel):
    """Define como uma listagem de produtos será retornada."""

    funcionarios: List[FuncionarioSchema]


class InterfaceParaSenha(BaseModel):
    """Define como o retorno da consulta de senha do funcionario ocorre."""

    senha: str = "******"


class InterfaceParaLogin(BaseModel):
    """Define como o formado do envio do dado para login."""

    login: str = "jsilva"
    senha: str = "123456"


class RetornoLoginValido(BaseModel):
    """
    Retorna o status de login do usuário, após validação do login e senha no banco
    """

    logado: bool = True
    alterar_senha: bool = False


class RetornoLoginNaoValido(BaseModel):
    """
    Retorna o status de login do usuário, após validação do login e senha no banco
    """

    logado: bool = False
    alterar_senha: bool = False


class FuncionarioViewSchema(BaseModel):
    """Define como um funcinário será retornado"""

    nome: str = "Joao da Silva"
    cpf: str = "123456789-10"
    endereco: str = "Rua Alguma coisa, 22 Baixo: Qualquer Cidade: Alguma"
    funcao: str = "Operador"
    matricula: int = 12345
    email: str = "joao.silva@empresa.com"
    login: str = "jsilva"
    senha: str = "*******"
    alterar_senha: bool = True
    cadastrado_por: str = "Admin"


def apresenta_funcionarios(funcionarios: List[Funcionario]):
    """Retorna um dicionario com todos os funcionarios cadastrados no banco e seus respectivos capos."""
    result = []

    for funcionario in funcionarios:
        result.append(apresenta_funcionario(funcionario))

    return {"funcionarios": result}


def apresenta_funcionario(funcionario: Funcionario):
    """Retorna os campos que representam o funcionaro."""
    return {
        "nome": funcionario.nome,
        "cpf": funcionario.cpf,
        "endereco": funcionario.endereco,
        "funcao": funcionario.funcao,
        "matricula": funcionario.matricula,
        "email": funcionario.email,
        "login": funcionario.login,
        "cadastrato_por": funcionario.cadastrado_por,
        "alterar_senha": funcionario.alterar_senha,
    }


def apresenta_senha(funcionario: Funcionario):
    """Retorna uma string com a senha do usuario

    Args:
        funcionario (Funcionario): objeto funcionaro obtido pela query
    """

    return {
        "senha": funcionario.senha,
    }
