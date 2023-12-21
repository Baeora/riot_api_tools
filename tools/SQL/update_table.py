from common.database_utils import *
from common.core import *

from LoLAPI.soloq import api_get_match_history, api_get_ladder
from scripts.lol_get.soloq import *
from scripts.lol_get.drafts import *

from datetime import datetime, timezone
from sqlalchemy import text
import pandas as pd

def add_upsert(df):
    df['upsert_at'] = datetime.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    return df

def get_tournament_tags(year=None):
    lcs_spring = f'LCS+{year}+Spring%2C+LCS+{year}+Spring+Playoffs'
    lcs_summer = f'LCS+{year}+Summer%2C+LCS+{year}+Championship'

    nacl_spring = f'NA+Academy+{year}+Spring%2C+NA+Academy+{year}+Spring+Playoffs%2C+NACL+{year}+Spring%2C+LCS+Proving+Grounds+{year}+Spring%2C+PGCQ+{year}+Spring+1%2C+PGCQ+{year}+Spring+1+OQ%2C+PGCQ+{year}+Spring+2%2C+PGCQ+{year}+Spring+2+OQ'
    nacl_summer = f'NA+Academy+{year}+Summer%2C+NA+Academy+{year}+Summer+Playoffs%2C+NACL+{year}+Summer%2C+LCS+Proving+Grounds+{year}+Summer%2C+PGCQ+{year}+Summer+1%2C+PGCQ+{year}+Summer+1+OQ%2C+PGCQ+{year}+Summer+2%2C+PGCQ+{year}+Summer+2+OQ'

    lec_spring = f'LEC+{year}+Spring%2C+LEC+{year}+Spring+Playoffs%2C+EM+{year}+Spring+Main+Event%2C+LVP+SL+{year}+Spring+Playoffs%2C+LVP+SL+{year}+Spring'
    lec_summer = f'LEC+{year}+Summer%2C+LEC+{year}+Summer+Playoffs%2C+LVP+SL+{year}+Summer'

    lck_spring = f'LCK+{year}+Spring%2C+LCS+{year}+Spring+Playoffs'
    lck_summer = f'LCK+{year}+Summer%2C+LCS+{year}+Summer+Playoffs%2C+{year}+Regional+finals'

    lpl_spring = f'LPL+{year}+Spring%2C+LPL+{year}+Spring+Playoffs'
    lpl_summer = f'LPL+{year}+Summer%2C+LPL+{year}+Summer+Playoffs%2C+{year}+Regional+finals'

    ljl_spring = f'LJL+{year}+Spring%2C+LJL+{year}+Spring+Playoffs'
    ljl_summer = f'LJL+{year}+Summer%2C+LJL+{year}+Summer+Playoffs'

    pcs_spring = f'PCS+{year}+Spring%2C+PCS+{year}+Spring+Playoffs'
    pcs_summer = f'PCS+{year}+Summer%2C+PCS+{year}+Summer+Playoffs'

    vcs_spring = f'VCS+{year}+Spring%2C+VCS+{year}+Spring+Playoffs'
    vcs_summer = f'VCS+{year}+Summer+Promotion%2C+VCS+{year}+Summer%2C+VCS+{year}+Summer+Playoffs'

    lco_spring = f'LCO+{year}+Split+1%2C+LCO+{year}+Split+1+Playoffs'
    lco_summer = f'LCO+{year}+Split+2%2C+LCO+{year}+Split+2+Playoffs'

    cblol_spring = f'CBLOL+{year}+Split+1%2C+CBLOL+{year}+Split+1+Playoffs'
    cblol_summer = f'CBLOL+{year}+Split+2%2C+CBLOL+{year}+Split+2+Playoffs'

    lla_spring = f'LLA+{year}+Opening+Promotion%2C+LLA+{year}+Opening+Promotion%2C+LLA+{year}+Opening+Playoffs'
    lla_summer = f'LLA+{year}+Closing%2C+LLA+{year}+Closing+Playoffs'

    tcl_spring = f'TCS+{year}+Winter%2C+TCS+{year}+Winter+Playoffs'
    tcl_summer = f'LCS+{year}+Summer%2C+LCS+{year}+Summer+Playoffs'

    lcl_spring = f'LCL+{year}+Spring%2C+LCL+{year}+Spring+Playoffs'
    lcl_summer = f'LCL+{year}+Summer%2C+LCL+{year}+Summer+Playoffs'

    tags = [lcs_spring, lcs_summer, 
            nacl_spring, nacl_summer, 
            lec_spring, lec_summer, 
            lck_spring, lck_summer, 
            lpl_spring, lpl_summer, 
            ljl_spring, ljl_summer,
            pcs_spring, pcs_summer,
            vcs_spring, vcs_summer,
            lco_spring, lco_summer,
            cblol_spring, cblol_summer,
            lla_spring, lla_summer,
            tcl_spring, tcl_summer,
            lcl_spring, lcl_summer]
    
    return tags

#####################
### Update Tables ###
#####################

def update_table_ladder():
    ladder = api_get_ladder(top=2000)
    df_to_sql(add_upsert(ladder), db_engine, 'soloq', 'ladder', 'rank')

def update_table_soloq():

    ladder = get_ladder(top=750)

    soloq_df = pd.DataFrame()
    i=0
    for id, tag in zip(ladder['riot_id'].tolist(), ladder['riot_tag'].tolist()):
        print(f'{i} - {id}#{tag}')
        mh = api_get_match_history(gameName=id, tagLine=tag)
        soloq_df = pd.concat([soloq_df, mh])
        i += 1

    soloq_df['uuid'] = soloq_df['match_id'] + '_' + soloq_df['riot_id']
    soloq_df.set_index('uuid')

    print(f'Upserting {len(soloq_df)} new entries . . .')
    df_to_sql(add_upsert(soloq_df), db_engine, 'soloq', 'regional_player_matches', 'uuid')

def update_table_game_summary():
    pb = pd.DataFrame()
    for year in [2021, 2022, 2023]:
        for long_tag in get_tournament_tags(year):
            try:
                link = f'https://lol.fandom.com/wiki/Special:RunQuery/PickBanHistory?PBH%5Bpage%5D={long_tag}&PBH%5Bteam%5D=&PBH%5Btextonly%5D%5Bis_checkbox%5D=true&PBH%5Btextonly%5D%5Bvalue%5D=&_run=&pfRunQueryFormName=PickBanHistory&wpRunQuery=&pf_free_text='
                df = clean_leaguepedia(link)

                if 'spring' in long_tag.lower():
                    tag = 'Spring'
                if 'summer' in long_tag.lower():
                    tag = 'Summer'
                if 'winter' in long_tag.lower():
                    tag = 'Winter'
                
                df['year'] = str(year)
                df['tag'] = tag

                pb = pd.concat([pb, df]).reset_index(drop=True)
                print({long_tag})
            except:
                print(f'Could not find tables for {long_tag}')

    pb['uuid'] = pb['team_1_name'] + '_' + pb['team_2_name'] + '_' + pb['year'] + '_' + pb['tag'] + '_' + pb['phase'] + '_' + pb['score']
    pb = pb.drop_duplicates(subset='uuid')
    df_to_sql(add_upsert(pb), db_engine, 'stage', 'game_summary', 'uuid')