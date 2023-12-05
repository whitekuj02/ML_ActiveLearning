import pandas as pd

# # Load data before preprocessing
# column_names = ['UserID', 'StreamID', 'StreamerName', 'TimeStart', 'TimeStop']
# df = pd.read_csv('100k_a.csv', names=column_names)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# # describe raw data
# print(df)
# print(df.describe().drop('count'))

# import matplotlib.pyplot as plt

# plt.figure(figsize=(12, 8))
# # Show the frequency of TimeStop relative to TimeStart
# plt.scatter(df['TimeStart'], df['TimeStop'], alpha=0.5)
# plt.title('TimeStart vs. TimeStop', fontsize=22)
# plt.xlabel('TimeStart', fontsize=18)
# plt.ylabel('TimeStop', fontsize=18)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.grid(True)
# plt.show()

# Load data after preprocessing
data = pd.read_csv('result_encoded.csv')
print(data.describe().drop(['StreamID', 'TimeStart', 'TimeStop'], axis=1))
print(data[['UserID', 'encoded_StreamerName', 'StartTime', 'StopTime', 'WatchTime']])

# # Group by StreamerName
# grouped_dfs = [group for _, group in data.groupby('encoded_StreamerName') if len(group) >= 50]

# plt.figure(figsize=(12, 8))
# for i, df in enumerate(grouped_dfs):
#     # Show frequency by StreamerName
#     plt.hist(df['encoded_StreamerName'], bins=1, alpha=0.5, label=f'DF{i + 1}', edgecolor='black')

# # Show frequency by StreamerName
# plt.title('Histogram of StreamerName', fontsize=22)
# plt.xlabel('StreamerName', fontsize=18)
# plt.ylabel('Frequency', fontsize=18)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.grid(True)
# plt.show()

# # Group by UserID
# grouped_dfs = [group for _, group in data.groupby('UserID') if len(group) >= 50]

# plt.figure(figsize=(12, 8))
# for i, df in enumerate(grouped_dfs):
#     # Show frequency by UserId
#     plt.hist(df['UserID'], bins=1, alpha=0.5, label=f'DF{i + 1}', edgecolor='black')

# # Show frequency by UserId
# plt.title('Histogram of UserID', fontsize=22)
# plt.xlabel('UserID', fontsize=18)
# plt.ylabel('Frequency', fontsize=18)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.grid(True)
# plt.show()

# # change the shape of time
# # ex. 01:40 => 1 * 60 + 40 = 100
# data['StartTime_min'] = data['StartTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
# data['StopTime_min'] = data['StopTime'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

# # Show the frequency of stop time relative to start time
# plt.figure(figsize=(12, 8))
# plt.hist2d(data['StartTime_min'], data['StopTime_min'], bins=(50, 50), cmap='Blues')
# plt.colorbar(label='Frequency')
# plt.xlabel('Start Time (minutes)', fontsize=18)
# plt.ylabel('Stop Time (minutes)', fontsize=18)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.title('Start Time vs. Stop Time Histogram', fontsize=22)
# plt.show()
