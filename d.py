import pandas as pd
import numpy as np
import os
from openpyxl import Workbook, load_workbook
import re
from itertools import product
player_name_mapping = {
    # Exact matches between first and second file
    "Virat Kohli": "Virat Kohli",
    "Ruturaj Gaikwad": "Ruturaj Gaikwad",
    "Riyan Parag": "Riyan Parag",
    "Travis Head": "Travis Head",
    "Sanju Samson": "Sanju Samson",
    "Sai Sudharsan": "Sai Sudharsan",
    "K L Rahul": "Lokesh Rahul",#,,
    "Nicholas Pooran": "Nicholas Pooran",
    "Sunil Narine": "Sunil Narine",
    "Abhishek Sharma": "Abhishek Sharma",
    "Heinrich Klaasen": "Heinrich Klaasen",
    "Rishabh Pant": "Rishabh Pant",
    "Faf Du Plessis": "Faf du Plessis",
    "Phil Salt": "Philip Salt",#,,
    "Yashasvi Jaiswal": "Yashasvi Jaiswal",
    "Shubman Gill": "Shubman Gill",
    "Rohit Sharma": "Rohit Sharma",
    "Tilak Varma": "Tilak Varma",
    "Shivam Dube": "Shivam Dube",
    "Rajat Patidar": "Rajat Patidar",
    "Marcus Stoinis": "Marcus Stoinis",
    "Tristan Stubbs": "Tristan Stubbs",
    "Venkatesh Iyer": "Venkatesh Iyer",
    "Jos Buttler": "Jos Buttler",
    "Shashank Singh": "Shashank Singh",
    "Shreyas Iyer": "Shreyas Iyer",
    "Suryakumar Yadav": "Suryakumar Yadav",
    "Prabhsimran Singh": "Prabhsimran Singh",
    "Jake Fraser - McGurk": "Jake Fraser-McGurk",
    "Abishek Porel": "Abishek Porel",
    "Ishan Kishan": "Ishan Kishan",
    "Nitish Kumar Reddy": "K Nitish Reddy",#,,
    
    "Sam Curran": "Sam Curran",
    "Ravindra Jadeja": "Ravindra Jadeja",
    
    "Quinton De Kock": "Quinton de Kock",
    "Ajinkya Rahane": "Ajinkya Rahane",
    "Tim David": "Tim David",
    "Ayush Badoni": "Ayush Badoni",
    "Axar Patel": "Axar Patel",
    "Will Jacks": "Will Jacks",
    "Andre Russell": "Andre Russell",
    "Rachin Ravindra": "Rachin Ravindra",
    "Aiden Markram": "Aiden Markram",
    "Hardik Pandya": "Hardik Pandya",
    "Shahbaz Ahmed": "Shahbaz Ahmed",
    "David Miller": "David Miller",
    "Dhruv Jurel": "Dhruv Jurel",
    "Ashutosh Sharma": "Ashutosh Sharma",
    "Rahul Tewatia": "Rahul Tewatia",
    "Jitesh Sharma": "Jitesh Sharma",
    "Abdul Samad": "Abdul Samad",
    "Rinku Singh": "Rinku Singh",
    "Rahul Tripathi": "Rahul Tripathi",
    "Angkrish Raghuvanshi": "Angkrish Raghuvanshi",
    "MS Dhoni": "MS Dhoni",
    "Deepak Hooda": "Deepak Hooda",
    "Naman Dhir": "Naman Dhir",
    "Pat Cummins": "Pat Cummins",
    "Krunal Pandya": "Krunal Pandya",
    "Moeen Ali": "Moeen Ali",
    "Shahrukh Khan": "Shahrukh Khan",
    "Ramandeep Singh": "Ramandeep Singh",
    "Mahipal Lomror": "Mahipal Lomror",
    "Shimron Hetmyer": "Shimron Hetmyer",
    "Liam Livingstone": "Liam Livingstone",
    "Nehal Wadhera": "Nehal Wadhera",
    "Rovman Powell": "Rovman Powell",
    "Rashid Khan": "Rashid-Khan",
    "Anuj Rawat": "Anuj Rawat",
    "Ravichandran Ashwin": "Ravichandran Ashwin",
    "Arshad Khan": "Arshad Khan",
    "Vijay Shankar": "Vijay Shankar",
    "Harpreet Brar": "Harpreet Brar",
    "Rahmanullah Gurbaz": "Rahmanullah Gurbaz",
    "Mitchell Marsh": "Mitchell Marsh",
    "Atharva Taide": "Atharva Taide",
    "Romario Shepherd": "Romario Shepherd",
    "Glenn Maxwell": "Glenn Maxwell",
    "Sameer Rizwi": "Sameer Rizvi",
    "Kuldeep Yadav": "Kuldeep Yadav",
    "Manish Pandey": "Manish Pandey",
    "Azmatullah Omarzai": "Azmatullah Omarzai",
    "Nitish Rana": "Nitish Rana",
    "Devdutt Padikkal": "Devdutt Padikkal",
    "Swapnil Singh": "Swapnil Singh",
    "Mohammad Nabi": "Mohammed Nabi",
    "Shubham Dubey": "Shubham Dubey",
    "Karn Sharma": "Karn Sharma",
    "Rasikh Salam": "Rasikh Salam",
    "Suyash S Prabhudessai": "Suyash Sharma",#,,
    "Jaydev Unadkat": "Jaydev Unadkat",
    "Bhuvneshwar Kumar": "Bhuvneshwar Kumar",
    "Yudhvir Singh": "Yudhvir Singh Charak",#,,
    "Rahul Chahar": "Rahul Chahar",
    "Shardul Thakur": "Shardul Thakur",
    "Kagiso Rabada": "Kagiso Rabada",
    "Marco Jansen": "Marco Jansen",
    "Trent Boult": "Trent Boult",
    "Mitchell Santner": "Mitchell Santner",
    "Gerald Coetzee": "Gerald Coetzee",
    "Sai Kishore": "Ravisrinivasan Sai Kishore",
    "Harshal Patel": "Harshal Patel",
    "Mohammed Siraj": "Mohammed Siraj",
    "Darshan Nalkande": "Darshan Nalkande",
    "Jasprit Bumrah": "Jasprit Bumrah",
    "Umesh Yadav": "Umesh Yadav",
    "Avesh Khan": "Avesh Khan",
    "Luke Wood": "Luke Wood",
    "Arshin Atul Kulkarni": "Arshin Kulkarni",
    "Mitchell Starc": "Mitchell Starc",
    "Abhinav Manohar": "Abhinav Manohar",
    "Donovan Ferreira": "Donovan Ferreira",
    "Vijayakanth Viyaskanth": "Vijayakanth Viyaskanth",
    "Spencer Johnson": "Spencer Johnson",
    "Noor Ahmad": "Noor Ahmad",
    "Arshdeep Singh": "Arshdeep Singh",
    "Akash Madhwal": "Akash Madhwal",
    "Ravi Bishnoi": "Ravi Bishnoi",
    "Anrich Nortje": "Anrich Nortje",
    "Mohit Sharma": "Mohit Sharma",
    "Anukul Roy": "Anukul Sudhakar Roy",
    "Reece Topley": "Reece Topley",
    "Kumar Kushagra": "Kumar Kushagra",
    "Mukesh Kumar": "Mukesh Kumar",
    "Mohsin Khan": "Mohsin Khan",
    "Richard Gleeson": "Richard Gleeson",
    "Anshul Kamboj": "Anshul Kamboj",
    "Akash Deep": "Akash Deep",
    "Vaibhav Arora": "Vaibhav Arora",
    "Lockie Ferguson": "Lockie Ferguson",
    "Lizaad Williams": "Lizaad Williams",
    "Keshav Maharaj": "Keshav Maharaj",
    "Manav Suthar": "Manav Suthar",
    "Vyshak Vijaykumar": "Vyshak Vijaykumar",
    "Ishant Sharma": "Ishant Sharma",
    
    # Players from most_wickets_2024.csv that aren't in the mapping above
    "Varun Chakaravarthy": "Varun Chakravarthy",
    "T Natarajan": "T Natarajan",
    "Harshit Rana": "Harshit Rana",
    "Yuzvendra Chahal": "Yuzvendra Chahal",
    "Tushar Deshpande": "Tushar Deshpande",
    "Khaleel Ahmed": "Khaleel Ahmed",
    "Yash Dayal": "Yash Dayal",
    "Matheesha Pathirana": "Matheesha Pathirana",
    "Sandeep Sharma": "Sandeep Sharma",
    "Yash Thakur": "Yash Thakur",
    "Kuldeep Sen": "Kuldeep Sen",
    "Deepak Chahar": "Deepak Chahar",
    "Simarjeet Singh": "Simarjeet- Singh",#,,
    "Shreyas Gopal": "Shreyas Gopal",
    "Maheesh Theekshana": "Maheesh Theekshana",
    "M Siddharth": "Manimaran Siddharth",
    
    "Washington Sundar": "Washington Sundar",
    "Kwena Maphaka": "Kwena Maphaka",

    # Matches from most_wickets_2023.csv
    "Mohammed Shami": "Mohammad Shami",
    "Adam Zampa": "Adam Zampa",
    "Wanindu Hasaranga": "Wanindu Hasaranga",
    "Jofra Archer": "Jofra Archer", 
    "Fazalhaq Farooqi": "Fazalhaq Farooqi",
    "Josh Hazlewood": "Josh Hazlewood",
    "Lungi Ngidi": "Lungi Ngidi ",  # Not an exact match but adding for completeness
    "Umran Malik": "Umran Malik",
    "Mayank Markande": "Mayank Markande",
    "Chetan Sakariya": "Chetan Sakariya",
    
    
    "Glenn Phillips": "Glenn Phillips",
    "Kulwant Khejroliya": "Kulwant Khejroliya",
    
    
    # Matches from top_run_scorers_2023.csv
    "Devon Conway": "Devon Conway",
    
}
k=pd.read_csv('SquadPlayerNames_IndianT20League - SquadData_AllTeams.csv')
for i in k['Player Name']:
    if i not in player_name_mapping.values():
        player_name_mapping[i]=i
