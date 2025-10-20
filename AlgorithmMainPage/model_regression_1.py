import pandas as pd
import numpy as np
import math


df = pd.read_csv('filles/abalone.csv')
# print(df.head())
# print(df.info())
# print(df.describe().to_string())
# print(df.isnull().sum())

data = pd.get_dummies(df, columns=["Sex"], drop_first=True)
# print(data.head().to_string())

Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1

data = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
# print(data.head().to_string())
# print(data.shape)


X = data.drop(['Rings'], axis=1)
y = data['Rings']



from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("MSE:", mean_squared_error(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:",math.sqrt(mean_squared_error(y_test, y_pred)))


final_model = LinearRegression()
final_model.fit(X ,y)
y_hat = final_model.predict(X)

print(X.columns)



# from joblib import  dump
# dump(final_model,'model_regression_1_alabama.joblib')