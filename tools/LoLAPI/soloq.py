import requests
import pandas as pd
from concurrent.futures import as_completed, ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

from scripts.lol_get.soloq import *
from common.core import *
from common.database_utils import *

###############
### Process ###
###############

def process_match_json(match_json, puuid):

    side_dict = {
        100:'blue',
        200:'red'
    }

    try:
        info = match_json['info']


        metadata = match_json['metadata']
        matchId = metadata['matchId']
        participants = metadata['participants']

        player = info['participants'][participants.index(puuid)]

        gameCreation = info['gameCreation']
        gameStartTimestamp = info['gameStartTimestamp']
        gameEndTimestamp = info['gameEndTimestamp']
        timePlayed = (gameEndTimestamp-gameStartTimestamp)/1000
        gameMode = info['gameMode']
        gameVersion = info['gameVersion']
        platformId = info['platformId']
        queueId = info['queueId']
        puuid = player['puuid']
        riotIdGameName = player['summonerName']
        try:
            riotIdTagLine = player['riotIdTagline']
        except:
            riotIdTagLine = ''
        side = side_dict[player['teamId']]
        win = player['win']

        champion = player['championName']
        kills = player['kills']
        deaths = player['deaths']
        assists = player['assists']
        summOne = player['summoner1Id']
        summTwo = player['summoner2Id']
        earlySurrender = player['gameEndedInEarlySurrender']
        surrender = player['gameEndedInSurrender']
        firstBlood = player['firstBloodKill']
        firstBloodAssist = player['firstBloodAssist']
        firstTower = player['firstTowerKill']
        firstTowerAssist = player['firstTowerAssist']
        dragonKills = player['dragonKills']

        damageDealtToBuildings = player['damageDealtToBuildings']
        damageDealtToObjectives = player['damageDealtToObjectives']
        damageSelfMitigated = player['damageSelfMitigated']
        goldEarned = player['goldEarned']
        teamPosition = player['teamPosition']
        lane = player['lane']
        largestKillingSpree = player['largestKillingSpree']
        longestTimeSpentLiving = player['longestTimeSpentLiving']
        objectivesStolen = player['objectivesStolen']
        totalMinionsKilled = player['totalMinionsKilled']
        totalAllyJungleMinionsKilled = player['totalAllyJungleMinionsKilled']
        totalEnemyJungleMinionsKilled = player['totalEnemyJungleMinionsKilled']
        totalNeutralMinionsKilled = totalAllyJungleMinionsKilled + totalEnemyJungleMinionsKilled
        totalDamageDealtToChampions = player['totalDamageDealtToChampions']
        totalDamageShieldedOnTeammates = player['totalDamageShieldedOnTeammates']
        totalHealsOnTeammates = player['totalHealsOnTeammates']
        totalDamageTaken = player['totalDamageTaken']
        totalTimeCCDealt = player['totalTimeCCDealt']
        totalTimeSpentDead = player['totalTimeSpentDead']
        turretKills = player['turretKills']
        turretsLost = player['turretsLost']
        visionScore = player['visionScore']
        controlWardsPlaced = player['detectorWardsPlaced']
        wardsKilled = player['wardsKilled']
        wardsPlaced = player['wardsPlaced']

        item0 = player['item0']
        item1 = player['item1']
        item2 = player['item2']
        item3 = player['item3']
        item4 = player['item4']
        item5 = player['item5']
        item6 = player['item6']

        perks = player['perks']

        perkKeystone = perks['styles'][0]['selections'][0]['perk']
        perkPrimaryRow1 = perks['styles'][0]['selections'][1]['perk']
        perkPrimaryRow2 = perks['styles'][0]['selections'][2]['perk']
        perkPrimaryRow3 = perks['styles'][0]['selections'][3]['perk']
        perkPrimaryStyle = perks['styles'][0]['style']
        perkSecondaryRow1 = perks['styles'][1]['selections'][0]['perk']
        perkSecondaryRow2 = perks['styles'][1]['selections'][1]['perk']
        perkSecondaryStyle = perks['styles'][1]['style']
        perkShardDefense = perks['statPerks']['defense']
        perkShardFlex = perks['statPerks']['flex']
        perkShardOffense = perks['statPerks']['offense']


        matchDF = pd.DataFrame({
            'match_id': [matchId],
            'participants': [participants],
            'game_creation': [gameCreation],
            'game_start_timestamp': [gameStartTimestamp],
            'game_end_timestamp': [gameEndTimestamp],
            'game_version': [gameVersion],
            'queue_id': [queueId],
            'game_mode': [gameMode],
            'platform_id': [platformId],
            'puuid': [puuid],
            'riot_id': [riotIdGameName],
            'riot_tag': [riotIdTagLine],
            'time_played': [timePlayed],
            'side': [side],
            'win': [win],
            'team_position': [teamPosition],
            'lane': [lane],
            'champion': [champion],
            'kills': [kills],
            'deaths': [deaths],
            'assists': [assists],
            'summoner1_id': [summOne],
            'summoner2_id': [summTwo],
            'gold_earned': [goldEarned],
            'total_minions_killed': [totalMinionsKilled],
            'total_neutral_minions_killed': [totalNeutralMinionsKilled],
            'total_ally_jungle_minions_killed': [totalAllyJungleMinionsKilled],
            'total_enemy_jungle_minions_killed': [totalEnemyJungleMinionsKilled],
            'early_surrender': [earlySurrender],
            'surrender': [surrender],
            'first_blood': [firstBlood],
            'first_blood_assist': [firstBloodAssist],
            'first_tower': [firstTower],
            'first_tower_assist': [firstTowerAssist],
            'damage_dealt_to_buildings': [damageDealtToBuildings],
            'turret_kills': [turretKills],
            'turrets_lost': [turretsLost],
            'damage_dealt_to_objectives': [damageDealtToObjectives],
            'dragonKills': [dragonKills],
            'objectives_stolen': [objectivesStolen],
            'longest_time_spent_living': [longestTimeSpentLiving],
            'largest_killing_spree': [largestKillingSpree],
            'total_damage_dealt_champions': [totalDamageDealtToChampions],
            'total_damage_taken': [totalDamageTaken],
            'total_damage_self_mitigated': [damageSelfMitigated],
            'total_damage_shielded_teammates': [totalDamageShieldedOnTeammates],
            'total_heals_teammates': [totalHealsOnTeammates],
            'total_time_crowd_controlled': [totalTimeCCDealt],
            'total_time_spent_dead': [totalTimeSpentDead],
            'vision_score': [visionScore],
            'wards_killed': [wardsKilled],
            'wards_placed': [wardsPlaced],
            'control_wards_placed': [controlWardsPlaced],
            'item0': [item0],
            'item1': [item1],
            'item2': [item2],
            'item3': [item3],
            'item4': [item4],
            'item5': [item5],
            'item6': [item6],
            'perk_keystone': [perkKeystone],
            'perk_primary_row_1': [perkPrimaryRow1],
            'perk_primary_row_2': [perkPrimaryRow2],
            'perk_primary_row_3': [perkPrimaryRow3],
            'perk_secondary_row_1': [perkSecondaryRow1],
            'perk_secondary_row_2': [perkSecondaryRow2],
            'perk_primary_style': [perkPrimaryStyle],
            'perk_secondary_style': [perkSecondaryStyle],
            'perk_shard_defense': [perkShardDefense],
            'perk_shard_flex': [perkShardFlex],
            'perk_shard_offense': [perkShardOffense],
        })
    
        return matchDF
    except:
        return pd.DataFrame()

