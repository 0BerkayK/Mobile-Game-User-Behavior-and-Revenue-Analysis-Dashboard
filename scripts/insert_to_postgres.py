import pandas as pd
from sqlalchemy import create_engine, types
import os
import json
from dotenv import load_dotenv

# Ortam değişkenlerini .env dosyasından yükle (isteğe bağlı)
load_dotenv()

# Bağlantı bilgileri (env'den alınır, yoksa varsayılanlar)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "your_password")   # kendi şifreni yazabilirsin
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mobile_game_analytics")

# PostgreSQL bağlantı URI'si
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy engine oluştur
engine = create_engine(DATABASE_URL)

# USERS tablosunu yükle
try:
    users_df = pd.read_csv("../data/users.csv")
    users_df["is_paying_user"] = users_df["is_paying_user"].astype(bool)
    users_df.to_sql("users", con=engine, if_exists="append", index=False)
    print("✅ 'users' tablosuna veri başarıyla yüklendi.")
except Exception as e:
    print("❌ 'users' yükleme hatası:", e)

# EVENTS tablosunu yükle
try:
    events_df = pd.read_csv("../data/events.csv")

    # event_params kolonunu JSON formatına çevir
    events_df["event_params"] = events_df["event_params"].apply(
        lambda x: json.loads(x.replace("'", "\"")) if isinstance(x, str) else {}
    )

    # to_sql işlemi
    events_df.to_sql(
        "events",
        con=engine,
        if_exists="append",
        index=False,
        dtype={
            "event_id": types.VARCHAR(36),             # UUID yerine string olarak alıyoruz
            "event_params": types.JSON                 # PostgreSQL JSONB alanı ile uyumlu
        }
    )
    print("✅ 'events' tablosuna veri başarıyla yüklendi.")
except Exception as e:
    print("❌ 'events' yükleme hatası:", e)
