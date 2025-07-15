# simulate_game_data.py
import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta
import os

# Veri klasörü
os.makedirs("data", exist_ok=True)

# Parametreler
NUM_USERS = 1000 ## Demo olarak 1000 kullanıcı belirledim.
DAYS = 30 ## 30 gümlük alındı.
START_DATE = datetime.today() - timedelta(days=DAYS)

# Ülke, cihaz ve kaynak seçenekleri
countries = ["US", "TR", "DE", "BR", "IN"]
devices = ["iOS", "Android"]
sources = ["organic", "ad_facebook", "ad_tiktok", "referral"]

# 1. USERS CSV oluşturma
users = []

for user_id in range(1, NUM_USERS + 1):
    register_offset = np.random.randint(0, DAYS)
    register_date = START_DATE + timedelta(days=register_offset)
    users.append({
        "user_id": user_id,
        "country": random.choice(countries),
        "device_type": random.choice(devices),
        "signup_source": random.choice(sources),
        "register_date": register_date.date(),
        "user_level": np.random.randint(1, 50),
        "is_paying_user": np.random.choice([0, 1], p=[0.85, 0.15])  # %15 ödeme yapan
    })

df_users = pd.DataFrame(users)
df_users.to_csv("../data/users.csv", index=False)

# 2. EVENTS CSV
events = []
event_types = [
    "session_start", "session_end", "tutorial_complete", "level_complete",
    "purchase", "item_purchase", "ad_click", "achievement_unlock", "friend_invite"
]

event_params_templates = {
    "level_complete": lambda: {"level": np.random.randint(1, 101)},
    "purchase": lambda: {"revenue": round(np.random.uniform(0.99, 19.99), 2), "currency": "USD"},
    "item_purchase": lambda: {"item": random.choice(["SkinA", "SkinB", "BoostX"]), "price": round(np.random.uniform(0.5, 5), 2)},
    "ad_click": lambda: {"ad_type": random.choice(["rewarded", "interstitial"])},
    "achievement_unlock": lambda: {"achievement": random.choice(["FirstBlood", "Collector", "SpeedRunner"])},
    "friend_invite": lambda: {"platform": random.choice(["WhatsApp", "Instagram", "Facebook"])},
    "tutorial_complete": lambda: {},
    "session_start": lambda: {},
    "session_end": lambda: {},
}

for user in users:
    user_id = user["user_id"]
    register_date = user["register_date"]
    days_active = (datetime.today().date() - register_date).days

    for day in range(days_active):
        current_day = datetime.strptime(str(register_date), "%Y-%m-%d") + timedelta(days=day)
        session_count = np.random.poisson(1.5)  # günde ortalama 1-2 oturum

        for _ in range(session_count):
            session_start = current_day + timedelta(minutes=np.random.randint(0, 1440))
            session_end = session_start + timedelta(minutes=np.random.randint(2, 60))

            events.append({
                "event_id": str(uuid.uuid4()),
                "user_id": user_id,
                "event_name": "session_start",
                "timestamp": session_start,
                "event_params": "{}"
            })
            events.append({
                "event_id": str(uuid.uuid4()),
                "user_id": user_id,
                "event_name": "session_end",
                "timestamp": session_end,
                "event_params": "{}"
            })

            # Diğer event'ler (random ihtimallerle)
            for event in event_types:
                if event not in ["session_start", "session_end"] and np.random.rand() < 0.3:
                    events.append({
                        "event_id": str(uuid.uuid4()),
                        "user_id": user_id,
                        "event_name": event,
                        "timestamp": session_start + timedelta(minutes=np.random.randint(0, 60)),
                        "event_params": str(event_params_templates[event]())
                    })

df_events = pd.DataFrame(events)
df_events.to_csv("../data/events.csv", index=False)

print("Simülasyon veri dosyaları oluşturuldu.")
