import pandas as pd
import matplotlib.pyplot as plt
import os
df = pd.read_csv('Problem 1/results.csv', na_values='N/a')
df.drop(columns='Unnamed: 0', inplace=True)
numeric_col = df.select_dtypes(include='number').columns

for col in numeric_col:
    if df[col].isna().all():
        continue
    teams = df['Team'].unique()
    len_teams = len(teams)
    fig, axes = plt.subplots(3, 7, figsize = (15, 10))
    axes = axes.flatten() if len_teams > 1 else [axes]
    
    axes[0].hist(df[col].dropna(), bins = 30, color='blue', edgecolor='black')
    axes[0].set_title(f'Epl {col}', fontsize=7)

    for i,team in enumerate(teams[:len(axes)-1], 1):
        df_team = df[df['Team'] == team][col].dropna()
        if len(df_team) > 1:
            axes[i].hist(df_team, bins=30, color='green', edgecolor='black')
            axes[i].set_title(f'{team} {col}', fontsize=7)
    plt.tight_layout()
    plt.show()
    plt.close()