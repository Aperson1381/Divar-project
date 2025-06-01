import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

df = pd.read_csv('cleaned_divar_data.csv')

df = df.dropna(subset=['price','elevator', 'parking', 'storage', 'location_encoded', 'floor_number'])

features = ['elevator', 'parking', 'storage', 'location_encoded', 'floor_number']
target = 'price'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("MAE:", round(mean_absolute_error(y_test, y_pred)))
print("MSE:", round(mean_squared_error(y_test, y_pred)))
print("RMSE:", round(np.sqrt(mean_squared_error(y_test, y_pred))))
print("R^2 Score:", round(r2_score(y_test, y_pred), 3))

sample = pd.DataFrame([{
    'elevator': 1,
    'parking': 1,
    'storage': 1,
    'location_encoded': 21,  # رایج‌ترین موقعیت مکانی
    'floor_number': 1
}])

predicted_price = model.predict(sample)[0]
print(f"\n✅predict: {int(predicted_price):,} toman")