# Global variables to store loaded data
SQUAD_DF = None
BATSMAN_ALL_YEARS = None
BOWLER_ALL_YEARS = None
BATSMAN_RECENT = None
BOWLER_RECENT = None
actual_points_df = pd.read_csv('New Folder/point13.csv')

def load_cricket_data():
    """Load all cricket data once and store in global variables"""
    global SQUAD_DF, BATSMAN_ALL_YEARS, BOWLER_ALL_YEARS, BATSMAN_RECENT, BOWLER_RECENT
    
    try:
        SQUAD_DF = pd.read_csv('New Folder/SquadPlayerNames13.csv')
        playing_players = SQUAD_DF[SQUAD_DF['IsPlaying'] == 'PLAYING']
        playing_names = playing_players['Player Name'].tolist()
        print(f"Loaded {len(playing_names)} active players from squad list")
    except FileNotFoundError:
        raise ValueError("SquadPlayerNames.csv file not found.")
    except Exception as e:
        raise ValueError(f"Error loading squad data: {e}")

    batsman_dfs = []
    bowler_dfs = []
    
    for year in range(2018, 2026):
        try:
            # Load batsman data with new format
            batsman_df = pd.read_csv(f"a/top_run_scorers_{year}.csv")
            
            # Map new column names to old format
            column_mapping = {
                'StrikerName': 'player_name',
                'PlayerId': 'player_id',
                'Matches': 'matches_played',
                'Innings': 'innings_played',
                'NotOuts': 'not_outs',
                'TotalRuns': 'runs_scored',
                'Balls': 'balls_faced',
                'Fours': 'fours',
                'Sixes': 'sixes',
                'HighestScore': 'highest_score',
                'Outs': 'zeroes',  # This mapping might need adjustment
                'BattingAverage': 'batting_average'
            }
            
            # Add derived columns based on new format
            if 'NotOuts' not in batsman_df.columns and 'Outs' in batsman_df.columns and 'Innings' in batsman_df.columns:
                batsman_df['NotOuts'] = batsman_df['Innings'] - batsman_df['Outs']
            
            # Handle 30s, 50s, 100s if not in the new format
            if 'FiftyPlusRuns' in batsman_df.columns:
                if 'Centuries' in batsman_df.columns:
                    batsman_df['fifties'] = batsman_df['FiftyPlusRuns'] - batsman_df['Centuries']
                else:
                    batsman_df['fifties'] = batsman_df['FiftyPlusRuns']
            else:
                batsman_df['fifties'] = 0
                
            if 'Centuries' in batsman_df.columns:
                batsman_df['hundred'] = batsman_df['Centuries']
            else:
                batsman_df['hundred'] = 0
                
            # Add thirties as a computed field if not present
            batsman_df['thirties'] = 0  # This would need actual calculation based on your criteria
            
            # Rename columns to match expected format
            for new_col, old_col in column_mapping.items():
                if new_col in batsman_df.columns:
                    batsman_df.rename(columns={new_col: old_col}, inplace=True)
            
            # Filter for playing players
            
            mask=[]
            for x in batsman_df['player_name']:
                if x in playing_names or player_name_mapping.get(x) in playing_names:
                    mask.append(True)
                else:
                    mask.append(False)

           
            
            batsman_df = batsman_df [mask]
            batsman_df['player_name'] = batsman_df['player_name'].map(lambda x: player_name_mapping.get(x, x))
            
            # Handle highest_score formatting
            if 'highest_score' in batsman_df.columns:
                batsman_df['highest_score'] = batsman_df['highest_score'].apply(
                    lambda x: re.sub(r'[^0-9]', '', str(x)) if pd.notna(x) else x
                )
                batsman_df['highest_score'] = pd.to_numeric(batsman_df['highest_score'], errors='coerce')
            
            batsman_df['year'] = year
            batsman_dfs.append(batsman_df)
            print(f"Loaded and filtered batting stats for {year}: {len(batsman_df)} players")
            
        except FileNotFoundError:
            print(f"Batsman stats file for {year} not found.")
        except Exception as e:
            print(f"Error processing batsman data for {year}: {e}")
        
        try:
            # Load bowler data with new format
            bowler_df = pd.read_csv(f"a/most_wickets_{year}.csv")
            
            # Map new column names to old format
            bowl_column_mapping = {
                'BowlerName': 'player_name',
                'BowlerID': 'player_id',
                'Matches': 'matches_played',
                'Innings': 'innings',
                'OversBowled': 'overs',
                'Maidens': 'most_maidens',
                'TotalRunsConceded': 'runs_given',
                'Wickets': 'wickets',
                'LegalBallsBowled': 'balls_bowled',
                'FourWickets': 'four_wickets_haul',
                'FiveWickets': 'five_wickets_haul',
                'BBIW': 'best_bowling_figures'  # Best Bowling in an Innings (Wickets)
            }
            
            # Add derived columns for three wicket hauls if not present
            if 'ThreeWickets' not in bowler_df.columns:
                # Calculate three wicket hauls as matches where wickets >= 3 but < 4
                if 'MatchWickets' in bowler_df.columns:
                    bowler_df['three_wickets_haul'] = bowler_df.apply(
                        lambda row: 0 if row['MatchWickets'] >= 3 and row['MatchWickets'] < 4 else 0, 
                        axis=1
                    ).sum()
                else:
                    # Approximate if we don't have match-level data
                    bowler_df['three_wickets_haul'] = 0
            else:
                bowler_df['three_wickets_haul'] = bowler_df['ThreeWickets']
            
            # Rename columns to match expected format
            for new_col, old_col in bowl_column_mapping.items():
                if new_col in bowler_df.columns:
                    bowler_df.rename(columns={new_col: old_col}, inplace=True)
            
            # Filter for playing players
            mask=[]
            #mask = batsman_df.apply(lambda player_name_mapping: player_name_mapping.get('player_name') in playing_names, axis=1)
            for x in bowler_df['player_name']:
                if x in playing_names or player_name_mapping.get(x) in playing_names:
                    mask.append(True)
                else:
                    mask.append(False)
            # Filter the DataFrame using the Boolean mask
            bowler_df = bowler_df [mask]
            bowler_df['player_name'] = bowler_df['player_name'].map(lambda x: player_name_mapping.get(x, x))
            bowler_df['year'] = year
            bowler_dfs.append(bowler_df)
            print(f"Loaded and filtered bowling stats for {year}: {len(bowler_df)} players")
            
        except FileNotFoundError:
            print(f"Bowler stats file for {year} not found.")
        except Exception as e:
            print(f"Error processing bowler data for {year}: {e}")
    
    if batsman_dfs:
        BATSMAN_ALL_YEARS = pd.concat(batsman_dfs, ignore_index=True)
    else:
        raise ValueError("No batsman data files found or no batsmen match the active squad list.")
    
    if bowler_dfs:
        BOWLER_ALL_YEARS = pd.concat(bowler_dfs, ignore_index=True)
    else:
        raise ValueError("No bowler data files found or no bowlers match the active squad list.")
    
    last_two_years = [2024,2025]
    BATSMAN_RECENT = BATSMAN_ALL_YEARS[BATSMAN_ALL_YEARS['year'].isin(last_two_years)]
    BOWLER_RECENT = BOWLER_ALL_YEARS[BOWLER_ALL_YEARS['year'].isin(last_two_years)]

