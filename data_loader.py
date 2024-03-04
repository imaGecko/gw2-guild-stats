import datetime
import os
import json
import requests

# get ids like so
# https://api.guildwars2.com/v2/guild/search?name=Cruel%20Unending%20Tyrannic%20Entity
# https://api.guildwars2.com/v2/guild/search?name=Chaotic%20Untamed%20Tranquil%20Evil
base_url = "https://api.guildwars2.com/v2/guild/"

guild_ids = {
    "cruel": "8321DC5B-627B-EB11-81AC-95DFE50946EB",
    "chaotic" : "B50E754B-E625-ED11-84B0-06B485C7CFFE"
}

data_to_load = {
    "members": "/members",
    "logs": "/log",
    "stash": "/stash",
    "storage": "/storage",
    "treasury": "/treasury",
}

today = datetime.datetime.now().strftime("%Y_%m_%d")
data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"data/{today}")

def get_file_path(guild:str, data_type:str) -> str:
    file_name = f"{today}_{data_type}_{guild}.json"
    return os.path.join(data_folder, file_name)

def fetch_all_data() -> None:
    if not os.path.isdir(data_folder):
        os.makedirs(data_folder)
    for guild in guild_ids.keys():
        print(f"Loading data for {guild}")
        for data_type in data_to_load.keys():
            print(f"Checking {data_type}")
            path = get_file_path(guild, data_type)

            if os.path.isfile(path):
                print("Data already present")
                continue

            print("Fetching Data")
            r = requests.get(f"{base_url}{guild_ids[guild]}{data_to_load[data_type]}", 
                             headers = {'Authorization': f'Bearer {get_key()}'})
            with open(path, "w+") as outfile:
                json.dump(r.json(), outfile)
            print("Data Saved")

def load(data_type:str) -> dict[str, list]:    
    data = dict()
    for guild in guild_ids.keys():
        print(f"Loading file for {guild}")
        path = get_file_path(guild, data_type)        
        #if file for current day has already been created load it
        if not os.path.isfile(path):
            print("Missing Data")
            fetch_all_data()

        with open(path, "r") as infile:
            data[guild] = json.load(infile)
    return data

#api key in the same folder as current working directory as a one liner in a file "token.txt"
def get_key() -> str:
    with open("token.txt", "r") as infile:
        return infile.readline()

#show key holder and permissions for sanity checking
def check_token() -> None:
    uri = "https://api.guildwars2.com/v2/tokeninfo"
    r = requests.get(uri, headers = {'Authorization': f'Bearer {get_key()}'})
    print(r.json())

def main() -> None:
    check_token()
    fetch_all_data()

if __name__ == "__main__":
    main()