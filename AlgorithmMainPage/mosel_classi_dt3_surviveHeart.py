import  pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,recall_score
from sklearn.model_selection import GridSearchCV
from joblib import dump
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


df = pd.read_csv('filles/heart attack_survive.csv', header=None, names=['raw_data'])

df[["Survival", "Still-alive", "Age-at-heart-attack", "Pericardial-effusion", "Fractional-shortening", "Epss", "Lvdd", "Wall-motion-score", "Wall-motion-index", "Mult", "Name", "Group", "Alive-at-1",'n']] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)
# print(df.head(20).to_string())
# filtered_df = df[df['n'].notna()]
# print(filtered_df)
df = df.drop(columns='n',index=1)
columns_to_drop = ["Name", "Group", "Mult", "Still-alive", "Survival"]
df = df.drop(columns=columns_to_drop)
#print(df.describe().to_string())
# print(df.isnull().sum())
# print(df.info())
# print(df['Alive-at-1'].value_counts())


df = df.replace('?', np.nan)

df = df.astype('float64')
int_columns = ['Age-at-heart-attack', 'Pericardial-effusion', 'Alive-at-1']
for col in int_columns:
    df[col] = df[col].round().astype('Int64')

# print(df.dtypes)

num_cols = ['Age-at-heart-attack', 'Fractional-shortening', 'Epss', 'Lvdd',
            'Wall-motion-score', 'Wall-motion-index']


# df[num_cols] = df[num_cols].fillna(df[num_cols].median())

from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)
df[num_cols] = imputer.fit_transform(df[num_cols])

###تارگت ؟😅
# پر کردن با مقدار پرتکرار (برای داده‌های طبقه‌بندی)
df['Alive-at-1'] = df['Alive-at-1'].fillna(df['Alive-at-1'].mode()[0])

# df = df.dropna(subset=['Alive-at-1'])
# print(df.isnull().sum())

df['Alive-at-1'] = df['Alive-at-1'].astype(int)
df = df[df['Alive-at-1'] != 2]


# print(df['Alive-at-1'].value_counts())

X = df.drop('Alive-at-1', axis=1)
y = df['Alive-at-1']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# base_dt = DecisionTreeClassifier(random_state=42)
# base_dt.fit(X_train, y_train)
# y_pred = base_dt.predict(X_test)
#
# print("دقت (Accuracy):", accuracy_score(y_test, y_pred))
# print("دقت (recal):", recall_score(y_test, y_pred,average='micro'))
# print("\nگزارش طبقه‌بندی:")
# print(classification_report(y_test, y_pred))
#
# param_grid = {
#     'max_depth': [3, 5, 7, 10, None],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'criterion': ['gini', 'entropy']
# }
#
# # جستجوی گرید با اعتبارسنجی متقاطع
# grid_search = GridSearchCV(
#     DecisionTreeClassifier(random_state=42),
#     param_grid,
#     cv=5,
#     scoring='accuracy',
#     n_jobs=-1
# )
# grid_search.fit(X_train, y_train)
#
# # بهترین مدل
# best_dt = grid_search.best_estimator_
# print("بهترین پارامترها:", grid_search.best_params_)
# # پیش‌بینی با مدل بهبود یافته
# y_pred_best = best_dt.predict(X_test)
#
# print("دقت بهبود یافته:", accuracy_score(y_test, y_pred_best))
# print("دقت (recal):", recall_score(y_test, y_pred_best,average='micro'))
# print("\nگزارش طبقه‌بندی بهبود یافته:")
# print(classification_report(y_test, y_pred_best))
#بهترین پارامترها: {'criterion': 'entropy', 'max_depth': 5, 'min_samples_leaf': 2, 'min_samples_split': 2}

final_model =DecisionTreeClassifier(
    class_weight={0: 1, 1: 7.4},
    max_depth=5,
    min_samples_split=2,
    min_samples_leaf=2,
    criterion='entropy',
    random_state=42
)

final_model.fit(X, y)

# dump(final_model, 'final_model_dt3_heart_survive.joblib')
print(X.head(5).to_string())
print(y.value_counts())

# num_cols = ['Age-at-heart-attack', 'Fractional-shortening', 'Epss', 'Lvdd',
#             'Wall-motion-score', 'Wall-motion-index']
# for i in num_cols :
#     print(X[i].value_counts())

