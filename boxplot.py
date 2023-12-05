import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the data
# Assuming 'df' is your DataFrame
# If not, replace it with the actual DataFrame variable name
df = pd.read_csv('result_encoded.csv')

grouped_dfs = [group for _, group in df.groupby('encoded_StreamerName') if len(group) >= 1000]

for grouped_df in grouped_dfs:
	streamer_name = grouped_df['encoded_StreamerName'].iloc[0]
	grouped_df['StartTime'] = grouped_df['StartTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
	grouped_df['StopTime'] = grouped_df['StopTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

    # Calculate mean and standard deviation for WatchTime
	watch_time_mean = grouped_df['WatchTime'].mean()
	watch_time_std = grouped_df['WatchTime'].std()

    # Calculate mean and standard deviation for StartTime
	start_time_mean = grouped_df['StartTime'].mean()
	start_time_std = grouped_df['StartTime'].std()

    # Calculate mean and standard deviation for StopTime
	stop_time_mean = grouped_df['StopTime'].mean()
	stop_time_std = grouped_df['StopTime'].std()

    # Display the results
	print(f"Streamer: {streamer_name}")
	print(f"WatchTime - Mean: {watch_time_mean}, Standard Deviation: {watch_time_std}")
	print(f"StartTime - Mean: {start_time_mean}, Standard Deviation: {start_time_std}")
	print(f"StopTime - Mean: {stop_time_mean}, Standard Deviation: {stop_time_std}")
	print("\n")

