from pandas import read_csv

df = read_csv('valorPRO_empresas.csv', index_col=0)
n = df.shape[0]
collected = df["collected"].eq("X").sum()
unavailable = df["collected"].eq("unavailable").sum()
missing = df["collected"].isna().sum()

print(f'Total: {df.shape[0]}')
print(f'Total collected: {collected} = {round(collected / n * 100, 2)}%')
print(f'Total unavailable: {unavailable} = {round(unavailable / n * 100, 2)}%')
print(f'Total missing: {missing} = {round(missing / n * 100, 2)}%')
