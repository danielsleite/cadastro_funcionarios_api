# API para cadastro de funcionários

Esse projeto apresenta o MVP de requisido para conclusão da sprint 3 da curso de  **Engenharia de Softaware**  oferecido pela **PUC-Rio**

Para tal, foi criado uma API em python, utilizando como base as bibliotecas flask e sqlalchemy. 

Essa API tem como objetivo prover ferramentas para criação de um sistema de cadastro de funcionário, cadastrando dados relaciodados à empresa, como: e-mail, função, login e matrícula.

Essa API, interga com a [api_login](https://github.com/danielsleite/api_login) e [API Cadastro Pessoas](https://github.com/danielsleite/api_cadastro_pessoas), para obter o compilado de todos os dados de um determinado funcionário que a empresa possui.

Para interação da API com o banco e front-end, foram criadas diversas rodas, entre elas:


>**/funcionario** - para incluir un novo funcionário

>**/funcionarios** - para obter uma lista com os dados de cada funcionário

>**/ficha** - para obter os dados de cadastro de um dado funcionário

>**/ficha_completa** - para obter os dados do funcionário salvos por essas api e pelas APIs [api_login](https://github.com/danielsleite/api_login) e [API Cadastro Pessoas](https://github.com/danielsleite/api_cadastro_pessoas

>**/excluir** - para apagar um funcionário

>**/atualiza** - para alterar algum campo dos dados do funcionario

---
## Banco

Para realizar a rentenção dos dados, a API cria um banco .sqlite3, caso o mesmo não exista. O banco criado possui a seguinte tabela:

* `funcionario`, que armazenda dados referentes à empresa (matricula, login, email, funcao,...). 

Os demais dados do funcionário, como dados de login e senha e dados pessoais, são gerenciados pelas APIs [api_login](https://github.com/danielsleite/api_login) e [API Cadastro Pessoas](https://github.com/danielsleite/api_cadastro_pessoas), contudo, a api cadastro de funcionário, se conecta as demais para realizar a leitura completa, através da rota \ficha_completa

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5002
```

Abra o [http://localhost:5002/#/](http://localhost:5002/#/) no navegador para verificar o status da API em execução nas três vesões disponíveis (Sswagger, ReDoc, RapiDoc).

Para versão `Swagger` abra o link [http://localhost:5002/openapi/swagger#/](http://localhost:5002/openapi/swagger#/) no navegador

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t api-cadastro-funcionarios .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5002:5002 api-cadastro-funcionarios
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5002/#/](http://localhost:5002/#/) no navegador.
