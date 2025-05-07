def run_inference():
    from sqlalchemy import create_engine
    import pandas as pd

    import os

    TRINO_USER = os.getenv('TRINO_USER')
    TRINO_ENDPOINT = os.getenv('TRINO_ENDPOINT')
    TRINO_CATALOG = os.getenv('TRINO_CATALOG')
    TRINO_SCHEMA = os.getenv('TRINO_SCHEMA')

    engine = create_engine(f'trino://{TRINO_USER}@{TRINO_ENDPOINT}/{TRINO_CATALOG}/{TRINO_SCHEMA}')
    connection = engine.connect()

    df = pd.read_sql('SELECT * FROM patients', connection)
    print(df.size)

if __name__ == '__main__':
    run_inference()