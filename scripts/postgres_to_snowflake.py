import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

sf_account   = os.getenv("SF_ACCOUNT")
sf_user      = os.getenv("SF_USER")
sf_password  = os.getenv("SF_PASSWORD")
sf_warehouse = os.getenv("SF_WAREHOUSE")
sf_database  = os.getenv("SF_DATABASE")
sf_schema    = os.getenv("SF_SCHEMA", "PUBLIC")

PG_ENGINE = create_engine(
    f'postgresql://{db_username}:{db_password}@localhost:5432/olist_ecommerce'
)

SF_CONN = snowflake.connector.connect(
    account=sf_account,
    user=sf_user,
    password=sf_password,
    warehouse=sf_warehouse,
    database=sf_database,
    schema=sf_schema,
)

TABELAS = [
    'customers',
    'order_items',
    'order_payments',
    'order_reviews',
    'orders',
    'products',
    'sellers',
]

def create_database():
    cur = SF_CONN.cursor()
    cur.execute(f'CREATE DATABASE IF NOT EXISTS {sf_database}')
    cur.execute(f'CREATE SCHEMA IF NOT EXISTS {sf_database}.{sf_schema}')
    cur.execute(f'USE SCHEMA {sf_database}.{sf_schema}')
    cur.close()
    print(f'Database/schema {sf_database}.{sf_schema} verificado')

def table_exists(tabela: str) -> bool:
    cur = SF_CONN.cursor()
    cur.execute(f"""
        SELECT COUNT(*)
        FROM {sf_database}.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = '{sf_schema.upper()}'
          AND TABLE_NAME   = '{tabela.upper()}'
    """)
    result = cur.fetchone()[0]
    cur.close()
    return result > 0

def get_snowflake_type(dtype) -> str:
    dtype = str(dtype)
    if 'int' in dtype:
        return 'INT'
    elif 'float' in dtype:
        return 'FLOAT'
    elif 'datetime' in dtype:
        return 'TIMESTAMP'
    else:
        return 'VARCHAR'

def load_table(tabela: str):
    with PG_ENGINE.connect() as conn:
        df = pd.read_sql(text(f'SELECT * FROM {tabela}'), conn)

    df = df.where(pd.notnull(df), None)

    df.columns = [c.upper() for c in df.columns]

    cur = SF_CONN.cursor()

    if not table_exists(tabela):
        cols_def = [
            f'"{col}" {get_snowflake_type(dtype)}'
            for col, dtype in df.dtypes.items()
        ]
        cur.execute(
            f'CREATE TABLE {sf_database}.{sf_schema}.{tabela.upper()} '
            f'({", ".join(cols_def)})'
        )
        print(f'Tabela {tabela} criada')
    else:
        cur.execute(f'TRUNCATE TABLE {sf_database}.{sf_schema}.{tabela.upper()}')
        print(f'Tabela {tabela} truncada')

    cur.close()

    success, nchunks, nrows, _ = write_pandas(
        conn=SF_CONN,
        df=df,
        table_name=tabela.upper(),
        database=sf_database,
        schema=sf_schema,
    )
    print(f'{tabela} - {nrows} linhas carregadas (sucesso={success})')

def main():
    create_database()
    for tabela in TABELAS:
        print(f'Carregando {tabela}...')
        load_table(tabela)
    print('Carga completa')

if __name__ == '__main__':
    main()