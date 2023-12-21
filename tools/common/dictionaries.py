## HOW TO ADD A TEAM
'''
Update:

- team_dict
- url_team_dict
    - Check fandom for any unique characters
- leaguepedia_player_dict
- leaguepedia_team_name_dct
- leaguepedia_team_name_dct_reversed
- team_region_dict

Create spreadsheet for team

Update set_sheets to include spreadsheet

Add SoloQ IDs for players here:
https://docs.google.com/forms/d/e/1FAIpQLSce17nXhEXUR7ZZKNJ-4LI1LD8c9ReFFuBoBphx_vPSbzsRLg/viewform

Run automate_spreadsheet(team)

'''


sheet_dct = {
    'DUMMY' : 'https://docs.google.com/spreadsheets/d/1dzrKdY6in6lBgvW7xx6A0dqLalTWa94wje3q4GpQ4yw/edit?usp=sharing',
    'REGIONAL_13.1' : 'https://docs.google.com/spreadsheets/d/1omLVb1x6IYk_FlMWzO0kyFgTnDQPM1rpnA5ZSgPaYpA/edit?usp=sharing',
    'REGIONAL_13.3' : 'https://docs.google.com/spreadsheets/d/17KssLGzBQTpWseWYj6PGXScQwS4nOT8rlA-YX5owUPI/edit?usp=sharing',
    'REGIONAL_13.4' : 'https://docs.google.com/spreadsheets/d/1F6fEhmQi49g1LghKhxbTPatWSmPj9vAnQH4UNtImy-o/edit?usp=sharing',
    'REGIONAL_13.5' : 'https://docs.google.com/spreadsheets/d/1GuyqpOH2byBoBnC-y4Qkbl-BBPHKuE_VZ3bajtDEJ4o/edit?usp=sharing',
    'REGIONAL_MSI': 'https://docs.google.com/spreadsheets/d/1OtyVGCd6ACVc9oCgd4h2yX21Fzu8-aukTR9m7SHe8Lg/edit?usp=sharing',
    'REGIONAL_13.10': 'https://docs.google.com/spreadsheets/d/1K4fviQltzAFwHD7oB4LnKhVW3K0MhHstyNOo73TlrtE/edit?usp=sharing',
    'REGIONAL_13.11': 'https://docs.google.com/spreadsheets/d/19Vq3B77eXNhphvBWbm0kakCxdXsOxiTFgtdUz238h_w/edit?usp=sharing',
    'REGIONAL_13.12': 'https://docs.google.com/spreadsheets/d/1qJn0Ub9ScmhwKVcBqCBLqRyoabt6GytmXxI3cCQGeZ8/edit?usp=sharing',
    'REGIONAL_13.13': 'https://docs.google.com/spreadsheets/d/1a58Xtzwrcz30OZe8sXtB-dywZ8fXBhqXreiF5vcBP-w/edit?usp=sharing',
    'REGIONAL_13.14': 'https://docs.google.com/spreadsheets/d/1UBI8dnQNhPfecYEE03D_L27VtLmu71pAH8KgraNUsbc/edit?usp=sharing',
    'REGIONAL_DUMMY': 'https://docs.google.com/spreadsheets/d/1x5PG1sH0oomlRCSXLiUBymB7A2lQmTxTVdaNLeMIG3Q/edit?usp=sharing',

    # LCS
    '100': 'https://docs.google.com/spreadsheets/d/1a181TJD1I8-admoVz2s-uF4QYsHVVq5u6STF1duH_lA/edit?usp=sharing',
    'C9': 'https://docs.google.com/spreadsheets/d/1cewv2M9GPgWjKvnKlH0c3Cb4No5P4XZFrIk_Y1mCqKQ/edit?usp=sharing',
    'DIG': 'https://docs.google.com/spreadsheets/d/1GBRTlCJaBD5D852ks_9Vr2g_GFKLFb4EVepreDnwS0A/edit?usp=sharing',
    'EG': 'https://docs.google.com/spreadsheets/d/1OF4uSNH7KhEf0Z3e73iVQAjmOyJ_YxNKSZvOf2vtrs0/edit?usp=sharing',
    'FLY': 'https://docs.google.com/spreadsheets/d/1Ms5hI9K9YmYGFBHWSVxTnmlYF2UQ1Zmm0W5f0jxhf0c/edit?usp=sharing',
    'GG': 'https://docs.google.com/spreadsheets/d/11Jt1bSUPqXWiCvG9oKMnrRBq7rl2lHkrQTxDAbivKOo/edit?usp=sharing',
    'IMT': 'https://docs.google.com/spreadsheets/d/193oEGwybl8gpobfnLVnJUtr5iSvNbw50mPWip1tddU0/edit?usp=sharing',
    'NRG': 'https://docs.google.com/spreadsheets/d/1f5NnzZCiETb8A_RpJrLZXlmuUFJn5q-SEf6RQpB_UWM/edit?usp=sharing',
    'TL': 'https://docs.google.com/spreadsheets/d/1SZN3eFV_uA2jKJjskFEnJGu82mwo0dnN2XuOI6NfxOg/edit?usp=sharing',
    'TSM': 'https://docs.google.com/spreadsheets/d/1lTTOawFsc5Vsvon8n28NvmqueiQ5N1PEyuQokNtlcqY/edit?usp=sharing',
    # ACADEMY
    'TLC' : 'https://docs.google.com/spreadsheets/d/1q6aHXaePk5TNZe6jK-Slwsw-gdqCwCbau1ojFi2XVC4/edit?usp=sharing',
    'EGC': 'https://docs.google.com/spreadsheets/d/1roIXArzUUSEs2fg6gxHhr3ir0qnrfIZK0ARZvlppb9k/edit?usp=sharing',
    'FLYC': 'https://docs.google.com/spreadsheets/d/1VXWgdRVJ1OcDmMJfaOOFVGC0TCT2ZMvEIkeX8LDFjdA/edit?usp=sharing',
    'CF': 'https://docs.google.com/spreadsheets/d/1_R4zeP7PitN0LHKMRrFPi23c0EvhW6_aOqGofimcy4M/edit?usp=sharing',
    'WC': 'https://docs.google.com/spreadsheets/d/1Xuo-5G9Ndlo20WIHz9OdiDdNBJ7mfIYS0UAb2jXtr14/edit?usp=sharing',
    'AOE': 'https://docs.google.com/spreadsheets/d/1dB9iDlIfokf8QHSbrs_16M_BXW4we_RtDe9RD_R7HKA/edit?usp=sharing',
    'MU': 'https://docs.google.com/spreadsheets/d/1cgaX2burvnzx5PEXa7Rf6Jb1sR0cVE8w63kaXA14f5I/edit?usp=sharing',
    'DSG': 'https://docs.google.com/spreadsheets/d/1fUd_KbaPrhtnHdQ4xJwWZVRKE9r1xdePWsu0RwCYATI/edit?usp=sharing',
    'TFT': 'https://docs.google.com/spreadsheets/d/1uxvvT7HKoj65Qf3rCzlHeklpJB8snaADxzZmK_ntqF8/edit?usp=sharing',
    'SN': 'https://docs.google.com/spreadsheets/d/1wb2wYrtI760Z8iVnq8GpUppbcu2AuI29R6eqGj7RjN8/edit?usp=sharing',
}

