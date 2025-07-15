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

def calculate_ltv(engine):
    query = """
    WITH purchases AS (
        SELECT
            user_id,
            CAST(json_extract_path_text(event_params::json, 'price') AS FLOAT) AS price
        FROM events
        WHERE event_name = 'item_purchase'
    ),
    ltv AS (
        SELECT
            u.user_id,
            u.register_date,
            SUM(p.price) AS total_revenue
        FROM users u
        LEFT JOIN purchases p ON u.user_id = p.user_id
        GROUP BY u.user_id, u.register_date
    )
    SELECT
        user_id,
        register_date,
        COALESCE(total_revenue, 0) AS lifetime_value
    FROM ltv
    ORDER BY user_id;
    """
    return pd.read_sql(query, engine)

def main():
    engine = get_database_engine()
    ltv_df = calculate_ltv(engine)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "ltv.csv")

    ltv_df.to_csv(output_path, index=False)
    print(f"✅ LTV analizi başarıyla kaydedildi: {output_path}")

if __name__ == "__main__":
    main()
