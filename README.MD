# 📚 Beanary API

API REST desenvolvida em Django + Django REST Framework para gerenciamento de uma biblioteca: cadastro de livros, autores, gêneros, empréstimos e avaliações de usuários.

🔗 **Em produção:** [beanary-production.up.railway.app](https://beanary-production.up.railway.app/api/v1/authors/)

## 🚀 Tecnologias

- Python
- Django + Django REST Framework
- Simple JWT (autenticação via token)
- PostgreSQL, hospedado no [Neon](https://neon.tech)
- Pandas (scripts de importação de dados via CSV)
- Deploy no [Railway](https://railway.app), com Gunicorn + Whitenoise

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

## 🔐 Autenticação e permissões

A API usa autenticação via **JWT** (`djangorestframework-simplejwt`):

```
POST /api/v1/authentication/token          → obtém access e refresh token
POST /api/v1/authentication/token/refresh  → renova o access token
POST /api/v1/authentication/token/verify   → verifica validade do token
```

Toda requisição autenticada precisa do header:

```
Authorization: Bearer <access_token>
```

As permissões são organizadas em três grupos, configurados no Django Admin:

| Grupo | Acesso |
|---|---|
| **Visitor** | Somente leitura (`GET`, `HEAD`, `OPTIONS`) no catálogo público |
| **Member** | Leitura + criação/edição das próprias reviews e criação de empréstimos |
| **Staff** | Acesso amplo, incluindo gerenciamento de empréstimos, usuários e catálogo |

A checagem é feita pela permission classe customizada `app.permissions.GlobalDefaultPermission`, que mapeia cada verbo HTTP para a permissão nativa do Django correspondente (`add_`, `change_`, `delete_`, `view_`).

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

## 🧠 Regras de negócio implementadas

- Cálculo automático de **cópias disponíveis** de um livro (`total_copies` − empréstimos ativos).
- Cálculo automático de **quantos empréstimos um usuário ainda pode fazer** (`max_loan_allowed` − empréstimos ativos).
- Validação: não é possível criar um empréstimo se não houver cópias disponíveis.
- Validação: não é possível criar um empréstimo se o usuário atingiu seu limite.
- Proteção contra criação de empréstimos/avaliações em nome de outro usuário: o campo `user` é automaticamente vinculado a quem está autenticado, exceto para membros do grupo `Staff` ou superusuários.
- Serializers separados por ação (listagem enxuta, detalhe completo com relacionamentos aninhados, escrita simplificada), evitando payloads desnecessários e import circular entre apps.
- Nacionalidade dos autores validada via `TextChoices` (códigos de país, ex: `US`, `GB`, `BR`).

## 📥 Importação de dados via CSV

O projeto inclui management commands, usando **pandas**, para popular o banco a partir de arquivos CSV:

```bash
python manage.py import_genres genres.csv
python manage.py import_authors authors.csv
python manage.py import_books books.csv
```

Os comandos evitam duplicidade de registros e resolvem automaticamente relacionamentos `ManyToMany` (gêneros/autores de um livro) a partir dos nomes informados no CSV.

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

# configurar variáveis de ambiente (.env)
SECRET_KEY=...
DEBUG=True
DATABASE_URL=postgresql://usuario:senha@host/banco
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000

# rodar migrations
python manage.py migrate

# criar superusuário (para acessar o admin e gerenciar grupos/permissões)
python manage.py createsuperuser

# rodar o servidor
python manage.py runserver
```

## ☁️ Deploy

Hospedado no **Railway**, com banco de dados **PostgreSQL** gerenciado pelo **Neon**. O `railway.toml` cuida de rodar as migrations e coletar os arquivos estáticos automaticamente a cada deploy:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn app.wsgi --log-file -"
```

## 🗺️ Roadmap / próximos passos

- [ ] Documentação automática da API (OpenAPI/Swagger)
- [ ] Testes automatizados
- [ ] Endpoint de registro de `Member` (atualmente `User` só é criado via admin)

## ✍️ Autor

Desenvolvido por Erick Mazur (Sousa).
