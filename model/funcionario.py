from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from model import Base


"""
    Classe Funcionario.
    Armazena os dados cadastrais específicos da empersa, como: matricula, funcao e login
    Cria a tabela de nome funcionario para retenção desses dados no banco.

    """


class Funcionario(Base):
    __tablename__ = "funcionario"

    id = Column("id_funcionario", Integer, primary_key=True)
    cpf = Column(String(12), unique=True, nullable=False)
    matricula = Column(Integer, unique=True)
    funcao = Column(String(15), nullable=False)
    email = Column(String(25), unique=True, nullable=False)
    login = Column(String(15), unique=True, nullable=False)

    def __init__(
        self,
        cpf: str,
        funcao: str,
        email: str,
        login: str,
        matricula: int,
    ) -> None:
        self.cpf: str = cpf
        self.funcao: str = funcao
        self.email: str = email
        self.login: str = login
        self.matricula: Integer = matricula
