from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Example database connection
def get_db_engine():
    return create_engine(
        f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}'
        f'@{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DB"]}'
    )

# Example function
def example_query():
    engine = get_db_engine()
    with engine.connect() as conn:
        return pd.read_sql("SELECT * FROM users LIMIT 5", conn)

if __name__ == "__main__":
    print(example_query())