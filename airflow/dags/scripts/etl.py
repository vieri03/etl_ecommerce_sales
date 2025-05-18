import pandas as pd
import numpy as np
import os
import re
import logging
import clickhouse_connect

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_client():
    try:
        client = clickhouse_connect.get_client(
            host=os.getenv("CLICKHOUSE_HOST"),
            port=int(os.getenv("CLICKHOUSE_PORT")),
            username=os.getenv("CLICKHOUSE_USER"),
            password=os.getenv("CLICKHOUSE_PASSWORD"),
            database=os.getenv("CLICKHOUSE_DB")
        )
        logging.info("Connected to ClickHouse")
        return client
    except Exception as e:
        logging.exception("Failed to connect to ClickHouse")
        raise

def create_tables(client):
    try:
        # customer_details
        client.command("""CREATE TABLE IF NOT EXISTS warehouse.customer_details (
            customer_id             Int64,
            age                     Nullable(Int64),
            gender                  Nullable(String),
            item_purchased          Nullable(String),
            category                Nullable(String),
            purchase_amount_usd     Nullable(Int64),
            location                Nullable(String),
            size                    Nullable(String),
            color                   Nullable(String),
            season                  Nullable(String),
            review_rating           Nullable(Float64),
            subscription_status     Nullable(Bool),
            shipping_type           Nullable(String),
            discount_applied        Nullable(Bool),
            promo_code_used         Nullable(Bool),
            previous_purchases      Nullable(Int64),
            payment_method          Nullable(String),
            frequency_of_purchases  Nullable(String)
        ) ENGINE = MergeTree ORDER BY customer_id;""")

        # product_details
        client.command("""CREATE TABLE IF NOT EXISTS warehouse.product_details (
            unique_id               String,
            product_name            Nullable(String),
            brand_name              Nullable(String),
            asin                    Nullable(String),
            category                Nullable(String),
            upc_ean_code            Nullable(String),
            list_price              Nullable(Float64),
            selling_price           Nullable(String),
            quantity                Nullable(Float64),
            model_number            Nullable(String),
            about_product           Nullable(String),
            product_specification   Nullable(String),
            technical_details       Nullable(String),
            shipping_weight         Nullable(String),
            product_dimensions      Nullable(String),
            image                   Nullable(String),
            variants                Nullable(String),
            sku                     Nullable(String),
            product_url             Nullable(String),
            stock                   Nullable(Float64),
            product_details         Nullable(String),
            dimensions              Nullable(String),
            color                   Nullable(String),
            ingredients             Nullable(String),
            direction_to_use        Nullable(String),
            is_amazon_seller        Nullable(Bool),
            size_quantity_variant   Nullable(String),
            product_description     Nullable(String),
            category_level_1        Nullable(String),
            category_level_2        Nullable(String),
            category_level_3        Nullable(String),
            category_level_4        Nullable(String),
            category_level_5        Nullable(String),
            category_level_6        Nullable(String),
            category_level_7        Nullable(String),
            selling_price_lower     Nullable(Float64),
            selling_price_upper     Nullable(Float64)                       
        ) ENGINE = MergeTree ORDER BY unique_id;""")

        # sales
        client.command("""CREATE TABLE IF NOT EXISTS warehouse.sales (
            user_id           Int64,
            product_id        Nullable(String),
            interaction_type  Nullable(String),
            time_stamp        Nullable(DateTime)
        ) ENGINE = MergeTree ORDER BY user_id;""")

        logging.info("Tables created or verified")
    except Exception as e:
        logging.exception("Failed to create tables")
        raise

def truncate_tables(client):
    try:
        client.command("TRUNCATE TABLE IF EXISTS warehouse.customer_details;")
        client.command("TRUNCATE TABLE IF EXISTS warehouse.product_details;")
        client.command("TRUNCATE TABLE IF EXISTS warehouse.sales;")
        logging.info("Tables truncated")
    except Exception as e:
        logging.exception("Failed to truncate tables")
        raise

def process_customer_data(client, file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for c in df.columns]
        df['subscription_status'] = df['subscription_status'].map({'Yes': True, 'No': False})
        df['discount_applied'] = df['discount_applied'].map({'Yes': True, 'No': False})
        df['promo_code_used'] = df['promo_code_used'].map({'Yes': True, 'No': False})
        client.insert_df('customer_details', df)
        logging.info("Customer data inserted")
    except Exception as e:
        logging.exception("Failed to process customer data")
        raise

def extract_dimensions(spec):
    if not isinstance(spec, str):
        return None
    match = re.search(r'Product\s*Dimensions\s*:?\s*([\d.xX\s]+inches)', spec, re.IGNORECASE)
    if not match:
        match = re.search(r'ProductDimensions\s*:?\s*([\d.xX\s]+inches)', spec, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_asin(spec):
    if not isinstance(spec, str):
        return None
    match = re.search(r'ASIN\s*:?\s*([A-Z0-9]{10})', spec, re.IGNORECASE)
    return match.group(1) if match else None

def parse_price(value):
    if pd.isna(value):
        return (np.nan, np.nan)
    cleaned = re.sub(r'[\$ ]+', '', str(value))
    matches = re.findall(r'\d+(?:\.\d+)?', cleaned)
    if not matches:
        return (np.nan, np.nan)
    numbers = [float(m) for m in matches]
    return (numbers[0], numbers[0]) if len(numbers) == 1 else (min(numbers), max(numbers))

def process_product_data(client, file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for c in df.columns]
        df = df.rename(columns={"uniqe_id": "unique_id"})
        df['is_amazon_seller'] = df['is_amazon_seller'].map({'Y': True, 'N': False})

        # Clean dimensions
        df['dimensions'] = df.apply(
            lambda row: extract_dimensions(row['product_specification']) if pd.isna(row['dimensions']) or row['dimensions'] == '' else row['dimensions'],
            axis=1
        )

        # Clean ASIN
        df['asin'] = df.apply(
            lambda row: extract_asin(row['product_specification']) if pd.isna(row['asin']) or row['asin'] == '' else row['asin'],
            axis=1
        )

        # Expand category
        category_split = df['category'].fillna('').str.split('|').apply(lambda x: [i.strip() for i in x if i])
        category_df = category_split.apply(pd.Series)
        category_df.columns = [f'category_level_{i+1}' for i in category_df.columns]
        df = pd.concat([df, category_df], axis=1)

        # Clean price
        df[['selling_price_lower', 'selling_price_upper']] = df['selling_price'].apply(parse_price).apply(pd.Series)

        client.insert_df('product_details', df)
        logging.info("Product data inserted")
    except Exception as e:
        logging.exception("Failed to process product data")
        raise

def process_sales_data(client, file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for c in df.columns]
        df = df[df['user_id'].notna()]
        df = df.loc[:, ['user_id','product_id','interaction_type','time_stamp']]
        df['time_stamp'] = pd.to_datetime(df['time_stamp'], format='%d/%m/%Y %H:%M')
        client.insert_df('sales', df)
        logging.info("Sales data inserted")
    except Exception as e:
        logging.exception("Failed to process sales data")
        raise

def main():
    client = get_client()
    create_tables(client)
    truncate_tables(client)

    base_path = '/app/data'
    files = {
        'customer_details': f'{base_path}/customer_details.csv',
        'product_details': f'{base_path}/product_details.csv',
        'sales': f'{base_path}/E-commerece sales data 2024.csv'
    }

    process_customer_data(client, files['customer_details'])
    process_product_data(client, files['product_details'])
    process_sales_data(client, files['sales'])

if __name__ == "__main__":
    main()