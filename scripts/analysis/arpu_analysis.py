import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_engine():
    load_dotenv()
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "your_password")  # Şifreni .env dosyasına ekle
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "mobile_game_analytics")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(DATABASE_URL)

def calculate_arpu(engine):
    query = """
    WITH purchases AS (
        SELECT
            DATE(timestamp) AS purchase_date,
            user_id,
            CAST(json_extract_path_text(event_params::json, 'price') AS FLOAT) AS price
        FROM events
        WHERE event_name = 'item_purchase'
    ),
    daily_revenue AS (
        SELECT
            purchase_date,
            SUM(price) AS total_revenue,
            COUNT(DISTINCT user_id) AS paying_users
        FROM purchases
        GROUP BY purchase_date
    ),
    daily_active_users AS (
        SELECT
            DATE(timestamp) AS activity_date,
            COUNT(DISTINCT user_id) AS dau
        FROM events
        GROUP BY activity_date
    )
    SELECT
        d.activity_date AS date,
        COALESCE(r.total_revenue, 0) AS total_revenue,
        d.dau AS active_users,
        ROUND((COALESCE(r.total_revenue, 0) / d.dau)::numeric, 4) AS arpu
    FROM daily_active_users d
    LEFT JOIN daily_revenue r
    ON d.activity_date = r.purchase_date
    ORDER BY d.activity_date;
    """
    return pd.read_sql(query, engine)

def main():
    engine = get_database_engine()
    arpu_df = calculate_arpu(engine)

    # outputs klasörü varsa oluştur, yoksa oluştur
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "arpu.csv")
    arpu_df.to_csv(output_path, index=False)

    print(f"ARPU analizi başarıyla kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
