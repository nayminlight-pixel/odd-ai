import requests
import json
import os

API_KEY = os.getenv("API_KEY")

url = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"

params = {
    "apiKey": API_KEY,
    "regions": "eu",
    "markets": "h2h"
}

if os.path.exists("odds.json"):
    with open("odds.json") as f:
        old_data = json.load(f)
else:
    old_data = {}

res = requests.get(url, params=params)
data = res.json()

new_data = {}

print("\n=== ODDS AI AGENT ===\n")

for match in data:
    teams = " vs ".join(match['teams'])
    odds = match['bookmakers'][0]['markets'][0]['outcomes']

    home = odds[0]['price']
    away = odds[1]['price']

    new_data[teams] = {"home": home, "away": away}

    if teams in old_data:
        home_open = old_data[teams]['home']
        away_open = old_data[teams]['away']

        home_diff = home - home_open
        away_diff = away - away_open

        if home_diff <= -0.3 and away_diff >= 0.3:
            result = "HOME WIN"
        elif home_diff >= 0.3 and away_diff <= -0.3:
            result = "AWAY WIN"
        elif abs(home_diff) < 0.3 and abs(away_diff) < 0.3:
            result = "DRAW"
        else:
            result = "NO SIGNAL"

        print(teams, "→", result)

with open("odds.json", "w") as f:
    json.dump(new_data, f, indent=2)
