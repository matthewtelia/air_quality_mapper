# %%
from data_plotter import load_data,process_mod_data,process_google_data,plot_data,process_epa_data,plot_regression_plot,merge_data,calculate_error
from data_plotter import load_data, process_mod_data, process_google_data, plot_data, process_epa_data, plot_regression_plot, merge_data, calculate_error

# %% # 
# Paths to the data files

#QuantAQ paths
mod_247_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00247_2024-5-18_2024-6-17.csv'
mod_238_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00238_2024-5-18_2024-6-17.csv'
mod_248_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00248_2024-5-18_2024-6-17.csv'
mod_246_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00246_2024-5-18_2024-6-17.csv'
mod_257_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00257_2024-5-18_2024-6-17.csv'
mod_255_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00255_2024-5-18_2024-6-17.csv'
mod_256_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\MOD-00256_2024-5-18_2024-6-17.csv'

mod_247_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00247_2024-5-18_2024-6-17_raw.csv'
mod_238_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00238_2024-5-18_2024-6-17_raw.csv'
mod_248_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00248_2024-5-18_2024-6-17_raw.csv'
mod_246_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00246_2024-5-18_2024-6-17_raw.csv'
mod_257_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00257_2024-5-18_2024-6-17_raw.csv'
mod_255_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00255_2024-5-18_2024-6-17_raw.csv'
mod_256_raw_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaqMOD-00256_2024-5-18_2024-6-17_raw.csv'

#Google paths
google_247_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\googleMOD-00247_-71.025_42.387.csv'
google_238_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\MOD-00238_-71.056_42.325.csv'
google_248_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\MOD-00248_-71.056_42.325.csv'
google_246_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\MOD-00246_-71.083_42.33.csv'
google_257_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\MOD-00257_-71.083_42.33.csv'
google_255_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\MOD-00255_-71.056_42.325.csv'
google_256_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google\\MOD-00256_-71.083_42.33.csv'

#epa paths
chelsea_epa_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\EPA\\chelsea_epa\\chelsea_epa_hourly.csv'
rox_epa_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\EPA\\rox_epa\\rox_epa_hourly.csv'
vh_epa_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\EPA\\vh_epa\\vh_epa_hourly.csv'

#Process EPA data
chelsea_epa_data, chelsea_epa_name = process_epa_data(chelsea_epa_path)
rox_epa_data, rox_epa_name = process_epa_data(rox_epa_path)
vh_epa_data, vh_epa_name = process_epa_data(vh_epa_path)


##############################################
#Mod 247
#Chelsea Colocated
# Load the data
mod_247_data,mod_247_raw_data, google_247_data, mod247_name,mod247_raw_name, google247_name = load_data(mod_247_path, mod_247_raw_path,google_247_path)

# Process the data
mod_pm25_247_data,mod_247_hourly= process_mod_data(mod_247_data,mod_247_raw_data, mod247_name)
google_pm25_247_data = process_google_data(google_247_data, google247_name)

# Plot the data
plot_data(chelsea_epa_data,mod_pm25_247_data,google_pm25_247_data,chelsea_epa_name,mod247_name,google247_name)

epa_mod_247_data = merge_data(chelsea_epa_data,mod_pm25_247_data,chelsea_epa_name,mod247_name)
#calculate error
plot_regression_plot(epa_mod_247_data,chelsea_epa_name,mod247_name)
error_247 = calculate_error(epa_mod_247_data, chelsea_epa_name, mod247_name)

#############################################
#Mod 238
# Dorchester Colocated
# Load the data
mod_238_data, mod_238_raw_data, google_238_data, mod238_name,mod238_raw_name, google238_name = load_data(mod_238_path,mod_238_raw_path, google_238_path)
# Process the data
mod_pm25_238_data,mod_238_hourly= process_mod_data(mod_238_data,mod_238_raw_data, mod238_name)
google_pm25_238_data = process_google_data(google_238_data, google238_name)
# Plot the data
plot_data(vh_epa_data,mod_pm25_238_data,google_pm25_238_data,vh_epa_name,mod238_name,google238_name)
epa_mod_238_data = merge_data(vh_epa_data,mod_pm25_238_data,vh_epa_name,mod238_name)
#calculate error
plot_regression_plot(epa_mod_238_data,vh_epa_name,mod238_name)
error_238 = calculate_error(epa_mod_238_data, vh_epa_name, mod238_name)


