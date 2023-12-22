import pandas as pd
import warnings

from common.dictionaries import *

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', None)
warnings.simplefilter(action='ignore', category=FutureWarning)

#############
### Draft ###
#############

def clean_leaguepedia(link):
    """Takes a leaguepedia match draft page and turns it into a dataframe with a similar format to the dataframes I work with that build off of bayes_lol.game_summary so that I can seemlessly swap it in if needed.

    Args:
        link (str): Leaguepedia page link

    Returns:
        df (dataframe): Dataframe of game summary page
    """    

    df = pd.read_html(link)[0]

    col_list = []

    for i in range(len(df.columns)):
        col_list.append(df.columns[i][1])

    df.columns = col_list

    df[['BP2', 'BP3']] = df['BP2-3'].str.split(', ',expand=True)
    df[['BP4', 'BP5']] = df['BP4-5'].str.split(', ',expand=True)
    df[['RP1', 'RP2']] = df['RP1-2'].str.split(', ',expand=True)

    df['team_1_top'] = ''
    df['team_1_top_pick_num'] = ''
    df['team_1_jng'] = ''
    df['team_1_jng_pick_num'] = ''
    df['team_1_mid'] = ''
    df['team_1_mid_pick_num'] = ''
    df['team_1_bot'] = ''
    df['team_1_bot_pick_num'] = ''
    df['team_1_sup'] = ''
    df['team_1_sup_pick_num'] = ''

    df['team_2_top'] = ''
    df['team_2_top_pick_num'] = ''
    df['team_2_jng'] = ''
    df['team_2_jng_pick_num'] = ''
    df['team_2_mid'] = ''
    df['team_2_mid_pick_num'] = ''
    df['team_2_bot'] = ''
    df['team_2_bot_pick_num'] = ''
    df['team_2_sup'] = ''
    df['team_2_sup_pick_num'] = ''

    for i in range(len(df)):

        orders = [x+1 for x in list(range(10))]
        champs = df[['BP1','RP1', 'RP2', 'BP2', 'BP3', 'RP3', 'RP4', 'BP4', 'BP5', 'RP5']].transpose()[i].values
        roles = df[['BR1', 'RR1', 'RR2', 'BR2', 'BR3', 'RR3', 'RR4', 'BR4', 'BR5', 'RR5']].transpose()[i].values

        pick_dict = [{order: {'champ': champ, 'role': role}} for order, champ, role in zip(orders, champs, roles)]

        blue_pick_list = [1,4,5,8,9]

        for j in range(10):
            champ = pick_dict[j][j+1]['champ']
            role = pick_dict[j][j+1]['role'].lower()

            if role in ['jungle', 'support']:
                replace = {
                    'jungle': 'jng',
                    'support': 'sup'
                }
                role = replace[role]
            try:
                if j+1 in blue_pick_list:
                    df[f'team_1_{role}'][i] = champ
                    df[f'team_1_{role}_pick_num'][i] = j+1
                else:
                    df[f'team_2_{role}'][i] = champ
                    df[f'team_2_{role}_pick_num'][i] = j+1
            except:
                continue

    df.rename(columns={'Blue':'team_1_name', 'Red':'team_2_name', 'Winner':'winning_side'}, inplace=True)
    df['winning_side'].replace({1:'blue', 2:'red'}, inplace=True)
    df['team_1_side'] = 'blue'
    df['team_2_side'] = 'red'

    df.insert(3, 'winning_team', '')

    for i in range(len(df)):
        if df['winning_side'][i] == 'blue':
            df['winning_team'][i] = df['team_1_name'][i]
        else:
            df['winning_team'][i] = df['team_2_name'][i]

    df.drop(columns=['BP1','RP1', 'RP2', 'BP2', 'BP3', 'RP3', 'RP4', 'BP4', 'BP5', 'RP5', 'BR1', 'RR1', 'RR2', 'BR2', 'BR3', 'RR3', 'RR4', 'BR4', 'BR5', 'RR5', 'BP2-3', 'BP4-5', 'RP1-2', 'SB', 'VOD'], inplace=True)

    df.columns= df.columns.str.strip().str.lower()

    return df
