# %%
from air_quality_mapper.air_pollution_mapper.api_caller.Client import Client
from air_quality_mapper.air_pollution_mapper.api_caller.historical_conditions import historical_conditions
from air_quality_mapper.air_pollution_mapper.api_caller.utils import load_secrets
from air_quality_mapper.air_pollution_mapper.pollution_timeseries.utils import historical_conditions_to_df
import pandas as pd
import os

# %%
def load_devices(file_path, city_name):
    if os.path.isfile(file_path):
        devices = pd.read_csv(file_path)
        city_devices = devices[devices["city"] == city_name]
        return city_devices
    else:
        print(f"File does not exist: {file_path}")
        return None

# %%
def fetch_historical_conditions(devices, google_maps_api_key, output_dir):
    client = Client(key=google_maps_api_key)
    for index, row in devices.iterrows():
        location = {"longitude": row["geo.lon"], "latitude": row["geo.lat"]}
        history_conditions_data = historical_conditions(client, location, lag_time=720)  # Assuming historical_conditions is defined
        df = historical_conditions_to_df(history_conditions_data)  # Assuming historical_conditions_to_df is defined
        output_path = os.path.join(output_dir, f'{row["sn"]}_{row["geo.lon"]}_{row["geo.lat"]}.csv')
        df.to_csv(output_path)

# %%
def plot_data(data, codes):
    import seaborn as sns
    g = sns.relplot(
        x="time",
        y="value",
        data=data[data["code"].isin(codes)],
        kind="line",
        col="name",
        col_wrap=4,
        hue="type",
        height=4,
        facet_kws={'sharey': False, 'sharex': False}
    )
    g.set_xticklabels(rotation=90)


# %%
# Example usage
secrets = load_secrets()  # Assuming load_secrets is defined
GOOGLE_MAPS_API_KEY = secrets["GOOGLE_MAPS_API_KEY"]
file_path = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\quantaq\\quantaq_devices.csv'
chelsea = "Chelsea"  # This can be changed to any city
output_dir = 'C:\\Users\\eliam\\OneDrive - Northeastern University\\Documents\\GitHub\\data_products_compare\\data\\google'

# %%
chelsea_devices = load_devices(file_path, chelsea)

# %%
if chelsea_devices is not None:
    fetch_historical_conditions(chelsea_devices, GOOGLE_MAPS_API_KEY, output_dir)

# %%
devices = pd.read_csv(file_path)
if devices is not None:
    fetch_historical_conditions(devices, GOOGLE_MAPS_API_KEY, output_dir)

