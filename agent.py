import requests
import os
from datetime import datetime

def check_odds():
    # GitHub Secrets ထဲက API_KEY ကိုယူခြင်း
    API_KEY = os.getenv('ODDS_API_KEY')
    
    # UEFA Youth League (U19) အတွက် API Key
    SPORT = 'soccer_uefa_youth_league' 
    
    print(f"--- Odds Analysis Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    print(f"Target League: UEFA U19 Champions League\n")

    # API URL - Betfair Exchange မှ Odds များကိုယူခြင်း
    URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions=uk&markets=h2h&bookmakers=betfair_ex"

    try:
        response = requests.get(URL)
        
        if response.status_code != 200:
            print(f"Error {response.status_code}: Check API Key or Quota Limit.")
            return
            
        data = response.json()

        if not data:
            print("ယခုရက်ပိုင်းအတွင်း UEFA U19 ပွဲစဉ်များ မရှိသေးပါ။")
            return

        for match in data:
            home_team = match.get('home_team')
            away_team = match.get('away_team')
            start_time = match.get('commence_time')
            
            if match.get('bookmakers'):
                # ပထမဆုံးရနိုင်သော Market Data ကိုယူခြင်း
                market = match['bookmakers'][0]['markets'][0]
                outcomes = market['outcomes']
                
                try:
                    # လက်ရှိ Odds တန်ဖိုးများ
                    h_price = next(o['price'] for o in outcomes if o['name'] == home_team)
                    a_price = next(o['price'] for o in outcomes if o['name'] == away_team)
                    
                    # --- သင်၏ Formula Logic (Diff တွက်ချက်မှု) ---
                    # ဤနေရာတွင် Open နှင့် Close Odd ခြားနားချက်ကို ထည့်သွင်းစဉ်းစားရန်
                    # လက်ရှိတွင် စမ်းသပ်ရန်အတွက် နမူနာ Diff တစ်ခုကို အသုံးပြုထားသည်
                    home_diff = 0.35  # ဥပမာ- Close - Open
                    away_diff = -0.40 

                    prediction = "--- No Signal ---"
                    if home_diff >= 0.3 and away_diff <= -0.3:
                        prediction = "🔥 RESULT: HOME WIN"
                    elif home_diff <= -0.3 and away_diff >= 0.3:
                        prediction = "🔥 RESULT: AWAY WIN"
                    elif abs(home_diff) < 0.3 and abs(away_diff) < 0.3:
                        prediction = "⚖️ RESULT: DRAW"

                    print(f"⚽ {home_team} vs {away_team}")
                    print(f"   Start Time: {start_time}")
                    print(f"   Current Odds: [H: {h_price}, A: {a_price}]")
                    print(f"   Analysis {prediction}\n")
                    print("-" * 30)
                
                except Exception:
                    continue
            else:
                print(f"⚽ {home_team} vs {away_team} | Odds data မရရှိသေးပါ။")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if name == "__main__":
    check_odds()
