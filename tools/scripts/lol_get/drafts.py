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

def get_draft_table(team=None, region=None, year=None, tag='', worlds=False, msi=False,  link=None):
    """Gets a teams drafts from X time period and returns them in a dataframe.

    Args:
        region (str, optional): The region of the team. Defaults to None.
        year (int, optional): The year of the scope. Defaults to None.
        tag (str, optional): The time of year (Ex: Spring, Summer, etc.). Defaults to ''.
        international (bool, optional): Whether or not it is an international tournament. Defaults to False.
        team (str, optional): The team being searched. Defaults to None.
        link (str, optional): Bypasses the need for any other tag and just uses a raw link. Defaults to None.

    Returns:
        dataframe: Returns a dataframe of the drafts featuring Pick Ban in the form of BB1 BB2 etc.
    """

    if region is not None:
        region = region.upper()

    if team in leaguepedia_team_name_dct:
        teamName = leaguepedia_team_name_dct[team].replace(' ', '+')
    else:
        teamName = team.replace(' ', '+')
    
    if region == 'LCSA':
        region = 'NA Academy'

    if region == 'LCO':
        if 'Spring' in tag:
            split, rest = tag.split('Spring')
            split = 'Split 1'
            tag = split + rest
        if 'Summer' in tag:
            split, rest = tag.split('Summer')
            split = 'Split 2'
            tag = split + rest

    if region == 'CBLOL':
        if 'Spring' in tag:
            split, rest = tag.split('Spring')
            split = 'Split 1'
            tag = split + rest
        if 'Summer' in tag:
            split, rest = tag.split('Summer')
            split = 'Split 2'
            tag = split + rest

    if region == 'LLA':
        if 'Spring' in tag:
            split, rest = tag.split('Spring')
            split = 'Opening'
            tag = split + rest
        if 'Summer' in tag:
            split, rest = tag.split('Summer')
            split = 'Closing'
            tag = split + rest

    if region == 'TCL':
        if 'Spring' in tag:
            split, rest = tag.split('Spring')
            split = 'Winter'
            tag = split + rest


    if link is None:
        url_region = region.replace(' ', '+')
        url_tag = tag.replace(' ', '+')

        if msi:
            tempDF = pd.read_html(f'https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?pfRunQueryFormName=PickBanHistory&PBH%5Bpage%5D=MSI+{year}&PBH%5Bteam%5D={teamName}&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text=')[0]
        elif worlds:
            playins = pd.DataFrame()
            main_event = pd.DataFrame()

            try:
                playins = pd.read_html(f'https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?pfRunQueryFormName=PickBanHistory&PBH%5Bpage%5D=Worlds+{year}+Play-In&PBH%5Bteam%5D={teamName}&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text=')[0]
            except:
                pass

            try:
                main_event = pd.read_html(f'https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?pfRunQueryFormName=PickBanHistory&PBH%5Bpage%5D=Worlds+{year}+Main+Event&PBH%5Bteam%5D={teamName}&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text=')[0]
            except:
                pass
            
            tempDF = pd.concat([playins, main_event])
        else:
            tempDF = pd.read_html(f'https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?pfRunQueryFormName=PickBanHistory&PBH%5Bpage%5D={url_region}+{year}+{url_tag}&PBH%5Bteam%5D={teamName}&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text=')[0]
    
    elif link is not None:
        tempDF = pd.read_html(link)[0]

    title = tempDF.columns[0][0]

    rp1_list = []
    rp2_list = []
    bp2_list = []
    bp3_list = []
    bp4_list = []
    bp5_list = []

    for i in range(len(tempDF)):
        gameDF = tempDF[tempDF.index == i]
        rp1, rp2 = gameDF[(title,'RP1-2')].to_string().split(', ')
        bp2, bp3 = gameDF[(title,'BP2-3')].to_string().split(', ')
        bp4, bp5 = gameDF[(title,'BP4-5')].to_string().split(', ')

        if rp1[0].isnumeric():
            trash, rp1 = rp1.split('    ')
        if bp2[0].isnumeric():
            trash, bp2 = bp2.split('    ')
        if bp4[0].isnumeric():
            trash, bp4 = bp4.split('    ')

        rp1_list.append(rp1)
        rp2_list.append(rp2)
        bp2_list.append(bp2)
        bp3_list.append(bp3)
        bp4_list.append(bp4)
        bp5_list.append(bp5)


    df = pd.DataFrame({
        'Phase' : tempDF[(title,'Phase')],
        'Blue' : tempDF[(title,'Blue')],
        'Red' : tempDF[(title,'Red')],
        'Score' : tempDF[(title,'Score')],
        'Patch' : tempDF[(title,'Patch')],
        'BB1' : tempDF[(title,'BB1')],
        'RB1' : tempDF[(title,'RB1')],
        'BB2' : tempDF[(title,'BB2')],
        'RB2' : tempDF[(title,'RB2')],
        'BB3' : tempDF[(title,'BB3')],
        'RB3' : tempDF[(title,'RB3')],
        'BP1' : tempDF[(title,'BP1')],
        'RP1' : rp1_list,
        'RP2' : rp2_list,
        'BP2' : bp2_list,
        'BP3' : bp3_list,
        'RP3' : tempDF[(title,'RP3')],
        'RB4' : tempDF[(title,'RB4')],
        'BB4' : tempDF[(title,'BB4')],
        'RB5' : tempDF[(title,'RB5')],
        'BB5' : tempDF[(title,'BB5')],
        'RP4' : tempDF[(title,'RP4')],
        'BP4' : bp4_list,
        'BP5' : bp5_list,
        'RP5' : tempDF[(title,'RP5')],
        'BR1' : tempDF[(title,'BR1')],
        'BR2' : tempDF[(title,'BR2')],
        'BR3' : tempDF[(title,'BR3')],
        'BR4' : tempDF[(title,'BR4')],
        'BR5' : tempDF[(title,'BR5')],
        'RR1' : tempDF[(title,'RR1')],
        'RR2' : tempDF[(title,'RR2')],
        'RR3' : tempDF[(title,'RR3')],
        'RR4' : tempDF[(title,'RR4')],
        'RR5' : tempDF[(title,'RR5')],
    })

    try:
        df['Winner'] = tempDF[(title,'Winner')]
    except:
        0
    try:
        df['Result'] = tempDF[(title,'Result')]
    except:
        0


    return df