def get_stored_matches(): 
    with db_engine.connect() as connection:
        df = pd.read_sql(text(f"""
            select distinct(match_id) from soloq.regional_player_matches
        """), connection)

    return df['match_id'].tolist()

################
### Riot API ###
################

def api_get_puuid(summonerId=None, gameName=None, tagLine=None, region='americas'):

    if summonerId is not None:
        root_url = 'https://na1.api.riotgames.com/'
        endpoint = 'lol/summoner/v4/summoners/'

        response = requests.get(root_url+endpoint+summonerId+'?'+api_key)

        return response.json()['puuid']
    else:
        root_url = f'https://{region}.api.riotgames.com/'
        endpoint = f'riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'

        response = requests.get(root_url+endpoint+'?'+api_key)

        return response.json()['puuid']

def api_get_idtag_from_puuid(puuid=None):

    root_url = 'https://americas.api.riotgames.com/'
    endpoint = 'riot/account/v1/accounts/by-puuid/'

    response = requests.get(root_url+endpoint+puuid+'?'+api_key)

    id = {
        'gameName': response.json()['gameName'],
        'tagLine': response.json()['tagLine']
    }

    return id

def api_get_idtag_from_summonerId_df(df):
    
    puuid_session = FuturesSession(executor=ProcessPoolExecutor(max_workers=10))
    idtag_session = FuturesSession(executor=ProcessPoolExecutor(max_workers=10))
    retries = 5
    status_forcelist = [429]
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        respect_retry_after_header=True,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)

    puuid_session.mount('http://', adapter)
    puuid_session.mount('https://', adapter)

    idtag_session.mount('http://', adapter)
    idtag_session.mount('https://', adapter)

    summonerIds = df['summonerId'].tolist()
    puuid_threads=[puuid_session.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}'+'?'+api_key) for summonerId in summonerIds]

    puuids = []
    summonerIds = []
    t1=time.time()
    for future in as_completed(puuid_threads):
        resp = future.result()
        summonerIds.append(resp.json()['id'])
        puuids.append(resp.json()['puuid'])
    t2=time.time()
    print(f'summonerId -> puuid -- {round(t2-t1, 2)}s')
        
    sum_puuid_df = pd.DataFrame({
        'puuid': puuids,
        'summonerId': summonerIds
    })

    idtag_threads=[puuid_session.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'+'?'+api_key) for puuid in puuids]

    df = pd.DataFrame()
    t1=time.time()
    for future in as_completed(idtag_threads):
        resp = future.result()
        idtag = pd.DataFrame({
            'puuid': [resp.json()['puuid']],
            'gameName': [resp.json()['gameName']],
            'tagLine': [resp.json()['tagLine']],
        })
        df = pd.concat([df, idtag])
    t2=time.time()
    print(f'puuid -> idtag -- {round(t2-t1, 2)}s')

    df = df.merge(sum_puuid_df, on='puuid', how='inner')

    return df[['summonerId', 'puuid', 'gameName', 'tagLine']]

def api_get_ladder(top=300, include_tag=True):

    root_url = 'https://na1.api.riotgames.com/'
    challenger = 'lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    grandmaster = 'lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5'
    master = 'lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5'

    chall_resp = requests.get(root_url+challenger+'?'+api_key)
    chall_df = pd.DataFrame(chall_resp.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)

    gm_df = pd.DataFrame()
    m_df = pd.DataFrame()
    
    if top > 300:
        gm_resp = requests.get(root_url+grandmaster+'?'+api_key)
        gm_df = pd.DataFrame(gm_resp.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)
    if top > 1000:
        m_resp = requests.get(root_url+master+'?'+api_key)
        m_df = pd.DataFrame(m_resp.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)

    df = pd.concat([chall_df, gm_df, m_df]).reset_index(drop=True)[0:top]

    if include_tag:
        print('Grabbing Tags . . .')
        idtags = api_get_idtag_from_summonerId_df(df)
        df = df.merge(idtags, on='summonerId', how='outer')

        col = df.columns.tolist()
        col.remove('summonerName')
        col.remove('gameName')
        col.remove('tagLine')
        col.remove('puuid')
        col.insert(1, 'tagLine')
        col.insert(1, 'gameName')
        col.insert(1, 'puuid')

        df = df[col].reset_index()
        df.columns = ['rank', 'summoner_id', 'puuid', 'riot_id', 'riot_tag', 'lp', 'tier', 'wins', 'losses', 'veteran', 'inactive', 'fresh_blood', 'hot_streak']
        df['rank'] +=1

        return df 

    df = df.reset_index()
    df.columns = ['rank', 'summoner_id', 'puuid', 'riot_id', 'riot_tag', 'lp', 'tier', 'wins', 'losses', 'veteran', 'inactive', 'fresh_blood', 'hot_streak']
    df['rank'] +=1

    return df

def api_get_match_history_ids(puuid=None, region='americas', queue=420, start=0, count=100):

    try:
        root_url = f'https://{region}.api.riotgames.com'
        endpoint = f'/lol/match/v5/matches/by-puuid/{puuid}/ids'
        query_params = f'?queue={queue}&start={start}&count={count}'

        response = requests.get(root_url+endpoint+query_params+'&'+api_key)

        return response.json()
    except:
        return False

def api_get_match_history(gameName=None, tagLine=None, region='americas', debug=False):


    session = FuturesSession(executor=ProcessPoolExecutor(max_workers=10))
    retries = 5
    status_forcelist = [429]
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        respect_retry_after_header=True,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        puuid = get_puuid(riot_id=gameName, riot_tag=tagLine, region=region)
    except:
        puuid = api_get_puuid(gameName=gameName, tagLine=tagLine, region=region)

    matchIds = api_get_match_history_ids(puuid=puuid)

    try:
        stored_matches = get_stored_matches()
        matchIds = [x for x in matchIds if x not in stored_matches]
    except:
        pass

    df = pd.DataFrame()
    if len(matchIds) > 0:
        futures=[session.get(f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}'+'?'+api_key) for matchId in matchIds]
        
        i=0
        for future in as_completed(futures):
            resp = future.result()
            if debug:
                t1=time.time()
                df = pd.concat([df, process_match_json(resp.json(), puuid)])
                t2=time.time()
                print(resp.json()['metadata']['matchId']+f' - {i} ({round(t2-t1, 2)}s)')
                i+=1
            else:
                df = pd.concat([df, process_match_json(resp.json(), puuid)])

        return df
    else:
        print(f'No new matches for {gameName}#{tagLine}')
        return pd.DataFrame()
