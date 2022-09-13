import pandas as pd


data = pd.read_excel('StandardVoterExport.xlsx')

for col in data.columns:
    print(col)