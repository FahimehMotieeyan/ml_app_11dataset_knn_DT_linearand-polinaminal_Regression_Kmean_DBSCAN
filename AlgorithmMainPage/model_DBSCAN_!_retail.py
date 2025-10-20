import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from itertools import product
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import joblib


df = pd.read_csv('filles/Wholesale customers data.csv', header=None, names=['raw_data'])


df[['Channel', 'Region', 'Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)

#
scaler = StandardScaler()
X = scaler.fit_transform(df)



# # تعریف محدوده‌های هایپرپارامترها برای جستجو
# eps_values = np.linspace(0.1, 2.0, 10)
# min_samples_values = range(2, 10)
#
# best_score = -1
# best_params = {}
# best_clusters = None
#
#
# for eps, min_samples in product(eps_values, min_samples_values):
#     try:
#
#         dbscan = DBSCAN(eps=eps, min_samples=min_samples)
#         clusters = dbscan.fit_predict(X)
#
#
#         unique_clusters = np.unique(clusters)
#         if len(unique_clusters) > 1:
#             score = silhouette_score(X, clusters)
#
#             # ذخیره بهترین مدل
#             if score > best_score:
#                 best_score = score
#                 best_params = {'eps': eps, 'min_samples': min_samples}
#                 best_clusters = clusters
#         else:
#             score = -1
#
#         print(f"eps: {eps:.2f}, min_samples: {min_samples}, silhouette_score: {score:.4f}")
#
#     except Exception as e:
#         print(f"Error with eps={eps:.2f}, min_samples={min_samples}: {str(e)}")
#
#
# print("\n\nبهترین پارامترها:")
# print(f"eps: {best_params['eps']:.2f}, min_samples: {best_params['min_samples']}")
# print(f"بهترین silhouette_score: {best_score:.4f}")
#
# # تحلیل خوشه‌های بهترین مدل
# if best_clusters is not None:
#     df['Cluster'] = best_clusters
#     print("\nتعداد نقاط در هر خوشه:")
#     print(df['Cluster'].value_counts())
#
#     # نمایش نقاط پرت
#     outliers = df[df['Cluster'] == -1]
#     print(f"\nتعداد نقاط پرت: {len(outliers)}")
#
#     # تجسم خوشه‌ها با PCA
#     from sklearn.decomposition import PCA
#     import matplotlib.pyplot as plt
#     import seaborn as sns
#
#     pca = PCA(n_components=2)
#     X_pca = pca.fit_transform(X)
#
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=best_clusters,
#                     palette='viridis', s=100, style=best_clusters)
#     plt.title(f'بهترین خوشه‌بندی DBSCAN (silhouette_score = {best_score:.2f})')
#     plt.xlabel('Component 1')
#     plt.ylabel('Component 2')
#     plt.legend(title='Cluster')
#     plt.show()
# else:
#     print("هیچ مدل مناسبی یافت نشد!")



final_dbscan = DBSCAN(eps= 1.79, min_samples=3)
final_clusters = final_dbscan.fit_predict(X)
final_score = silhouette_score(X, final_clusters)

# joblib.dump({
#     'model': final_dbscan,
#     'clusters': final_clusters,
#     'silhouette_score': final_score,
#     'features': X  # در صورت نیاز
# }, 'dbscan_results.joblib')

# تحلیل نتایج (اختیاری)
df = pd.DataFrame(X)  # یا استفاده از DataFrame اصلی شما
df['Cluster'] = final_clusters

print("توزیع خوشه‌ها:")
print(df['Cluster'].value_counts())

print("\nمیانگین ویژگی‌های هر خوشه:")
print(df.groupby('Cluster').mean())


# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X)
#
# plt.figure(figsize=(12, 8))
# sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1],
#                 hue=final_clusters, palette='viridis',
#                 style=final_clusters, s=100,
#                 edgecolor='black', alpha=0.8)
# plt.title('DBSCAN Clustering')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')
# plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.grid(True)
# plt.tight_layout()
# plt.savefig('dbscan_clusters.png', dpi=300, bbox_inches='tight')
# plt.close()