import pandas as pd

s1 = pd.Series([+10, -20, +30, -40, +50])
s2 = pd.Series([+1, -2, +3, -4, +5])
s3 = pd.Series([-10, +20, -30, +40, -50])
df = pd.DataFrame({'S1': s1, 'S2': s2, 'S3': s3})

print(df)

print(df.corr())