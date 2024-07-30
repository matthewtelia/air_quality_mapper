import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from scipy import stats

#extract name from file path
def extract_mod_name(file_path):
    # Extracts the MOD name from the file path
    base_name = os.path.basename(file_path)
    mod_name = base_name.split('_')[0]  # Adjust the split based on your file naming convention
    return mod_name

#load data from csv files and extract the name from each of the file paths
def load_data(mod_path,mod_raw_path, google_path):
    #read in quantaq and google data
    mod_data = pd.read_csv(mod_path)
    mod_raw_data = pd.read_csv(mod_raw_path)
    google_data = pd.read_csv(google_path)
   
    #extract mod name
    mod_name = extract_mod_name(mod_path)
    mod_raw_name = extract_mod_name(mod_raw_path)
    
    #extract google name
    google_name = extract_mod_name(google_path)
    
    return mod_data, mod_raw_data, google_data, mod_name, mod_raw_name, google_name

#process the quantaq data from dataframe
def process_mod_data(mod_data,mod_raw_data,mod_name):
    mod_data['timestamp'] = pd.to_datetime(mod_data['timestamp']) #convert timestampe to datetime
    mod_data['timestamp'] = mod_data['timestamp'].dt.tz_localize('UTC') #set timezone to UTC

    mod_raw_data['timestamp'] = pd.to_datetime(mod_raw_data['timestamp']) #convert timestampe to datetime
    mod_raw_data['timestamp'] = mod_raw_data['timestamp'].dt.tz_localize('UTC') #set timezone to UTC

    
    #set timestamp as index 
    mod_data.set_index('timestamp', inplace=True) 
    # print(f"mod_data after setting time_stamp as index {mod_data.head()}")

    #set timestamp as index 
    mod_raw_data.set_index('timestamp', inplace=True) 
    # print(f"mod_data after setting time_stamp as index {mod_data.head()}")
    print(f"Number of rows in mod_data: {len(mod_data)}")

    merged_mod_data = pd.merge(mod_data, mod_raw_data, on='timestamp', how='inner')
    print(f"Number of rows after time merge: {len(merged_mod_data)}")
    
    # Calculate dew point using magnus formula
    merged_mod_data['dew_point'] = (243.04 * (np.log(merged_mod_data['rh'] / 100) + ((17.625 * merged_mod_data['temp']) / (243.04 + merged_mod_data['temp']))) / (17.625 - np.log(merged_mod_data['rh'] / 100) - ((17.625 * merged_mod_data['temp']) / (243.04 + merged_mod_data['temp']))))
    dew_point = merged_mod_data['dew_point']
    print(dew_point)
    
    # Filter data based on dew point
    merged_mod_data = merged_mod_data[merged_mod_data['temp'] > merged_mod_data['dew_point']]
    print(merged_mod_data['dew_point'].head())
    print(f"Number of rows after dew point filtering: {len(merged_mod_data)}")

    merged_mod_data = merged_mod_data[merged_mod_data['flag'] == 0]
    print(f"Number of rows after flag dropping flag entries: {len(merged_mod_data)}")
    
    numeric_cols = merged_mod_data.select_dtypes(include=[np.number]).columns 
    print(numeric_cols)
    
    #resample the data to hourly
    mod_data_hourly = merged_mod_data[numeric_cols].resample('h').mean().reset_index()


    #create a new dataframe with the pm25, time, rh, and source
    mod_pm25_data = pd.DataFrame({
        'pm25': mod_data_hourly["pm25"],
        'time': pd.to_datetime(mod_data_hourly['timestamp']),
        'rh': mod_data_hourly['rh'],
        'dew_point': mod_data_hourly['dew_point'],
        'source': f'QuantAQ_{mod_name}',
        'flag': mod_data_hourly['flag']
    })

        
    return mod_pm25_data, mod_data_hourly


def process_google_data(google_data, google_name):
    google_pm25_data = google_data[google_data["code"] == "pm25"].copy()
    google_pm25_data.rename(columns={'value': 'pm25'}, inplace=True)
    google_pm25_data['time'] = pd.to_datetime(google_pm25_data['time'])
    google_pm25_data['source'] = f'Google_{google_name}'

    return google_pm25_data
def process_epa_data(google_path):
    #read csv file
    epa_data = pd.read_csv(google_path)
    epa_name = extract_mod_name(google_path)

    #set datetime
    epa_data['Date'] = pd.to_datetime(epa_data['Date'])
    
    #rename columns
    epa_data.rename(columns={'PM2.5': 'pm25'}, inplace=True)
    
    epa_data['time'] = epa_data['Date']
    epa_data['time'] = epa_data['time'].dt.tz_localize('EST').dt.tz_convert('UTC')

    epa_data['source'] = f'{epa_name}_EPA'
    return epa_data,epa_name