def get_blue_drafts(team=None, region=None, year=None, tag='', playoffs=False, worlds=False, msi=False,  link=None, forLine=False):
    """Splits the get_draft_table function's results into blue side for proper parsing.

    Args:
        region (str, optional): The region of the team. Defaults to None.
        year (int, optional): The year of the scope. Defaults to None.
        tag (str, optional): The time of year (Ex: Spring, Summer, etc.). Defaults to ''.
        playoffs (bool, required): Whether to consider playoffs. Defaults to False.
        MSI (bool, required): Whether to consider MSI. Defaults to False.
        team (str, optional): The team being searched. Defaults to None.
        link (str, optional): Bypasses the need for any other tag and just uses a raw link. Defaults to None.
        forLine (boolean, required): Adds a * next to counterpicks for line draft format. Defaults to False.

    Returns:
        dataframe: Returns a dataframe of just the blue side drafts for a team.
    """


    if link is None:
        if msi:
            df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag, msi=True), get_draft_table(team=team, region=region, year=year, tag=tag+' Playoffs'), get_draft_table(team=team, region=region, year=year, tag=tag)])
        if worlds:
            if region == 'LCS':
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag, worlds=True), get_draft_table(team=team, region=region, year=year, tag='Championship'), get_draft_table(team=team, region=region, year=year, tag=tag)])
            else:
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag, worlds=True), get_draft_table(team=team, region=region, year=year, tag=tag+' Playoffs'), get_draft_table(team=team, region=region, year=year, tag=tag)])
        elif playoffs:
            if region == 'LCS':
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag='Championship'), get_draft_table(team=team, region=region, year=year, tag=tag)])
            else:
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag+' Playoffs'), get_draft_table(team=team, region=region, year=year, tag=tag)])
        else:
            df = get_draft_table(team=team, region=region, year=year, tag=tag)
    elif link is not None:
        df = get_draft_table(link=link, team=team)

    if team in leaguepedia_team_name_dct:
        df = df.loc[df['Blue'] == leaguepedia_team_name_dct[team]].reset_index()
    else:
        df = df.loc[df['Blue'] == team].reset_index()


    blue_top_list = []
    blue_jng_list = []
    blue_mid_list = []
    blue_bot_list = []
    blue_sup_list = []

    red_top_list = []
    red_jng_list = []
    red_mid_list = []
    red_bot_list = []
    red_sup_list = []

    blue_top_num_list = []
    blue_jng_num_list = []
    blue_mid_num_list = []
    blue_bot_num_list = []
    blue_sup_num_list = []

    red_top_num_list = []
    red_jng_num_list = []
    red_mid_num_list = []
    red_bot_num_list = []
    red_sup_num_list = []

    opponent_list = []

    win_list = []
    opp_win_list = []

    spacer = []
    

    for i in range(len(df)):
        gameDF = df[df.index == i]
        if gameDF['Red'][i] in leaguepedia_team_name_dct_reversed:
            opponent_list.append(leaguepedia_team_name_dct_reversed[gameDF['Red'][i]])
        else:
            opponent_list.append(gameDF['Red'][i])
        blue_top_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][0]]][i])
        blue_jng_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][0]]][i])
        blue_mid_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][0]]][i])
        blue_bot_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][0]]][i])
        blue_sup_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][0]]][i])

        red_top_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][1]]][i])
        red_jng_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][1]]][i])
        red_mid_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][1]]][i])
        red_bot_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][1]]][i])
        red_sup_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][1]]][i])

        blue_top_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][0]])
        blue_jng_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][0]])
        blue_mid_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][0]])
        blue_bot_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][0]])
        blue_sup_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][0]])

        red_top_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][1]])
        red_jng_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][1]])
        red_mid_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][1]])
        red_bot_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][1]])
        red_sup_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][1]])

        if 'Winner' in df.columns:
            if gameDF['Winner'][i] == 1:
                win_list.append('W')
                opp_win_list.append('L')
            else:
                win_list.append('L')
                opp_win_list.append('W')
        
        if 'Result' in df.columns:
            if gameDF['Result'][i] == 'Win':
                win_list.append('W')
                opp_win_list.append('L')
            else:
                win_list.append('L')
                opp_win_list.append('W')
        
        spacer.append('')
        
    
    finalDF = pd.DataFrame({
        'week' : df['Phase'],
        'patch' : df['Patch'],
        'blue top' : blue_top_list,
        'blue jungle' : blue_jng_list,
        'blue mid' : blue_mid_list,
        'blue bot' : blue_bot_list,
        'blue support' : blue_sup_list,
        ' ' : win_list,
        '  ' : spacer,
        '   ' : opponent_list,
        '    ' : spacer,
        '     ' : opp_win_list,
        'red top' : red_top_list,
        'red jungle' : red_jng_list,
        'red mid' : red_mid_list,
        'red bot' : red_bot_list,
        'red support' : red_sup_list,
        '      ' : spacer,
        'team ban 1' : df['BB1'],
        'team ban 2' : df['BB2'],
        'team ban 3' : df['BB3'],
        'team ban 4' : df['BB4'],
        'team ban 5' : df['BB5'],
        '       ' : spacer,
        'enemy ban 1' : df['RB1'],
        'enemy ban 2' : df['RB2'],
        'enemy ban 3' : df['RB3'],
        'enemy ban 4' : df['RB4'],
        'enemy ban 5' : df['RB5'],
        'E' : blue_top_num_list,
        'F' : blue_jng_num_list,
        'G' : blue_mid_num_list,
        'H' : blue_bot_num_list,
        'I' : blue_sup_num_list,
        'O' : red_top_num_list,
        'P' : red_jng_num_list,
        'Q' : red_mid_num_list,
        'R' : red_bot_num_list,
        'S' : red_sup_num_list,
        'BR1': df['BR1'],
        'BR2': df['BR2'],
        'BR3': df['BR3'],
        'BR4': df['BR4'],
        'BR5': df['BR5'],
        'RR1': df['RR1'],
        'RR2': df['RR2'],
        'RR3': df['RR3'],
        'RR4': df['RR4'],
        'RR5': df['RR5'],
        
        
    })

    if forLine:
        for i in range(len(finalDF)):
            if color_dict[finalDF['E'][i]] > color_dict[finalDF['O'][i]]:
                finalDF['blue top'][i] += '*'
            if color_dict[finalDF['F'][i]] > color_dict[finalDF['P'][i]]:
                finalDF['blue jungle'][i] += '*'
            if color_dict[finalDF['G'][i]] > color_dict[finalDF['Q'][i]]:
                finalDF['blue mid'][i] += '*'
            if color_dict[finalDF['H'][i]] > color_dict[finalDF['R'][i]]:
                finalDF['blue bot'][i] += '*'
            if color_dict[finalDF['I'][i]] > color_dict[finalDF['S'][i]]:
                finalDF['blue support'][i] += '*'


    return finalDF

