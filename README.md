# Documentação do Projeto
## 1. Visão Geral do Projeto
Este é um sistema web desenvolvido em Python/Flask para gerenciar fãs de eSports, com foco especial em análise de engajamento em redes sociais e recomendações personalizadas.
## 2. Estrutura do Projeto
``` 
/
├── app.py                 # Aplicação principal
├── buscaDadosTwitter.py  # Módulo de integração com Twitter
├── chat_bot.py           # Módulo do chatbot
├── database.py           # Configurações do banco de dados
├── ai_processing.py      # Processamento de IA
├── routes.py             # Rotas da aplicação
├── static/              # Arquivos estáticos
│   └── uploads/         # Pasta para uploads
└── templates/           # Templates HTML
```
## 3. Componentes Principais
### 3.1. Sistema de Cadastro () `app.py`
- Coleta informações pessoais dos usuários
- Gerencia upload de documentos
- Armazena preferências de jogos
- Integração com redes sociais

### 3.2. Análise de Twitter () `buscaDadosTwitter.py`
- Busca perfil do usuário
- Coleta tweets recentes
- Análise de menções à FURIA
- Cálculo de score de engajamento

### 3.3. Chatbot () `chat_bot.py`
- Integração com Google AI
- Processamento de mensagens
- Respostas automatizadas

### 3.4. Sistema de Recomendações
- Baseado em jogos favoritos
- Análise de sentimentos
- Score de engajamento
- Recomendações personalizadas

## 4. Funcionalidades
### 4.1. Gestão de Usuários
- Cadastro de informações pessoais
- Upload de documentos de identificação
- Gerenciamento de endereços
- Preferências de jogos

### 4.2. Integração Social
- Conexão com perfil do Twitter
- Análise de engajamento
- Monitoramento de menções
- Score de interação

### 4.3. Dashboard
- Visualização de dados do usuário
- Métricas de engajamento
- Histórico de interações
- Recomendações ativas

### 4.4. Sistema de Chat
- Atendimento automatizado
- Respostas contextuais
- Integração com IA

## 5. Rotas da Aplicação
### 5.1. Rotas Principais
- `/` - Formulário principal
- `/submit_form` - Envio de dados
- `/thank_you` - Confirmação
- `/dashboard` - Painel do usuário
- `/chatbot` - Interface do chat

### 5.2. Rotas de API
- `/dashboard/data` - Dados do usuário
- `/chatbot/send` - Endpoint do chatbot

## 6. Banco de Dados
### 6.1. Tabelas Principais
- `users` - Dados dos usuários
- `documents` - Documentos enviados
- `interactions` - Histórico de interações

## 7. Integrações
### 7.1. Twitter API
- Autenticação via Bearer Token
- Coleta de dados do perfil
- Análise de tweets
- Métricas de engajamento

### 7.2. Google AI
- Integração para chatbot
- Processamento de linguagem natural

## 8. Segurança
### 8.1. Uploads
- Validação de tipos de arquivo
- Limite de tamanho (16MB)
- Nomes de arquivo seguros

### 8.2. Dados
- Proteção de rotas
- Validação de entradas
- Sanitização de dados

## 9. Tratamento de Erros
### 9.1. Erros HTTP
- 404 - Página não encontrada
- 413 - Arquivo muito grande
- 500 - Erro interno

### 9.2. Logs
- Registro de erros
- Monitoramento de falhas
- Debug em desenvolvimento

## 10. Configurações do Ambiente
### 10.1. Requisitos
- Python 3.13.3
- Virtualenv
- PostgreSQL

### 10.2. Variáveis de Ambiente
- Chaves de API
- Configurações de banco
- Tokens de acesso

## 11. Processamento de Dados
### 11.1. Análise de Sentimentos
- Processamento de tweets
- Classificação de conteúdo
- Cálculo de scores

### 11.2. Recomendações
- Baseadas em preferências
- Análise de comportamento
- Personalização de conteúdo

## 12. Manutenção
### 12.1. Backups
- Dados do usuário
- Documentos enviados
- Logs do sistema

### 12.2. Monitoramento
- Performance da aplicação
- Uso de APIs
- Erros e exceções

## 13. Considerações Finais
O sistema foi projetado para ser escalável e modular, permitindo fácil manutenção e adição de novas funcionalidades. A integração com APIs externas e o processamento de dados em tempo real proporcionam uma experiência rica e personalizada para os usuários.
