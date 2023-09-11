# from sqlalchemy import Column, String, Integer
# from model import Base

# """
#     Classe Pessoa
#     A classe cria uma representação genérica de uma pessoa, com os campos de nome,
#     cpf e senha. 
#     Cria a tabela de nome pessoa para retenção desses dados no banco.
# """


# class Pessoa(Base):
#     __tablename__ = "pessoa"

#     id = Column("id_pessoa", Integer, primary_key=True)
#     nome = Column("nome", String(60))
#     cpf = Column("cpf", String(15), unique=True, nullable=False)
#     endereco = Column("endereco", String(140))

#     def __init__(self, nome: str, cpf: str, endereco: str) -> None:
#         super().__init__()
#         self.nome = nome
#         self.cpf = cpf
#         self.endereco = endereco

#     def get_cpf(self) -> str:
#         return self.cpf

#     def get_nome(self) -> str:
#         return self.nome

#     def get_endereco(self) -> str:
#         return self.endereco

#     def get_cpf(self) -> None:
#         return self.cpf
    
#     def set_cpf(self, cpf) -> bool:
#         self.cpf = cpf
#         return True

#     def set_nome(self, nome) -> bool:
#         self.nome = nome
#         return True

#     def set_endereco(self, endereco) -> bool:
#         self.endereco = endereco
#         return True
