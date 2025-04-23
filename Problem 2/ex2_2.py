import pandas as pd

df = pd.read_csv('Problem 1/results.csv', na_values='N/a')
df.drop(columns='Unnamed: 0', inplace=True)
numeric_col = df.select_dtypes(include='number').columns

epl_clb = []
all_team = {'Team': 'all'}
for col in numeric_col:
    all_team[f'Median of {col}'] = df[col].median()
    all_team[f'Mean of {col}'] = df[col].mean()
    all_team[f'Std of {col}'] = df[col].std()
epl_clb.append(all_team)

for team in df['Team'].unique():
    club = {'Team': team}
    df_team = df[df['Team'] == team]
    for col in numeric_col:
        club[f'Median of {col}'] = df_team[col].median()
        club[f'Mean of {col}'] = df_team[col].mean()
        club[f'Std of {col}'] = df_team[col].std()
    epl_clb.append(club)
epl_df = pd.DataFrame(epl_clb)
epl_df.to_csv('Problem 2/results2.csv', index = True)