# PRD — MVP Plataforma de Inteligência Municipal

## Informações Gerais

| Campo    | Valor                                                        |
| -------- | ------------------------------------------------------------ |
| Produto  | Plataforma de Inteligência Municipal                         |
| Versão   | MVP 1.0                                                      |
| Status   | Draft                                                        |
| Stack    | Python                                                       |
| Objetivo | Centralizar gastos municipais e gerar dashboards financeiros |
| Tipo     | Web App Responsivo                                           |

---

# 1. Visão Geral

A Plataforma de Inteligência Municipal é um sistema web focado na centralização e visualização de dados financeiros da prefeitura.

O MVP terá como foco resolver o problema de desorganização das planilhas financeiras municipais, permitindo que gestores acompanhem gastos, orçamento e indicadores de forma rápida e acessível pelo celular.

O sistema funcionará inicialmente através do upload de planilhas Excel contendo gastos das secretarias municipais.

---

# 2. Problema

Hoje os dados financeiros:

* estão espalhados em planilhas;
* são difíceis de visualizar;
* não possuem dashboards;
* dificultam tomada de decisão;
* exigem consultas manuais;
* não possuem centralização.

Isso gera:

* retrabalho;
* demora;
* pouca visibilidade da gestão;
* dificuldade de controle orçamentário.

---

# 3. Objetivo do MVP

O MVP deve permitir:

* Upload de planilhas Excel
* Importação automática dos gastos
* Dashboard financeiro simples
* Visualização por secretaria
* Controle básico de acesso
* Visualização mobile

---

# 4. Usuários

## Prefeito

Pode visualizar todos os dados.

## Secretário

Visualiza apenas dados da própria secretaria.

---

# 5. Escopo do MVP

## Inclusos

* Login
* Upload Excel
* Dashboard financeiro
* Lista de gastos
* Filtros básicos
* Controle simples de permissões
* Alertas visuais de orçamento

---

## Fora do Escopo

* IA conversacional
* Aplicativo mobile
* Integrações externas
* Relatórios PDF
* Emails automáticos
* Multi-município
* APIs complexas

---

# 6. Stack Tecnológica

| Camada   | Tecnologia        |
| -------- | ----------------- |
| Backend  | FastAPI           |
| Banco    | SQLite            |
| ORM      | SQLAlchemy        |
| Frontend | Jinja2            |
| Excel    | pandas + openpyxl |
| Gráficos | Chart.js          |
| Auth     | JWT               |

---

# 7. Arquitetura Simplificada

```text
Planilha Excel
      ↓
Upload no sistema
      ↓
Leitura com pandas
      ↓
Banco SQLite
      ↓
Dashboard FastAPI + Jinja2
```

---

# 8. Estrutura de Pastas

```text
app/
│
├── main.py
├── database.py
├── models.py
├── auth.py
├── excel.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── gastos.html
│
└── static/
```

---

# 9. Banco de Dados

## Tabela: usuarios

| Campo      | Tipo   |
| ---------- | ------ |
| id         | int    |
| nome       | string |
| email      | string |
| senha      | string |
| cargo      | string |
| secretaria | string |

---

## Tabela: gastos

| Campo      | Tipo   |
| ---------- | ------ |
| id         | int    |
| secretaria | string |
| valor      | float  |
| categoria  | string |
| descricao  | string |
| data       | date   |

---

# 10. Fluxo Principal

```text
1. Usuário faz login
2. Faz upload da planilha
3. Sistema importa os dados
4. Dados são salvos no banco
5. Dashboard atualiza automaticamente
6. Gestor visualiza indicadores
```

---

# 11. Funcionalidades

## 11.1 Login

### Requisitos

* Login com email e senha
* Sessão autenticada
* Redirecionamento para dashboard

---

## 11.2 Upload Excel

### Requisitos

* Upload de arquivo `.xlsx`
* Leitura automática via pandas
* Salvamento no banco

### Colunas esperadas

| Coluna     |
| ---------- |
| secretaria |
| valor      |
| categoria  |
| descricao  |
| data       |

---

## 11.3 Dashboard

### Cards

* Total gasto no mês
* Orçamento restante
* Maior secretaria em gastos

### Gráficos

* Gastos por secretaria
* Gastos por categoria

### Tabela

* Últimos gastos

---

## 11.4 Lista de Gastos

### Filtros

* Secretaria
* Categoria
* Data

---

## 11.5 Alertas

### Regras

* 80% orçamento → alerta amarelo
* 100% orçamento → alerta vermelho

---

# 12. Regras de Permissão

## Prefeito

Acesso total.

## Secretário

Apenas dados da própria secretaria.

---

# 13. Requisitos Não Funcionais

| Requisito    | Descrição                 |
| ------------ | ------------------------- |
| Mobile-first | Funcionar bem no celular  |
| Simplicidade | Interface simples         |
| Performance  | Dashboard carregar rápido |
| Segurança    | Rotas autenticadas        |
| Facilidade   | Upload simples            |

---

# 14. Critérios de Aceite

| Feature    | Critério                               |
| ---------- | -------------------------------------- |
| Login      | Usuário consegue autenticar            |
| Upload     | Planilha salva corretamente            |
| Dashboard  | Dados aparecem corretamente            |
| Permissões | Secretário não acessa outra secretaria |
| Mobile     | Interface utilizável no celular        |

---
