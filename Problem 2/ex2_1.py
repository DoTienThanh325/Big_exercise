import pandas as pd

df = pd.read_csv('Problem 1/results.csv', na_values='N/a')
df.drop(columns='Unnamed: 0', inplace=True)
numeric_col = df.select_dtypes(include='number').columns
index = 1
with open('Problem 2/top_3.txt', 'w', encoding='utf-8') as f:
    for col in numeric_col:
        f.write(f'{index}. {col}\n')
        f.write('Top 3: \n')
        top3 = df[['Player', col]].sort_values(by=col, ascending=False).head(3)
        f.write(top3.to_string(index=False) + '\n')

        f.write('Bottom 3: \n')
        bottom3 = df[['Player', col]].sort_values(by = col, ascending=True).head(3)
        f.write(bottom3.to_string(index=False) + '\n\n')
        index += 1