team_dict = {
    # LCS
    '100' : {
        'top': 'Ssumday',
        'jungle': 'Closer',
        'mid': 'Quid',
        'bot': 'Doublelift',
        'support': 'Busio'
    },
    'C9' : {
        'top': 'Fudge',
        'jungle': 'Blaber',
        'mid' : 'EMENES',
        'bot': 'Berserker',
        'support': 'Zven'
    },
    'DIG' : {
        'top': 'Rich',
        'jungle': 'Santorin',
        'mid': 'Jensen',
        'bot': 'Tomo',
        'support': 'Diamond',
    },
    'EG' : {
        'top': 'Revenge',
        # 'jungle': 'Sheiden',
        'jungle': 'Armao',
        'mid': 'Jojopyun',
        'bot': 'UNF0RGIVEN',
        'support': 'Eyla'
    },
    'FLY' : {
        'top': 'Impact',
        'jungle': 'Spica',
        # 'mid': 'Spirax',
        'mid': 'VicLa',
        'bot': 'Prince',
        'support': 'Vulcan'
    },
    'GG' : {
        'top': 'Licorice',
        'jungle': 'River',
        'mid': 'Gori',
        'bot': 'Stixxay',
        'support': 'huhi'
    },
    'IMT' : {
        'top': 'Solo',
        'jungle': 'Kenvi',
        'mid': 'Bolulu',
        'bot': 'Tactical',
        'support': 'Treatz'
    },
    'NRG' : {
        'top': 'Dhokla',
        'jungle': 'Contractz',
        'mid': 'Palafox',
        'bot': 'FBI',
        'support': 'IgNar'
    },
    'TL' : {
        'top': 'Summit',
        'jungle': 'Pyosik',
        'mid': 'APA',
        'bot': 'Yeon',
        'support': 'CoreJJ'
    },
    'TSM' : {
        'top': 'Hauntzer',
        'jungle': 'Bugi',
        'mid': 'Insanity',
        # 'mid': 'Ruby',
        'bot' : 'WildTurtle',
        'support': 'Chime'
    },

    # ACADEMY
    'EGC' : {
        'top' : 'S0ul',
        'jungle' : 'Sheiden',
        'mid' : 'ry0ma',
        'bot' : 'k1ng',
        'support' : 'Smoothie',
    },
    'FLYC' : {
        'top' : 'Faisal',
        'jungle' : 'Yuuji',
        'mid' : 'Spirax',
        'bot' : 'Massu',
        'support' : 'Winsome',
    },
    'TLC' : {
        'top' : 'Bradley',
        'jungle' : 'Mir',
        'mid' : 'APA',
        'bot' : 'Arrow',
        'support' : 'Kim Down',
    },
    'CF': {
        'top' : 'Philip',
        'jungle' : 'Perry',
        'mid' : 'Shochi',
        'bot' : 'Minui',
        'support' : 'JayJ',
    },
    'WC': {
        'top' : 'Zamudo',
        'jungle' : 'Keel',
        'mid' : 'Soligo',
        'bot' : 'Lens',
        'support' : 'Duoking1',
    },
    'AOE' : {
        'top' : 'Concept',
        'jungle' : 'Will',
        'mid' : 'DARKWINGS',
        'bot' : 'links',
        'support' : 'Breezy',
    },
    'MU' : {
        'top' : 'Niles',
        'jungle' : 'OddOrange',
        'mid' : 'Getback',
        'bot' : 'ScaryJerry',
        'support' : 'Zyko',
    },
    'SN' : {
        'top' : 'Qwacker',
        'jungle' : 'Music',
        'mid' : 'RobbyBob',
        'bot' : 'Sketch',
        'support' : 'Trevor',
    },
    'TFT' : {
        'top' : 'Lunacia',
        'jungle' : 'RoseThorn',
        'mid' : 'Onat',
        'bot' : 'Spawn',
        'support' : 'Nxi',
    },
    'DSG' : {
        'top' : 'FakeGod',
        'jungle' : 'Tomio',
        'mid' : 'Young',
        'bot' : 'Meech',
        'support' : 'Zeyzal',
    },

    
}

