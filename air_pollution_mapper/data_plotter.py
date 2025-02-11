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
    # print(dew_point)
    
    # Filter data based on dew point
    merged_mod_data = merged_mod_data[merged_mod_data['temp'] > merged_mod_data['dew_point']]
    # print(merged_mod_data['dew_point'].head())
    print(f"Number of rows after dew point filtering: {len(merged_mod_data)}")

    merged_mod_data = merged_mod_data[merged_mod_data['flag'] == 0]
    print(f"Number of rows after flag dropping flag entries: {len(merged_mod_data)}")
    
    numeric_cols = merged_mod_data.select_dtypes(include=[np.number]).columns 
    # print(numeric_cols)
    
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
    sns.lineplot(x="time", y="pm25", data=epa_data, label=f'{epa_name.capitalize()} EPA')
    sns.lineplot(x="time", y="pm25", data=mod_data, label=f'QuantAQ{mod_name}')
    sns.lineplot(x="time", y="pm25", data=google_data, label=f'Google {google_name}')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def merge_data(epa_data,mod_data,google_pm_data,epa_name,mod_name,google_name):

    # Print the time zones for all three data sets
    print(f'EPA Time Zone: {epa_data["time"].dt.tz}')
    print(f'QuantAQ Time Zone: {mod_data["time"].dt.tz}')
    print(f'Google Time Zone: {google_pm_data["time"].dt.tz}\n')

    print(f'Number of entries in EPA data: {len(epa_data)}')
    print(f'Number of entries in QuantAQ data: {len(mod_data)}')
    print(f'Number of entries in Google data: {len(google_pm_data)}')

    #merge the data
    merged_data = pd.merge(epa_data, mod_data, on='time', how='inner')
    merged_data.rename(columns={'pm25_x': f'{epa_name} EPA PM2.5', 'pm25_y': f'QuantAQ {mod_name} PM2.5'}, inplace=True)
   
    # Merge Google data
    merged_data = pd.merge(merged_data, google_pm_data, on='time', how='inner')
    merged_data.rename(columns={'pm25': f'Google {google_name} PM2.5'}, inplace=True)
    
    # Drop rows with missing values
    merged_data.dropna(subset=[f'{epa_name} EPA PM2.5', f'QuantAQ {mod_name} PM2.5'], inplace=True)

    # Set time as the index
    merged_data['time'] = pd.to_datetime(merged_data['time'])
    
    # Calculate the number of entries in the merged data
    
    num_entries = len(merged_data)
    print(f"Number of matched entries in the merged data: {num_entries}") 

    # Plot the merged data
    sns.scatterplot(x="time", y=f'{epa_name} EPA PM2.5', data=merged_data, label=f'{epa_name} EPA PM2.5 ($\\mu$g/m$^3$)')
    sns.scatterplot(x="time", y=f'QuantAQ {mod_name} PM2.5', data=merged_data, label=f'QuantAQ {mod_name} PM2.5 ($\\mu$g/m$^3$)')
    sns.scatterplot(x="time", y=f'Google {google_name} PM2.5', data=merged_data, label=f'Google {google_name} PM2.5 ($\\mu$g/m$^3$)')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.title(f'Merged Time Series Measurements {mod_name} vs {epa_name.capitalize()}')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()
    
    return merged_data,num_entries


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
def plot_regression_plot(epa_mod_data_merge,epa_name, mod_name, google_name):
    # Create a line for the y=x reference
    x_line = np.linspace(0, 16, 100)
    y_line = x_line

    epa_pm25 = epa_mod_data_merge[f'{epa_name} EPA PM2.5']
    quantaq_pm25 = epa_mod_data_merge[f'QuantAQ {mod_name} PM2.5']
    google_pm25 = epa_mod_data_merge[f'Google {google_name} PM2.5']

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the line with a slope of 1
    ax.plot(x_line, y_line, color='red', label='Line with slope 1')

    # Create a scatter plot with a continuous hue
    scatter = sns.scatterplot(x=epa_pm25, 
                              y=quantaq_pm25, 
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
    
        # Determine the limits
    max_limit = max(ax.get_xlim()[1], ax.get_ylim()[1])
    min_limit = min(ax.get_xlim()[0], ax.get_ylim()[0])

    # Set the same limits for both x and y axes
    ax.set_xlim(min_limit, max_limit)
    ax.set_ylim(min_limit, max_limit)

    # Set labels and title
    ax.set_xlabel(f'{epa_name.capitalize()} EPA PM2.5 ($\\mu$g/m$^3$)')
    ax.set_ylabel(f'QuantAQ {mod_name} PM2.5 ($\\mu$g/m$^3$)')
    ax.set_title('Comparison of PM2.5 Measurements')

    # Rotate x-axis labels if needed
    plt.xticks(rotation=90)

    # Add a legend to the plot
    ax.get_legend().remove()

    # Add a color bar
    norm = plt.Normalize(epa_mod_data_merge['rh'].min(), epa_mod_data_merge['rh'].max())
    sm = plt.cm.ScalarMappable(cmap='RdYlGn', norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, label='Relative Humidity (%)')

    # Display the plot
    plt.show()

    slope, intercept, r, p, std_err = stats.linregress(epa_mod_data_merge[f'{epa_name} EPA PM2.5'],epa_mod_data_merge[f'QuantAQ {mod_name} PM2.5'])
    
    # Round the results to the desired number of decimal places
    decimal_places = 3  # Change this to the number of decimal places you want
    slope = round(slope, decimal_places)
    intercept = round(intercept, decimal_places)
    r_squared = round(r**2, decimal_places)
    p_value = round(p, decimal_places)
    std_err = round(std_err, decimal_places)

    # Print the results
    print(f'QuantAQ Sensor: {mod_name}') 
    print(f'EPA Location: {epa_name.capitalize()}')
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"R-squared: {r_squared}")
    if p < 0.001:
        print(f"P-value: < 0.001")
    else:
        print(f"P-value: {p_value}")
    print(f"Standard error: {std_err}")
 
 #############################################################################


 # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the line with a slope of 1
    ax.plot(x_line, y_line, color='red', label='Line with slope 1')

    # Create a scatter plot with a continuous hue
    scatter = sns.scatterplot(x=epa_pm25, 
                              y=google_pm25, 
                              hue=epa_mod_data_merge['rh'], 
                              palette='RdYlGn', 
                              edgecolor=None, 
                              ax=ax)

    # Add a regression line
    sns.regplot(x=epa_mod_data_merge[f'{epa_name} EPA PM2.5'], 
                y=epa_mod_data_merge[f'Google {google_name} PM2.5'], 
                scatter=False, 
                line_kws={'linestyle': 'dotted', 'color': 'blue'}, 
                label='Regression Line', 
                ax=ax)
    
        # Determine the limits
    max_limit = max(ax.get_xlim()[1], ax.get_ylim()[1])
    min_limit = min(ax.get_xlim()[0], ax.get_ylim()[0])

    # Set the same limits for both x and y axes
    ax.set_xlim(min_limit, max_limit)
    ax.set_ylim(min_limit, max_limit)

    # Set labels and title
    ax.set_xlabel(f'{epa_name.capitalize()} EPA PM2.5 ($\\mu$g/m$^3$)')
    ax.set_ylabel(f'Google {google_name} PM2.5 ($\\mu$g/m$^3$)')
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

    slope, intercept, r, p, std_err = stats.linregress(epa_mod_data_merge[f'{epa_name} EPA PM2.5'],epa_mod_data_merge[f'Google {google_name} PM2.5'])
    
    # Round the results to the desired number of decimal places
    decimal_places = 3  # Change this to the number of decimal places you want
    slope = round(slope, decimal_places)
    intercept = round(intercept, decimal_places)
    r_squared = round(r**2, decimal_places)
    p_value = round(p, decimal_places)
    std_err = round(std_err, decimal_places)

    # Print the results
    print(f'Google Prediction: {google_name}') 
    print(f'EPA Location: {epa_name.capitalize()}')
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"R-squared: {r_squared}")
    if p < 0.001:
        print(f"P-value: < 0.001")
    else:
        print(f"P-value: {p_value}")
    print(f"Standard error: {std_err}")

