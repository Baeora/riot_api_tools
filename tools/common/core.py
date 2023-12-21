import os
from pathlib import Path
import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

def convert_perks(df):
    """Converts Perk IDs in a dataframe to their actual given Perk names

    Args:
        df (dataframe): Dataframe who's Perk IDs you wish to alter

    Returns:
        df: New dataframe with given Perk names
    """    
    perk_index = df.columns.get_loc('perks')

    df.insert(perk_index, 'keystone', '')
    df.insert(perk_index+1, 'secondary', '')

    for i in range(len(df)):

        df['keystone'][i] = json_extract(df['perks'][i], 'perk')[0]
        df['secondary'][i] = json_extract(df['perks'][i], 'style')[1]

    df.drop(columns=['perks'], inplace=True)
    
    return df

def json_extract(obj, key):
    """Nested json extract function

    Args:
        obj (dict): Dictionary you're searching through
        key (str): Key you're looking for

    Returns:
        value: Returns dictionary value at key
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
    from urllib.request import urlopen, Request
    import json

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

def get_rune_ids():
    """Pulls all rune IDs from Cdragon and returns them as a dataframe.

    Returns:
        rune_ids (dataframe): Dataframe of rune IDs.
    """
    from urllib.request import urlopen, Request
    import json

    raw_keystone = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json', headers={'User-Agent': 'Mozilla'}))

    keystone_json = json.loads(raw_keystone.read())

    keystone_ids = pd.DataFrame({
        'id': json_extract(keystone_json, 'id'),
        'name': json_extract(keystone_json, 'name'),
        'path_name': json_extract(keystone_json, 'iconPath')
    })

    for i in range(len(keystone_ids)):

        keystone_ids['path_name'][i] = (keystone_ids['path_name'][i].split('/lol-game-data/assets/v1/perk-images/')[1].lower())

    raw_secondary_runes = urlopen(Request('https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json', headers={'User-Agent': 'Mozilla'}))

    secondary_runes_json = json.loads(raw_secondary_runes.read())

    secondary_runes_ids = pd.DataFrame({
        'id': json_extract(secondary_runes_json, 'id')[0::5],
        'name': json_extract(secondary_runes_json, 'name'),
        'path_name': json_extract(secondary_runes_json, 'iconPath')
    })

    for i in range(len(secondary_runes_ids)):

        secondary_runes_ids['path_name'][i] = (secondary_runes_ids['path_name'][i].split('/lol-game-data/assets/v1/perk-images/')[1].lower())

    rune_ids = pd.concat([keystone_ids, secondary_runes_ids]).reset_index(drop=True)

    return rune_ids

def get_champion_ids():
    """Pulls all champion IDs from Cdragon and returns them as a dataframe.

    Returns:
        champion_ids (dataframe): Dataframe of champion IDs.
    """
    from urllib.request import urlopen, Request
    import json
    
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
    from urllib.request import urlopen, Request
    import json

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
    return get_champion_ids().sort_values('id', ascending=False).reset_index(drop=True)['name'][0]

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
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def remove_outlier_IQR(df=None, stat=None):
    Q1=df[stat].quantile(0.25)
    Q3=df[stat].quantile(0.75)
    IQR=Q3-Q1
    df_final=df[~((df[stat]<(Q1-1.5*IQR)) | (df[stat]>(Q3+1.5*IQR)))]
    return df_final

######################
### Misc Functions ###
######################

def send_email(type=None):
    """Quick function to send an email to myself for daily runs so I can see from home if they succeeded or not / whether or not I need to come in early to bugfix. Don't ask why it's written so poorly

    Args:
        type (str, optional): 'Started', 'Complete', 'Failed'. Defaults to None.
    """    
    

    if type == 'Started':
        msg_type = 'Started'
    elif type == 'Complete':
        msg_type = 'Complete'
    elif type == 'Failed':
        msg_type = 'Failed'
    else:
        print("Type must be 'Started', 'Failed' or 'Complete'")

    msg = MIMEMultipart()
    msg['From'] = 'lolbeora@gmail.com'
    msg['To'] = 'mskriloff@evilgeniuses.gg'
    msg['Subject'] = f'{msg_type}'
    message = f'Daily Run {msg_type}!'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('lolbeora@gmail.com', 'oahoqlaccrgpgroo')

    mailserver.sendmail('lolbeora@gmail.com','mskriloff@evilgeniuses.gg',msg.as_string())

    mailserver.quit()
