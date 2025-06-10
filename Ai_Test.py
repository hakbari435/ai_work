from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt

# بارگذاری دیتاست
data = fetch_california_housing()
print(data)
df = pd.DataFrame(data.data, columns=data.feature_names)
df['Price'] = data.target

# انتخاب ویژگی و هدف
X = df[['MedInc','HouseAge']]  # درآمد متوسط منطقه
y = df['Price']     # قیمت خانه

# تقسیم داده‌ها
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# آموزش مدل
model = LinearRegression()
model.fit(X_train, y_train)

# پیش‌بینی و ارزیابی
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"MSE (میانگین مربعات خطا): {mse:.3f}")


plt.scatter(X_test['MedInc'], y_test, color='blue', alpha=0.5, label='واقعی')
plt.scatter(X_test['MedInc'], y_pred, color='red', alpha=0.5, label='پیش‌بینی‌شده')
plt.xlabel('درآمد متوسط منطقه (MedInc)')
plt.ylabel('قیمت خانه (x100,000 دلار)')
plt.title('مقایسه قیمت واقعی و پیش‌بینی‌شده')
plt.legend()
plt.grid(True)
plt.show()