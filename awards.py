import pandas as pd

csv = 'Awards.csv'

df = pd.read_csv(csv)

for i, row in df.iterrows():
    print(row["NSFOrganization"])