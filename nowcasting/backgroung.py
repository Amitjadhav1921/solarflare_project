def rolling_background(series,window=60):
 return series.rolling(window,min_periods=1).quantile(0.2)
