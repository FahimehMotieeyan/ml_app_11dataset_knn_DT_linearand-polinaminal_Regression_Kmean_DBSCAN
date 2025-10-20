import pandas as pd
import numpy as np
import math
import  matplotlib.pyplot as plt
import  seaborn as sns


data= pd.read_excel('filles/Real estate valuation data set.xlsx')
# print(data.head().to_string())
# print(data.info())
print(data.describe().to_string())
# print(df.isnull().sum())
# print(data.shape)

# plt.figure(figsize=(10, 6))
# sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
# plt.title('ماتریس همبستگی')
# plt.show()
#حذف ایکس 1 به علت کوریلیشن بسیار کم با ایگرگ و تایم سری نمی خوام برسی کنم
data=data.drop('X1 transaction date',axis=1)
# print(data.to_string())

print(data.columns)

Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1

data = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]

# print(data.shape)

X = data.drop(['Y house price of unit area'], axis=1)
y = data['Y house price of unit area']
# print(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score

# model = LinearRegression()
# model.fit(X_train, y_train)
#
# y_pred = model.predict(X_test)
#
# print("MSE:", mean_squared_error(y_test, y_pred))
# print("MAE:", mean_absolute_error(y_test, y_pred))
# print("RMSE:",math.sqrt(mean_squared_error(y_test, y_pred)))
# print("r2_score:", r2_score(y_test, y_pred))
#
# residuals = y_test - y_pred
# sns.scatterplot(x=y_pred, y=residuals)
# plt.axhline(y=0, color='r', linestyle='--')
# plt.title('نمودار باقیمانده‌ها')
# plt.show()

# MSE: 48.989410626352765
# MAE: 5.033763859325932
# RMSE: 6.999243575298174
# r2_score: 0.6171140162582718
#
# from sklearn.linear_model import Ridge
#
# ridge = Ridge(alpha=1.0)
# ridge.fit(X_train, y_train)
# y_pred = ridge.predict(X_test)
#
# print("MSE:", mean_squared_error(y_test, y_pred))
# print("MAE:", mean_absolute_error(y_test, y_pred))
# print("RMSE:",math.sqrt(mean_squared_error(y_test, y_pred)))
# print("r2_score:", r2_score(y_test, y_pred))

# residuals = y_test - y_pred
# sns.scatterplot(x=y_pred, y=residuals)
# plt.axhline(y=0, color='r', linestyle='--')
# plt.title('نمودار باقیمانده‌ها ridge')
# plt.show()


# MSE: 57.7897895097978
# MAE: 5.442945257931643
# RMSE: 7.601959583541457
# r2_score: 0.5483329943393183
#
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import make_pipeline
import math

# from sklearn.preprocessing import StandardScaler
#
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# ایجاد مدل رگرسیون چندجمله‌ای درجه 2 (میتوانید درجه را تغییر دهید)
degree = 2  # میتوانید 3 یا بیشتر هم آزمایش کنید
poly_model = make_pipeline(
    PolynomialFeatures(degree=degree),
    LinearRegression()
)

# آموزش مدل
poly_model.fit(X_train, y_train)


y_pred_poly = poly_model.predict(X_test)


print("معیارهای رگرسیون چندجمله‌ای (درجه {}):".format(degree))
print("MSE:", mean_squared_error(y_test, y_pred_poly))
print("MAE:", mean_absolute_error(y_test, y_pred_poly))
print("RMSE:", math.sqrt(mean_squared_error(y_test, y_pred_poly)))
print("R2_score:", r2_score(y_test, y_pred_poly))
#
# residuals = y_test - y_pred
# sns.scatterplot(x=y_pred, y=residuals)
# plt.axhline(y=0, color='r', linestyle='--')
# plt.title('نمودار باقیمانده‌ها Polynomial')
# plt.show()

# MSE: 42.53069208337573
# MAE: 4.775218557566404
# RMSE: 6.5215559557038025
# R2_score: 0.667593349882025



final_model = make_pipeline(
    PolynomialFeatures(degree=2),
    LinearRegression()
)

# آموزش مدل بر روی تمام داده‌ها
final_model.fit(X, y)

# نمایش نام ستون‌ها
print("ویژگی‌های مدل:")
print(X.columns)

# # n_data = [[12,100.4,5,24.4,121]]
# n_data = pd.DataFrame([[12, 100.4, 5, 24.4, 121]], columns=X.columns)
# print(final_model.predict(n_data))

#
# from joblib import dump
# dump(final_model, 'model_polynomial_regression_degree2.joblib')