url_team_dict = {
    # LCS
    '100' : {
        'top': 'Ssumday',
        'jungle': 'Closer%20%28Can%20%C3%87elik%29%0A',
        'mid': 'Quid',
        'bot': 'Doublelift',
        'support': 'Busio'
    },
    'C9' : {
        'top': 'Fudge',
        'jungle': 'Blaber',
        'mid' : 'EMENES',
        'bot': 'Berserker%20%28Kim%20Min-cheol%29%0A',
        'support': 'Zven'
    },
    'DIG' : {
        'top': 'Rich%20%28Lee%20Jae-won%29',
        'jungle': 'Santorin',
        'mid': 'Jensen',
        'bot': 'Tomo',
        'support': 'Diamond%20%28David%20B%C3%A9rub%C3%A9%29',
    },
    'EG' : {
        'top': 'Revenge%20%28Mohamed%20Kaddoura%29%0A',
        # 'jungle': 'Sheiden',
        'jungle': 'Armao',
        'mid': 'Jojopyun',
        'bot': 'UNF0RGIVEN',
        'support': 'Eyla'
    }, 
    'FLY' : {
        'top': 'Impact',
        'jungle': 'Spica',
        # 'mid': 'Spirax',
        'mid': 'VicLa',
        'bot': 'Prince%20%28Lee%20Chae-hwan%29%0A',
        'support': 'Vulcan%20%28Philippe%20Laflamme%29'
    },
    'GG' : {
        'top': 'Licorice',
        'jungle': 'River%20%28Kim%20Dong-woo%29%0A',
        'mid': 'Gori',
        'bot': 'Stixxay',
        'support': 'Huhi'
    },
    'IMT' : {
        'top': 'Solo%20%28Colin%20Earnest%29',
        'jungle': 'Kenvi',
        'mid': 'Bolulu',
        'bot': 'Tactical',
        'support': 'Treatz'
    },
    'NRG' : {
        'top': 'Dhokla',
        'jungle': 'Contractz',
        'mid': 'Palafox',
        'bot': 'FBI',
        'support': 'IgNar'
    },
    'TL' : {
        'top': 'Summit',
        'jungle': 'Pyosik',
        'mid': 'APA%20%28Eain%20Stearns%29',
        'bot': 'Yeon%20%28Sean%20Sung%29%0A',
        'support': 'CoreJJ'
    },
    'TSM' : {
        'top': 'Hauntzer',
        'jungle': 'Bugi',
        'mid': 'Insanity',
        # 'mid': 'Ruby%20%28Lee%20Sol-min%29',
        'bot' : 'WildTurtle',
        'support': 'Chime'
    },
    
    # ACADEMY
    'EGC' : {
        'top' : 'S0ul',
        'jungle' : 'Sheiden',
        'mid' : 'ry0ma',
        'bot' : 'k1ng',
        'support' : 'Smoothie',
    },
    'FLYC' : {
        'top' : 'Faisal',
        'jungle' : 'Yuuji',
        'mid' : 'Spirax',
        'bot' : 'Massu',
        'support' : 'Winsome',
    },
    'TLC' : {
        'top' : 'Bradley',
        'jungle' : 'Mir%20%28Park%20Mi-reu%29',
        'mid' : 'APA%20%28Eain%20Stearns%29',
        'bot' : 'Arrow',
        'support' : 'Kim Down',
    },
    'CF': {
        'top' : 'Philip%20%28Philip%20Zeng%29',
        'jungle' : 'Perry%20%28Perry%20Norman%29',
        'mid' : 'Shochi',
        'bot' : 'Minui',
        'support' : 'JayJ',
    },
    'WC': {
        'top' : 'Zamudo',
        'jungle' : 'Keel',
        'mid' : 'Soligo',
        'bot' : 'Lens',
        'support' : 'Duoking1',
    },
    'AOE' : {
        'top' : 'Concept',
        'jungle' : 'Will%20%28William%20Cummins%29',
        'mid' : 'DARKWINGS',
        'bot' : 'links',
        'support' : 'Breezy',
    },
    'MU' : {
        'top' : 'Niles%20%28Aiden%20Tidwell%29',
        'jungle' : 'OddOrange',
        'mid' : 'Getback',
        'bot' : 'ScaryJerry',
        'support' : 'Zyko',
    },
    'SN' : {
        'top' : 'Qwacker',
        'jungle' : 'Music%20%28Sean%20Wishko%29',
        'mid' : 'RobbyBob',
        'bot' : 'Sketch%20%28Brady%20Holmich%29',
        'support' : 'Trevor',
    },
    'TFT' : {
        'top' : 'Lunacia',
        'jungle' : 'RoseThorn',
        'mid' : 'Onat',
        'bot' : 'Spawn%20%28Trevor%20Kerr-Taylor%29',
        'support' : 'Nxi',
    },
    'DSG' : {
        'top' : 'FakeGod',
        'jungle' : 'Tomio',
        'mid' : 'Young%20%28Young%20Choi%29',
        'bot' : 'Meech',
        'support' : 'Zeyzal',
    },

   # WORLDS

}

