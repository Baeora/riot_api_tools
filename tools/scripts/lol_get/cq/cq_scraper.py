"""
Created on Wed Feb  9 02:06:56 2022
@author: isheng
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
import itertools
from uuid import uuid4
import time
from datetime import datetime, timedelta
import os
from pathlib import Path

from selenium.webdriver.firefox.options import Options

def days_before(days_prior=1, date=datetime.now(), return_str=True):
    """Returns the date from N days ago as a datetime object.

    Args:
        n (int, required): Number of days ago.
    Returns:
        datetime: Returns a datetime object for the date from N days prior to given date (Default Today).
    """
    raw_n_days_before = date - timedelta(days=days_prior)

    n_days_before = raw_n_days_before.strftime("%m/%d/%Y")

    if return_str:
        return n_days_before
    else:
        return raw_n_days_before

def format_team(match_ids, team_ids, dates, time, score, team):
    
    role = ['top','jungle','mid','bot','support']*len(score)
    score = np.repeat(list(map(int, score)),5)
    time = [t for t in time for i in range(5)]
    match_ids = [mi for mi in match_ids for i in range(5)]
    team_ids = [ti for ti in team_ids for i in range(5)]
    
    team_stats = []
    for p in team[1:]:
        try:
            cs = int(p.find_element(By.CLASS_NAME, 'cs').text)
            gold = int(p.find_element(By.CLASS_NAME, 'gold').text.replace(',',''))
            name = p.find_element(By.CLASS_NAME, 'name').text
            kda = p.find_element(By.CLASS_NAME, 'kda').text
            team_stats.append([name, kda, cs, gold])
        except ValueError:
            pass
        
    df_team = pd.DataFrame(team_stats, columns = ['player', 'kda', 'cs', 'gold'])
    df_team.loc[~df_team['player'].str.contains(' '), ['player']] = ' ' + df_team.loc[~df_team['player'].str.contains(' '), ['player']] 
    df_team[['team','player']] = df_team["player"].str.split(" ", 1, expand=True)
    df_team[['kills', 'deaths', 'assists']] = df_team['kda'].str.split('/',expand=True)
    df_team.drop(columns = 'kda', inplace=True)
    col_to_int = ['kills', 'deaths', 'assists']
    df_team[col_to_int] = df_team[col_to_int].apply(pd.to_numeric)
    df_team['result'] = score
    df_team['time'] = time
    df_team['date'] = dates
    df_team['champion'] = get_champs(team)
    df_team['match_id'] = match_ids
    df_team['role'] = role
    df_team['team_id'] = team_ids
    summoners = get_summoners(team)
    df_team['summoner_1'] = summoners[0]
    df_team['summoner_2'] = summoners[1]
    
    col_order = ['match_id','team_id','date','time','team','player','champion','role','summoner_1','summoner_2','result','kills','deaths','assists','cs','gold']
    return(df_team[col_order])

def get_champs(team):
    avatar = []
    champ_name = []
    for player in team:
        try:
            avatar.append(player.find_element(By.CLASS_NAME, 'style__StyledMatchPlayerAvatar-sc-3nnwgv-0'))
        except:
            pass
    
    for i in avatar:
        try:
            img_name = i.find_element(By.TAG_NAME, 'img').get_attribute('alt')
        except:
            img_name = 'Unknown'
        champ_name.append(img_name)
    return(champ_name)

def get_summoners(team):
    summoners = []
    for player in team:
        for i in player.find_elements(By.CLASS_NAME, 'style__StyledMatchPlayerSummoner-sc-191ei4l-0'):
            summoners.append(i.find_element(By.TAG_NAME, 'img').get_attribute('alt'))
    
    summoners_1 = summoners[::2]
    summoners_2 = summoners[1::2]
    return([summoners_1, summoners_2])

def Handler(event, lambda_context):

    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Firefox(options=options)
    url = "https://championsqueue.lolesports.com/en-us/match-history/"
    driver.get(url)
    script_path = os.path.abspath(os.path.dirname(__file__))
    time.sleep(15)

    t0 = time.time()

    print('clicking things')
    more = driver.find_elements(By.CLASS_NAME, 'see-more-button')

    try:
        last_date = pd.read_csv(os.path.join(script_path, 'CSVs\\champions_queue.csv'))['date'][0]
        date = datetime.strptime(last_date, '%Y-%m-%d')
        date = days_before(days_prior=1, date=date, return_str=False)
    except:
        date = datetime.now() - timedelta(days=120)


    last_year = date.date().year
    last_month = date.date().month
    last_day = date.date().day 

    prev_month = None
    
    while len(more) > 0: #maybe also include a condition that if there is no new date element so we can break after 1 days worth of data
        grab_dates = driver.find_elements(By.CLASS_NAME, 'day-and-month')
        date_check = grab_dates[len(grab_dates)-1].text.split()
        curr_month = date_check[0]
        curr_day = date_check[1]
        curr_year = datetime.now().year
        if prev_month == 'JANUARY' and curr_month != 'JANUARY':
            s = f'{curr_year-1} {curr_month} {curr_day}'
        else:
            s = f'{curr_year} {curr_month} {curr_day}'
        formatted_day = datetime.strptime(s, '%Y %B %d')
        if formatted_day < datetime(last_year,last_month,last_day):
            break
        prev_month = curr_month
        more[0].click()
        more = driver.find_elements(By.CLASS_NAME, 'see-more-button')

    expand = driver.find_elements(By.CLASS_NAME, 'expand-button')
    for e in expand:
        e.click()
        #consider extracting data as you click instead of clicking all then pulling all to avoid stale element exception

    match_date = [md.text for md in driver.find_elements(By.CLASS_NAME, 'day-and-month')]
    match_hist = [len(mh.find_elements(By.CLASS_NAME, 'match-card-time')*5) for mh in driver.find_elements(By.CLASS_NAME, 'match-history__StyledMatcHHistoryDay-sc-hdkyby-0')]

    match_time =  [mt.text for mt in driver.find_elements(By.CLASS_NAME, 'match-card-time')]
    score_container = [score.split(' - ') for score in [s.text for s in driver.find_elements(By.CLASS_NAME, 'score-container')]]

    team_left = driver.find_elements(By.CSS_SELECTOR, '.row.left')
    team_right = driver.find_elements(By.CSS_SELECTOR, '.row.right') 

    print('grabbing data')
    match_id = [str(uuid4()) for x in range(len(expand))]
    team_id1 = [str(uuid4()) for x in range(len(expand))]
    team_id2 = [str(uuid4()) for x in range(len(expand))]

    match_dates = list(itertools.chain(*(itertools.repeat(elem, n) for elem, n in zip(match_date, match_hist))))

    left_score, right_score = map(list, zip(*score_container))

    print('creating DFs...')
    df_left = format_team(match_id, team_id1, match_dates, match_time, left_score, team_left)
    df_right = format_team(match_id, team_id2, match_dates, match_time, right_score, team_right)

    df_output = pd.concat([df_left, df_right])

    df_output['date'] = df_output['date'] + f' {datetime.now().year}'
    df_output['date'] = pd.to_datetime(df_output['date'], format = '%B %d %Y')

    #%%
    test_h = df_output['time'].str[:5].str.strip()
    df_output['time'] = pd.to_datetime(test_h, format = '%I %p', utc = True).dt.hour

    #df_output.loc[~df_output['player'].str.contains(' '), ['player']] = ' ' + df_output.loc[~df_output['player'].str.contains(' '), ['player']] 
    #df_output[['team','player1']] = df_output["player"].str.split(" ", 1, expand=True)

    df_output['date'] = df_output['date'] + pd.to_timedelta(df_output['time'], unit='h')
    df_output['date'] = df_output['date'].dt.tz_localize('EST').dt.tz_convert('US/Pacific')
    df_output['time'] = df_output['date'].dt.time
    df_output['date'] = df_output['date'].dt.date
    # df_output = df_output[df_output.date >= datetime(last_year,last_month,last_day).date()].reset_index()
    df_output = df_output.drop_duplicates(subset=['date', 'time', 'team', 'player', 'champion', 'role', 'summoner_1', 'summoner_2', 'result', 'kills', 'deaths', 'assists', 'cs', 'gold']).reset_index(drop=True)
    df_output = df_output[['match_id', 'team_id', 'date', 'time', 'team', 'player', 'champion', 'role', 'summoner_1', 'summoner_2', 'result', 'kills', 'deaths', 'assists', 'cs', 'gold']]
    df_output.to_csv(os.path.join(script_path, 'CSVs\\champions_queue.csv'))

    t1 = time.time()
    print(t1-t0)

if __name__ == "__main__":
    Handler("","")

