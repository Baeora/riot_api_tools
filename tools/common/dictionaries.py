"""
sql_role_dct: Used to normalize roles when querying vs a SQL database
replacement_dct: Used to grab colloquial Champion names (MonkeyKing = Wukong etc)
soloq_region_dict: Used to normalize routing between SoloQ regions for Riot Endpoints
"""

sql_role_dct = {
            'top': 'TOP',
            'jungle': 'JUNGLE',
            'jng': 'JUNGLE',
            'jg': 'JUNGLE',
            'mid': 'MIDDLE',
            'middle': 'MIDDLE',
            'bot': 'BOTTOM',
            'bottom': 'BOTTOM',
            'adc': 'BOTTOM',
            'support': 'UTILITY',
            'sup': 'UTILITY',
            'utility': 'UTILITY'
}

replacement_dct = {
            'TahmKench' : 'Tahm Kench',
            'MonkeyKing' : 'Wukong',
            'LeeSin' : 'Lee Sin',
            'XinZhao' : 'Xin Zhao',
            'Kaisa' : 'Kai\'Sa',
            'TwistedFate' : 'Twisted Fate',
            'AurelionSol' : 'Aurelion Sol',
            'KogMaw' : 'Kog\'Maw',
            'RekSai' : 'Rek\'Sai',
            'Chogath' : 'Cho\'Gath',
            'Khazix' : 'Kha\'Zix',
            'Velkoz' : 'Vel\'Koz',
            'DrMundo' : 'Dr. Mundo',
            'Leblanc' : 'LeBlanc',
            'MasterYi' : 'Master Yi',
            'MissFortune' : 'Miss Fortune',
            'JarvanIV' : 'Jarvan IV',
            'Belveth' : 'Bel\'Veth',
            'KSante' : 'K\'Sante'
        }

soloq_region_dict = {
    'NA': 'NA1',
    'LCS': 'NA1',
    'NA1': 'NA1',
    'EU': 'EUW1',
    'EUW': 'EUW1',
    'LEC': 'EUW1',
    'EUM': 'EUW1',
    'EUW1': 'EUW1',
    'EUN': 'EUN1',
    'EUNE': 'EUN1',
    'EUN1': 'EUN1',
    'LATAM': 'LA1',
    'LA': 'LA1',
    'LA1': 'LA1',
    'LA2': 'LA2',
    'TR': 'TR1',
    'TR1': 'TR1',
    'OCE': 'OC1',
    'AUS': 'OC1',
    'NZ': 'OC1',
    'OC': 'OC1',
    'OC1': 'OC1',
    'KR': 'KR',
    'LCK': 'KR',
    'RU': 'RU'
}
















