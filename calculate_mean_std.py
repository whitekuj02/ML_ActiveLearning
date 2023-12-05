import pandas as pd

# Load preprocessed data
df = pd.read_csv('result_encoded.csv')

# Group based on StreamerName encoded in data
# However, in order to secure meaningful data, only streamers with more than 1000 or more than 100 data are collected.
grouped_dfs = [group for _, group in df.groupby('encoded_StreamerName') if len(group) >= 1000]

# Create an empty DataFrame to store the calculated data
calculated_df = pd.DataFrame(columns=[
    'encoded_StreamerName',
    'watch_time_mean',
    'watch_time_std',
    'start_time_median',
    'start_time_std',
    'stop_time_median',
    'stop_time_std'
])

# Calculate grouped data one by one using loop statements
for grouped_df in grouped_dfs:
	# The HH:MM format of the time in the data is calculated as minutes.
	streamer_name = grouped_df['encoded_StreamerName'].iloc[0]
	grouped_df['StartTime'] = grouped_df['StartTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
	grouped_df['StopTime'] = grouped_df['StopTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

    # Calculate mean and standard deviation for WatchTime
	watch_time_mean = grouped_df['WatchTime'].mean()
	watch_time_std = grouped_df['WatchTime'].std()

	# Add 24 hours to values whose end time is earlier than the start time.
	# ex) start: 23:50, stop: 00:10 => 24:10
	mask = grouped_df['StartTime'] > grouped_df['StopTime']
	selected_rows = grouped_df[mask]
	grouped_df.loc[mask, 'StopTime'] += 1440

	from sklearn.cluster import DBSCAN
	# Select columns to use (here only "StartTime" column) -> DBScan cluster on Start_time
	X = grouped_df[["StartTime"]]

	# Create and train DBSCAN model
	dbscan = DBSCAN(eps=30, min_samples=5)
	grouped_df["Cluster"] = dbscan.fit_predict(X)

	# Check the number of points in each cluster
	cluster_counts = grouped_df["Cluster"].value_counts()

	# Select the cluster with the most points
	most_points_cluster = cluster_counts.idxmax()

	# Calculate the average or median value of selected clusters
	average_value_most_points_cluster = grouped_df.loc[grouped_df["Cluster"] == most_points_cluster, "StartTime"].median()
	std_value_most_points_cluster = grouped_df.loc[grouped_df["Cluster"] == most_points_cluster, "StartTime"].std()

	# Select columns to use (here only "StopTime" column) -> DBScan cluster on StopTime
	X = grouped_df[["StopTime"]]

	# Create and train DBSCAN model
	dbscan = DBSCAN(eps=30, min_samples=5)
	grouped_df["Cluster"] = dbscan.fit_predict(X)

	# Check the number of points in each cluster
	cluster_counts = grouped_df["Cluster"].value_counts()

	# Select the cluster with the most points
	most_points_cluster = cluster_counts.idxmax()

	# Calculate the average or median value of selected clusters
	average_value_most_points_cluster_stop = grouped_df.loc[grouped_df["Cluster"] == most_points_cluster, "StopTime"].mean()
	std_value_most_points_cluster_stop = grouped_df.loc[grouped_df["Cluster"] == most_points_cluster, "StopTime"].std()

	# Append the calculated data to the new DataFrame
	calculated_df = calculated_df._append({
		'encoded_StreamerName': streamer_name,
		'watch_time_mean': watch_time_mean,
		'watch_time_std': watch_time_std,
		'start_time_median': average_value_most_points_cluster,
		'start_time_std': std_value_most_points_cluster,
		'stop_time_median': average_value_most_points_cluster_stop,
		'stop_time_std': std_value_most_points_cluster_stop
	}, ignore_index=True)

# Save preprocessed data as csv file
calculated_df.to_csv('calculated_mean_std_result.csv', index=False)