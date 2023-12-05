import numpy as np
import pandas as pd
from sklearn import preprocessing

# Removal of outlier data using the IQR method
def get_outlier(df=None, column=None, weight=1.5):
    for c in column:
        quantile_25 = np.percentile(df[c].values, 25)
        quantile_75 = np.percentile(df[c].values, 75)

        iqr = quantile_75 - quantile_25
        iqr_weight = iqr * weight

        lowest = quantile_25 - iqr_weight
        highest = quantile_75 + iqr_weight

        outlier_idx = df[c][(df[c] < lowest) | (df[c] > highest)].index
        df = df.drop(outlier_idx)
    return df

# A function that calls the IQR function and removes data below 
# the top 90% (default value) based on the number of data for UserID and StreamerName.
def preprocess(df=None, weight=1.5, percent=0.1):
    # Returns after removing values less than percent based on the count of UserID
    user_name_counts = df['UserID'].value_counts().reset_index()
    user_name_counts.columns = ['UserID', 'count']
    sorted_df = user_name_counts.sort_values(by='count', ascending=False)
    top_90_percent_value = sorted_df['count'].quantile(percent)
    filtered_df = sorted_df[sorted_df['count'] <= top_90_percent_value]
    df_cleaned = df.drop(df[df['UserID'].isin(filtered_df['UserID'])].index)

    # Returns after removing values less than percent based on the count of StreamerName
    user_name_counts = df['StreamerName'].value_counts().reset_index()
    user_name_counts.columns = ['StreamerName', 'count']
    sorted_df = user_name_counts.sort_values(by='count', ascending=False)
    top_90_percent_value = sorted_df['count'].quantile(percent)
    filtered_df = sorted_df[sorted_df['count'] <= top_90_percent_value]
    df_cleaned = df.drop(df[df['StreamerName'].isin(filtered_df['StreamerName'])].index)

    # Remove outliers using IQR function based on viewing time
    df_cleaned['WatchTime'] = (df_cleaned['TimeStop'] - df_cleaned['TimeStart']) * 10
    outlier_df = get_outlier(df_cleaned, ['WatchTime'], weight)
    df_cleaned = outlier_df.reset_index(drop=True)

    return df_cleaned

# Convert data format saved in raw data to HH:MM format for easy use
def convert_to_time(minutes):
    minutes = minutes % 144
    hours = minutes // 6
    minutes = (minutes % 6) * 10
    return f"{hours:02d}:{minutes:02d}"

# Load data before preprocessing
column_names = ['UserID', 'StreamID', 'StreamerName', 'TimeStart', 'TimeStop']
df = pd.read_csv('100k_a.csv', names=column_names)
print(df)
print(df.isna().sum())

# Use the preprocessing function by parameter(dataFrame, IQR parameter, percent)
df = preprocess(df, 1.5, 0.1)

# Encoding the value of the StreamerName using the label encoder method
label_encoder = preprocessing.LabelEncoder()
encoded_column = label_encoder.fit_transform(df['StreamerName'])
df['encoded_StreamerName'] = encoded_column

# Convert values in TimeStart and TimeStop columns to hours
df['StartTime'] = df['TimeStart'].apply(convert_to_time)
df['StopTime'] = df['TimeStop'].apply(convert_to_time)
print(df)

# Randomly extract part of preprocessed data
sampled_df = df.sample(n=10000, random_state=42)
print(sampled_df)

# Save preprocessed data as csv file
sampled_df.to_csv('sampled_result1.csv', index=False)
