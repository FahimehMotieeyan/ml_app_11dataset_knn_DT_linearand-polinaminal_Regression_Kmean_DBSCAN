import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
#


df = pd.read_csv('filles/Qualitative_Bankruptcy.data.csv', header=None, names=['raw_data'])

df[['Industrial Risk', 'Management Risk', 'Financial Flexibility', 'Credibility','Competitiveness', 'Operating Risk', 'class']] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)

# print(df.head().to_string())
# print(df.info())
# print(df.describe().to_string())
# print(df.isnull().sum())
# print(df.shape)

# list_column=['Industrial Risk', 'Management Risk', 'Financial Flexibility', 'Credibility','Competitiveness', 'Operating Risk', 'class']
# # for i in list_column:
# #     print(df[i].value_counts())
#
# #الگوریتم به داده پرت حساس نیست 😅
# le = LabelEncoder()
# for col in list_column:
#     df[col] = le.fit_transform(df[col])
#
# # print(df.head().to_string())
#
# X = df.drop('class', axis=1)
# y = df['class']
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#

from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from joblib import dump

X = df.drop('class', axis=1)
y = df['class']

encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)

final_model = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
final_model.fit(X_encoded, y)


dump(final_model, 'final_model_dt1_Bankruptcy.joblib')
dump(encoder, 'encoder_dt1_Bankruptcy.joblib')

