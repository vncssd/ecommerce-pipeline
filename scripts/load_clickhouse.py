import pandas as pd
import os
import clickhouse_connect
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

ch_host = os.getenv("CH_HOST")
ch_user = os.getenv("CH_USER")
ch_password = os.getenv("CH_PASSWORD")

PG_ENGINE = create_engine(f'postgresql://{db_username}:{db_password}@localhost:5432/olist_ecommerce')
CH_DB = 'olist_ecommerce'

CH_CLIENT = clickhouse_connect.get_client(
    host=ch_host,
    user=ch_user,
    password=ch_password,
    secure=True 
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
    CH_CLIENT.command(f'CREATE DATABASE IF NOT EXISTS {CH_DB}')
    print(f'Database {CH_DB} verificado')

def table_exists(tabela: str) -> bool:
    result = CH_CLIENT.query(f"SELECT count() FROM system.tables WHERE database = '{CH_DB}' AND name = '{tabela}'")
    return result.result_set [0][0] > 0

def load_table(tabela: str):
    with PG_ENGINE.connect() as conn:
        df = pd.read_sql(text(f'SELECT * FROM {tabela}'), conn)   

    df = df.where(pd.notnull(df), None)

    if not table_exists(tabela):
        cols_def = []
        for col, dtype in df.dtypes.items():
            if 'int' in str(dtype):
                ch_type = 'Nullable(Int64)'
            elif 'float' in str(dtype):
                ch_type = 'Nullable(Float64)'
            elif 'datetime' in str(dtype):
                ch_type = 'Nullable(DateTime)'
            else:
                ch_type = 'Nullable(String)'
            cols_def.append(f'`{col}` {ch_type}')

        CH_CLIENT.command(f'CREATE TABLE {CH_DB}.{tabela} ({", ".join(cols_def)}) ENGINE = MergeTree() ORDER BY tuple()')
        print(f'Tabela {tabela} criada')

    else:
        CH_CLIENT.command(f'TRUNCATE TABLE  {CH_DB}.{tabela}')
        print(f'Tabela {tabela} truncada.')

    CH_CLIENT.insert_df(table=tabela, df=df, database=CH_DB)
    print(f'{tabela} - {len(df)} linhas carregadas')

def main():
    create_database()
    for tabela in TABELAS:
        print(f'Carregando {tabela}...')
        load_table(tabela)
    print('Carga completa')

if __name__ == '__main__':
    main()
