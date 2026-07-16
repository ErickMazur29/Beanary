# 📚 Beanary API

API REST desenvolvida em Django + Django REST Framework para gerenciamento de uma biblioteca: cadastro de livros, autores, gêneros, empréstimos e avaliações de usuários.

## 🚀 Tecnologias

- Python
- Django
- Django REST Framework
- Simple JWT (autenticação via token)
- SQLite (ambiente de desenvolvimento)

## 📁 Estrutura do projeto

O projeto é dividido em apps, cada um responsável por um domínio:

| App | Responsabilidade |
|---|---|
| `authentication` | Emissão, refresh e verificação de tokens JWT |
| `users` | Perfil do usuário (telefone, limite de empréstimos) |
| `authors` | Cadastro de autores |
| `genres` | Cadastro de gêneros literários |
| `books` | Cadastro de livros, relacionado a autores e gêneros |
| `loans` | Empréstimos de livros |
| `reviews` | Avaliações de livros pelos usuários |

## 🔗 Relacionamentos principais

- Um **livro** pode ter vários **autores** e vários **gêneros** (`ManyToMany`).
- Um **empréstimo** pertence a um **livro** e a um **usuário** (`ForeignKey`).
- Uma **avaliação** pertence a um **livro** e a um **usuário** (`ForeignKey`).
- Cada **usuário** possui um **perfil** (`OneToOne`) com telefone e limite de empréstimos permitidos.

## 🔐 Autenticação

A API usa autenticação via **JWT** (`djangorestframework-simplejwt`). Endpoints principais:

```
POST /api/v1/authentication/token          → obtém access e refresh token
POST /api/v1/authentication/token/refresh  → renova o access token
POST /api/v1/authentication/token/verify   → verifica validade do token
```

Toda requisição autenticada precisa do header:

```
Authorization: Bearer <access_token>
```

## 📌 Endpoints

Todos os endpoints estão prefixados por `/api/v1/`.

| Recurso | Endpoints |
|---|---|
| Authors | `authors/`, `authors/<id>/` |
| Genres | `genres/`, `genres/<id>/` |
| Books | `books/`, `books/<id>/`, `books/stats/` |
| Loans | `loans/`, `loans/<id>/` |
| Reviews | `reviews/`, `reviews/<id>/` |
| Users | `users/`, `users/<id>/` |

A listagem completa de requisições (com exemplos de payload) está disponível na collection do Postman incluída no projeto.

## 🧠 Regras de negócio já implementadas

- Cálculo automático de **cópias disponíveis** de um livro (`total_copies` − empréstimos ativos).
- Cálculo automático de **quantos empréstimos um usuário ainda pode fazer** (`max_loan_allowed` − empréstimos ativos).
- Validação: não é possível criar um empréstimo se não houver cópias disponíveis.
- Validação: não é possível criar um empréstimo se o usuário atingiu seu limite.
- Serializers diferentes por tipo de requisição (listagem enxuta, detalhe completo com estatísticas de avaliação, escrita simplificada).
- Permissões por modelo e por ação, usando o sistema de permissões nativo do Django (`app.permissions.GlobalDefaultPermission`).

## ⚙️ Como rodar localmente

```bash
# clonar o repositório
git clone <url-do-repositorio>
cd Beanary-main

# criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# instalar dependências
pip install -r requirements.txt

# rodar migrations
python manage.py migrate

# criar superusuário (para acessar o admin e gerar permissões)
python manage.py createsuperuser

# rodar o servidor
python manage.py runserver
```

## 🗺️ Roadmap / próximos passos

- [ ] Migrar de SQLite para PostgreSQL
- [ ] Mover configurações sensíveis (`SECRET_KEY`, `DEBUG`, banco de dados) para variáveis de ambiente
- [ ] Script de importação de dados via CSV
- [ ] Vincular automaticamente o usuário autenticado na criação de empréstimos e avaliações (evitar que um usuário crie registros em nome de outro)
- [ ] Documentação automática da API (OpenAPI/Swagger)
- [ ] Testes automatizados

## ✍️ Autor

Desenvolvido por Erick Mazur (Sousa).