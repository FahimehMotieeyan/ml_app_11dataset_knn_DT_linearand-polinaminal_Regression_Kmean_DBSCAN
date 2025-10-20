# import pandas as pd
# import numpy as np
# import math
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import train_test_split
# from scipy import stats
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.utils import resample
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
#
# df = pd.read_csv('filles/fertility.csv')
# # print(df)
# # print(df.info())
# # print(df.describe().to_string())
# # print(df.isnull().sum())
# # print(df.shape)
# # print(df.columns)
#
# # duplicates = df.duplicated().sum()
# # print(f"تعداد ردیف‌های تکراری: {duplicates}")
#
# # print(df['output'].value_counts())
# wifi_columns = ['season', 'age', 'childish-disease', 'trauma', 'surgical-intervention',
#                 'fevers', 'alcoholic', 'smoking', 'sitting']
#
# def remove_outliers_iqr(data, columns):
#     clean_data = data.copy()
#     for col in columns:
#         Q1 = clean_data[col].quantile(0.25)
#         Q3 = clean_data[col].quantile(0.75)
#         IQR = Q3 - Q1
#         lower_bound = Q1 - 1.5 * IQR
#         upper_bound = Q3 + 1.5 * IQR
#
#         # فیلتر کردن داده‌های خارج از محدوده IQR
#         clean_data = clean_data[(clean_data[col] >= lower_bound) & (clean_data[col] <= upper_bound)]
#     return clean_data
#
# df = remove_outliers_iqr(df, wifi_columns)
# # print(df.shape)
#
# X = df.drop('output', axis=1)
# y = df['output']
#
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)
#
# ####balance
#
#
# from sklearn.utils import resample
#
# from sklearn.utils import resample
#
# # اورسمپلینگ کلاس اقلیت
# df_minority_upsampled = resample(df[y == 'O'],
#                                 replace=True,  # اجازه تکرار نمونه‌ها
#                                 n_samples=15,  # مثلاً ۱۵ نمونه
#                                 random_state=42)
#
# # آندرسمپلینگ کلاس اکثریت
# df_majority_downsampled = resample(df[y == 'N'],
#                                   replace=False,
#                                   n_samples=15)
#
# df_balanced = pd.concat([df_minority_upsampled, df_majority_downsampled])
#
# # تقسیم داده‌های بالانس شده به X و y
# X = df_balanced.drop('output', axis=1)
# y = df_balanced['output']
# print(y.value_counts())


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, LeaveOneOut, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import resample
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# 1. بارگذاری و پیش‌پردازش داده
df = pd.read_csv('filles/fertility.csv')

# 2. حذف outlierها
numeric_cols = ['season', 'age', 'childish-disease', 'trauma',
                'surgical-intervention', 'fevers', 'alcoholic',
                'smoking', 'sitting']


def remove_outliers(df, columns):
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
    return df


df_clean = remove_outliers(df, numeric_cols)

# 3. بالانس کردن داده‌ها با اورسمپلینگ
minority = df_clean[df_clean['output'] == 'O']
majority = df_clean[df_clean['output'] == 'N']

minority_upsampled = resample(minority,
                              replace=True,
                              n_samples=len(majority),
                              random_state=42)

df_balanced = pd.concat([majority, minority_upsampled]).sample(frac=1, random_state=42)

# 4. آماده‌سازی داده‌ها
X = df_balanced.drop('output', axis=1)
y = df_balanced['output']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# # 5. آموزش و ارزیابی مدل
# def evaluate_knn(X, y, k=3):
#     loo = LeaveOneOut()
#     model = KNeighborsClassifier(n_neighbors=k, weights='distance')
#
#     # ارزیابی با Leave-One-Out
#     scores = cross_val_score(model, X, y, cv=loo, scoring='accuracy')
#     print(f'میانگین دقت: {scores.mean():.2f} (±{scores.std():.2f})')
#
#     # آموزش مدل نهایی
#     model.fit(X, y)
#     return model
#
#
# # 6. یافتن بهترین مقدار k
# k_values = range(1, 10)
# accuracies = []
#
# for k in k_values:
#     knn = KNeighborsClassifier(n_neighbors=k)
#     scores = cross_val_score(knn, X_scaled, y, cv=LeaveOneOut())
#     accuracies.append(scores.mean())
#
# best_k = k_values[np.argmax(accuracies)]
# print(f'\nبهترین مقدار k: {best_k} با دقت {max(accuracies):.2f}')

# 7. آموزش مدل نهایی با بهترین پارامترها
final_model = KNeighborsClassifier(n_neighbors=3, weights='distance')
final_model.fit(X_scaled, y)

# new = [-0,1,1,0,1,0,0.6,-1,0.5]
# new_array = np.array(new).reshape(1, -1)
# prediction = final_model.predict(new_array)
# prediction_prob = final_model.predict_proba(new_array)
# print(prediction_prob,prediction)

# 8. ذخیره مدل و اسکیلر
import joblib

joblib.dump(final_model, 'final_model_knn3_sperm.joblib')
joblib.dump(scaler, 'scaler_knn3_sperm.joblib')
