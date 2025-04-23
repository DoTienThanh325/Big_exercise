import pandas as pd
from collections import Counter
import time
def deduplicate_columns(columns):
    counts = Counter()
    new_col = []
    for col in columns:
        if counts[col]:
            new_col.append(f"{col}_{counts[col]}")
        else:
            new_col.append(col)
        counts[col] += 1
    return new_col

def crawl_data_table(df,list,club):
    df.columns = df.columns.droplevel() if isinstance(df.columns, pd.MultiIndex) else df.columns
    df.columns = deduplicate_columns(df.columns)
    df['Team'] = club
    df = df[list]
    return df

def create_team_table(url, club):
    table = pd.read_html(url)
    df_playerstats = crawl_data_table(table[0], ['Player', 'Nation', 'Team', 'Pos', 'Age', 'MP', 'Starts', 
         'Min', 'Gls', 'Ast', 'CrdY', 'CrdR', 'xG', 'xAG', 'PrgC', 
         'PrgP', 'PrgR', 'Gls_1', 'Ast_1', 'xG_1', 'xAG_1'], club)
    df_gk = crawl_data_table(table[2], ['Player', 'GA90', 'Save%', 'CS%', 'Save%_1'], club)
    df_shooting = crawl_data_table(table[4], ['Player', 'SoT%', 'SoT/90', 'G/Sh', 'Dist'], club)
    df_passing = crawl_data_table(table[5], ['Player', 'Cmp', 'Cmp%', 'TotDist', 'Cmp%_1', 'Cmp%_2', 'Cmp%_3', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP'], club)
    df_goalshot = crawl_data_table(table[7], ['Player', 'SCA', 'SCA90', 'GCA', 'GCA90'], club)
    df_defensive = crawl_data_table(table[8], ['Player', 'Tkl', 'TklW', 'Att', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int'], club)
    df_possesion = crawl_data_table(table[9], ['Player', 'Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'Att', 'Succ%', 'Tkld%', 'Carries', 'PrgDist', 'PrgC', '1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'PrgR'], club)
    df_miscellaneus = crawl_data_table(table[11], ['Player', 'Fls', 'Fld', 'Off', 'Crs', 'Recov', 'Won', 'Lost', 'Won%'], club)
    df = df_playerstats.merge(df_gk, on = 'Player', how = 'outer').merge(df_shooting,on = 'Player',how = 'outer').merge(df_passing, on = 'Player', how = 'outer').merge(df_goalshot,on = 'Player', how = 'outer').merge(df_defensive,on = 'Player',how = 'outer').merge(df_possesion,on='Player',how='outer').merge(df_miscellaneus,on='Player',how='outer')
    df = df[df['Min'] > 90]
    df.fillna("N/a", inplace=True)
    df['first_name'] = df['Player'].apply(lambda x: x.split()[0])
    df = df.rename(columns={
        'MP': 'Playing_time: MP', 
        'Starts': 'Playing_time: Starts', 
        'Min': 'Playing_time: Min', 
        'Gls': 'Performance: Gls',
        'Ast': 'Performance: Ast', 
        'CrdY': 'Performance: CrdY', 
        'CrdR': 'Performance: CrdR', 
        'xG': 'Expected: xG',
        'xAG': 'Expected: xAG', 
        'PrgC_x': 'Progression: PrgC', 
        'PrgP_x': 'Progression: PrgP', 
        'PrgR_x': 'Progression: PrgR',
        'Gls_1': 'Per_90_minutes: Gls', 
        'Ast_1': 'Per_90_minutes: Ast', 
        'xG_1': 'Per_90_minutes: xG', 
        'xAG_1': 'Per_90_minutes: xAG',
        'GA90': 'Goalkeeping_Performance: GA90', 
        'Save%': 'Goalkeeping_Performance: Save%', 
        'CS%': 'Goalkeeping_Performance: CS%',
        'Save%_1': 'Goalkeeping_Penalty_Kicks: Save%', 
        'Cmp': 'Passing_Total: Cmp', 
        'Cmp%': 'Passing_Total: Cmp%',
        'TotDist': 'Passing_Total: TotDist', 
        'Cmp%_1': 'Passing_Short: Cmp%', 
        'Cmp%_2': 'Passing_Medium: Cmp%',
        'Cmp%_3': 'Passing_Long: Cmp%', 
        'KP': 'Passing_Expected: KP', 
        '1/3_x': 'Passing_Expected: 1/3', 
        'PPA': 'Passing_Expected: PPA',
        'CrsPA': 'Passing_Expected: CrsPA', 
        'PrgP_y': 'Passing_Expected: PrgP', 
        'SCA': 'Goal_shot_creation: SCA',
        'SCA90': 'Goal_shot_creation: SCA90', 
        'GCA': 'Goal_shot_creation: GCA', 
        'GCA90': 'Goal_shot_creation: GCA90',
        'Tkl': 'Defensive_Tackles: Tkl',
        'TklW': 'Defensive_Tackles: TklW',
        'Att_x': 'Defensive_Challenges: Att',
        'Lost_x': 'Defensive_Challenge: Lost',
        'Blocks': 'Defensive_Blocks: Blocks',
        'Sh': 'Defensive_Blocks: Sh',
        'Pass': 'Defensive_Blocks: Pass',
        'Int': 'Defensive_Blocks: Int',
        'Touches': 'Possesion_Touches: Touches',
        'Def Pen': 'Possesion_Touches: Def Pen',
        'Def 3rd': 'Possesion_Touches: Def 3rd',
        'Mid 3rd': 'Possesion_Touches: Mid 3rd',
        'Att 3rd': 'Possesion_Touches: Att 3rd',
        'Att Pen': 'Possesion_Touches: Att Pen',
        'Att_y': 'Possesion_Take: Ons: Att',
        'Succ%': 'Possesion_Take: Ons: Succ%',
        'Tkld%': 'Possesion_Take: Ons: Tkld%',
        'Carries': 'Possesion_Carries: Carries',
        'PrgDist': 'Possesion_Carries: PrgDist',
        'PrgC_y': 'Possesion_Carries: PrgC',
        '1/3_y': 'Possesion_Carries: 1/3',
        'CPA': 'Possesion_Carries: CPA',
        'Mis': 'Possesion_Carries: Mis',
        'Dis': 'Possesion_Carries: Dis',
        'Rec': 'Possesion_Receiving: Rec',
        'PrgR_y': 'Possesion_Receiving: PrgR',
        'Fls': 'Miscellaneous_Stats_Performance: Fls',
        'Fld': 'Miscellaneous_Stats_Performance: Fld',
        'Off': 'Miscellaneous_Stats_Performance: Off',
        'Crs': 'Miscellaneous_Stats_Performance: Crs',
        'Recov': 'Miscellaneous_Stats_Performance: Recov',
        'Won': 'Miscellaneous_Stats_Aerial Duels: Won',
        'Lost_y': 'Miscellaneous_Stats_Aerial Duels: Lost',
        'Won%': 'Miscellaneous_Stats_Aerial Duels: Won%',
    })
    return df

if __name__ == '__main__':
    df_liv = create_team_table('https://fbref.com/en/squads/822bd0ba/Liverpool-Stats', 'Liverpool')
    time.sleep(3)
    df_mu = create_team_table('https://fbref.com/en/squads/19538871/Manchester-United-Stats', 'Manchester United')
    time.sleep(3)
    df_ars = create_team_table('https://fbref.com/en/squads/18bb7c10/Arsenal-Stats', 'Arsenal')
    time.sleep(3)
    df_villa = create_team_table('https://fbref.com/en/squads/8602292d/Aston-Villa-Stats', 'Aston Villa')
    time.sleep(3)
    df_bou = create_team_table('https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats', 'Bournemouth')
    df_epl = pd.concat([df_liv, df_mu, df_ars, df_villa, df_bou], ignore_index=True)

    time.sleep(3)
    df_bren = create_team_table('https://fbref.com/en/squads/cd051869/Brentford-Stats', 'Brentford')
    time.sleep(3)
    df_brighton = create_team_table('https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats', 'Brighton & Hove Albion')
    time.sleep(3)
    df_chel = create_team_table('https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats', 'Chelsea')
    time.sleep(3)
    df_crystal = create_team_table('https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats', 'Crystal Palace')
    time.sleep(3)
    df_ever = create_team_table('https://fbref.com/en/squads/d3fd31cc/Everton-Stats', 'Everton')
    df_epl = pd.concat([df_epl, df_bren, df_brighton, df_chel, df_crystal, df_ever], ignore_index=True)

    time.sleep(3)
    df_fulham = create_team_table('https://fbref.com/en/squads/fd962109/Fulham-Stats', 'Fulham')
    time.sleep(3)
    df_ips = create_team_table('https://fbref.com/en/squads/b74092de/Ipswich-Town-Stats', 'Ipswich Town')
    time.sleep(3)
    df_lei = create_team_table('https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats', 'Leicester City')
    time.sleep(3)
    df_mc = create_team_table('https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats', 'Manchester City')
    time.sleep(3)
    df_new = create_team_table('https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats', 'Newcastle United')
    df_epl = pd.concat([df_epl, df_fulham, df_ips, df_lei, df_mc, df_new], ignore_index=True)
    
    time.sleep(3)
    df_not = create_team_table('https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats', 'Nottingham Forest')
    time.sleep(3)
    df_sou = create_team_table('https://fbref.com/en/squads/33c895d4/Southampton-Stats', 'Southampton')
    time.sleep(3)
    df_tot = create_team_table('https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats', 'Tottenham Hotspur')
    time.sleep(3)
    df_wes = create_team_table('https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats', 'West Ham United')
    time.sleep(3)
    df_wolves = create_team_table('https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats', 'Wolverhampton Wanderers')
    
    df_epl = pd.concat([df_epl, df_not, df_sou, df_tot, df_wes, df_wolves], ignore_index=True)
    df_epl = df_epl.sort_values(by = 'first_name').reset_index(drop = True)
    df_epl = df_epl.drop(columns='first_name', errors='ignore')
    df_epl = df_epl[df_epl['Player'] != 'Squad Total']
    df_epl = df_epl[df_epl['Player'] != 'Opponent Total']
    df_epl.to_csv('D:/file python/bài tập lớn/Problem 1/results.csv', index = True)