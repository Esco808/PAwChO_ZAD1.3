from flask import Flask, render_template, request
import requests
import logging
from datetime import datetime
import os

# Konfiguracja
AUTHOR_NAME = "Paweł Ostrowski"
PORT = int(os.environ.get("PORT", 8000))
API_KEY = os.environ.get("OPENWEATHER_API_KEY")  # Klucz do OpenWeatherMap

# Logowanie
logging.basicConfig(level=logging.INFO)
logging.info(f"Aplikacja uruchomiona {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logging.info(f"Autor: {AUTHOR_NAME}")
logging.info(f"Nasłuchuję na porcie {PORT}")

# Inicjalizacja aplikacji
app = Flask(__name__)

# Predefiniowana lista krajów i miast
locations = {
    "Polska": ["Warszawa", "Kraków", "Gdańsk"],
    "Niemcy": ["Berlin", "Monachium", "Hamburg"],
    "Francja": ["Paryż", "Lyon", "Marsylia"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_country = None
    selected_city = None
    weather = None
    previous_country = None
    
    if request.method == "POST":
        # Sprawdzamy, czy użytkownik wybrał kraj i miasto
        selected_country = request.form.get("country")
        selected_city = request.form.get("city")

        # Wyczyszczenie selected_city, jeśli kraj został zmieniony
        if selected_country and selected_country != request.form.get("previous_country"):
            selected_city = None

        # Zapisujemy wybrany kraj w hidden field, aby porównać przy kolejnej zmianie
        previous_country = selected_country

        if selected_country and selected_city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}&units=metric&lang=pl"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "city": selected_city,
                    "country": selected_country
                }
            else:
                weather = {"error": "Nie udało się pobrać pogody"}
        else:
            # Jeśli nie wybrano miasta, wyczyść dane pogodowe
            weather = None

    return render_template("index.html",
                           locations=locations,
                           selected_country=selected_country,
                           selected_city=selected_city,
                           weather=weather,
                           previous_country=previous_country)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
