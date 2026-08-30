# Workshop de Backend — Fábrica de Software 26.2

API REST desenvolvida em Django + Django REST Framework para gerenciamento de
Fabricantes e Componentes de hardware, com relacionamento entre as
entidades (chave estrangeira) e consumo de uma API externa.

## Sumário

- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Passo a passo para rodar o projeto](#passo-a-passo-para-rodar-o-projeto)
- [Problemas comuns](#problemas-comuns)
- [Modelagem](#modelagem)
- [Endpoints da API](#endpoints-da-api)
- [Como testar a API](#como-testar-a-api)
- [Exemplos de uso](#exemplos-de-uso)

## Estrutura do projeto

```
wsBackendFabricaDeSoftware26.2/
├── app/                    # App principal (models, views, serializers)
│   ├── migrations/         # Migrações do banco de dados
│   ├── __init__.py
│   ├── admin.py            # Registro dos models no Django Admin
│   ├── apps.py             # Configuração do app
│   ├── models.py           # Fabricante e Componente
│   ├── serializers.py      # Serializers do DRF
│   ├── tests.py
│   └── views.py            # ViewSets + consumo de API externa
├── projeto/                # Configurações do projeto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Configurações gerais (apps, banco, etc.)
│   ├── urls.py             # Rotas da API
│   └── wsgi.py
├── .gitignore
├── db.sqlite3               # Banco de dados (gerado após o migrate)
├── manage.py                 # Utilitário de linha de comando do Django
├── README.md
└── requirements.txt           # Dependências do projeto
```

## Pré-requisitos

Instalar na sua máquina:

- *Python 3.12*
- *Git* (para clonar o repositório)
- Um editor de código, como o VS Code

Para conferir se o Python está instalado corretamente, abra o terminal e rode:

```bash
python --version
```

Deve aparecer "Python 3.12.0". Se der erro de comando não encontrado, reinstale o Python marcando a opção *"Add Python to PATH"* durante a instalação.

## Passo a passo para rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/wsBackendFabricaDeSoftware26.2.git
cd wsBackendFabricaDeSoftware26.2
```

### 2. Crie o ambiente virtual

O ambiente virtual isola as dependências do projeto do resto do sistema.

**Windows (PowerShell):**
```powershell
python -m venv venv
```

Cria uma pasta `venv/` dentro do projeto.

### 3. Ative o ambiente virtual

**Windows (PowerShell):**
```powershell
venv\Scripts\activate
```

Se o nome `(venv)` aparece no início da linha do terminal, tá funcionando (o venv tem que estar ativado sempre que for rodar um comando).
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

Isso vai instalar: `Django`, `djangorestframework`, `requests`, `asgiref`, `sqlparse` e `tzdata`, nas versões especificadas no `requirements.txt`.

Para conferir se tudo foi instalado:
```bash
pip list
```

### 5. Gere as migrações

As migrações traduzem os models Python (`app/models.py`) em comandos SQL para criar as tabelas no banco.

```bash
python manage.py makemigrations
```

Saída esperada:
```
Migrations for 'app':
  app\migrations\0001_initial.py
    - Create model Fabricante
    - Create model Componente
```

- Se aparecer **"No changes detected"**, as migrações já existem — pode seguir para o próximo passo.

### 6. Aplique as migrações no banco de dados

```bash
python manage.py migrate
```

Saída esperada (a lista pode variar, mas deve incluir):
```
Applying app.0001_initial... OK
```

Esse comando cria o arquivo `db.sqlite3` com todas as tabelas necessárias (inclusive as do próprio Django, como autenticação e sessões).

### 7. (Opcional) Crie um usuário administrador

Permite acessar o Django Admin (`/admin/`) para gerenciar os dados por uma interface visual.

```bash
python manage.py createsuperuser
```

Preencha usuário, e-mail (opcional) e senha quando solicitado.

### 8. Suba o servidor

```bash
python manage.py runserver
```

Saída esperada:
```
Starting WSGI development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 9. Acesse a API

Abra o navegador em:

```
http://127.0.0.1:8000/
```

Você verá a *Api Root* do Django REST Framework, com links para `fabricantes` e `componentes`.

## Problemas comuns

*`ModuleNotFoundError: No module named 'django'` ou similar*
O ambiente virtual não está ativado, ou as dependências não foram instaladas. Repita os passos 3 e 4.

*`OperationalError: no such table: app_fabricante`*
As migrações não foram geradas/aplicadas. Repita os passos 5 e 6.

*`ModuleNotFoundError: No module named 'requests'`*
Faltou instalar essa dependência — rode `pip install -r requirements.txt` novamente (ela já está listada no arquivo).

*Porta 8000 já em uso*
Rode o servidor em outra porta:
```bash
python manage.py runserver 8001
```

## Modelagem

### Fabricante

| Campo         | Tipo          | Observações                 |
|---------------|---------------|-------------------------------|
| nome          | CharField     | único                          |
| pais_origem   | CharField     | opcional                       |
| site          | URLField      | opcional                       |
| criado_em     | DateTimeField | preenchido automaticamente     |

### Componente

| Campo           | Tipo             | Observações                             |
|                 |                  |                                         |
| nome            | CharField        |                                         |
| tipo            | CharField        | CPU, GPU, RAM, SSD, HD, MOBO, PSU, CASE |
| fabricante      | ForeignKey       | referencia `Fabricante`related_name="componentes"|
| preco           | DecimalField     |                                       |
| especificacoes  | TextField        | opcional                              |
| em_estoque      | PositiveInteger  |                                       |
| criado_em       | DateTimeField    | preenchido automaticamente               |

Um Fabricante possui vários Componentes (relação 1:N).

## Endpoints da API

### Fabricantes

| Método | Rota                 |Descrição                                    |
|        |
| GET    | `/fabricantes/`      | Lista todos os fabricantes                     |
| POST   | `/fabricantes/`      | Cria um novo fabricante                        |
| GET    | `/fabricantes/{id}/` | Detalha um fabricante (com seus componentes)   |
| PUT    | `/fabricantes/{id}/` | Atualiza um fabricante (completo)              |
| PATCH  | `/fabricantes/{id}/` | Atualiza um fabricante (parcial)               |
| DELETE | `/fabricantes/{id}/` | Remove um fabricante                           |

### Componentes

| Método | Rota                         | Descrição                              |
|        |                              |
| GET    | `/componentes/`                | Lista todos os componentes          |
| GET    | `/componentes/?fabricante={id}`| Filtra por fabricante              |
| GET    | `/componentes/?tipo=CPU`       | Filtra por tipo                    |
| POST   | `/componentes/`                | Cria um novo componente            |
| GET    | `/componentes/{id}/`           | Detalha um componente              |
| PUT    | `/componentes/{id}/`           | Atualiza um componente (completo)  |
| PATCH  | `/componentes/{id}/`           | Atualiza um componente (parcial)   |
| DELETE | `/componentes/{id}/`           | Remove um componente               |

### Consumo de API externa

Consome a *Fake Store API* sem necessidade de autenticação.

| Método | Rota                   |Descrição                                    |
|        |                        |
| GET    | `/produtos-externos/`  | Lista todos os produtos da API externa     |
| GET    | `/produtos-externos/?categoria=electronics`| Filtra produtos por categoria|

Tratamento de erros implementado:

- *503 Service Unavailable* — quando a API externa está fora do ar ou o
  tempo de resposta excede o timeout configurado (5 segundos).
- *404 Not Found* — quando a categoria informada não retorna nenhum
  produto.

## Como testar a API

A forma mais simples é pelo navegador, usando a interface navegável do DRF:

1. Acesse `http://127.0.0.1:8000/fabricantes/`.
2. Role até o formulário *HTML form* no final da página.
3. Preencha os campos e clique em *POST* para criar um registro.
4. A própria página recarrega mostrando o resultado dentro de `"results"`.

Para os métodos `PUT`, `PATCH` e `DELETE`, acesse o detalhe do registro
(`/fabricantes/{id}/` ou `/componentes/{id}/`) — os botões correspondentes
aparecem no topo da página.


## Exemplos para usar

Criar um fabricante:

```json
POST /fabricantes/
{
    "nome": "AMD",
    "pais_origem": "EUA",
    "site": "https://amd.com"
}
```

Criar um componente vinculado a esse fabricante:

```json
POST /componentes/
{
    "nome": "Ryzen 5 5600G",
    "tipo": "CPU",
    "fabricante": 1,
}
```

Consultar produtos externos por categoria:

```
GET /produtos-externos/?categoria=electronics
```

