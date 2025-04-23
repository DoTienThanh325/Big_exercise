import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.decomposition import PCA
df = pd.read_csv('Problem 1/results.csv')
columns_str = ['Unnamed: 0', 'Player', 'Nation', 'Team', 'Pos', 'Age']
df_2 = df.drop(columns=columns_str, errors='ignore')
df_2 = df_2.replace('N/a', 0)
df_2 = df_2.fillna(0)   

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_2)

inertias = []
k_range = range(1,11)

for k in k_range:
    k_means = KMeans(n_clusters=k, random_state=42)
    labels = k_means.fit_predict(scaled_features)
    inertias.append(k_means.inertia_)

plt.figure(figsize=(12,5))
plt.plot(k_range, inertias, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.grid(True)
plt.savefig('Problem 3/elbow_method.png')

elbow_pos = KneeLocator(k_range, inertias, curve='convex', direction='decreasing')
k = elbow_pos.knee
print(f'Điểm elbow chon được là: {k}')
print(f'Chọn {k} là do từ {k - 1} đến {k} thì inertia giảm mạnh còn từ {k} đến {k+1} và sau nữa độ giảm inertia không còn lớn như trước')

target_name = ['Group_' + str(x) for x in range(1,k+1)]
k_means = KMeans(n_clusters=k, random_state=42)
cluster = k_means.fit_predict(scaled_features)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)
plt.figure(figsize=(12,8))
for i in range(k):
    plt.scatter(
        pca_result[cluster == i, 0],
        pca_result[cluster == i, 1],
        label=target_name[i],
        cmap='viridis',
        s=50
    )
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('PCA of Epl player in 2024 - 2025 season')
plt.savefig('Problem 3/cluster_pca_2d.png')