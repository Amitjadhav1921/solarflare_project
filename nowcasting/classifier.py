def classify_goes_flare(f):
 return 'X' if f>=1e-4 else 'M' if f>=1e-5 else 'C' if f>=1e-6 else 'B' if f>=1e-7 else 'A'
