
import requests
import json
import csv
import re
import os

urls = {
    "most_wickets": "https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/stats/10012-mostwickets.js?callback=onmostwickets&_=1742828483769",
    "top_run_scorers": "https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/stats/10012-toprunsscorers.js?callback=ontoprunsscorers&_=1742828483768",
    "match_schedule": "https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/archievefeeds/10012-matchschedule.js?MatchSchedule=_jqjsp&_1742828484761="
}


def remove_existing_csv(filename):
    csv_filename = f"{filename}.csv"
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
        print(f"Removed existing file: {csv_filename}")

def fetch_and_save(url, callback, filename, selected_columns=None):
    response = requests.get(url)
    data_text = response.text
    
    match = re.search(rf'{re.escape(callback)}\((.*)\)', data_text)

    if match:
        json_str = match.group(1).strip()
        json_data = json.loads(json_str)  
        key = list(json_data.keys())[0]  
        records = json_data.get(key, [])
    else:
        print(f"Error: JSON data not found for {filename}")
        return

    if selected_columns:
        records = [{k: v for k, v in record.items() if k in selected_columns} for record in records]

    csv_filename = f"{filename}.csv"

    if records:
        headers = records[0].keys()
    else:
        print(f"No data available for {filename}")
        return

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    print(f"Data saved to {csv_filename}")

remove_existing_csv("New Folder/most_wickets_2020")
fetch_and_save(urls["most_wickets"], "onmostwickets", "New Folder/most_wickets_2020")

remove_existing_csv("New Folder/top_run_scorers_2020")
fetch_and_save(urls["top_run_scorers"], "ontoprunsscorers", "New Folder/top_run_scorers_2020")

match_schedule_columns = [
    "CompetitionID", "MatchID", "MatchTypeID", "MatchType", "MatchStatus", "MatchDate", "MatchDateNew",
    "MatchName", "MatchTime", "GMTMatchTime", "GMTMatchDate", "GMTMatchEndTime", "GMTMatchEndDate",
    "FirstBattingTeamID", "FirstBattingTeamName", "SecondBattingTeamID", "SecondBattingTeamName",
    "FirstBattingTeamCode", "SecondBattingTeamCode", "GroundID", "GroundName", "Commentss", "TossTeam",
    "TossDetails", "TossText", "FirstBattingSummary", "SecondBattingSummary", "MatchEndDate", "MatchEndTime",
    "MatchTypeName", "CompetitionName", "GroundUmpire1", "GroundUmpire2", "ThirdUmpire", "Comments"
]

remove_existing_csv("match_schedule_2020")
fetch_and_save(urls["match_schedule"], "MatchSchedule", "match_schedule_2020", match_schedule_columns)