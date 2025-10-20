import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from scipy import stats
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
#


df = pd.read_csv('filles/car.data.csv', header=None, names=['raw_data'])

df[['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)

# print(df.head())

# print(df.info())
# print(df.describe().to_string())
# print(df.isnull().sum())
# print(df.shape)

# print("مقادیر منحصر به فرد doors:", df['doors'].unique())
# print("مقادیر منحصر به فرد doors:", df['doors'].value_counts())
# print("مقادیر منحصر به فرد persons:", df['persons'].unique())
# print("مقادیر منحصر به فرد persons:", df['persons'].value_counts())

df['doors'] = df['doors'].replace('5more', '5').astype(int)
df['persons'] = df['persons'].replace('more', '5').astype(int)
# print(df.info())



# لیست ستون‌های کیفی
categorical_cols = ['buying', 'maint', 'lug_boot', 'safety','class']


label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# print(df.head().to_string())

numeric_cols = ['doors', 'persons']
z_scores = np.abs(stats.zscore(df[numeric_cols]))
threshold = 3
df = df[(z_scores < threshold).all(axis=1)]

X = df.drop('class', axis=1)
y = df['class']


scaler = StandardScaler()
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
# print(X.to_string())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

error_rates = []
for k in range(1, 30):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    pred = knn.predict(X_test)
    error_rates.append(np.mean(pred != y_test))

# plt.figure(figsize=(10,6))
# plt.plot(range(1,30), error_rates, color='blue', linestyle='dashed', marker='o',
#          markerfacecolor='red', markersize=10)
# plt.title('Error Rate vs. K Value')
# plt.xlabel('K')
# plt.ylabel('Error Rate')
# plt.show()

# # یافتن K با کمترین نرخ خطا
# best_k = np.argmin(error_rates) + 1  # +1 چون range از 1 شروع می‌شود
# print(f"بهترین مقدار K: {best_k} با نرخ خطا: {min(error_rates):.4f}")

# knn = KNeighborsClassifier(n_neighbors=8)
# knn.fit(X_train, y_train)
#
# train_error = np.mean(knn.predict(X_train) != y_train)
# test_error = np.mean(knn.predict(X_test) != y_test)
#
# # print(f"K=8 -> Train Error: {train_error:.3f}, Test Error: {test_error:.3f}")
# y_pred = knn.predict(X_test)
# print(f"Accuracy after outlier removal: {accuracy_score(y_test, y_pred):.2f}")

final_knn = KNeighborsClassifier(n_neighbors=8)
final_knn.fit(X, y)


new_data= ['med','low',2,4,'big','low']


new_processed = [
    label_encoders['buying'].transform([new_data[0]])[0],
    label_encoders['maint'].transform([new_data[1]])[0],
    new_data[2],
    new_data[3],
    label_encoders['lug_boot'].transform([new_data[4]])[0],
    label_encoders['safety'].transform([new_data[5]])[0]
]

new_array = np.array(new_processed).reshape(1, -1)
prediction = final_knn.predict(new_array)
prediction_prob = final_knn.predict_proba(new_array)
# print(prediction,prediction_prob)

import joblib

# ذخیره LabelEncoderها
joblib.dump(label_encoders, 'label_encoders_car_2.pkl')
joblib.dump(scaler, 'standard_scaler_car_2.pkl')
joblib.dump(final_knn, 'final_knn_model_car_2.pkl')