def optimize_bowling_point_system():
    # Ensure data is loaded
    if SQUAD_DF is None:
        load_cricket_data()
        
    # Define point value options
    wicket_points_options = [25, 35, 45]
    three_wicket_points_options = [4, 6, 8]
    maiden_points_options = [12, 18, 24]
    
    # For four and five wicket hauls, we'll derive as multiples of three_wicket_points
    # (i.e., 2x and 3x respectively)
    
    # Define independent factor options (no requirement that lifetime + form = 1)
    # Here we use a reduced set for demonstration; adjust as needed.
    batting_lifetime_options = [round(i/20,2) for i in range(1,20)]
    
    bowling_lifetime_options = [round(i/20,2) for i in range(1,20)]
    
    
    # Generate all point combinations
    point_combinations = list(product(
        wicket_points_options,
        three_wicket_points_options,
        maiden_points_options,
    ))
    
    total_point_combos = len(point_combinations)
    total_factor_combos = (len(batting_lifetime_options) *
                           len(bowling_lifetime_options) )
    
    print(f"Testing {total_point_combos} bowling point system combinations...")
    print(f"With {total_factor_combos} independent batting/bowling factor combinations...")
    print(f"Total parameter combinations to test: {total_point_combos * total_factor_combos}")
    
    # Check for existing results file
    excel_file = "bowling_point_system_results.xlsx"
    existing_results = {}
    if os.path.exists(excel_file):
        print(f"Found existing results file: {excel_file}")
        try:
            existing_df = pd.read_excel(excel_file)
            for _, row in existing_df.iterrows():
                key = (
                    row['wicket_points'], row['three_wicket_points'], row['four_wicket_points'],
                    row['five_wicket_points'], row['maiden_points'],
                    row['batting_lifetime_factor'], row['batting_form_factor'],
                    row['bowling_lifetime_factor'], row['bowling_form_factor']
                )
                existing_results[key] = row['total_team_points']
            print(f"Loaded {len(existing_results)} existing results")
        except Exception as e:
            print(f"Error loading existing results: {e}")
            existing_results = {}
    
    results = []
    
    # Iterate over independent factor combinations
    for batting_lifetime_factor in batting_lifetime_options:
        for batting_form_factor in [round(1-batting_lifetime_factor,2)]:
            for bowling_lifetime_factor in bowling_lifetime_options:
                for bowling_form_factor in [round(1-bowling_lifetime_factor,2)]:
                    print(f"\nTesting with Batting LT={batting_lifetime_factor}, Batting Form={batting_form_factor}, "
                          f"Bowling LT={bowling_lifetime_factor}, Bowling Form={bowling_form_factor}")
                    
                    for combo in point_combinations:
                        wicket_pts, three_wkt_pts, maiden_pts = combo
                        # Derive additional point values
                        four_wkt_pts = 2 * three_wkt_pts
                        five_wkt_pts = 3 * three_wkt_pts
                        
                        key = (
                            wicket_pts, three_wkt_pts, four_wkt_pts, five_wkt_pts, maiden_pts,
                            batting_lifetime_factor, batting_form_factor,
                            bowling_lifetime_factor, bowling_form_factor
                        )
                        
                        try:
                            player_points, fantasy_team = calculate_points_and_select_team(
                                batting_lifetime_factor=batting_lifetime_factor,
                                batting_form_factor=batting_form_factor,
                                bowling_lifetime_factor=bowling_lifetime_factor,
                                bowling_form_factor=bowling_form_factor,
                                wicket_points=wicket_pts,
                                three_wicket_points=three_wkt_pts,
                                four_wicket_points=four_wkt_pts,
                                five_wicket_points=five_wkt_pts,
                                maiden_points=maiden_pts,
                            )
                            fantasy_team = fantasy_team.sort_values(by='total_points', ascending=False).reset_index(drop=True)
                            if actual_points_df is not None:
                                
                                fantasy_team = pd.merge(
                                    fantasy_team,
                                    actual_points_df,
                                    left_on='player_name',
                                    right_on='player_name',
                                    how='left'
                                )
                                weighted_points = 0
                                if len(fantasy_team) > 0:
                                    weighted_points += fantasy_team.loc[0, 'Points'] * 2
                                if len(fantasy_team) > 1:
                                    weighted_points += fantasy_team.loc[1, 'Points'] * 1.5
                                if len(fantasy_team) > 2:
                                    weighted_points += fantasy_team.loc[2:, 'Points'].sum()
                                total_team_points = weighted_points
                            else:
                                total_team_points = 0
                            
                            source_label = 'new'
                            if key in existing_results:
                                old_points = existing_results[key]
                                total_team_points += old_points
                                source_label = 'updated'
                            
                            results.append({
                                'wicket_points': wicket_pts,
                                'three_wicket_points': three_wkt_pts,
                                'four_wicket_points': four_wkt_pts,
                                'five_wicket_points': five_wkt_pts,
                                'maiden_points': maiden_pts,
                                'batting_lifetime_factor': batting_lifetime_factor,
                                'batting_form_factor': batting_form_factor,
                                'bowling_lifetime_factor': bowling_lifetime_factor,
                                'bowling_form_factor': bowling_form_factor,
                                'total_team_points': total_team_points,
                                'source': source_label
                            })
                            
                            print(f"BT LT={batting_lifetime_factor}, BT Form={batting_form_factor}, "
                                  f"BW LT={bowling_lifetime_factor}, BW Form={bowling_form_factor}, "
                                  f"W={wicket_pts}, 3W={three_wkt_pts}, 4W={four_wkt_pts}, 5W={five_wkt_pts}, "
                                  f"M={maiden_pts} → Team Points: {total_team_points:.2f}")
                            
                        except Exception as e:
                            print(f"Error with combo {combo} and factors BT LT={batting_lifetime_factor}, "
                                  f"BT Form={batting_form_factor}, BW LT={bowling_lifetime_factor}, "
                                  f"BW Form={bowling_form_factor}: {e}")
                            results.append({
                                'wicket_points': wicket_pts,
                                'three_wicket_points': three_wkt_pts,
                                'four_wicket_points': four_wkt_pts,
                                'five_wicket_points': five_wkt_pts,
                                'maiden_points': maiden_pts,
                                'batting_lifetime_factor': batting_lifetime_factor,
                                'batting_form_factor': batting_form_factor,
                                'bowling_lifetime_factor': bowling_lifetime_factor,
                                'bowling_form_factor': bowling_form_factor,
                                'total_team_points': 0,
                                'source': 'error'
                            })
    
    results_df = pd.DataFrame(results)
    results_df['weighted_score'] = results_df['total_team_points']
    results_df = results_df.sort_values(by='weighted_score', ascending=False)
    
    try:
        results_df.to_excel(excel_file, index=False)
        print(f"\nResults overwritten to {excel_file}")
        print("\nTop 5 bowling point system combinations:")
        print(results_df[['wicket_points', 'three_wicket_points', 'four_wicket_points', 
                          'five_wicket_points', 'maiden_points',  
                          'batting_lifetime_factor', 'batting_form_factor',
                          'bowling_lifetime_factor', 'bowling_form_factor',
                          'total_team_points','weighted_score']].head(5))
        
        best_combo = results_df.iloc[0]
        print(f"\nBest combination:")
        print(f"Batting Lifetime Factor: {best_combo['batting_lifetime_factor']}")
        print(f"Batting Form Factor: {best_combo['batting_form_factor']}")
        print(f"Bowling Lifetime Factor: {best_combo['bowling_lifetime_factor']}")
        print(f"Bowling Form Factor: {best_combo['bowling_form_factor']}")
        print(f"Wicket: {best_combo['wicket_points']} points")
        print(f"3 Wicket Haul: {best_combo['three_wicket_points']} points")
        print(f"4 Wicket Haul: {best_combo['four_wicket_points']} points")
        print(f"5 Wicket Haul: {best_combo['five_wicket_points']} points")
        print(f"Maiden Over: {best_combo['maiden_points']} points")
        print(f"Total team points: {best_combo['total_team_points']:.2f}")
        print(f"Weighted score: {best_combo['weighted_score']:.2f}")
        
    except Exception as e:
        print(f"Error saving results: {e}")
    
    return results_df

