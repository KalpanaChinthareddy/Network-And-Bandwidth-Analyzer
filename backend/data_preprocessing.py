# backend/data_preprocessing.py

import pandas as pd
import json

def preprocess_data(filename="network_data.json"):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(json.loads(line))

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    # Optional: Feature engineering (e.g., extracting time of day, rolling averages, etc.)
    df['latency_rollavg'] = df['latency'].rolling(window=5).mean()
    df['bandwidth_rollavg'] = df['bandwidth'].rolling(window=5).mean()

    # Drop any rows with NaN values (due to rolling averages)
    df.dropna(inplace=True)

    # Save the preprocessed data to CSV for training
    df.to_csv('processed_network_data.csv')
    return df

if __name__ == "__main__":
    preprocess_data()
