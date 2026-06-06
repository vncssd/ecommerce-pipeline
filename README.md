# Ecommerce Pipeline

Pipeline de dados completo utilizando dados públicos do e-commerce brasileiro Olist. O projeto cobre todas as etapas de um pipeline moderno: ingestão, transformação e visualização.
<a href="https://datastudio.google.com/reporting/67fe7c26-c473-4f60-ba65-9b376170d3a0">
Acesse o dashboard
</a>
---

## Arquitetura

```
PostgreSQL → Python → Snowflake (RAW) → dbt → Snowflake (ANALYTICS) → Looker Studio
```

### Stack
- **PostgreSQL** — banco de dados de origem com os dados brutos do Olist
- **Python** — script de ingestão (extração do Postgres e carga no Snowflake)
- **Snowflake** — data warehouse em nuvem (camadas RAW e ANALYTICS)
- **dbt** — transformação e modelagem dos dados
- **Looker Studio** — dashboard executivo de visualização

---

## Estrutura do projeto

```
ecommerce-pipeline/
├── scripts/
│   ├── load_postgres.py           # carga inicial no PostgreSQL
│   └── postgres_to_snowflake.py   # ingestão PostgreSQL → Snowflake
└── ecommerce_analytics/           # projeto dbt
    ├── models/
    │   ├── stages/                # views de staging (limpeza e renomeação)
    │   │   ├── sources.yml
    │   │   ├── stg_customers.sql
    │   │   ├── stg_order_items.sql
    │   │   ├── stg_order_payments.sql
    │   │   ├── stg_order_reviews.sql
    │   │   ├── stg_orders.sql
    │   │   ├── stg_products.sql
    │   │   └── stg_sellers.sql
    │   ├── dimensions/            # tabelas dimensionais
    │   │   ├── dim_customers.sql
    │   │   ├── dim_date.sql
    │   │   ├── dim_products.sql
    │   │   └── dim_sellers.sql
    │   └── fact/                  # tabela fato
    │       └── fact_orders.sql
    ├── dbt_project.yml
    └── profiles.yml
```

---

## Modelagem

### Camada Staging (`ANALYTICS.stg_*`)
Views que limpam e renomeiam as colunas brutas da camada RAW. Sem regras de negócio.

| Model | Fonte | Descrição |
|---|---|---|
| `stg_customers` | `RAW.customers` | Dados de clientes |
| `stg_order_items` | `RAW.order_items` | Itens dos pedidos |
| `stg_order_payments` | `RAW.order_payments` | Pagamentos |
| `stg_order_reviews` | `RAW.order_reviews` | Avaliações |
| `stg_orders` | `RAW.orders` | Pedidos com cast de timestamps |
| `stg_products` | `RAW.products` | Produtos |
| `stg_sellers` | `RAW.sellers` | Vendedores |

### Camada Dimensional (`ANALYTICS.dim_*`)
Tabelas materializadas com enriquecimento e regras de negócio.

| Model | Descrição |
|---|---|
| `dim_customers` | Clientes com classificação por região do Brasil |
| `dim_date` | Calendário extraído das datas de compra |
| `dim_products` | Produtos com volume calculado e categoria formatada |
| `dim_sellers` | Vendedores com classificação por região do Brasil |

### Camada Fato (`ANALYTICS.fact_*`)

| Model | Descrição |
|---|---|
| `fact_orders` | Pedidos com métricas de preço, frete, pagamento, avaliação e prazo de entrega |

---

## Como rodar

### Pré-requisitos
- Python 3.10+
- PostgreSQL com os dados do Olist carregados
- Conta no Snowflake
- dbt instalado (`pip install dbt-snowflake`)

### 1. Configurar variáveis de ambiente

Crie um arquivo `.env` na pasta `scripts/`:

```env
DB_USERNAME=seu_user_postgres
DB_PASSWORD=sua_senha_postgres

SF_ACCOUNT=sua_account_snowflake
SF_USER=seu_user_snowflake
SF_PASSWORD=sua_senha_snowflake
SF_WAREHOUSE=seu_warehouse
SF_DATABASE=OLIST_ECOMMERCE
SF_SCHEMA=RAW
```

### 2. Instalar dependências Python

```bash
pip install pandas sqlalchemy psycopg2 python-dotenv "snowflake-connector-python[pandas]"
```

### 3. Carregar dados brutos no Snowflake

```bash
cd scripts
python3 postgres_to_snowflake.py
```

Isso vai criar o schema `RAW` e carregar as 7 tabelas brutas no Snowflake.

### 4. Configurar o dbt

No arquivo `~/.dbt/profiles.yml`:

```yaml
ecommerce_analytics:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: sua_account_snowflake
      user: seu_user_snowflake
      password: sua_senha_snowflake
      role: ACCOUNTADMIN
      warehouse: seu_warehouse
      database: OLIST_ECOMMERCE
      schema: ANALYTICS
      threads: 1
```

### 5. Rodar o dbt

```bash
cd ecommerce_analytics
dbt run
```

### 6. (Opcional) Gerar documentação do dbt

```bash
dbt docs generate
dbt docs serve
```

---

## Fonte dos dados

Dataset público [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) disponível no Kaggle.

O dataset contém ~100 mil pedidos realizados entre 2017 e 2018 em diversas categorias de produtos, com informações de clientes, vendedores, pagamentos, avaliações e logística.
