# Plataforma de Inteligencia Municipal

MVP simples em FastAPI para centralizar gastos municipais a partir de uma planilha Excel ou CSV e visualizar um dashboard financeiro.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse: <http://127.0.0.1:8000>

## Usuarios demo

| Perfil | Email | Senha |
| --- | --- | --- |
| Prefeito | prefeito@demo.com | 123456 |
| Secretario Saude | saude@demo.com | 123456 |

## Planilha esperada

Envie um arquivo `.xlsx` ou `.csv` com estas colunas:

| secretaria | valor | categoria | descricao | data |
| --- | --- | --- | --- | --- |
| Saude | 12000.50 | Medicamentos | Compra mensal | 2026-05-10 |

O secretario visualiza somente os dados da propria secretaria. O prefeito visualiza tudo.
