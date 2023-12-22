import os
from pathlib import Path
import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta

from urllib.request import urlopen, Request
import json
from pathlib import Path

from common.dictionaries import *
from common.database_utils import *

from dotenv import load_dotenv
load_dotenv()

pd.options.mode.chained_assignment = None  # default='warn'
warnings.simplefilter(action='ignore', category=FutureWarning)

database_username = os.environ.get('database_username')
database_password = os.environ.get('database_password')
database_url = os.environ.get('database_url')
database_port = os.environ.get('database_port')
database_name = os.environ.get('database_name')
database_schema_name = os.environ.get('database_schema')

db_engine = create_db_engine(
    database_url, database_port, database_username, database_password, database_name)

service_file = os.path.join(os.path.dirname(Path.cwd()), 'JSONs\\unique-epigram-337119-5b7bc9cfd665.json')

api_key = f"api_key={os.environ.get('api_key')}"

###############
### CDragon ###
###############

def json_extract(obj, key):
    """Nested json extract function

    Args:
        obj (dict): Dictionary you're searching through
        key (str): Key you're looking for

    Returns:
        list: Returns a list of every dictionary value at key
    """    
    arr = []

    def extract(obj, arr, key):

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def get_item_ids():
    """Pulls all item IDs from Cdragon and returns them as a dataframe.

    Returns:
        item_ids (dataframe): Dataframe of item IDs.
    """    

    response = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json', headers={'User-Agent': 'Mozilla'}))

    data_json = json.loads(response.read())

    icon_path = json_extract(data_json, 'iconPath')
    path_name = []
    for path in icon_path:
        path_name.append(path.split('/lol-game-data/assets/ASSETS/Items/Icons2D/')[1].lower())

    item_ids = pd.DataFrame({
        'id': json_extract(data_json, 'id'),
        'name': json_extract(data_json, 'name'),
        'path_name': path_name
    })

    return item_ids

def get_perk_ids(addPaths=False):
    """Pulls all perk IDs from Cdragon and returns them as a dictionary (or dataframe with image strings).

    Args:
        addPaths: If True, will instead return a 3-Column DataFrame containing image strings for each perk.

    Returns:
        perk_ids (dictionary): Dictionary of perk IDs.
        perk_ids (dataframe): Dataframe of perk IDs containing image strings for each perk.
    """

    perk_req = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json', headers={'User-Agent': 'Mozilla'}))
    style_req = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json', headers={'User-Agent': 'Mozilla'}))

    perk_json = json.loads(perk_req.read())
    style_json = json.loads(style_req.read())

    if addPaths:
        perk_ids = pd.DataFrame({
            'id': json_extract(perk_json, 'id'),
            'name': json_extract(perk_json, 'name'),
            'path_name': json_extract(perk_json, 'iconPath')
        })

        style_ids = pd.DataFrame({
            'id': json_extract(style_json, 'id')[0::5],
            'name': json_extract(style_json, 'name'),
            'path_name': json_extract(style_json, 'iconPath')
        })        

        for i in range(len(perk_ids)):
            perk_ids['path_name'][i] = (perk_ids['path_name'][i].split('/lol-game-data/assets/v1/perk-images/')[1].lower())

        for i in range(len(style_ids)):
            style_ids['path_name'][i] = (style_ids['path_name'][i].split('/lol-game-data/assets/v1/perk-images/')[1].lower())

        perks = pd.concat([perk_ids, style_ids]).reset_index(drop=True)
    else:
        perk_ids = json_extract(perk_json, 'id')
        perk_names = json_extract(perk_json, 'name')

        perk_ids.extend(json_extract(style_json, 'id'))
        perk_names.extend(json_extract(style_json, 'name'))

        perks = dict(map(lambda i,j : (int(i),j) , perk_ids,perk_names))

    return perks

def get_champion_ids():
    """Pulls all champion IDs from Cdragon and returns them as a dataframe.

    Returns:
        champion_ids (dataframe): Dataframe of champion IDs.
    """
    
    response = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json', headers={'User-Agent': 'Mozilla'}))

    data_json = json.loads(response.read())

    champion_ids = pd.DataFrame({
        'id': json_extract(data_json, 'id'),
        'name': json_extract(data_json, 'name'),
        'alias': json_extract(data_json, 'alias')
    })
    
    champion_ids['link_head'] = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/"
    champion_ids['link_tail'] = ".png"


    champion_ids['img'] = champion_ids['link_head'] + champion_ids['id'].astype(str) + champion_ids['link_tail']

    champion_ids.drop(columns=['link_head', 'link_tail'], inplace=True)

    champion_ids = champion_ids[1:].sort_values('name').reset_index(drop=True)

    return champion_ids

