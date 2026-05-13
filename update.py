import yfinance as yf
import json
from datetime import datetime

def get_live_data():
    try:
        # We halen de ticker voor de BEL20 op (^BFX)
        bel20 = yf.Ticker("^BFX")
        # Haal de koers van vandaag op
        data = bel20.history(period="1d")
        
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            open_price = data['Open'].iloc[0]
            change_pct = ((current_price - open_price) / open_price) * 100
            
            # Bepaal een simpel sentiment op basis van de dagbeweging
            sentiment = "Optimistisch" if change_pct > 0 else "Voorzichtig"
            if change_pct > 1: sentiment = "Zeer Bullish"
            if change_pct < -1: sentiment = "Bearish"

            # Maak het lijstje voor je website
            result = {
                "price": f"{current_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "change": f"{change_pct:+.2g}%".replace(".", ","),
                "sentiment": sentiment,
                "last_update": datetime.now().strftime("%H:%M:%S")
            }

            # Schrijf dit weg naar data.json
            with open('data.json', 'w') as f:
                json.dump(result, f, indent=4)
            print("Data succesvol bijgewerkt!")
        else:
            print("Kon geen data vinden.")

    except Exception as e:
        print(f"Fout opgetreden: {e}")

if __name__ == "__main__":
    get_live_data()
