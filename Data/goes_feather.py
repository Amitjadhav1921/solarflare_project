import requests,pandas as pd
URL='https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json'
def fetch_goes_data():
 r=requests.get(URL,timeout=20); r.raise_for_status();
 df=pd.DataFrame(r.json()); df['time_tag']=pd.to_datetime(df['time_tag']); return df