def plot_data(epa_data,mod_data,google_data, epa_name, mod_name, google_name):
    #plot the data
    sns.lineplot(x="time", y="pm25", data=epa_data, label=f'{epa_name} EPA')
    sns.lineplot(x="time", y="pm25", data=mod_data, label=f'QuantAQ{mod_name}')
    sns.lineplot(x="time", y="pm25", data=google_data, label=f'Google {google_name}')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def merge_data(epa_data,mod_data,epa_name,mod_name):


    #merge the data
    merged_data = pd.merge(epa_data, mod_data, on='time', how='inner')
    merged_data.rename(columns={'pm25_x': f'{epa_name} EPA PM2.5', 'pm25_y': f'QuantAQ {mod_name} PM2.5'}, inplace=True)
   
    
    # Drop rows with missing values
    merged_data.dropna(subset=[f'{epa_name} EPA PM2.5', f'QuantAQ {mod_name} PM2.5'], inplace=True)

    # Set time as the index
    merged_data['time'] = pd.to_datetime(merged_data['time'])
    
    # Plot the merged data
    sns.scatterplot(x="time", y=f'{epa_name} EPA PM2.5', data=merged_data, label=f'{epa_name} EPA PM2.5')
    sns.scatterplot(x="time", y=f'QuantAQ {mod_name} PM2.5', data=merged_data, label=f'QuantAQ {mod_name} PM2.5')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.title(f'Merged Time Series Measurements {mod_name} vs {epa_name}')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()
    
    return merged_data


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_regression_plot(epa_mod_data_merge, epa_name, mod_name):
    # Create a line for the y=x reference
    x_line = np.linspace(0, 16, 100)
    y_line = x_line

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the line with a slope of 1
    ax.plot(x_line, y_line, color='red', label='Line with slope 1')

    # Create a scatter plot with a continuous hue
    scatter = sns.scatterplot(x=epa_mod_data_merge[f'{epa_name} EPA PM2.5'], 
                              y=epa_mod_data_merge[f'QuantAQ {mod_name} PM2.5'], 
                              hue=epa_mod_data_merge['rh'], 
                              palette='RdYlGn', 
                              edgecolor=None, 
                              ax=ax)

    # Add a regression line
    sns.regplot(x=epa_mod_data_merge[f'{epa_name} EPA PM2.5'], 
                y=epa_mod_data_merge[f'QuantAQ {mod_name} PM2.5'], 
                scatter=False, 
                line_kws={'linestyle': 'dotted', 'color': 'blue'}, 
                label='Regression Line', 
                ax=ax)

    # Set labels and title
    ax.set_xlabel(f'{epa_name} EPA PM2.5')
    ax.set_ylabel(f'QuantAQ {mod_name} PM2.5')
    ax.set_title('Comparison of PM2.5 Measurements')

    # Rotate x-axis labels if needed
    plt.xticks(rotation=90)

    # Add a legend to the plot
    ax.get_legend().remove()

    # Add a color bar
    norm = plt.Normalize(epa_mod_data_merge['rh'].min(), epa_mod_data_merge['rh'].max())
    sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, label='Relative Humidity (rh)')

    # Display the plot
    plt.show()

    slope, intercept, r, p, std_err = stats.linregress(epa_mod_data_merge[f'{epa_name} EPA PM2.5'],epa_mod_data_merge[f'QuantAQ {mod_name} PM2.5'])
    print(f'QuantAQ Sensor: {mod_name} EPA Location: {epa_name} Slope: {slope}, Intercept: {intercept}, R: {r}, P: {p}, Std Err: {std_err}')


def calculate_error(merged_data, epa_name, mod_name):
    error = merged_data[f'QuantAQ {mod_name} PM2.5'] - merged_data[f'{epa_name} EPA PM2.5']
    error_df = pd.DataFrame({'time': merged_data['time'], 'error': error})
    

    sns.histplot(error_df, kde=True)
    plt.xlabel('Error')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Error {mod_name} vs {epa_name}')
    plt.show()



    plt.scatter(error_df['time'], error_df['error'], label=f'{mod_name} Error')
    plt.xlabel('Time')
    plt.ylabel('Error')
    plt.xticks(rotation=90)
    plt.title(f'Comparison of Error Over Time {mod_name} vs {epa_name}')
    plt.legend()
    plt.show()
    
    return error_df



# Paths to the data files

chelsea_epa_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\EPA\\chelsea_epa\\chelsea_epa_hourly.csv'
mod_247_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00247_2024-5-18_2024-6-17.csv'
mod_247_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00247_2024-5-18_2024-6-17_raw.csv'
google_247_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\googleMOD-00247_-71.025_42.387.csv'

# Load the data
mod_247_data, mod_247_raw_data, google_247_data, mod247_name, mod247_raw_name, google247_name = load_data(mod_247_path, mod_247_raw_path, google_247_path)

# Process the data
chelsea_epa_data, chelsea_epa_name = process_epa_data(chelsea_epa_path)
mod_pm25_247_data,mod_247_hourly= process_mod_data(mod_247_data,mod_247_raw_data, mod247_name)
google_pm25_247_data = process_google_data(google_247_data, google247_name)

# Plot the data
plot_data(chelsea_epa_data,mod_pm25_247_data,google_pm25_247_data,chelsea_epa_name,mod247_name,google247_name)
epa_mod_247_data = merge_data(chelsea_epa_data,mod_pm25_247_data,chelsea_epa_name,mod247_name)

#calculate error
plot_regression_plot(epa_mod_247_data,chelsea_epa_name,mod247_name)
error_247 = calculate_error(epa_mod_247_data, chelsea_epa_name, mod247_name)