leaguepedia_player_dict = {
    #LCS

    'Ssumday': 'Ssumday',
    'Closer': 'Closer%20%28Can%20%C3%87elik%29%0A',
    'Quid': 'Quid',
    'Nukeduck': 'Nukeduck',
    'Doublelift': 'Doublelift',
    'Busio': 'Busio',

    'Fudge': 'Fudge',
    'Blaber': 'Blaber',
    'Diplex': 'Diplex',
    'Berserker': 'Berserker%20%28Kim%20Min-cheol%29%0A',
    'Zven': 'Zven',

    'Dhokla': 'Dhokla',
    'Contractz': 'Contractz',
    'Palafox': 'Palafox',
    'FBI': 'FBI',
    'Poome': 'Poome',

    'Rich': 'Rich%20%28Lee%20Jae-won%29',
    'Santorin': 'Santorin',
    'Jensen': 'Jensen',
    'IgNar': 'IgNar',
    'Biofrost': 'Biofrost',
    'Diamond': 'Diamond%20%28David%20B%C3%A9rub%C3%A9%29',

    'Revenge': 'Revenge%20%28Mohamed%20Kaddoura%29%0A',
    'Sheiden': 'Sheiden',
    'Jojopyun': 'Jojopyun',
    'UNF0RGIVEN': 'UNF0RGIVEN',
    'Eyla': 'Eyla',

    'Impact': 'Impact',
    'Spica': 'Spica',
    'Spirax': 'Spirax',
    'VicLa': 'VicLa',
    'Prince': 'Prince%20%28Lee%20Chae-hwan%29%0A',
    'Vulcan': 'Vulcan%20%28Philippe%20Laflamme%29',

    'Licorice': 'Licorice',
    'River': 'River%20%28Kim%20Dong-woo%29%0A',
    'Gori': 'Gori',
    'Sitxxay': 'Stixxay',
    'Huhi': 'Huhi',

    'Solo': 'Solo%20%28Colin%20Earnest%29',
    'Kenvi': 'Kenvi',
    'Bolulu': 'Bolulu',
    'Tactical': 'Tactical',
    'Treatz': 'Treatz',

    'Summit': 'Summit',
    'Pyosik': 'Pyosik',
    'APA': 'APA%20%28Eain%20Stearns%29',
    'Yeon': 'Yeon%20%28Sean%20Sung%29%0A',
    'CoreJJ': 'CoreJJ',

    'Hauntzer': 'Hauntzer',
    'Bugi': 'Bugi',
    'Insanity': 'Insanity',
    'Ruby': 'Ruby%20%28Lee%20Sol-min%29',
    'WildTurtle': 'WildTurtle',
    'Chime': 'Chime',

    # ACADEMY

    'S0ul' : 'S0ul',
    'Sheiden' : 'Sheiden',
    'ry0ma' : 'ry0ma',
    'k1ng' : 'k1ng',
    'Smoothie' : 'Smoothie',

    'Faisal' : 'Faisal',
    'Yuuji' : 'Yuuji',
    'Massu' : 'Massu',
    'Winsome' : 'Winsome',

    'Bradley' : 'Bradley',
    'Mir' : 'Mir%20%28Park%20Mi-reu%29',
    'APA' : 'APA%20%28Eain%20Stearns%29',
    'Arrow' : 'Arrow',
    'Kim Down' : 'Kim Down',

    'Philip' : 'Philip%20%28Philip%20Zeng%29',
    'Perry' : 'Perry%20%28Perry%20Norman%29',
    'Shochi' : 'Shochi',
    'Minui' : 'Minui',
    'JayJ' : 'JayJ',

    'Zamudo' : 'Zamudo',
    'Keel' : 'Keel',
    'Soligo' : 'Soligo',
    'Lens' : 'Lens',
    'Duoking1' : 'Duoking1',

    'Concept' : 'Concept',
    'Will' : 'Will%20%28William%20Cummins%29',
    'DARKWINGS' : 'DARKWINGS',
    'links' : 'links',
    'Breezy' : 'Breezy',

    'Niles' : 'Niles%20%28Aiden%20Tidwell%29',
    'OddOrange' : 'OddOrange',
    'Getback' : 'Getback',
    'ScaryJerry' : 'ScaryJerry',
    'Zyko' : 'Zyko',

    'Qwacker' : 'Qwacker',
    'Music' : 'Music%20%28Sean%20Wishko%29',
    'RobbyBob' : 'RobbyBob',
    'Sketch' : 'Sketch%20%28Brady%20Holmich%29',
    'Trevor' : 'Trevor',

    'Lunacia' : 'Lunacia',
    'RoseThorn' : 'RoseThorn',
    'Onat' : 'Onat',
    'Spawn' : 'Spawn%20%28Trevor%20Kerr-Taylor%29',
    'Nxi' : 'Nxi',

    'FakeGod' : 'FakeGod',
    'Tomio' : 'Tomio',
    'Young' : 'Young%20%28Young%20Choi%29',
    'Meech' : 'Meech',
    'Zeyzal' : 'Zeyzal',


}