#############################################
#Mod 248
#Dorchester Colocated
# Load the data
mod_248_data, mod_248_raw_data,google_248_data, mod248_name, mod_248_raw_name, google248_name = load_data(mod_248_path,mod_248_raw_path, google_248_path)
# Process the data
mod_pm25_248_data,mod_248_hourly= process_mod_data(mod_248_data,mod_248_raw_data,mod248_name)
google_pm25_248_data = process_google_data(google_248_data, google248_name)

# Plot the data
plot_data(vh_epa_data,mod_pm25_248_data,google_pm25_248_data,vh_epa_name,mod248_name,google248_name)
epa_mod_248_data = merge_data(vh_epa_data,mod_pm25_248_data,vh_epa_name,mod248_name)
#calculate error
plot_regression_plot(epa_mod_248_data,vh_epa_name,mod248_name)
#calculate error
error_248 = calculate_error(epa_mod_248_data, vh_epa_name, mod248_name)

#############################################
#Mod 246
# Roxbury Colocated
# Load the data
mod_246_data, mod_246_raw_data, google_246_data, mod246_name, mod246_raw_name,google246_name = load_data(mod_246_path, mod_246_raw_path,google_246_path)

# Process the data
mod_pm25_246_data,mod_246_hourly= process_mod_data(mod_246_data, mod_246_raw_data, mod246_name)
google_pm25_246_data = process_google_data(google_246_data, google246_name)

# Plot the data
plot_data(rox_epa_data,mod_pm25_246_data,google_pm25_246_data,rox_epa_name,mod246_name,google246_name)
epa_mod_246_data = merge_data(rox_epa_data,mod_pm25_246_data,rox_epa_name,mod246_name)
#calculate error
plot_regression_plot(epa_mod_246_data,rox_epa_name,mod246_name)
#calculate error
error_246 = calculate_error(epa_mod_246_data, rox_epa_name, mod246_name)

#############################################
#Mod 257
# Roxbury Colocated
# Load the data
mod_257_data,mod_257_raw_data, google_257_data, mod257_name,mod_257_raw_name, google257_name = load_data(mod_257_path, mod_257_raw_path,google_257_path)

# Process the data
mod_pm25_257_data,mod_257_hourly= process_mod_data(mod_257_data,mod_257_raw_data, mod257_name)
google_pm25_257_data = process_google_data(google_257_data, google257_name)

# Plot the data
plot_data(rox_epa_data,mod_pm25_257_data,google_pm25_257_data,rox_epa_name,mod257_name,google257_name)
epa_mod_257_data = merge_data(rox_epa_data,mod_pm25_257_data,rox_epa_name,mod257_name)
#calculate error
plot_regression_plot(epa_mod_257_data,rox_epa_name,mod257_name)
#calculate error
error_257 = calculate_error(epa_mod_257_data, rox_epa_name, mod257_name)

#############################################
#Mod 255
1# Dorchester Colocated
# Load the data
mod_255_data, mod_255_raw_data, google_255_data, mod255_name,mod255_raw_name, google255_name = load_data(mod_255_path,mod_255_raw_path, google_255_path)
# Process the data
mod_pm25_255_data,mod_255_hourly= process_mod_data(mod_255_data,mod_255_raw_data, mod255_name)
google_pm25_255_data = process_google_data(google_255_data, google255_name)
# Plot the data
plot_data(vh_epa_data,mod_pm25_255_data,google_pm25_255_data,vh_epa_name,mod255_name,google255_name)
epa_mod_255_data = merge_data(vh_epa_data,mod_pm25_255_data,vh_epa_name,mod255_name)
#calculate error
plot_regression_plot(epa_mod_255_data,vh_epa_name,mod255_name)
#calculate error
error_255 = calculate_error(epa_mod_255_data, vh_epa_name, mod255_name)

#############################################
#Mod 256
# Roxbury Colocated
# Load the data
mod_256_data, mod_256_raw_data, google_256_data, mod256_name,mod256_raw_name, google256_name = load_data(mod_256_path, mod_256_raw_path, google_256_path)
# Process the data
mod_pm25_256_data,mod_256_hourly= process_mod_data(mod_256_data,mod_256_raw_data, mod256_name)
google_pm25_256_data = process_google_data(google_256_data, google256_name)
# Plot the data
plot_data(rox_epa_data,mod_pm25_256_data,google_pm25_256_data,rox_epa_name,mod256_name,google256_name)
epa_mod_256_data = merge_data(rox_epa_data,mod_pm25_256_data,rox_epa_name,mod256_name)
#calculate error
plot_regression_plot(epa_mod_256_data,rox_epa_name,mod256_name)
#calculate error
error_256 = calculate_error(epa_mod_256_data, rox_epa_name, mod256_name)

