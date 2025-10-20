import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import joblib
from sklearn.decomposition import PCA


df = pd.read_csv('filles/bupa.data.csv', header=None, names=['raw_data'])
df[["Mcv", "Alkphos", "Sgpt", "Sgot", "Gammagt", "Drinks", "Selector"]] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)

df = df.apply(pd.to_numeric, errors='coerce')

# print(df.head().to_string())
# print(df.info())
# print(df.describe().to_string())
# print(df.isnull().sum())

z_scores = stats.zscore(df)
df = df[(z_scores < 3).all(axis=1)]
#
scaler = MinMaxScaler()
df2= pd.DataFrame(scaler.fit_transform(df), columns=df.columns)



########
# kmeans = KMeans(n_clusters=3, random_state=42)
# kmeans.fit(df2)
#
# df['Cluster'] = kmeans.labels_
# silhouette_avg = silhouette_score(df2, kmeans.labels_)
# print(f"Silhouette Score: {silhouette_avg:.3f}")
# print(f"Inertia: {kmeans.inertia_:.2f}")
# ###تیون کردن
# inertia = []
# silhouette_scores = []
# for k in range(2, 10):
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(df2)
#     inertia.append(kmeans.inertia_)
#     silhouette_scores.append(silhouette_score(df2, kmeans.labels_))
#
# # Plot results
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
# ax1.plot(range(2, 10), inertia, 'bx-')
# ax1.set_title('Elbow Method')
# ax2.plot(range(2, 10), silhouette_scores, 'bx-')
# ax2.set_title('Silhouette Scores')
# plt.show()

#####


final_kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = final_kmeans.fit_predict(df2)


print("Cluster distribution:")
print(df['Cluster'].value_counts())
cluster_means = df.groupby('Cluster').mean()
print(" mean feachers info in each cluster:\n")
print(cluster_means)


pca = PCA(n_components=2)
df_pca = pca.fit_transform(df2)
plt.scatter(df_pca[:, 0], df_pca[:, 1], c=df['Cluster'], cmap='viridis')
plt.title('Cluster Visualization (PCA-reduced)')
plt.show()

#import joblib

final_kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = final_kmeans.fit_predict(df2)

print("Cluster distribution:")
print(df['Cluster'].value_counts())

cluster_means = df.groupby('Cluster').mean()
print("Mean features info in each cluster:\n")
print(cluster_means.to_string())

pca = PCA(n_components=2)
df_pca = pca.fit_transform(df2)

plt.scatter(df_pca[:, 0], df_pca[:, 1], c=df['Cluster'], cmap='viridis')
plt.title('Cluster Visualization (PCA-reduced)')


# plt.savefig('cluster_visualization.png')
# plt.close()

# joblib.dump(final_kmeans, 'kmeans_model.joblib')

# joblib.dump(cluster_means, 'cluster_means.joblib')