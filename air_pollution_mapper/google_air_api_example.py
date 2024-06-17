
# %%
import sys
import os
print(sys.path)

# %%
print(os.getcwd())


# %%
from api_caller.Client import Client
from api_caller.historical_conditions import historical_conditions
from api_caller.utils import load_secrets
from pollution_timeseries.utils import historical_conditions_to_df

# load secrets
secrets = load_secrets()
GOOGLE_MAPS_API_KEY = secrets["GOOGLE_MAPS_API_KEY"]

# set up client
client = Client(key=GOOGLE_MAPS_API_KEY)
# a location in Los Angeles, CA
location = {"longitude":-118.3,"latitude":34.1}
# a JSON response
history_conditions_data = historical_conditions(
    client,
    location,
    lag_time=720
)

# %%
# convert to dataframe
df = historical_conditions_to_df(history_conditions_data)
df.head()


# %%
#plot the data
import seaborn as sns

g = sns.relplot(
    x="time",
    y="value",
    data=df[df["code"].isin(["uaqi","usa_epa","pm25","pm10"])],
    kind="line",
    col="name",
    col_wrap=4,
    hue="type",
    height=4,
    facet_kws={'sharey': False, 'sharex': False}
)
g.set_xticklabels(rotation=90)



