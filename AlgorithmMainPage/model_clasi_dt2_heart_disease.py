import  pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,recall_score
from sklearn.model_selection import GridSearchCV
from joblib import dump


df = pd.read_csv('filles/processed.cleveland.data.csv', header=None, names=['raw_data'])

df[["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)

# print(df.head().to_string())
# print(df.head().to_string())
# print(df.info())
# print(df.describe().to_string())
# print(df.isnull().sum())
# print(df.shape)

list_column=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
# for i in list_column:
#     print(df[i].value_counts())


numeric_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
               'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')


df['ca'] = df['ca'].replace('?', np.nan)
df['thal'] = df['thal'].replace('?', np.nan)

df['ca'].fillna(df['ca'].mode()[0], inplace=True)
df['thal'].fillna(df['thal'].mode()[0], inplace=True)
# for i in list_column:
#     print(df[i].value_counts())

numeric_list =['oldpeak','thalach','chol','trestbps','age']
for i in numeric_list:
    Q1 = df[i].quantile(0.25)
    Q3 = df[i].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[i] < (Q1 - 1.5 * IQR)) | (df[i] > (Q3 + 1.5 * IQR)))]

X = df.drop('num', axis=1)
y = df['num']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ایجاد مدل درخت تصمیم با پارامترهای پیش‌فرض
# dt_model = DecisionTreeClassifier(random_state=42)
# dt_model.fit(X_train, y_train)
# y_pred = dt_model.predict(X_test)
#
#
# print("recall:", recall_score(y_test, y_pred))
# print("\nClassification Report:\n", classification_report(y_test, y_pred))

# استفاده از class_weight='balanced'
##### وزن‌دهی سفارشی بر اساس تعداد نمونه‌ها
# class_weights = {0: 1, 1: 5, 2: 3, 3: 4, 4: 10}
# dt_model = DecisionTreeClassifier(class_weight=class_weights, random_state=42)
# dt_model.fit(X_train, y_train)
# y_pred = dt_model.predict(X_test)
#
#
# print("recall:", recall_score(y_test, y_pred, average='micro'))
# print("\nClassification Report:\n", classification_report(y_test, y_pred))
########تیون کردن هایپر پارامتر
from sklearn.model_selection import GridSearchCV

# param_grid = {
#     'max_depth': [5, 10, 15],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'max_features': ['sqrt', 'log2']
# }
#
# grid_search = GridSearchCV(DecisionTreeClassifier(class_weight='balanced', random_state=42),
#                           param_grid, cv=5, scoring='recall_macro')
# grid_search.fit(X_train, y_train)
# print("Best Parameters:", grid_search.best_params_)
# #Best Parameters: {'max_depth': 15, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2}
#############
#مدل بهینه
final_model =DecisionTreeClassifier(
    class_weight={0: 1, 1: 6, 2: 4, 3: 6, 4: 16},
    max_depth=12,
    min_samples_split=8,
    min_samples_leaf=4,
    max_features='log2',
    criterion='entropy',
    random_state=42
)

final_model.fit(X, y)

dump(final_model, 'final_model_dt2_heart_disease.joblib')




