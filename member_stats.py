import datetime
import os
import json
import requests

# get ids like so
# https://api.guildwars2.com/v2/guild/search?name=Cruel%20Unending%20Tyrannic%20Entity
# https://api.guildwars2.com/v2/guild/search?name=Chaotic%20Untamed%20Tranquil%20Evil
guild_ids = {
    "cruel": "8321DC5B-627B-EB11-81AC-95DFE50946EB",
    "chaotic" : "B50E754B-E625-ED11-84B0-06B485C7CFFE"
}

def load_member_json() -> dict[str, list]:
    #only pull data once for each day
    #will be saved in the member_data folder as yyyy_mm_dd_guildname.json
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    data = dict()

    for guild in guild_ids.keys():
        #build path to data folder
        folder = os.path.dirname(os.path.realpath(__file__))
        rel_path = f"member_data/{today}_{guild}.json"
        path = os.path.join(folder, rel_path)
        
        #if file for current day has already been created load it
        if os.path.isfile(path):
            print(f"loading file for {guild}")
            with open(path, "r") as infile:
                data[guild] = json.load(infile)

        #else get guild data from api
        else:
            print(f"requesting data for {guild}")
            #read api key
            #request data
            r = requests.get(f"https://api.guildwars2.com/v2/guild/{guild_ids[guild]}/members", 
                             headers = {'Authorization': f'Bearer {get_key()}'})
            #hold data as json
            data[guild] = r.json()
            #save data to file so we don't have to request every time
            with open(path, "w+") as outfile:
                json.dump(data[guild], outfile)
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
    data = load_member_json()
    #throw data into table form here

if __name__ == "__main__":
    main()