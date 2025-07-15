# scripts/ab_test_simulation.py

import pandas as pd
import numpy as np
from scipy import stats
import os

# Dosyaları kaydetmek için data klasörü oluştur
os.makedirs("../data", exist_ok=True)

# RNG için sabit seed
np.random.seed(42)

# Kullanıcı sayıları
n_A = 490
n_B = 510

# Simülasyon: Kontrol grubu (A)
arpu_A = np.random.normal(loc=5.0, scale=1.5, size=n_A)

# Simülasyon: Test grubu (B) → yeni özellik
arpu_B = np.random.normal(loc=5.6, scale=1.5, size=n_B)

# VeriFrame oluştur
df_A = pd.DataFrame({
    'user_id': [f'A_{i}' for i in range(n_A)],
    'group': 'A',
    'arpu': arpu_A
})

df_B = pd.DataFrame({
    'user_id': [f'B_{i}' for i in range(n_B)],
    'group': 'B',
    'arpu': arpu_B
})

ab_df = pd.concat([df_A, df_B], ignore_index=True)

# CSV olarak kaydet
ab_df.to_csv("../../data/ab_test_data.csv", index=False)

# t-testi hesapla
t_stat, p_val = stats.ttest_ind(df_A["arpu"], df_B["arpu"], equal_var=False)

# Özet tablo oluştur
summary = pd.DataFrame({
    "group": ["A", "B"],
    "mean_arpu": [df_A["arpu"].mean(), df_B["arpu"].mean()],
    "std_arpu": [df_A["arpu"].std(), df_B["arpu"].std()],
    "count": [n_A, n_B],
    "t_statistic": [t_stat]*2,
    "p_value": [p_val]*2
})

# Özet CSV'yi kaydet
summary.to_csv("../../data/ab_test_summary.csv", index=False)

print("✅ A/B test veri dosyaları oluşturuldu: ab_test_data.csv & ab_test_summary.csv")
