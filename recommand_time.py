import numpy as np
import pandas as pd

# Load previously calculated data using DBScan
df = pd.read_csv('calculated_mean_std_result.csv')

# Taking the natural logarithm of the standard deviation
df['watch_time_std'] = np.log(df['watch_time_std']) * 10
df['start_time_std'] = np.log(df['start_time_std']) * 10
df['stop_time_std'] = np.log(df['stop_time_std']) * 10

# Apply to mean using edited standard deviation
df['start_time_median'] = df['start_time_median'] - df['start_time_std']
df['stop_time_median'] = df['stop_time_median'] + df['stop_time_std']

from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

# Select which columns to use (only the "start_time_median" and "stop_time_median" columns are used here)
X = df[["start_time_median", "stop_time_median"]]

# Create and train DBSCAN model
dbscan = DBSCAN(eps=20, min_samples=5)
df["Cluster"] = dbscan.fit_predict(X)

# Check the number of points in each cluster
cluster_counts = df["Cluster"].value_counts()

# Select the cluster with the most points
most_points_cluster = cluster_counts.idxmax()

# Calculate the mean and standard deviation of "start_time_median" and "stop_time_median" for selected clusters
cluster_mean = df.loc[df["Cluster"] == most_points_cluster, ["start_time_median", "stop_time_median"]].mean()
cluster_std = df.loc[df["Cluster"] == most_points_cluster, ["start_time_median", "stop_time_median"]].std()

print("Most Points Cluster:", most_points_cluster)
print("Cluster Mean:")
print(cluster_mean)
print("Cluster Standard Deviation:")
print(cluster_std)

print("추천 시간")
print("시작 시간")
print(int((cluster_mean.start_time_median - cluster_std.start_time_median) / 60), ":", int((cluster_mean.start_time_median - cluster_std.start_time_median) % 60))
print("종료 시간")
print(int((cluster_mean.stop_time_median + cluster_std.stop_time_median) / 60), ":", int((cluster_mean.stop_time_median + cluster_std.stop_time_median) % 60))

# Scatterplot for clustering using DBScan
plt.scatter(df["start_time_median"], df["stop_time_median"], c=df["Cluster"], cmap="viridis", marker="o", alpha=0.5)
plt.title("DBSCAN Clustering Results")
plt.xlabel("start_time_median")
plt.ylabel("stop_time_median")
plt.show()
