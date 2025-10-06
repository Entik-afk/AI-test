import requests
import json
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Stáhnout data o počasí (pokud ještě nejsou stažena)
url="https://api.open-meteo.com/v1/forecast?latitude=49.58&longitude=18.75&hourly=temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    with open("pocasi.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f" Staženo")
else:
    print(" Chyba:", response.status_code, response.text)

# 1️⃣ Načíst data z JSON (pokud už jsou stažena)
with open("pocasi.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hourly = data["hourly"]

# 2️⃣ Převést do DataFrame
df = pd.DataFrame(hourly)

# Převod času na datetime, pokud je ve sloupci "time"
if "time" in df.columns:
    df["time"] = pd.to_datetime(df["time"])

df = df.fillna(0)


# 3️⃣ Spočítat statistiky
stats = df.describe().loc[["min", "max", "mean"]].round(1)
print("✅ Statistiky počasí:\n", stats)

# 4️⃣ Připravený souhrn pro OpenAI
summary = (
    f"Teplota: min {stats['temperature_2m']['min']}°C, max {stats['temperature_2m']['max']}°C, průměr {stats['temperature_2m']['mean']}°C\n"
    f"Vlhkost: min {stats['relative_humidity_2m']['min']}%, max {stats['relative_humidity_2m']['max']}%, průměr {stats['relative_humidity_2m']['mean']}%\n"
    f"Srážky: min {stats['precipitation']['min']} mm, max {stats['precipitation']['max']} mm, průměr {stats['precipitation']['mean']} mm\n"
    f"Vítr: min {stats['wind_speed_10m']['min']} m/s, max {stats['wind_speed_10m']['max']} m/s, průměr {stats['wind_speed_10m']['mean']} m/s"
)
print(summary)


lat, lon = 49.58, 18.75
geo_url = f"https://geocode.maps.co/reverse?lat={lat}&lon={lon}"
geo_resp = requests.get(geo_url)
address = geo_resp.json().get("address", {})

city = (
    address.get("city")
    or address.get("town")
    or address.get("village")
    or address.get("municipality")
    or "Neznámé město"
)



# 5️⃣ Vygenerovat komentář přes OpenAI

prompt = f"Napiš krátký a srozumitelný komentář o počasí v lokalitě {city} podle těchto statistik:\n{summary}"

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=200
)

text = completion.choices[0].message.content

with open("pocasi.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(" Komentář uložen do pocasi.txt")
