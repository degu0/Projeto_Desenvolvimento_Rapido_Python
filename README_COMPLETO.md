# Plataforma de Inteligencia Municipal

Este projeto e um MVP web simples para centralizar e visualizar gastos municipais a partir de arquivos `.xlsx` ou `.csv`.

Ele foi criado seguindo o PRD localizado em `doc/PRD.MD`, com foco em simplicidade, uso rapido e uma estrutura pequena em Python.

## Objetivo

O sistema ajuda gestores municipais a importar dados financeiros que antes ficavam espalhados em planilhas e visualizar essas informacoes em um dashboard.

Com ele e possivel:

- Fazer login no sistema.
- Enviar planilhas Excel ou CSV com gastos.
- Salvar os dados em um banco SQLite.
- Visualizar indicadores financeiros.
- Consultar gastos com filtros.
- Separar permissoes entre prefeito e secretario.

## Stack utilizada

| Camada | Tecnologia |
| --- | --- |
| Backend | FastAPI |
| Banco de dados | SQLite |
| ORM | SQLAlchemy |
| Templates | Jinja2 |
| Upload e leitura de arquivos | pandas + openpyxl |
| Graficos | Chart.js |
| Autenticacao | JWT em cookie HTTP-only |
| Estilos | CSS puro |

## Estrutura do projeto

```text
.
+-- app/
|   +-- main.py              # Rotas principais da aplicacao
|   +-- database.py          # Configuracao do SQLite e sessao do banco
|   +-- models.py            # Modelos Usuario e Gasto
|   +-- auth.py              # Login, senha hash e JWT
|   +-- excel.py             # Importacao de arquivos .xlsx e .csv
|   +-- templates/
|   |   +-- base.html        # Layout base
|   |   +-- login.html       # Tela de login
|   |   +-- dashboard.html   # Dashboard financeiro
|   |   +-- gastos.html      # Lista de gastos com filtros
|   +-- static/
|       +-- styles.css       # Estilos responsivos
+-- doc/
|   +-- PRD.MD               # Documento de requisitos
+-- samples/
|   +-- gastos_exemplo.csv   # Arquivo exemplo para importacao
+-- requirements.txt         # Dependencias Python
+-- README.md                # Guia rapido
+-- README_COMPLETO.md       # Documentacao detalhada
```

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Depois acesse:

```text
http://127.0.0.1:8000
```

## Usuarios de demonstracao

O sistema cria automaticamente dois usuarios na primeira execucao:

| Perfil | Email | Senha | Permissao |
| --- | --- | --- | --- |
| Prefeito | prefeito@demo.com | 123456 | Visualiza todos os dados |
| Secretario da Saude | saude@demo.com | 123456 | Visualiza somente a secretaria Saude |

## Funcionalidades

### Login

A tela inicial permite autenticar com email e senha.

Apos o login, o sistema grava um token JWT em cookie HTTP-only e redireciona o usuario para o dashboard.

### Dashboard financeiro

O dashboard mostra:

- Total gasto no mes atual.
- Orcamento restante.
- Secretaria com maior volume de gastos.
- Grafico de gastos por secretaria.
- Grafico de gastos por categoria.
- Ultimos gastos importados.

O orcamento mensal usado no MVP e fixo:

```text
R$ 1.000.000,00
```

### Alertas de orcamento

O card de total gasto muda visualmente conforme o percentual usado:

| Percentual usado | Alerta |
| --- | --- |
| Abaixo de 80% | Normal |
| A partir de 80% | Amarelo |
| A partir de 100% | Vermelho |

### Upload de arquivos

O sistema aceita arquivos:

- `.xlsx`
- `.csv`

As colunas obrigatorias sao:

| Coluna | Descricao |
| --- | --- |
| secretaria | Nome da secretaria responsavel pelo gasto |
| valor | Valor numerico do gasto |
| categoria | Categoria do gasto |
| descricao | Descricao curta |
| data | Data do gasto |

Exemplo:

| secretaria | valor | categoria | descricao | data |
| --- | --- | --- | --- | --- |
| Saude | 12000.50 | Medicamentos | Compra mensal | 2026-05-10 |
| Educacao | 8400.00 | Transporte | Manutencao de vans | 2026-05-12 |