def get_red_drafts(team=None, region=None, year=None, tag='', playoffs=False, worlds=False, msi=False, link=None, forLine=False):
    """Splits the get_draft_table function's results into red side for proper parsing.

    Args:
        region (str, optional): The region of the team. Defaults to None.
        year (int, optional): The year of the scope. Defaults to None.
        tag (str, optional): The time of year (Ex: Spring, Summer, etc.). Defaults to ''.
        team (str, optional): The team being searched. Defaults to None.
        link (str, optional): Bypasses the need for any other tag and just uses a raw link. Defaults to None.
        forLine (boolean, required): Formats the return in a way that works best for the set_line_drafts function. Defaults to False.

    Returns:
        dataframe: Returns a dataframe of just the red side drafts for a team.
    """
   
    if link is None:
        if msi:
            df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag, msi=True), get_draft_table(team=team, region=region, year=year, tag=tag+' Playoffs'), get_draft_table(team=team, region=region, year=year, tag=tag)])
        if worlds:
            if region == 'LCS':
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag, worlds=True), get_draft_table(team=team, region=region, year=year, tag='Championship'), get_draft_table(team=team, region=region, year=year, tag=tag)])
            else:
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag, worlds=True), get_draft_table(team=team, region=region, year=year, tag=tag+' Playoffs'), get_draft_table(team=team, region=region, year=year, tag=tag)])
        elif playoffs:
            if region == 'LCS':
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag='Championship'), get_draft_table(team=team, region=region, year=year, tag=tag)])
            else:
                df = pd.concat([get_draft_table(team=team, region=region, year=year, tag=tag+' Playoffs'), get_draft_table(team=team, region=region, year=year, tag=tag)])
        else:
            df = get_draft_table(team=team, region=region, year=year, tag=tag)
    elif link is not None:
        df = get_draft_table(link=link, team=team)

    if team in leaguepedia_team_name_dct:
        df = df.loc[df['Red'] == leaguepedia_team_name_dct[team]].reset_index()
    else:
        df = df.loc[df['Red'] == team].reset_index()



    blue_top_list = []
    blue_jng_list = []
    blue_mid_list = []
    blue_bot_list = []
    blue_sup_list = []

    red_top_list = []
    red_jng_list = []
    red_mid_list = []
    red_bot_list = []
    red_sup_list = []

    blue_top_num_list = []
    blue_jng_num_list = []
    blue_mid_num_list = []
    blue_bot_num_list = []
    blue_sup_num_list = []

    red_top_num_list = []
    red_jng_num_list = []
    red_mid_num_list = []
    red_bot_num_list = []
    red_sup_num_list = []

    opponent_list = []

    win_list = []
    opp_win_list = []

    spacer = []
    

    for i in range(len(df)):
        gameDF = df[df.index == i]
        if gameDF['Blue'][i] in leaguepedia_team_name_dct_reversed:
            opponent_list.append(leaguepedia_team_name_dct_reversed[gameDF['Blue'][i]])
        else:
            opponent_list.append(gameDF['Blue'][i])
        blue_top_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][1]]][i])
        blue_jng_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][1]]][i])
        blue_mid_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][1]]][i])
        blue_bot_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][1]]][i])
        blue_sup_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][1]]][i])

        red_top_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][0]]][i])
        red_jng_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][0]]][i])
        red_mid_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][0]]][i])
        red_bot_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][0]]][i])
        red_sup_list.append(gameDF[role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][0]]][i])

        blue_top_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][1]])
        blue_jng_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][1]])
        blue_mid_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][1]])
        blue_bot_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][1]])
        blue_sup_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][1]])

        red_top_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Top').iloc[0]][0]])
        red_jng_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Jungle').iloc[0]][0]])
        red_mid_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Mid').iloc[0]][0]])
        red_bot_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Bot').iloc[0]][0]])
        red_sup_num_list.append(role_to_pick_dct[gameDF.columns[(gameDF == 'Support').iloc[0]][0]])

        if 'Winner' in df.columns:
            if gameDF['Winner'][i] == 2:
                win_list.append('W')
                opp_win_list.append('L')
            else:
                win_list.append('L')
                opp_win_list.append('W')
            
        if 'Result' in df.columns:
            if gameDF['Result'][i] == 'Win':
                win_list.append('W')
                opp_win_list.append('L')
            else:
                win_list.append('L')
                opp_win_list.append('W')
        
        spacer.append('')
        
    
    finalDF = pd.DataFrame({
        'week' : df['Phase'],
        'patch' : df['Patch'],
        'blue top' : blue_top_list,
        'blue jungle' : blue_jng_list,
        'blue mid' : blue_mid_list,
        'blue bot' : blue_bot_list,
        'blue support' : blue_sup_list,
        ' ' : win_list,
        '  ' : spacer,
        '   ' : opponent_list,
        '    ' : spacer,
        '     ' : opp_win_list,
        'red top' : red_top_list,
        'red jungle' : red_jng_list,
        'red mid' : red_mid_list,
        'red bot' : red_bot_list,
        'red support' : red_sup_list,
        '      ' : spacer,
        'team ban 1' : df['RB1'],
        'team ban 2' : df['RB2'],
        'team ban 3' : df['RB3'],
        'team ban 4' : df['RB4'],
        'team ban 5' : df['RB5'],
        '       ' : spacer,
        'enemy ban 1' : df['BB1'],
        'enemy ban 2' : df['BB2'],
        'enemy ban 3' : df['BB3'],
        'enemy ban 4' : df['BB4'],
        'enemy ban 5' : df['BB5'],
        'E' : blue_top_num_list,
        'F' : blue_jng_num_list,
        'G' : blue_mid_num_list,
        'H' : blue_bot_num_list,
        'I' : blue_sup_num_list,
        'O' : red_top_num_list,
        'P' : red_jng_num_list,
        'Q' : red_mid_num_list,
        'R' : red_bot_num_list,
        'S' : red_sup_num_list,
        'BR1': df['BR1'],
        'BR2': df['BR2'],
        'BR3': df['BR3'],
        'BR4': df['BR4'],
        'BR5': df['BR5'],
        'RR1': df['RR1'],
        'RR2': df['RR2'],
        'RR3': df['RR3'],
        'RR4': df['RR4'],
        'RR5': df['RR5'],
    })

    if forLine:
        for i in range(len(finalDF)):
            if color_dict[finalDF['E'][i]] > color_dict[finalDF['O'][i]]:
                finalDF['blue top'][i] += '*'
            if color_dict[finalDF['F'][i]] > color_dict[finalDF['P'][i]]:
                finalDF['blue jungle'][i] += '*'
            if color_dict[finalDF['G'][i]] > color_dict[finalDF['Q'][i]]:
                finalDF['blue mid'][i] += '*'
            if color_dict[finalDF['H'][i]] > color_dict[finalDF['R'][i]]:
                finalDF['blue bot'][i] += '*'
            if color_dict[finalDF['I'][i]] > color_dict[finalDF['S'][i]]:
                finalDF['blue support'][i] += '*'

    return finalDF
