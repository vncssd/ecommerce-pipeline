import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f'postgresql://{db_username}:{db_username}@localhost:5432/olist_ecommerce')

tabelas = {
    'customers': 'olist_customers_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'order_payments': 'olist_order_payments_dataset.csv',
    'order_reviews': 'olist_order_reviews_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
}

for tabela, arquivo in tabelas.items():
    df = pd.read_csv(arquivo)
    df.to_sql(tabela, engine, if_exists='replace', index=False)
    print(f'{tabela} carregada — {len(df)} registros')