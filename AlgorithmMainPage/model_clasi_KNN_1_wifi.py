import pandas as pd
import numpy as np
import math


data = pd.read_csv('filles/wifi_localization.csv')
# print(data.head())
# print(data.info())
# print(data.describe().to_string())
# print(data.isnull().sum())
# print(data.shape)

# حذف داده‌های تکراری
# data.drop_duplicates(inplace=True)
# print(data.shape)

# print(data['Room'].value_counts())


wifi_columns = ['Wifi 1', 'Wifi 2', 'Wifi 3', 'Wifi 4', 'Wifi 5', 'Wifi 6', 'Wifi 7']



def remove_outliers_iqr(data, columns):
    clean_data = data.copy()
    for col in columns:
        Q1 = clean_data[col].quantile(0.25)
        Q3 = clean_data[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # فیلتر کردن داده‌های خارج از محدوده IQR
        clean_data = clean_data[(clean_data[col] >= lower_bound) & (clean_data[col] <= upper_bound)]
    return clean_data


# اعمال تابع روی داده‌ها
data = remove_outliers_iqr(data, wifi_columns)
# print(data.shape)

from sklearn.preprocessing import StandardScaler

X = data.drop('Room', axis=1)
y = data['Room']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
#
#
# error_rates = []
# for k in range(1, 30):
#     knn = KNeighborsClassifier(n_neighbors=k)
#     knn.fit(X_train, y_train)
#     pred = knn.predict(X_test)
#     error_rates.append(np.mean(pred != y_test))

# plt.figure(figsize=(10,6))
# plt.plot(range(1,30), error_rates, color='blue', linestyle='dashed', marker='o',
#          markerfacecolor='red', markersize=10)
# plt.title('Error Rate vs. K Value')
# plt.xlabel('K')
# plt.ylabel('Error Rate')
# plt.show()


# # optimal_k = 5
#
# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.metrics import accuracy_score
#
# # ایجاد و آموزش مدل sklearn
# sklearn_knn = KNeighborsClassifier(n_neighbors=5)
# sklearn_knn.fit(X_train, y_train)
# sklearn_preds = sklearn_knn.predict(X_test)
#
# # # محاسبه دقت
# # sklearn_acc = accuracy_score(y_test, sklearn_preds)
# # print(f'sklearn KNN Accuracy: {sklearn_acc:.2f}')


###🙏👀
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
#
# final_model = KNeighborsClassifier(n_neighbors=5)
# final_model.fit(X_scaled,y)



# # نمونه داده فرضی برای تست
# sample_input = [-52,-55,-52,-49,-63,-88,-85]
# wifi_array = np.array(sample_input).reshape(1, -1)
# wifi_scaled = scaler.transform(wifi_array)
#
# y_hat = final_model.predict(wifi_scaled)
# y_hat_prob = final_model.predict_proba(wifi_scaled)
# print(y_hat,y_hat_prob)

# ایجاد مدل نهایی KNN با k=5 روی تمام داده‌ها
final_knn = KNeighborsClassifier(n_neighbors=5)
final_knn.fit(X_scaled, y)  # آموزش روی تمام داده‌های استاندارد شده

# ذخیره مدل و اسکیلر برای استفاده آینده
# import joblib

# # ذخیره مدل
# joblib.dump(final_knn, 'final_knn_model.pkl')
#
# # ذخیره اسکیلر
# joblib.dump(scaler, 'standard_scaler.pkl')




