import data_loader
import pandas as pd
import os

def load_logs() -> pd.DataFrame:
    raw_logs = data_loader.load("logs")
    logs: dict[str, pd.DataFrame] = dict()
    for guild in raw_logs.keys():
        logs[guild] = pd.DataFrame.from_records(raw_logs[guild])
        logs[guild].insert(1, "guild", guild, True)
    combined = pd.concat(logs.values())
    combined.sort_values(by = ["time", "id"], ascending=False, inplace=True)
    combined.info()
    return combined

def save_logs(table:pd.DataFrame, file_name:str) -> None:
    table_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"tables/{data_loader.today}")
    if not os.path.isdir(table_folder):
        os.makedirs(table_folder)
    with open(os.path.join(table_folder, f"{file_name}.csv"), "w+") as file:
        table.to_csv(file, index=False, line_terminator='\n')

def filter(logs:pd.DataFrame, filter:list[str]) -> pd.DataFrame:
    return logs.where(logs["type"].isin(filter)).dropna(how="all").dropna(axis=1, how="all")

def filter_join_leave(logs:pd.DataFrame) -> pd.DataFrame:
    filter_values = [
          "joined",
          "invited",
          "kick"
     ]
    columns = [
          "id",
          "time",
          "guild",
          "type",
          "user",
          "invited_by",
          "kicked_by"
    ]
    logs = filter(logs, filter_values)
    logs = logs.reindex(columns, axis=1)
    logs.info()
    return logs

def filter_treasury(logs:pd.DataFrame) -> pd.DataFrame:
    filter_values = [
          "treasury",
          "stash"
    ]
    logs = filter(logs, filter_values)
    logs.info()
    return logs

def gen_tables() -> None:
    logs = load_logs()
    save_logs(logs, "log_all")
    filtered_logs = filter_join_leave(logs)
    start_date = filtered_logs["time"].min()
    join_leave_count = filtered_logs.groupby("type").count()
    print(f"Log dating back to {start_date}")
    print(join_leave_count)
    save_logs(filtered_logs, "log_join_leave")

    #treasury and bank and stuff
    treasury_log = filter_treasury(logs)
    save_logs(treasury_log, "bank")

if __name__ == "__main__":
    gen_tables()