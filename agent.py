import requests
import os
from datetime import datetime

def check_odds():
    API_KEY = os.getenv('ODDS_API_KEY')
    
    # လက်ရှိပွဲရှိနိုင်မည့် League များ (U19 နှင့် အခြားပွဲများပါဝင်သည်)
    LEAGUES = [
        'soccer_uefa_youth_league', 
        'soccer_fifa_world_cup_qualifiers_afc', # Asia World Cup Qualifiers
        'soccer_international_friendly'         # နိုင်ငံတကာခြေစမ်းပွဲများ
    ]

    print(f"--- Odds Analysis Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

    for sport_key in LEAGUES:
        URL = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/?apiKey={API_KEY}&regions=uk&markets=h2h"

        try:
            response = requests.get(URL)
            
            # API Response ကို စစ်ဆေးခြင်း
            if response.status_code != 200:
                print(f"[{sport_key}] API Error {response.status_code}: {response.text}")
                continue
                
            data = response.json()

            # Data က List မဟုတ်ဘဲ Dictionary ဖြစ်နေရင် (Error Message ဖြစ်နိုင်သည်)
            if isinstance(data, dict):
                print(f"[{sport_key}] Message: {data.get('msg', 'Unknown Error')}")
                continue

            if not data:
                print(f"[{sport_key}] ယခုရက်ပိုင်းအတွင်း ပွဲစဉ်မရှိသေးပါ။")
                continue

            print(f"\n--- Checking: {sport_key.upper()} ---")
            
            for match in data:
                home_team = match.get('home_team')
                away_team = match.get('away_team')
                
                # Bookmakers data ရှိမှသာ ဆက်လုပ်မည်
                if not match.get('bookmakers'):
                    print(f"⚽ {home_team} vs {away_team} | Odds မထွက်သေးပါ။")
                    continue

                try:
                    # ပထမဆုံးရရှိနိုင်သော Bookmaker ၏ Odds ကိုယူခြင်း
                    outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
                    
                    h_price = next(o['price'] for o in outcomes if o['name'] == home_team)
                    a_price = next(o['price'] for o in outcomes if o['name'] == away_team)
                    
                    # --- သင်၏ Formula Logic ---
                    # အမှန်တကယ်အလုပ်လုပ်ရန် Open နှင့် Close Odd ခြားနားချက် လိုအပ်ပါသည်။
                    # လက်ရှိတွင် logic အလုပ်လုပ်ပုံကို နမူနာပြထားပါသည်
                    home_diff = 0.35  
                    away_diff = -0.40 

                    prediction = "No Clear Signal"
                    if home_diff >= 0.3 and away_diff <= -0.3:
                        prediction = "🔥 RESULT: HOME WIN"
                    elif home_diff <= -0.3 and away_diff >= 0.3:
                        prediction = "🔥 RESULT: AWAY WIN"

                    print(f"⚽ {home_team} vs {away_team} | Odds: [H:{h_price}, A:{a_price}] -> {prediction}")
                
                except (KeyError, IndexError, StopIteration):
                    continue

        except Exception as e:
            print(f"Error fetching {sport_key}: {str(e)}")

if name == "__main__":
    check_odds()
