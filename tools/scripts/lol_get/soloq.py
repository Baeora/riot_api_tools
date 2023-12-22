from common.core import *
from common.dictionaries import *

from datetime import datetime
from sqlalchemy import text
import pandas as pd
import numpy as np

def get_puuid(riot_id=None, riot_tag=None):

    with db_engine.connect() as connection:
        df = pd.read_sql(text(f"""
            select 
                distinct(puuid) 
            from
                soloq.ladder
            where
                riot_id = '{riot_id}' 
                and riot_tag = '{riot_tag}'
        """), connection)
    
    return df['puuid'][0]

def get_ladder(top=300):
    with db_engine.connect() as connection:
        ladder = pd.read_sql(text(f"""
            select * from soloq.ladder order by rank asc limit {top}
        """), connection)

    return ladder

def get_soloq_games(db_engine, riot_id=None, riot_tag=None, role=None, on_role=True, start_date=None, end_date=None, patch=None):

    """Gets all soloq games of the specified scope.

    Args:
        db_engine (obj, required): db_engine.
        playerName (str, required): Player you are searching.
        role (str, optional): Role of the player you are searching. (Filters offrole games out)
        startDate (str, required): Start Date.
        endDate (str, required): End Date.
        patch (float or list, required): Patch or list of patches for scope.
    
    Returns:
        dataframe: Returns a dataframe of all soloq games of the specified scope.
    """

    role = sql_role_dct[role.lower()]
    
    start_date = datetime.timestamp(datetime.strptime(start_date, '%m-%d-%Y'))*1000
    end_date = datetime.timestamp(datetime.strptime(end_date, '%m-%d-%Y'))*1000

    puuid_list = [get_puuid(riot_id=riot_id, riot_tag=riot_tag)]

    if len(puuid_list) == 0:
        print(f'No IDs for {riot_id}#{riot_tag}')
        return pd.DataFrame()
    
    select_block = '''TO_TIMESTAMP(game_creation/1000) as game_creation,
                    game_version,
                    match_id,
                    riot_id,
                    riot_tag,
                    REPLACE(team_position, 'UTILITY', 'SUPPORT') as team_position,
                    champion,
                    win,
                    gold_earned,
                    (total_minions_killed + total_neutral_minions_killed) as cs,
                    ROUND((gold_earned * 1.0 / (time_played/60)), 1) as gold_per_min,
                    ROUND(total_damage_dealt_champions * 1.0 / (time_played/60), 1) as dmg_per_min,
                    ROUND((total_neutral_minions_killed * 1.0 + total_minions_killed * 1.0) / (time_played/60), 1) as cs_per_min,
                    kills,
                    deaths,
                    assists,
                    summoner1_id,
                    summoner2_id,
                    vision_score,
                    wards_killed,
                    wards_placed,
                    control_wards_placed,
                    item0,
                    item1,
                    item2,
                    item3,
                    item4,
                    item5,
                    item6,
                    perk_keystone,
                    perk_primary_row_1,
                    perk_primary_row_2,
                    perk_primary_row_3,
                    perk_secondary_row_1,
                    perk_secondary_row_2,
                    perk_primary_style,
                    perk_secondary_style,
                    perk_shard_defense,
                    perk_shard_flex,
                    perk_shard_offense,
                    early_surrender,
                    surrender
                    '''
        
    from_block = '''soloq.regional_player_matches as sq'''

    sort_block = '''game_creation'''

    on_role_block = f""""""
    if on_role is True:
        on_role_block = f"""
                and team_position in ('{role}')"""

    if len(puuid_list) == 1:
        if start_date and end_date is not None:    
            where_block = f"""puuid in ('{puuid_list[0]}')
                and game_creation between ({start_date})
                and ({end_date})
                {on_role_block}
                and game_mode in ('CLASSIC')"""
        else:
            where_block = f"""puuid in ('{puuid_list[0]}')
                and game_version like ('{patch}%%')
                {on_role_block}
                and game_mode in ('CLASSIC')"""
    else: 
        if start_date and end_date is not None:    
            where_block = f"""
                puuid in{tuple(puuid_list)}
                and game_creation between ({start_date})
                and ({end_date})
                {on_role_block}
                and game_mode in ('CLASSIC')
            """
        else:
            where_block = f"""
                puuid in{tuple(puuid_list)}
                and game_version like ('{patch}%%')
                {on_role_block}
                and game_mode in ('CLASSIC')
            """

    with db_engine.connect() as connection:

        soloq = pd.read_sql(text(f"""
                select
                    {select_block}
                from
                    {from_block}
                where
                    {where_block}
                order by
                    {sort_block}
                """), connection)

    patchListTemp = soloq['game_version'].unique().tolist()
    patchList = []

    for item in patchListTemp:
        patch = ".".join(item.split(".", 2)[:2])
        patchList.append(patch)

    for i in range(len(patchListTemp)):
        soloq = soloq.replace(patchListTemp[i], patchList[i])
    
    soloq['riot_tag'] = soloq['riot_tag'].replace({'':np.NaN})
    soloq = soloq.replace({'':'?'})
    
    return soloq


