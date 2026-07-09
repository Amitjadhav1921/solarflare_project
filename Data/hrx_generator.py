import numpy as np

def generate_hxr(df):
 d=np.gradient(df['flux'].values)
 d[d<0]=0
 df['hxr_flux']=d
 return df