leaguepedia_team_name_dct = {
            # LCS
            'EG' : 'Evil Geniuses.NA',
            'TL' : 'Team Liquid',
            'CLG' : 'Counter Logic Gaming',
            '100' : '100 Thieves',
            'TSM' : 'TSM',
            'GG' : 'Golden Guardians',
            'IMT' : 'Immortals',
            'NRG': 'NRG',
            'FLY' : 'FlyQuest',
            'DIG' : 'Dignitas',
            'C9' : 'Cloud9',
            # ACADEMY
            'EGC' : 'Evil Geniuses Challengers',
            'TLC' : 'Team Liquid Challengers',
            'FLYC' : 'FlyQuest Challengers',
            'CF': 'Cincinnati Fear',
            'WC': 'Wildcard Gaming',
            'AOE': 'AOE Gold',
            'MU': 'Maryville University',
            'DSG': 'Disguised',
            'TFT': 'Team Fish Taco',
            'SN': 'Supernova',

            # LEC
            'G2': 'G2 Esports',
            'FNC': 'Fnatic',
            'MAD': 'MAD Lions',
            'RGE': 'Rogue (European Team)',
            'MSF': 'Misfits Gaming',
            'VIT': 'Team Vitality',
            'AST': 'Astralis',
            'XL': 'Excel Esports',
            'SK': 'SK Gaming',
            'BDS': 'Team BDS',

            # LCK
            'T1':'T1',
            'DK':'Dplus KIA',
            'GEN':'Gen.G',
            'HLE':'Hanwha Life Esports',
            'KT':'KT Rolster',
            'LSB':'Liiv Sandbox',
            'BRO':'BRION',
            'KDF':'Kwangdong Freecs',
            'DRX':'DRX',
            'NS':'Nongshim Redforce',
            
            # LCO
            'ORD': 'ORDER',
            'CHF': 'Chiefs Esports Club',
            'PGG': 'Pentanet.GG',
            'PCE': 'PEACE (Oceanic Team)',
            'MMM': 'MAMMOTH',
            'DW': 'Dire Wolves',
            'KNG': 'Kanga Esports',
            'GRV': 'Gravitas',
            # WORLDS
            'BYG': 'Beyond Gaming',
            'DFM': 'DetonatioN FocusMe',
            'LLL': 'LOUD',
            'SGB': 'Saigon Buffalo',
            'DK': 'DWG KIA',
            'JDG': 'JD Gaming'
            
        }

leaguepedia_team_name_dct_reversed = {
            # LCS
            'Evil Geniuses.NA': 'EG',
            'Team Liquid': 'TL',
            'Counter Logic Gaming': 'CLG',
            '100 Thieves': '100',
            'TSM': 'TSM',
            'Golden Guardians': 'GG',
            'Immortals': 'IMT',
            'NRG': 'NRG',
            'FlyQuest': 'FLY',
            'Dignitas': 'DIG',
            'Cloud9': 'C9',
            # ACADEMY
            'Evil Geniuses Challengers': 'EGC',
            'Team Liquid Challengers': 'TLC',
            'FlyQuest Challengers': 'FLYC',
            'Cincinnati Fear': 'CF',
            'Wildcard Gaming': 'WC',
            'AOE Gold': 'AOE',
            'Maryville University': 'MU',
            'Disguised': 'DSG',
            'Team Fish Taco': 'TFT',
            'Supernova': 'SN',
            # AMATEUR
            'Evil Geniuses Prodigies': 'EGP',
            'Ginger Turmeric': 'GT',
            'Maryville' : 'MU Saints',
            'Taco Gaming': 'TG',
            # LEC
            'G2 Esports': 'G2',
            'Fnatic': 'FNC',
            'MAD Lions': 'MAD',
            'Rogue (European Team)': 'RGE',
            'Misfits Gaming': 'MSF',
            'Team Vitality': 'VIT',
            'Astralis': 'AST',
            'Excel Esports': 'XL',
            'SK Gaming': 'SK',
            'Team BDS': 'BDS',
            # LCK
            'T1':'T1',
            'Dplus KIA':'DK',
            'Gen.G':'GEN',
            'Hanwha Life Esports':'HLE',
            'KT Rolster':'KT',
            'Liiv Sandbox':'LSB',
            'BRION':'BRO',
            'Kwangdong Freecs':'KDF',
            'DRX':'DRX',
            'Nongshim Redforce':'NS',
            # LCO
            'ORDER': 'ORD',
            'Chiefs Esports Club': 'CHF',
            'Pentanet.GG': 'PGG',
            'PEACE (Oceanic Team)': 'PCE',
            'MAMMOTH': 'MMM',
            'Dire Wolves': 'DW',
            'Kanga Esports': 'KNG',
            'Gravitas': 'GRV',


        }

