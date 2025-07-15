import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def get_database_engine():
    load_dotenv()
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "your_password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mobile_game_analytics")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(DATABASE_URL)

def calculate_dau(engine):
    query = """
    SELECT 
        DATE(timestamp) AS date,
        COUNT(DISTINCT user_id) AS dau
    FROM events
    GROUP BY date
    ORDER BY date;
    """
    return pd.read_sql(query, engine)

def main():
    engine = get_database_engine()
    dau_df = calculate_dau(engine)
    print(dau_df)

    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dau.csv")

    dau_df.to_csv(output_path, index=False)
    print(f"DAU verisi çıktı olarak kaydedildi: {output_path}")


if __name__ == "__main__":
    main()
