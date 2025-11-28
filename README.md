# av2-api-flask

4. Estrutura do Projeto

```
app.py
database.py
models/
	├── __init__.py
	├── user.py
	└── registro.py
routes/
	├── __init__.py
	├── users.py
	└── registros.py
requirements.txt
```

# av2-api-flask

## Descrição do sistema

Aplicação de exemplo construída com Flask que expõe uma API REST para gerenciar registros (ex.: compras/transações). A aplicação inclui:

- Autenticação via JWT para os endpoints da API.
- Modelos persistidos com SQLAlchemy em SQLite (`data.db`).
- Endpoints CRUD para `registros` (cada registro pode pertencer a um `User`).
- Uma interface web simples (session-based) para cadastro/login e gerenciamento visual de compras.

Casos de uso típicos: cadastrar usuários, autenticar, criar/listar/editar/remover registros ligados ao usuário.

## Requisitos

- Python 3.8+ (recomendado 3.10+)
- `pip` instalado

## Instalação e execução

1. (opcional) Criar e ativar um virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Ajustar variáveis de ambiente (opcional):

- `JWT_SECRET_KEY` — chave secreta para JWT (em produção sempre definir uma chave forte)
- `DATABASE_URL` — opcional para apontar para outro banco

4. Rodar a aplicação:

```bash
python app.py
```

Ao iniciar, se `data.db` não existir, o app criará as tabelas automaticamente. Para recriar o banco manualmente:

```bash
rm -f data.db
python -c "from app import create_app; create_app(); print('DB criado')"
```

## Estrutura do projeto (resumida)

```
app.py
database.py
models/
	├── __init__.py
	├── user.py
	└── registro.py
routes/
	├── users.py
	├── registros.py
	└── compras_routes.py
controllers/
templates/
static/
requirements.txt
```

## Exemplos de requisições (endpoints e JSONs)

Os exemplos usam `curl`. Substitua `127.0.0.1:5000` pelo host/porta em que a app estiver rodando.

1) Registrar usuário

Endpoint: `POST /users/register`

JSON de exemplo:

```json
{
	"username": "jose",
	"email": "a@b.com",
	"password": "senha"
}
```

curl:

```bash
curl -X POST http://127.0.0.1:5000/users/register \
	-H "Content-Type: application/json" \
	-d '{"username":"jose","email":"a@b.com","password":"senha"}'
```

Resposta: JSON com dados do usuário e `access_token`.

2) Login (obter token)

Endpoint: `POST /users/login`

JSON de exemplo:

```json
{
	"username": "jose",
	"password": "senha"
}
```

curl:

```bash
curl -X POST http://127.0.0.1:5000/users/login \
	-H "Content-Type: application/json" \
	-d '{"username":"jose","password":"senha"}'
```

Resposta: `{ "access_token": "<token>" , ... }`

3) Listar registros (autenticado)

Endpoint: `GET /registros/`

curl (usando token):

```bash
TOKEN=<access_token>
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/registros/
```

4) Criar um registro (autenticado)

Endpoint: `POST /registros/`

JSON de exemplo:

```json
{
	"descricao": "compra de pão",
	"valor": 5.5,
	"categoria": "alimentacao",
	"data": "2025-11-23",
	"tipo": "despesa"
}
```

curl:

```bash
curl -X POST http://127.0.0.1:5000/registros/ \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $TOKEN" \
	-d '{"descricao":"compra de pão","valor":5.5,"categoria":"alimentacao","data":"2025-11-23","tipo":"despesa"}'
```

5) Atualizar um registro (autenticado)

Endpoint: `PUT /registros/<id>`

JSON de exemplo (parcialmente atualizando campos):

```json
{
	"descricao": "compra de leite",
	"valor": 7.0
}
```

curl:

```bash
curl -X PUT http://127.0.0.1:5000/registros/1 \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer $TOKEN" \
	-d '{"descricao":"compra de leite","valor":7.0}'
```

6) Remover um registro (autenticado)

Endpoint: `DELETE /registros/<id>`

curl:

```bash
curl -X DELETE http://127.0.0.1:5000/registros/1 \
	-H "Authorization: Bearer $TOKEN"
```

## Interface web (rápido)

A aplicação também expõe páginas para cadastro/login e lista de compras (session-based):

- `GET /register` — cadastro via formulário HTML
- `GET /login` — login via formulário HTML
- `GET /` — lista de compras (requer sessão)

Observação: a UI usa sessão enquanto a API usa JWT.

## Recomendações

- Em produção, definir `JWT_SECRET_KEY` via variável de ambiente e usar migrações com `Flask-Migrate`.
- Adicionar proteção CSRF nas rotas que usam formulários (Flask-WTF).