team_region_dict = {
            # LCS
            'EG' : 'LCS',
            'TL' : 'LCS',
            'CLG' : 'LCS',
            '100' : 'LCS',
            'TSM' : 'LCS',
            'GG' : 'LCS',
            'IMT' : 'LCS',
            'NRG': 'LCS',
            'FLY' : 'LCS',
            'DIG' : 'LCS',
            'C9' : 'LCS',
            # ACADEMY
            'EGC' : 'NACL',
            'TLC' : 'NACL',
            'CLGC' : 'NACL',
            '100C' : 'NACL',
            'TSMC' : 'NACL',
            'GGC' : 'NACL',
            'IMTC' : 'NACL',
            'FLYC' : 'NACL',
            'DIGC' : 'NACL',
            'C9C' : 'NACL',
            'TLF': 'NACL',
            'CLGF': 'NACL',
            'FLYF': 'NACL',
            'CF': 'NACL',
            'WC': 'NACL',
            'AOE': 'NACL',
            'MU': 'NACL',
            'DSG': 'NACL',
            'SN': 'NACL',
            'TFT': 'NACL',
            # LEC
            'G2': 'LEC',
            'FNC': 'LEC',
            'MAD': 'LEC',
            'RGE': 'LEC',
            'MSF': 'LEC',
            'VIT': 'LEC',
            'AST': 'LEC',
            'XL': 'LEC',
            'SK': 'LEC',
            'BDS': 'LEC',
            # LCO
            'ORD': 'LCO',
            'CHF': 'LCO',
            'PGG': 'LCO',
            'PCE': 'LCO',
            'MMM': 'LCO',
            'DW': 'LCO',
            'KNG': 'LCO',
            'GRV': 'LCO',
            # WORLDS
            'BYG': 'PCS',
            'DFM': 'LJL',
            'LLL': 'CBLOL',
            'SGB': 'VCS',
            'DK': 'LCK',
            'JDG': 'LPL'
}

leaguepedia_role_dct = {
        'top' : 'Top',
        'jng' : 'Jungle',
        'jg' : 'Jungle',
        'jungle' : 'Jungle',
        'mid' : 'Mid',
        'bot' : 'Bot',
        'adc' : 'Bot',
        'sup' : 'Support',
        'support' : 'Support',
    }

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

