import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:senha@localhost:5432/olist')

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