def calculate_points_and_select_team(
    batting_lifetime_factor=0.7,
    batting_form_factor=0.3,
    bowling_lifetime_factor=0.7,
    bowling_form_factor=0.3,
    wicket_points=25,
    three_wicket_points=4,
    four_wicket_points=8,
    five_wicket_points=12,
    maiden_points=1,
):
    """Calculate points and select team using pre-loaded data"""
    if SQUAD_DF is None:
        load_cricket_data()
    
    # ------ BATSMAN DATA PROCESSING ------
    batsman_lifetime = BATSMAN_ALL_YEARS.groupby('player_name').agg({
        'player_id': 'first',
        'matches_played': 'sum',
        'innings_played': 'sum',
        'not_outs': 'sum',
        'runs_scored': 'sum',
        'thirties': 'sum',
        'fifties': 'sum',
        'hundred': 'sum',
        'fours': 'sum',
        'sixes': 'sum',
        'zeroes': 'sum',
        'highest_score': 'max',
        'balls_faced': 'sum'
    }).reset_index()
    
    batsman_form = BATSMAN_RECENT.groupby('player_name').agg({
        'player_id': 'first',
        'matches_played': 'sum',
        'innings_played': 'sum',
        'not_outs': 'sum',
        'runs_scored': 'sum',
        'thirties': 'sum',
        'fifties': 'sum',
        'hundred': 'sum',
        'fours': 'sum',
        'sixes': 'sum',
        'zeroes': 'sum',
        'highest_score': 'max',
        'balls_faced': 'sum'
    }).reset_index()
    
    # ------ BOWLER DATA PROCESSING ------
    bowler_lifetime = BOWLER_ALL_YEARS.groupby('player_name').agg({
        'player_id': 'first',
        'matches_played': 'sum',
        'overs': 'sum',
        'most_maidens': 'sum',
        'runs_given': 'sum',
        'wickets': 'sum',
        'three_wickets_haul': 'sum',
        'five_wickets_haul': 'sum',
        'four_wickets_haul': 'sum',
        'best_bowling_figures': 'first',
        'balls_bowled': 'sum',
        'innings': 'sum'
    }).reset_index()
    
    bowler_form = BOWLER_RECENT.groupby('player_name').agg({
        'player_id': 'first',
        'matches_played': 'sum',
        'overs': 'sum',
        'most_maidens': 'sum',
        'runs_given': 'sum',
        'wickets': 'sum',
        'three_wickets_haul': 'sum',
        'five_wickets_haul': 'sum',
        'four_wickets_haul': 'sum',
        'best_bowling_figures': 'first',
        'balls_bowled': 'sum',
        'innings': 'sum'
    }).reset_index()
        
    def calculate_batting_points(df):
        points = pd.DataFrame()
        points['player_id'] = df['player_id']
        points['player_name'] = df['player_name']
        points['runs_points'] = df['runs_scored'] * 1
        points['fours_points'] = df['fours'] * 4
        points['sixes_points'] = df['sixes'] * 6
        points['thirty_points'] = df['thirties'] * 4
        points['fifty_points'] = df['fifties'] * 8
        points['hundred_points'] = df['hundred'] * 16
        points['total_batting_points'] = (points['runs_points'] + points['fours_points'] +
                                            points['sixes_points'] + points['thirty_points'] +
                                            points['fifty_points'] + points['hundred_points'])
        points['innings_played'] = df['innings_played']
        points['batting_points_per_inning'] = points.apply(
            lambda row: row['total_batting_points'] / row['innings_played'] if row['innings_played'] > 0 else 0,
            axis=1
        )
        return points

    def calculate_bowling_points(df):
        points = pd.DataFrame()
        points['player_id'] = df['player_id']
        points['player_name'] = df['player_name']
        points['wicket_points'] = df['wickets'] * wicket_points
        points['three_wkt_points'] = df['three_wickets_haul'] * three_wicket_points
        points['four_wkt_points'] = df['four_wickets_haul'] * four_wicket_points
        points['five_wkt_points'] = df['five_wickets_haul'] * five_wicket_points
        points['maiden_points'] = df['most_maidens'] * maiden_points
        points['total_bowling_points'] = (points['wicket_points'] + points['three_wkt_points'] +
                                          points['four_wkt_points'] + points['five_wkt_points'] +
                                          points['maiden_points'])
        points['innings_played'] = df['innings']
        points['bowling_points_per_inning'] = points.apply(
            lambda row: row['total_bowling_points'] / row['innings_played'] if row['innings_played'] > 0 else 0,
            axis=1
        )
        return points

    batting_lifetime_points = calculate_batting_points(batsman_lifetime)
    batting_form_points = calculate_batting_points(batsman_form)
    bowling_lifetime_points = calculate_bowling_points(bowler_lifetime)
    bowling_form_points = calculate_bowling_points(bowler_form)
    batting_lifetime_points['stats_type'] = 'lifetime'
    batting_form_points['stats_type'] = 'form'
    bowling_lifetime_points['stats_type'] = 'lifetime'
    bowling_form_points['stats_type'] = 'form'
    
    batting_lifetime_points['weight'] = batting_lifetime_factor
    batting_form_points['weight'] = batting_form_factor
    bowling_lifetime_points['weight'] = bowling_lifetime_factor
    bowling_form_points['weight'] = bowling_form_factor
    
    batting_lifetime_points['weighted_batting_points'] = batting_lifetime_points['batting_points_per_inning'] * batting_lifetime_points['weight']
    batting_form_points['weighted_batting_points'] = batting_form_points['batting_points_per_inning'] * batting_form_points['weight']
    bowling_lifetime_points['weighted_bowling_points'] = bowling_lifetime_points['bowling_points_per_inning'] * bowling_lifetime_points['weight']
    bowling_form_points['weighted_bowling_points'] = bowling_form_points['bowling_points_per_inning'] * bowling_form_points['weight']
    
    batting_points = pd.concat([batting_lifetime_points, batting_form_points], ignore_index=True)
    bowling_points = pd.concat([bowling_lifetime_points, bowling_form_points], ignore_index=True)
    for df in [batting_points, bowling_points]:
        for col in df.columns:
            if df[col].dtype in [float, int]:
                df[col] = df[col].fillna(0)
    # Aggregate batting and bowling points by player_id
    batting_points_summary = batting_points.groupby('player_name').agg({
    'player_id': 'first',
    'weighted_batting_points': 'sum'
    }).reset_index()

    bowling_points_summary = bowling_points.groupby('player_name').agg({
    'player_id': 'first',
    'weighted_bowling_points': 'sum'
    }).reset_index()