Existe um arquivo CSV de exemplo em:

```text
samples/gastos_exemplo.csv
```

### Lista de gastos

A pagina `/gastos` mostra todos os gastos visiveis para o usuario logado.

Filtros disponiveis:

- Secretaria, apenas para prefeito.
- Categoria.
- Data.

### Permissoes

O controle de acesso e simples:

| Cargo | Regra |
| --- | --- |
| prefeito | Pode ver todos os gastos |
| secretario | Pode ver apenas gastos da propria secretaria |

Essa regra e aplicada tanto no dashboard quanto na lista de gastos.

## Banco de dados

O banco usado e SQLite.

Ao iniciar o sistema, o arquivo abaixo e criado automaticamente:

```text
municipal.db
```

### Tabela usuarios

| Campo | Tipo | Descricao |
| --- | --- | --- |
| id | inteiro | Identificador |
| nome | texto | Nome do usuario |
| email | texto | Email usado no login |
| senha | texto | Senha com hash |
| cargo | texto | prefeito ou secretario |
| secretaria | texto | Secretaria associada |

### Tabela gastos

| Campo | Tipo | Descricao |
| --- | --- | --- |
| id | inteiro | Identificador |
| secretaria | texto | Secretaria responsavel |
| valor | decimal | Valor do gasto |
| categoria | texto | Categoria do gasto |
| descricao | texto | Descricao |
| data | data | Data do gasto |

## Fluxo principal

```text
1. Usuario acessa o sistema
2. Faz login
3. Envia arquivo .xlsx ou .csv
4. O sistema valida as colunas
5. Os gastos sao salvos no SQLite
6. O dashboard e atualizado
7. O usuario consulta graficos e lista de gastos
```

## Decisoes de simplicidade

Este projeto foi mantido pequeno de proposito.

Algumas escolhas feitas para o MVP:

- Nao ha cadastro de usuarios pela interface.
- O orcamento mensal e fixo no codigo.
- Nao ha relatorio PDF.
- Nao ha integracoes externas.
- Nao ha aplicativo mobile separado.
- O layout e responsivo, mas usando HTML, Jinja2 e CSS simples.

## Arquivos principais

### `app/main.py`

Concentra as rotas da aplicacao:

- `/login`
- `/logout`
- `/dashboard`
- `/upload`
- `/gastos`

Tambem cria as tabelas e usuarios demo ao iniciar.

### `app/auth.py`

Responsavel por:

- Hash de senha.
- Validacao de senha.
- Criacao do JWT.
- Leitura do usuario autenticado pelo cookie.

### `app/excel.py`

Responsavel por importar os arquivos enviados.

Apesar do nome do arquivo ser `excel.py`, ele aceita tanto Excel quanto CSV.

### `app/models.py`

Define os modelos SQLAlchemy:

- `Usuario`
- `Gasto`

### `app/templates`

Contem as telas HTML renderizadas pelo FastAPI com Jinja2.

## Como testar manualmente

1. Rode o projeto.
2. Acesse `http://127.0.0.1:8000`.
3. Entre com `prefeito@demo.com` e senha `123456`.
4. Importe `samples/gastos_exemplo.csv`.
5. Confira os cards e graficos do dashboard.
6. Acesse a pagina `Gastos`.
7. Use os filtros de categoria, secretaria ou data.
8. Saia e entre com `saude@demo.com`.
9. Confira que o secretario ve apenas gastos da secretaria Saude.

## Possiveis proximos passos

- Tela para cadastrar usuarios.
- Cadastro e edicao de orcamento por secretaria.
- Exclusao de importacoes.
- Exportacao em PDF.
- Testes automatizados.
- Melhorias de seguranca para ambiente de producao.
- Deploy em servidor web.

## Observacoes de producao

Para uso real, antes de publicar o sistema:

- Trocar a chave `SECRET_KEY` em `app/auth.py`.
- Usar variaveis de ambiente.
- Configurar HTTPS.
- Criar controle de usuarios real.
- Definir politica de backup do banco.
- Revisar validacoes de arquivos enviados.