pgs_sql_role_dct = {
            'top': 'top',
            'jungle': 'jng',
            'jng': 'jng',
            'jg': 'jng',
            'mid': 'mid',
            'middle': 'mid',
            'bot': 'bot',
            'bottom': 'bot',
            'adc': 'bot',
            'support': 'sup',
            'sup': 'sup',
            'utility': 'sup'
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

summoner_spell_dct = {
    'Cleanse' : '1',
    'Exhaust' : '3',
    'Flash' : '4',
    'Ghost' : '6',
    'Heal' : '7',
    'Smite' : '11',
    'Teleport' : '12',
    'Ignite' : '14',
    'Barrier' : '21',
}

role_to_pick_dct = {
    'BR1' : 'BP1',
    'BR2' : 'BP2',
    'BR3' : 'BP3',
    'BR4' : 'BP4',
    'BR5' : 'BP5',
    'RR1' : 'RP1',
    'RR2' : 'RP2',
    'RR3' : 'RP3',
    'RR4' : 'RP4',
    'RR5' : 'RP5'
}

color_dict = {
    'BP1' : 1,

    'BP2' : 4,
    'BP3' : 5,

    'BP4' : 8,
    'BP5' : 9,

    'RP1' : 2,
    'RP2' : 3,

    'RP3' : 6,

    'RP4' : 7,

    'RP5' : 10
}

patch= {

    '12.1': {
       'start': '01-05-2022',
       'end': '01-18-2022'
    },

    '12.2': {
       'start': '01-19-2022',
       'end': '01-31-2022'
    },

    '12.3': {
       'start': '02-01-2022',
       'end': '02-14-2022'
    },

    '12.4': {
       'start': '02-15-2022',
       'end': '02-28-2022'
    },

    '12.5': {
       'start': '03-01-2022',
       'end': '03-28-2022'
    },

    '12.6': {
       'start': '03-29-2022',
       'end': '04-11-2022'
    },

    '12.7': {
       'start': '04-12-2022',
       'end': '04-25-2022'
    },

    '12.8': {
       'start': '04-26-2022',
       'end': '05-09-2022'
    },

    '12.9': {
       'start': '05-10-2022',
       'end': '05-23-2022'
    },

    '12.10': {
       'start': '05-24-2022',
       'end': '06-06-2022'
    },

    '12.11': {
       'start': '06-07-2022',
       'end': '06-21-2022'
    },

    '12.12': {
       'start': '06-22-2022',
       'end': '07-11-2022'
    },

    '12.13': {
       'start': '07-12-2022',
       'end': '07-25-2022'
    },

    '12.14': {
       'start': '07-26-2022',
       'end': '08-08-2022'
    },

    '12.15': {
       'start': '08-09-2022',
       'end': '08-22-2022'
    },

    '12.16': {
       'start': '08-23-2022',
       'end': '09-06-2022'
    },

    '12.17': {
       'start': '09-07-2022',
       'end': '09-19-2022'
    },

    '12.18': {
       'start': '09-20-2022',
       'end': '10-03-2022'
    },

    '12.19': {
       'start': '10-04-2022',
       'end': '10-17-2022'
    },

    '12.20': {
       'start': '10-18-2022',
       'end': '10-31-2022'
    },

    '12.21': {
       'start': '11-01-2022',
       'end': '11-14-2022'
    },

    '12.22': {
       'start': '11-15-2022',
       'end': '12-05-2022'
    },

    '12.23': {
       'start': '12-06-2022',
       'end': '12-19-2022'
    },

    '13.1': {
       'start': '01-11-2023',
       'end': '01-24-2023'
    },

    '13.2': {
       'start': '01-25-2023',
       'end': '02-07-2023'
    },

    '13.3': {
       'start': '02-08-2023',
       'end': '02-22-2023'
    },

    '13.4': {
       'start': '02-23-2023',
       'end': '03-07-2023'
    },

    '13.5': {
       'start': '03-08-2023',
       'end': '03-21-2023'
    },

    '13.6': {
       'start': '03-22-2023',
       'end': '04-04-2023'
    },

    '13.7': {
       'start': '04-05-2023',
       'end': '04-18-2023'
    },

    '13.8': {
       'start': '04-19-2023',
       'end': '05-02-2023'
    },

    '13.9': {
       'start': '05-03-2023',
       'end': '05-16-2023'
    },

    '13.10': {
       'start': '05-17-2023',
       'end': '05-31-2023'
    },

    '13.11': {
       'start': '06-01-2023',
       'end': '06-13-2023'
    },

    '13.12': {
       'start': '06-14-2023',
       'end': '06-27-2023'
    },

    '13.13': {
       'start': '06-28-2023',
       'end': '07-18-2023'
    },

    '13.14': {
       'start': '07-19-2023',
       'end': '08-01-2023'
    },

    '13.15': {
       'start': '08-02-2023',
       'end': '08-15-2023'
    },

    '13.16': {
       'start': '08-16-2023',
       'end': '08-29-2023'
    },

    '13.17': {
       'start': '08-30-2023',
       'end': '09-12-2023'
    },

    '13.18': {
       'start': '09-13-2023',
       'end': '09-26-2023'
    },

    '13.19': {
       'start': '09-27-2023',
       'end': '10-10-2023'
    },

    '13.20': {
       'start': '10-11-2023',
       'end': '10-24-2023'
    },

    '13.21': {
       'start': '10-25-2023',
       'end': '11-07-2023'
    },

    '13.22': {
       'start': '11-08-2023',
       'end': '11-20-2023'
    },

    '13.23': {
       'start': '11-21-2023',
       'end': '12-05-2023'
    },

    '13.24': {
       'start': '12-06-2023',
       'end': '12-31-2023'
    },



}

cq_week = {
    '2022':{
            'Spring':{
                'Split 1':{
                    'start': '02/06/2022',
                    'end': '03/08/2022'
                },
                'Split 2':{
                    'start': '03/13/2022',
                    'end': '04/12/2022'
                },
            },
            'Summer':{
                'Split 1':{
                    'start': '05/30/2022',
                    'end': '06/27/2022'
                },
                'Split 2':{
                    'start': '06/27/2022',
                    'end': '07/25/2022'
                },
                'Split 3':{
                    'start': '06/25/2022',
                    'end': '08/22/2022'
                }    
            },
            'Worlds':{
                'Split 1':{
                    'start': '09/24/2022',
                    'end': '11/06/2022'
                },  
            }
    },
    '2023':{
            'Spring':{
                'Split 1':{
                    'start': '01/12/2023',
                    'end': '03/05/2023'
                },
                'Split 2':{
                    'start': '01/12/2023',
                    'end': '03/05/2023'
                },
                'Split 3':{
                    'start': '01/17/2023',
                    'end': '03/26/2023'
                }
            },
            'Summer':{
                'Split 1':{
                    'start': '05/30/2023',
                    'end': '08/14/2023'
                }
            },
            'Worlds':{
                'Split 1':{
                    'start': '09/24/2023',
                    'end': '11/06/2023'
                },  
            }
    }
}

season = {
    
        'lcs': {
            2023: {
                'spring': {
                    'start': '01-26-2023',
                    'end': '04-09-2023'
                },
                'summer': {
                    'start': '06-13-2023',
                    'end': '08-07-2023'
                }
            }
        },
        'lec': {
            2023: {
                'winter': {
                    'start': '01-21-2023',
                    'end': '02-26-2023'
                },
                'spring': {
                    'start': '',
                    'end': ''
                },
                'summer': {
                    'start': '',
                    'end': ''
                }
            }
        },
        'lck': {
            2023: {
                'spring': {
                    'start': '01-18-2023',
                    'end': '04-09-2023'
                },
                'summer': {
                    'start': '',
                    'end': ''
                }
            }
        },
        'lpl': {
            2023: {
                'spring': {
                    'start': '01-14-2023',
                    'end': '04-09-2023'
                },
                'summer': {
                    'start': '',
                    'end': ''
                }
            }
        },
        'lcsa': {
            2023: {
                'spring': {
                    'start': '01-21-2023',
                    'end': '03-06-2023'
                },
                'summer': {
                    'start': '',
                    'end': ''
                }
            }
        },
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

active_item_ids = [
    2065, # Shurelya's Battlesong
    3050, # Zeke's Convergence
    3107, # Redemption
    3109, # Knight's Vow
    3139, # Mercurial Scimitar
    3140, # Quicksilver Sash
    3142, # Youmuu's Ghostblade
    3143, # Randuin's Omen
    3152, # Hextech Rocketbelt
    3190, # Locket of the Iron Solari
    3193, # Gargoyle's Stoneplate
    3222, # Mikael's Blessing
    6029, # Ironspike Whip
    6035, # Silvermere Dawn
    6630, # Goredrinker
    6631, # Stridebreaker
    6656, # Everfrost
    6664, # Turbo Chemtank
    6693, # Prowler's Claw
    7000, # (Ornn) Prowler's Claw
    7011, # (Ornn) Hextech Rocketbelt
    7014, # (Ornn) Everfrost
    7015, # (Ornn) Goredrinker
    7016, # (Ornn) Stridebreaker
    7019, # (Ornn) Locket of the Iron Solari
    7020, # (Ornn) Shurelya's Battlesong
    8001, # Anathema's Chains

    2419, # Commencing Stopwatch
    2420, # Stopwatch
    2421, # Broken Stopwatch
    2423, # Perfectly Timed Stopwatch
    2424, # Broken Stopwatch
    3157, # Zhonya's Hourglass

    2003, # Health Potion
    2010, # Total Biscuit of Everlasting Will
    2031, # Refillable Potion
    2033, # Corruption Potion

    3850, # Spellthief's Edge
    3851, # Frostfang
    3853, # Shard of True Ice
    3854, # Steel Shoulderguards
    3855, # Runesteel Spaulders
    3857, # Pauldrons of Whiterock
    3858, # Relic shield
    3859, # Targon's Buckler
    3860, # Bulwark of the Mountain
    3862, # Spectral Sickle
    3863, # Harrowing Crescent
    3864, # Black Mist Scythe

    2055, # Control Ward
    4643, # Vigilant Wardstone
]

stopwatch_ids = [
    2419, # Commencing Stopwatch
    2420, # Stopwatch
    2421, # Broken Stopwatch
    2423, # Perfectly Timed Stopwatch
    2424, # Broken Stopwatch
    3157, # Zhonya's Hourglass
]

potion_ids = [
    2003, # Health Potion
    2010, # Total Biscuit of Everlasting Will
    2031, # Refillable Potion
    2033, # Corruption Potion
]

ward_ids = [
    3850, # Spellthief's Edge
    3851, # Frostfang
    3853, # Shard of True Ice
    3854, # Steel Shoulderguards
    3855, # Runesteel Spaulders
    3857, # Pauldrons of Whiterock
    3858, # Relic shield
    3859, # Targon's Buckler
    3860, # Bulwark of the Mountain
    3862, # Spectral Sickle
    3863, # Harrowing Crescent
    3864, # Black Mist Scythe
]

control_ward_ids = [
    2055, # Control Ward
    4643, # Vigilant Wardstone
]

qss_ids = [
    3139, # Mercurial Scimitar
    3140, # Quicksilver Sash
    6035, # Silvermere Dawn
]

completed_items_list = [2065,
3001,
3003,
3004,
3011,
3026,
3031,
3033,
3035,
3036,
3040,
3042,
3046,
3050,
3053,
3065,
3068,
3071,
3072,
3074,
3075,
3078,
3083,
3084,
3085,
3089,
3091,
3094,
3095,
3100,
3102,
3109,
3110,
3115,
3116,
3119,
3121,
3124,
3135,
3139,
3143,
3152,
3153,
3156,
3157,
3161,
3165,
3179,
3181,
3190,
3193,
3222,
3504,
3508,
3742,
3748,
3814,
4005,
4401,
4628,
4629,
4633,
4636,
4637,
4644,
4645,
6035,
6333,
6616,
6617,
6630,
6631,
6632,
6653,
6655,
6657,
6662,
6665,
6667,
6671,
6672,
6673,
6675,
6676,
6691,
6692,
6694,
6695,
6696,
7001,
7002,
7005,
7006,
7007,
7008,
7009,
7010,
7011,
7012,
7013,
7015,
7016,
7017,
7018,
7019,
7020,
7021,
7022,
7023,
7024,
7025,
7026,
7027,
7028,
8001,
8020,]

gank_zones = [
        'Top Lane Brush Middle', 'Top Lane Brush Left', 'Top Lane Brush Right', 'Top Lane (Center) 1', 'Top Lane (Center) 2', 'Top Lane (Center) 3', 'Top Lane Alcove', 
        'Red Side Top Lane Outer Tower', 'Blue Side Top Lane Outer Tower', 'Red Side Top Lane Outside Outer Tower', 'Blue Side Top Lane Outside Outer Tower', 'Blue Side Top Lane Area', 'Red Side Top Lane Area', 
        'Mid Lane (Center)', 'Blue Side Mid Outside Outer Tower', 'Red Side Mid Outside Outer Tower', 'Red Side Mid Outer Tower', 'Blue Side Mid Outer Tower', 'Blue Side Mid Cross', 'Red Side Mid Cross',
        'Bot Lane Brush Middle', 'Bot Lane Brush Left', 'Bot Lane Brush Right', 'Bot Lane (Center) 1', 'Bot Lane (Center) 2', 'Bot Lane (Center) 3', 'Bot Lane Alcove', 
        'Red Side Bot Lane Outer Tower', 'Blue Side Bot Lane Outer Tower', 'Red Side Bot Lane Outside Outer Tower', 'Blue Side Bot Lane Outside Outer Tower', 'Blue Side Bot Lane Area', 'Red Side Bot Lane Area',
        ]
