def get_summoner_spell_ids():
    """Pulls all summoner spell IDs from Cdragon and returns them as a dataframe.

    Returns:
        summoner_spell_ids (dataframe): Dataframe of summoner spell IDs.
    """
    response = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/summoner-spells.json', headers={'User-Agent': 'Mozilla'}))

    summoner_spell_json = json.loads(response.read())

    icon_path = json_extract(summoner_spell_json, 'iconPath')
    path_name = []
    for path in icon_path:
        path_name.append(path.split('/lol-game-data/assets/')[1].lower())

    summoner_spell_ids = pd.DataFrame({
        'id': json_extract(summoner_spell_json, 'id'),
        'name': json_extract(summoner_spell_json, 'name'),
        'path_name': path_name
    })

    return summoner_spell_ids

def get_newest_champ():
    """Returns the most recently released champion's name

    Returns:
        str: Name of the most recently released champion.
    """
    return get_champion_ids().sort_values('id', ascending=False).reset_index(drop=True)['name'][0]

def convert_perks(df):
    """Converts Perk IDs in a dataframe to their actual given Perk names

    Args:
        df (dataframe): Dataframe who's Perk IDs you wish to alter

    Returns:
        df: New dataframe with given Perk names
    """    

    perks = get_perk_ids()

    perk_cols = ['perk_keystone',
                'perk_primary_row_1',
                'perk_primary_row_2',
                'perk_primary_row_3',
                'perk_secondary_row_1',
                'perk_secondary_row_2',
                'perk_primary_style',
                'perk_secondary_style',
                'perk_shard_defense',
                'perk_shard_flex',
                'perk_shard_offense']

    df[perk_cols] = df[perk_cols].replace(perks)
    
    return df

def add_images(df):
    """Adds image hyperlinks from Cdragon to a df based on the given IDs found in that df

    Args:
        df (dataframe): Dataframe that you wish to add image links to

    Returns:
        image_df: New dataframe with image links added
    """    
    df['image'] = ''
    ids = get_champion_ids()

    image_df = pd.merge(left=df, right=ids, left_on='champion', right_on='name', how='inner')

    for i in range(len(df)-1):
        id = image_df['id'][i]
        image_df['image'][i] = f'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{id}.png'
    
    image_df = image_df.drop(columns=['name', 'id'])

    images = image_df.pop('image')
    image_df.insert(0, 'image', images)

    return image_df

######################
### Time Functions ###
######################

def today(str="%m/%d/%Y"):
    """Returns today's date as a datetime object.

    Args:
        
    Returns:
        datetime: Returns a datetime object for today's date.
    """
    raw_today = datetime.now()
    today = raw_today.strftime(str)

    return today

def days_before(days_prior=1, date=datetime.now(), str_format="%m/%d/%Y", return_str=True):
    """Returns the date from N days ago as a datetime object.

    Args:
        n (int, required): Number of days ago.
    Returns:
        datetime: Returns a datetime object for the date from N days prior to given date (Default Today).
    """
    
    if type(date) == str:
        date = datetime.strptime(date, str_format)

    raw_n_days_before = date - timedelta(days=days_prior)

    n_days_before = raw_n_days_before.strftime(str_format)

    if return_str:
        return n_days_before
    else:
        return raw_n_days_before

def days_after(date=datetime.now(), days_after=1, str_format="%m/%d/%Y", return_str=True):

    """Returns the date from N days ago as a datetime object.

    Args:
        n (int, required): Number of days ago.
    Returns:
        datetime: Returns a datetime object for the date from N days prior to given date (Default Today).
    """

    if type(date) == str:
        date = datetime.strptime(date, str_format)

    raw_n_days_after = date + timedelta(days=days_after)

    n_days_after = raw_n_days_after.strftime("%m/%d/%Y")

    if return_str:
        return n_days_after
    else:
        return raw_n_days_after

def convert_ms(time):
    """Converts ms to game time xx:xx

    Args:
        time (int): Time in ms. 

    Returns:
        str: Returns min:sec time format
    """   
    if type(time) != str:
        min = str(int(time / 60000)).zfill(2)
        sec = str(int((time % 60000)/1000)).zfill(2)
        return f'{min}:{sec}'
    else:
        min = int(time.split(':')[0]) * 60000
        sec = int(time.split(':')[1]) * 1000
        return min+sec

######################
### Stat Functions ###
######################

def calc_dist_vect(x1, x2, y1, y2):
    """Calculates the distance vector between X1,Y1 and X2,Y2.

    Args:
        x1 (int, float): x1
        x2 (int, float): x2
        y1 (int, float): y1
        y2 (int, float): y2

    Returns:
        float: Returns the distance vector between X1,Y1 and X2,Y2.
    """

    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def remove_outlier_IQR(df=None, stat=None):
    """Removes outliers from a Dataframe based on inputted stat name. 

    Args:
        df (dataframe): Dataframe to be trimmed. Defaults to None.
        stat (str): Column name with the stat you wish to remove the outlier of. Defaults to None.

    Returns:
        dataframe: _description_
    """
    Q1=df[stat].quantile(0.25)
    Q3=df[stat].quantile(0.75)
    IQR=Q3-Q1
    df_final=df[~((df[stat]<(Q1-1.5*IQR)) | (df[stat]>(Q3+1.5*IQR)))]
    return df_final
