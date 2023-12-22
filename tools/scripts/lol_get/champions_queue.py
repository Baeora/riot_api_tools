import common.core as core
import numpy as np
import pandas as pd
import warnings
import os 

from common.dictionaries import *
from cq import cq_scraper

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', None)
warnings.simplefilter(action='ignore', category=FutureWarning)

script_path = os.path.abspath(os.path.dirname(__file__))

###############
### Scraper ###
###############

def scrape_cq_matches():
    """Scrapes the Champions Queue page and adds the results to the Champions Queue CSV"""
    cq_scraper.Handler()

########################
### Champion's Queue ###
########################

def get_cq_slice(player=None, role=None, startDate=None, endDate=None):
    """Returns a .loc of the Champions Queue CSV that filters via Team, Player and Role

    Args:
        player (str, optional): Player ID. Defaults to None.
        role (str, optional): Player's role (to exclude offrole games), none == all roles. Defaults to None.
        startDate (str, required): Start date of the query. Defaults to None.
        endDate (str, required): End date of the query. Defaults to None.

    Returns:
        dataframe: Returns a .loc of the Champions Queue CSV that filters via Team, Player and Role
    """
    
    if role is not None:
        role = role.lower()
    
    old_df = pd.read_csv(os.path.join(script_path, 'cq\\CSVs\\champions_queue.csv'))
    
    old_df['date'] = pd.to_datetime(old_df['date'])

    if player is not None:
        player = player.lower()

    if player is None:
        df = old_df
    else:
        df = old_df.loc[old_df['player'].astype(str).str.lower() ==  player]
    
    if startDate is not None and endDate is not None:
        if '-' in startDate:
            startDate = startDate.replace('-','/')
        if '-' in endDate:
            endDate = endDate.replace('-','/')
        startDate = core.days_before(date=startDate, return_str=False)
        endDate = core.days_after(date=endDate, return_str=False)
        df = df.loc[(df['date'] >= startDate) & (df['date'] <= endDate)]

    df['result'] = df['result'].astype(float)

    df = df.sort_values(['date', 'time'], ascending=False).reset_index().drop(columns='index')

    df = df.replace(replacement_dct)
    df = df.replace(summoner_spell_dct)
    
    return df

def get_cq_champion_history(player=None, role=None, startDate=None, endDate=None, forAutomation=False, forAlgo=False):
    """Converts the players CQ history into an OP.GG style dataframe

    Args:
        player (str, optional): Player ID. Defaults to None.
        role (str, optional): Player's role (to exclude offrole games), none == all roles. Defaults to None.
        startDate (str, required): Start date of the query. Defaults to None.
        endDate (str, required): End date of the query. Defaults to None.
        forAutomation (bool, optional): Formats the dataframe in a way that works nicely for spreadsheet automation. Defaults to False.
        forAlgo (boolean, optional): Formats the dataframe in a way that works nicely for the priority algorithm. Defaults to False.

    Returns:
        dataframe: Returns the players CQ history as an OP.GG style dataframe
    """

    df = get_cq_slice(player=player, role=role, startDate=startDate, endDate=endDate)

    df = df[['player', 'champion', 'result']].reset_index().drop(columns=['index'])

    if forAutomation:
        df = df.groupby(['player', 'champion']).agg(games=('result', 'count'), wins=('result', 'sum')).reset_index()
        df =  df.sort_values(['games'], ascending=False).reset_index().drop(columns=['index', 'player'])
    elif forAlgo:
        df = df.groupby(['player', 'champion']).agg(games=('result', 'count'), wins=('result', 'sum')).reset_index()
        df['losses'] = df['games'] - df['wins']
        df =  df.sort_values(['games'], ascending=False).reset_index().drop(columns=['index', 'player'])
    else:
        df = df.groupby(['player', 'champion']).agg(games=('result', 'count'), wins=('result', 'sum'), winrate=('result','mean')).reset_index()
        df = df.sort_values(['games', 'winrate'], ascending=False).reset_index().drop(columns=['index'])

    df = df.replace(replacement_dct)

    return df

