from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from model.pessoa import Pessoa


"""
    Classe Funcionario.
    Armazena os dados cadastrais específicos da empersa, como: matricula, funcao e login
    Cria a tabela de nome funcionario para retenção desses dados no banco.

    """

class Funcionario(Pessoa):
    __tablename__ = "funcionario"

    id = Column("id_funcionario", Integer, primary_key=True)
    cpf = Column(String(15), ForeignKey("pessoa.cpf"), nullable=False)
    matricula = Column(Integer, unique=True)
    funcao = Column(String(15), nullable=False)
    email = Column(String(25), unique=True, nullable=False)
    login = Column(String(15), unique=True, nullable=False)
    senha = Column(String(15), nullable=False)
    alterar_senha = Column(Boolean, nullable=False)
    cadastrado_por = Column(String(15))

    # tp_funcoes = ("Operador", "Lider", "Supervisor", "Suporte")

    def __init__(
        self,
        nome: str,
        cpf: str,
        endereco: str,
        funcao: str,
        email: str,
        login: str,
        matricula: int,
        cadastrado_por: str,
        alterar_senha: bool,
        senha: str = "123456",
    ) -> None:
        super().__init__(nome, cpf, endereco)
        self.funcao: str = funcao
        self.matricula: Integer = matricula
        self.cadastrado_por = cadastrado_por
        self.alterar_senha: bool = alterar_senha
        self.email: str = email
        self.login: str = login
        self.senha: str = senha
