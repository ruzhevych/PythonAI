import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# === 1. Зчитування даних з CSV ===
# Замінити шлях до файлу, якщо інший
file_path = 'usd_uah.csv'
df = pd.read_csv(file_path)

# === 2. Фільтрація долара США ===
df = df[df['Код літерний'] == 'USD'].copy()
df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
df = df.sort_values('Дата')

# === 3. Підготовка колонок ===
df = df.rename(columns={'Дата': 'Date', 'Офіційний курс гривні, грн': 'USD_UAH'})
df['Days'] = (df['Date'] - df['Date'].min()).dt.days

# === 4. Навчання моделі ===
X = df[['Days']]
y = df['USD_UAH']
model = LinearRegression()
model.fit(X, y)

# === 5. Прогноз на 10 днів ===
last_day = df['Days'].max()
future_days = np.array([last_day + i for i in range(1, 11)]).reshape(-1, 1)
future_preds = model.predict(future_days)
future_dates = [df['Date'].max() + pd.Timedelta(days=i) for i in range(1, 11)]

# === 6. Побудова графіка ===
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['USD_UAH'], label='Історичний курс')
plt.plot(future_dates, future_preds, label='Прогноз на 10 днів', linestyle='--', color='red')
plt.xlabel('Дата')
plt.ylabel('Курс USD/UAH')
plt.title('Прогноз курсу долара до гривні на 10 днів')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
