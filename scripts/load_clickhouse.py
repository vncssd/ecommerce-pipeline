import pandas as pd
import os
from sqlalchemy import create_engine, text
from clickhouse_driver import Client
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

PG_ENGINE = create_engine(f'postgresql://{db_username}:{db_username}@localhost:5432/olist_ecommerce')
CH_CLIENT = Client(host='localhost')
CH_DB = 'olist_ecommerce'

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
    CH_CLIENT.execute(f'CREATE DATABASE IF NOT EXISTS {CH_DB}')
    print(f'Database {CH_DB} verificado')

def table_exists(tabela: str) -> bool:
    result = CH_CLIENT.execute(f""" SELECT count() FROM system.tables WHERE database = '{CH_DB}' AND NAME = '{tabela}' """)
    return result [0][0] > 0


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
            cols_def.append(f'´{col}´ {ch_type}')

        CH_CLIENT.execute(f''' CREATE TABLE {CH_DB}.{tabela} ({", ".join(cols_def)}) ENGINE = MergeTree() ORDER BY tuple() ''')
        print(f'Tabela {tabela} criada')

    else:
        CH_CLIENT.execute(f'TRUNCATE TABLE  {CH_DB}.{tabela}')
        print(f'Tabela {tabela} truncada.')

    rows = df.values.tolist()

    CH_CLIENT.execute(f'INSERT INTO {CH_DB}.{tabela} VALUES', rows, types_check=True)
    print(f'{tabela} - {len(rows)} linhas carregadas')

def main():
    create_database()
    for tabela in TABELAS:
        print(f'Carregando {tabela}...')
        load_table(tabela)
    print('Carga completa')

if __name__ == '__main__':
    main()
