# Documentação de Bibliotecas do Projeto
## 1. Bibliotecas do Flask e Extensões
- - Framework web principal `flask`
- `flask-sqlalchemy` - ORM para banco de dados
- - Utilitários web e WSGI `werkzeug`

## 2. Bibliotecas para Banco de Dados
- `sqlalchemy` - ORM e toolkit SQL
- - Migrações de banco de dados `alembic`
- `psycopg2` - Adaptador PostgreSQL

## 3. Bibliotecas de Requisições e APIs
- `requests` - Cliente HTTP para Python
- `google-ai` - Cliente para API do Google AI (usado no chatbot)

## 4. Bibliotecas de Sistema
- `os` - Operações do sistema operacional
- `datetime` - Manipulação de datas e horários
- `time` - Funções relacionadas a tempo
- `json` - Manipulação de dados JSON

## 5. Bibliotecas de Template
- `jinja2` - Engine de template usado pelo Flask

## 6. Observações
- A biblioteca `google` é utilizada especificamente para o chatbot via API do Google AI
- As bibliotecas estão configuradas usando o gerenciador de pacotes `virtualenv`

Esta documentação reflete apenas as bibliotecas que estão sendo efetivamente importadas e utilizadas no código fonte do projeto, conforme solicitado.
