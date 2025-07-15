import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_engine():
    load_dotenv()
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "your_password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mobile_game_analytics")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(DATABASE_URL)

def calculate_retention(engine):
    query = """
    WITH event_days AS (
        SELECT
            u.user_id,
            u.register_date,
            DATE(e.timestamp) AS event_date,
            DATE(e.timestamp) - u.register_date AS days_since_signup
        FROM users u
        JOIN events e ON u.user_id = e.user_id
    ),
    retention_base AS (
        SELECT
            register_date,
            days_since_signup,
            COUNT(DISTINCT user_id) AS retained_users
        FROM event_days
        GROUP BY register_date, days_since_signup
    )
    SELECT 
        register_date,
        days_since_signup,
        retained_users
    FROM retention_base
    ORDER BY register_date, days_since_signup;
    """
    return pd.read_sql(query, engine)

def main():
    engine = get_database_engine()
    retention_df = calculate_retention(engine)

    # outputs klasörünü oluştur ve CSV kaydet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "retention.csv")

    retention_df.to_csv(output_path, index=False)
    print(f"Retention verisi CSV olarak kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
