import pandas as pd
from collections import Counter
df = pd.read_csv('Problem 1/results.csv', na_values='N/a')
df.drop(columns='Unnamed: 0', inplace=True)
numeric_col = df.select_dtypes(include='number').columns

team_high = {}
for col in numeric_col:
    if df[col].isna().all():
        continue
    team = df.groupby('Team')[col].mean()
    top_team = team.idxmax()
    top_value = team.max()
    team_high[col] = (top_team, top_value)

print("Team with highest score for each statistic:")
for stat, (team, value) in team_high.items():
    print(f"{stat}: {team} ({value})")

team_counts = Counter(team for team, _ in team_high.values())
highest = -10**9
for team, count in team_counts.most_common():
    if count > highest:
        highest = count
        best_peformance_team = team 
print()
print('The Best-Peforming team in 2024-2025 Premier League Season:', best_peformance_team)