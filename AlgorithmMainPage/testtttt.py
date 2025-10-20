import joblib
import matplotlib.pyplot as plt


loaded_model = joblib.load('kmeans_model.joblib')
cluster_means = joblib.load('cluster_means.joblib')


img = plt.imread('cluster_visualization.png')
plt.imshow(img)
plt.axis('off')
plt.show()


# predictions = loaded_model.predict(df2_new)

# نمایش اطلاعات خوشه‌ها
print("Loaded cluster means:")
print(cluster_means)