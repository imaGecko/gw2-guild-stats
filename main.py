import data_loader
import pandas as pd
import os

raw_data = data_loader.load("members")
guilds = raw_data.keys()
tables:dict[str, pd.DataFrame] = dict()

for guild in guilds:
    tables[guild] = pd.DataFrame.from_records(raw_data[guild])
    print(tables[guild])


combined_table = tables['cruel'].merge(right=tables['chaotic'], how='outer', on='name')
print(combined_table.info())
filter = combined_table['rank_x'].notnull()&combined_table['rank_y'].notnull() 
both_guilds = combined_table.where(filter).dropna()
print(both_guilds.info())
different_ranks = both_guilds.where(both_guilds['rank_x']!=both_guilds['rank_y']).dropna()
print(different_ranks)

table_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"tables/{data_loader.today}")
if not os.path.isdir(table_folder):
    os.makedirs(table_folder)

with open(os.path.join(table_folder, "guild_table.csv"), "w+") as file:
    combined_table.to_csv(file)
with open(os.path.join(table_folder, "both_guilds.csv"), "w+") as file:
    both_guilds.to_csv(file)
with open(os.path.join(table_folder, "different_ranks.csv"), "w+") as file:
    different_ranks.to_csv(file)