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

def calculate_churn(engine):
    query = """
    WITH user_activity AS (
        SELECT
            u.user_id,
            u.register_date,
            MIN(DATE(e.timestamp)) AS first_event_date,
            MAX(DATE(e.timestamp)) AS last_event_date
        FROM users u
        LEFT JOIN events e ON u.user_id = e.user_id
        GROUP BY u.user_id, u.register_date
    ),
    churn_flags AS (
        SELECT
            user_id,
            register_date,
            last_event_date,
            CASE 
                WHEN last_event_date <= register_date + INTERVAL '1 day' THEN 1
                WHEN last_event_date <= register_date + INTERVAL '7 days' THEN 1
                ELSE 0
            END AS is_churned
        FROM user_activity
    )
    SELECT
        register_date,
        COUNT(*) AS total_users,
        SUM(is_churned) AS churned_users,
        ROUND(100.0 * SUM(is_churned) / COUNT(*), 2) AS churn_rate
    FROM churn_flags
    GROUP BY register_date
    ORDER BY register_date;
    """
    return pd.read_sql(query, engine)

def main():
    engine = get_database_engine()
    churn_df = calculate_churn(engine)

    # outputs klasörüne kaydet
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "churn.csv")

    churn_df.to_csv(output_path, index=False)
    print(f"Churn analizi CSV olarak kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