def get_all_cq_winrates(sort=None, role=None, ascending=False, game_cutoff=None, wr_cutoff_below=None, wr_cutoff_above=None):
    """Gets all players WRs in a leaderboard style dataframe

    Args:
        sort (str, optional): Sorts by 'games' or 'winrate'. Defaults to None.
        role (str, optional): Allows you to filter by role.
        ascending (bool, optional): Whether or not the sort is ascending. Defaults to False.
        game_cutoff (int, optional): Cutoff point for the .loc, returns results for players with games above X cutoff. Defaults to None.
        wr_cutoff_below (float, optional): Cutoff point for the .loc, returns results for players with winrate below X cutoff. Defaults to None.
        wr_cutoff_above (float, optional): Cutoff point for the .loc, returns results for players with winrate above X cutoff. Defaults to None.

    Returns:
        dataframe: Returns all players WRs in a leaderboard style dataframe
    """

    df = pd.read_csv('champions_queue.csv')

    df = df.replace({'rjs':'RJS'})

    for i in range(len(df)):
        if df['team'][i] is not np.NaN and df['player'][i].lower() != 'rjs':
            df['player'][i] = df['team'][i]+' '+df['player'][i]

    if role is not None:
        df = df[df['role'] == role]

    df['result'] = df['result'].astype(float)

    unique_player_list = df['player'].unique().tolist()

    role_list = []
    player_list = []
    games_list = []
    winrate_list = []

    for player in unique_player_list:

        slice_df = df.loc[df['player'] == player]
        player_list.append(player)
        games_list.append(slice_df['result'].count())
        winrate_list.append(slice_df['result'].mean())

    finalDF = pd.DataFrame({
        'player': player_list,
        'games': games_list,
        'winrate': winrate_list
    })

    if game_cutoff is not None:
        finalDF = finalDF[finalDF['games'] >= game_cutoff]
    
    if wr_cutoff_below is not None:
        finalDF = finalDF[finalDF['winrate'] <= wr_cutoff_below]

    if wr_cutoff_above is not None:
        finalDF = finalDF[finalDF['winrate'] >= wr_cutoff_above]

    if sort.lower() == 'games':
        finalDF = finalDF.sort_values('games', ascending=ascending).reset_index().drop(columns='index')
    if sort.lower() == 'winrate' or sort.lower() == 'wr':
        finalDF = finalDF.sort_values('winrate', ascending=ascending).reset_index().drop(columns='index')

    return finalDF

def get_simple_cq(team=None, startDate=None, endDate=None):
    """A simplified cq query that returns only a player's games played and winrate alongside their name and role. 

    Args:
        team (str, optional): Team being queried, if Team is none then Player must not be none. If Player is none and Team is not none, returns the soloq results for a full team. Defaults to None.
        startDate (str, optional): Start date of query. If startDate and endDate are None then patch must have a value. Defaults to None.
        endDate (str, optional): End date of query. If startDate and endDate are None then patch must have a value. Defaults to None.

    Returns:
        cqDF (dataframe): This will return a 5-row df including role, player name, games played and winrate for the 5 players on the queried team.
    """

    zip_list = [(team_dict[team]['top'], 'top'),
                (team_dict[team]['jungle'], 'jungle'),
                (team_dict[team]['mid'], 'mid'),
                (team_dict[team]['bot'], 'bot'),
                (team_dict[team]['support'], 'support')]

    player_list = []
    role_list = []
    games_list = []
    wr_list = []

    for p, r in zip_list:

        df = get_cq_champion_history(player=p, role=r, startDate=startDate, endDate=endDate, forAutomation=False, forAlgo=False)
        wr = np.NaN
        games = df['games'].sum()
        if games > 0:
            wr = df['wins'].sum() / games
        player_list.append(p)
        role_list.append(r.capitalize())
        games_list.append(games)
        wr_list.append(wr)
    
    cqDF = pd.DataFrame({
        'role': role_list,
        'player': player_list,
        'games': games_list,
        'winrate': wr_list
    })

    return cqDF

