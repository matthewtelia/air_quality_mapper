import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

def extract_mod_name(file_path):
    # Extracts the MOD name from the file path
    base_name = os.path.basename(file_path)
    mod_name = base_name.split('_')[1]  # Adjust the split based on your file naming convention
    return mod_name

def load_data(mod_path, google_path):
    mod_data = pd.read_csv(mod_path)
    google_data = pd.read_csv(google_path)
    mod_name = extract_mod_name(mod_path)
    google_name = extract_mod_name(google_path)
    return mod_data, google_data, mod_name, google_name

def process_data(mod_data, google_data, mod_name, google_name):
    mod_data['timestamp'] = pd.to_datetime(mod_data['timestamp'])
    mod_data.set_index('timestamp', inplace=True)
    numeric_cols = mod_data.select_dtypes(include=[np.number]).columns
    mod_data_hourly = mod_data[numeric_cols].resample('h').mean().reset_index()

    mod_pm25_data = pd.DataFrame({
        'pm25': mod_data_hourly["pm25"],
        'time': pd.to_datetime(mod_data_hourly['timestamp']),
        'source': f'QuantAQ_{mod_name}'
    })

    google_pm25_data = google_data[google_data["code"] == "pm25"].copy()
    google_pm25_data.rename(columns={'value': 'pm25'}, inplace=True)
    google_pm25_data['time'] = pd.to_datetime(google_pm25_data['time'])
    google_pm25_data['source'] = f'Google_{google_name}'

    pm25_data = pd.concat([mod_pm25_data, google_pm25_data])
    return pm25_data

def plot_data(pm25_data):
    sns.lineplot(x="time", y="pm25", data=pm25_data, hue="source")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=90)
    plt.show()

# Paths to the data files
mod_142_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00142_2024-5-18_2024-6-17.csv'
google_142_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\googleMOD-00142_-71.0185_42.4029.csv'
# Load the data
mod_142_data, google_142_data,mod142_name,google142_name = load_data(mod_142_path, google_142_path)
# Process the data
pm25_142_data = process_data(mod_142_data, google_142_data,mod142_name,google142_name)
# Plot the data
plot_data(pm25_142_data)

# %%
mod_247_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00247_2024-5-18_2024-6-17.csv'
google_247_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\googleMOD-00247_-71.025_42.387.csv'
# Load the data
mod_247_data, google_247_data,mod247_name,google247_name = load_data(mod_247_path, google_247_path)
# Process the data
pm25_247_data = process_data(mod_247_data, google_247_data,mod247_name,google247_name)
# Plot the data
plot_data(pm25_247_data)
# %%