# Merge batting and bowling points summary with an outer join
    player_points = pd.merge(
    batting_points_summary,
    bowling_points_summary,
    on='player_name',
    how='outer',
    suffixes=('_batting', '_bowling')
    )


# Combine the player_name fields: if missing from batting, pick bowling's value
# Using `combine_first` to fill NaN in 'player_name_batting' with values from 'player_name_bowling'
    
# Replace NaNs in the points columns with 0
    player_points['weighted_batting_points'] = player_points['weighted_batting_points'].fillna(0)
    player_points['weighted_bowling_points'] = player_points['weighted_bowling_points'].fillna(0)

# Now aggregate points, since there might be duplicate player_ids
# First, group by 'player_id' and aggregate the stats
    
# Calculate total points
    player_points['total_points'] = player_points['weighted_batting_points'] + player_points['weighted_bowling_points']

# Reorder the columns to match the desired output
    player_points = player_points[['player_name', 'weighted_batting_points', 'weighted_bowling_points', 'total_points']]

    #import ace_tools as tools; tools.display_dataframe_to_user(name="Player Points Summary", dataframe=player_points)


    player_points = pd.merge(
        player_points,
        SQUAD_DF[['Player Name', 'Credits', 'Player Type', 'Team', 'IsPlaying', 'lineupOrder']],
        left_on='player_name',
        right_on='Player Name',
        how='left'
    )
    
    final_columns = [
        'player_name', 'Team', 
        'weighted_batting_points', 'weighted_bowling_points', 'total_points',
        'Player Type', 'Credits', 'IsPlaying', 'lineupOrder'
    ]
    
    player_points_final = player_points[final_columns].sort_values(by='total_points', ascending=False)
    
    def select_fantasy_team(players_df):
        df = players_df.copy()
        df = df[df['IsPlaying'] == 'PLAYING']
        df['total_points'] = df['total_points'].fillna(0).astype(float)
        df = df.sort_values(by='total_points', ascending=False)
        team = []
        selected_player_ids = set()
        teams = df['Team'].unique()
        
        wk_players = df[df['Player Type'] == 'WK']
        if len(wk_players) > 0:
            best_wk = wk_players.iloc[0]
            team.append(best_wk)
            selected_player_ids.add(best_wk['player_name'])
        
        bat_players = df[(df['Player Type'] == 'BAT') & (~df['player_name'].isin(selected_player_ids))]
        for team_name in teams:
            team_bats = bat_players[bat_players['Team'] == team_name]
            if len(team_bats) > 0:
                best_bat = team_bats.iloc[0]
                team.append(best_bat)
                selected_player_ids.add(best_bat['player_name'])
                if len([p for p in team if p['Player Type'] == 'BAT']) >= 2:
                    break
        
        bowl_players = df[(df['Player Type'] == 'BOWL') & (~df['player_name'].isin(selected_player_ids))]
        for team_name in teams:
            team_bowls = bowl_players[bowl_players['Team'] == team_name]
            if len(team_bowls) > 0:
                best_bowl = team_bowls.iloc[0]
                team.append(best_bowl)
                selected_player_ids.add(best_bowl['player_name'])
                if len([p for p in team if p['Player Type'] == 'BOWL']) >= 2:
                    break
        
        all_players = df[(df['Player Type'] == 'ALL') & (~df['player_name'].isin(selected_player_ids))]
        for team_name in teams:
            team_alls = all_players[all_players['Team'] == team_name]
            if len(team_alls) > 0:
                best_all = team_alls.iloc[0]
                team.append(best_all)
                selected_player_ids.add(best_all['player_name'])
                if len([p for p in team if p['Player Type'] == 'ALL']) >= 2:
                    break
        
        remaining_players = df[~df['player_name'].isin(selected_player_ids)]
        remaining_slots = 11 - len(team)
        for i in range(min(remaining_slots, len(remaining_players))):
            next_best = remaining_players.iloc[i]
            team.append(next_best)
        
        team_df = pd.DataFrame(team)
        return team_df
    fantasy_team = select_fantasy_team(player_points_final)
    
    return player_points_final, fantasy_team
if __name__ == "__main__":
    load_cricket_data()
    optimize_bowling_point_system()