def calculate_error_metrics(actual, predicted):
    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    re = np.mean(np.abs((actual - predicted) / actual))
    return mae, rmse, re

 # %%
def calculate_error(merged_data, epa_name, mod_name, google_name):
    # Calculate the residuals between the QuantAQ and EPA PM2.5 values
    error_quantaq = merged_data[f'QuantAQ {mod_name} PM2.5'] - merged_data[f'{epa_name} EPA PM2.5']
    error_df = pd.DataFrame({'time': merged_data['time'], 'Error Quantaq': error_quantaq})

    #calculate residuals between google and epa
    error_google = merged_data[f'Google {google_name} PM2.5'] - merged_data[f'{epa_name} EPA PM2.5']
    error_df['Error Google'] = error_google
    

    #plot residuals in histogram
    sns.histplot(error_df, kde=True)
    plt.xlabel('Error')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Residuals {mod_name} vs {epa_name}')
    plt.show()


    #plot residuals over time
    plt.scatter(error_df['time'], error_df['Error Quantaq'], label=f'{mod_name} Error')
    plt.scatter(error_df['time'], error_df['Error Google'], label=f'{google_name} Error')
    plt.xlabel('Time')
    plt.ylabel('Error')
    plt.xticks(rotation=90)
    plt.title(f'Comparison of Residuals Over Time {mod_name} vs {epa_name.capitalize()}')
    plt.legend()
    plt.show()
    
    epa_data = merged_data[f'{epa_name} EPA PM2.5']
    quantaq_data = merged_data[f'QuantAQ {mod_name} PM2.5']
    google_data = merged_data[f'Google {google_name} PM2.5']

    # Calculate error metrics for QuantAQ data
    mae_quantaq, rmse_quantaq, re_quantaq = calculate_error_metrics(epa_data, quantaq_data)

     # Print error metrics
    print('\nQuantAQ Error Metrics')
    decimal_places = 3  # Change this to the number of decimal places you want
    print(f"Mean Absolute Error (MAE) QuantAQ: {round(mae_quantaq, decimal_places)}")
    print(f"Root Mean Square Error (RMSE) QuantAQ: {round(rmse_quantaq,decimal_places)}")
    print(f"Relative Error (RE) QuantAQ: {round(re_quantaq,decimal_places)}")

    # Calculate error metrics for Google data
    mae_google, rmse_google, re_google = calculate_error_metrics(epa_data, google_data)

    # Print error metrics
    print('\nGoogle Error Metrics')
    print(f"Mean Absolute Error (MAE) Google: {round(mae_google,decimal_places)}")
    print(f"Root Mean Square Error (RMSE) Google: {round(rmse_google,decimal_places)}")
    print(f"Relative Error (RE) Google: {round(re_google,decimal_places)}")

    return error_df, mae_quantaq, rmse_quantaq, re_quantaq, mae_google, rmse_google, re_google


if __name__ == "__main__":

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
    merged_247_data,merged_247_entries = merge_data(chelsea_epa_data,mod_pm25_247_data,google_pm25_247_data,chelsea_epa_name,mod247_name,google247_name)

    # %%

    #calculate error
    plot_regression_plot(merged_247_data,chelsea_epa_name,mod247_name,google247_name)


    # %%
    error_247, mae_247_quantaq, rmse_247_quantaq, re_247_quantaq, mae_247_google, rmse_247_google, re_247_google = calculate_error(merged_247_data, chelsea_epa_name, mod247_name, google247_name)



