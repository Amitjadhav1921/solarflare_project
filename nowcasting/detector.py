import numpy as np

def detect_flares(flux,bg,sigma=3):
 return flux>(bg+sigma*np.std(flux))
