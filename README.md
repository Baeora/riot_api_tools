
# Riot API Tools

## Greeting
Hello! Thank you for being interested, if you are new to coding - a lot of this will seem a bit overwhelming but remember you can always reach out to me via Discord @Beora.

If you'd like more indepth instruction and tools, I'll be building upon this repo and hosting educational live streams over on my [Patreon](https://www.patreon.com/beora)

  
## Table of Contents
- [Overview](#overview)
- [Usage](#usage)
- [Installation](#installation)
- [Riot API Endpoints]()
- [Version Notes](#version-notes)
- [License](#license)



## Overview
These tools were made with beginners in mind to help open access to the Riot API while also featuring some scraping techniques for non-API related data.

This project aims to make it easier for all people to work with data for

- SoloQ
- Champion's Queue
- Stage Games

## Usage
The code that I have written here requires a Riot Production Key in order to really function properly - because of this, you won't be able to get updated data using the tools in this repo (because you'd **very** quickly run into API limits).

**BUT**

I've included 3 .parquet files with Ladder, SoloQ and Stage data as of `December 21, 2023`

You can upsert these to your PostgreSQL database for now using the `update_table_` functions in `SQL.update_table`, just make sure to set `from_parquet` to `True`

Once you've got the data in your PostgreSQL database, the world is your oyster! I included some miscellaneous functions that can do different things, poke around and see what you can find / build upon!

If you're interested in more, I'll be releasing updates to this on my Patreon and I'll try to upload daily parquet updates for people who aren't able to grab a prod key (for now, until I can find a webapp solution to automate the process)

## Installation

### Preparation
Before installing, complete the following tasks:

- (For beginners) Make sure [Python](https://www.python.org/downloads/) and [PIP](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/) are added to [PATH](https://realpython.com/add-python-to-path/).

	- During your Python install, you can specify that you'd like to do this by choosing Custom Installation, highly recommend!

	- You'll also need an IDE to code in, I use [VSCode](https://code.visualstudio.com/download).

- Get your [Riot API Dev Key](https://developer.riotgames.com/)!

- Install [PostgreSQL](https://www.postgresql.org/download/) and establish a [Database](https://www.youtube.com/results?search_query=how+to+set+up+a+postgres+database).

	- You'll also need something like [PgAdmin](https://www.pgadmin.org/download/) in order to interact with said database.

- Obtain Google [Oauth2](https://console.cloud.google.com/projectselector2/apis/credentials?supportedpurview=project) credentials (JSON format).

	- Might need to google how to do this if you're new to it.

  
### Install
Once you have finished the above tasks, navigate to the directory you'd like to work in and do the following:

- Clone this repository

	```git clone https://github.com/Baeora/riot_api_tools.git```

- Inside said repository, use PipEnv to install dependencies

	```pipenv sync```

- Create a 'JSON' folder in the main `riot_api_tools` directory, put your Oauth2 JSON file here.

- Navigate to `tools` and create a `.env` file with the following information:

		api_key=<YOUR RIOT API KEY>

		database_username=<YOUR DB USERNAME>
		database_password=<YOUR DB PASSWORD>
		database_url=<YOUR DB URL>
		database_port=<YOUR DB PORT>
		database_name=<YOUR DB NAME>

- Inside `tools`, navigate to `common/core.py` and replace the following line:
`service_file  =  os.path.join(os.path.dirname(Path.cwd()), 'JSONs\\<Your Oauth2 filename>.json')`
  
That **should** be everything. If you run into errors or spot anything that I missed, please reach out!

## Riot API Endpoints
If you are curious what other Riot API endpoints are out there for you to play around with, you can find them [here](https://developer.riotgames.com/apis)!

The ones I use in this project are
- [Account V1](https://developer.riotgames.com/apis#account-v1)
- [Summoner V4](https://developer.riotgames.com/apis#summoner-v4)
- [League V4](https://developer.riotgames.com/apis#league-v4)
- [Match V5](https://developer.riotgames.com/apis#match-v5)

Once the `League V4` endpoint updates to `V5` I will likely sunset `Summoner V4` as it will no longer be needed

Take a look around, bring one of the api functions in `LoLAPI.soloq` into a python notebook and replace some of the code with a new endpoint and see what happens!

## Version Notes
For version notes, please see `/tools/version_notes.txt`! That is where I'll be putting all of my updates

Not exactly industry standard but that's how I like to do it. Enjoy!

## License
MIT License

Copyright (c) 2023 Beora

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.