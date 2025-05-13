import requests
from bs4 import BeautifulSoup
import json

URL = "https://probitki.com/sifali-bitkiler"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

bitkiler = []

# İlk 20 bitkiyi al
for i, li in enumerate(soup.select("ol > li")):
    if i >= 20:
        break

    ad_raw = li.find(text=True).strip()
    detaylar = li.find_all("li")
    kullanim = ""
    fayda = ""

    for detay in detaylar:
        metin = detay.get_text(strip=True)
        if "kullanım Alanları" in metin:
            kullanim = metin.replace("kullanım Alanları:", "").strip()
        elif "Faydalar" in metin:
            fayda = metin.replace("Faydalar:", "").strip()

    bitkiler.append({
        "ad": ad_raw,
        "kullanim_alanlari": kullanim,
        "faydalar": fayda
    })

# JSON dosyasına yaz
with open("bitkiler.json", "w", encoding="utf-8") as f:
    json.dump(bitkiler, f, ensure_ascii=False, indent=4)

print("✅ bitkiler.json dosyası oluşturuldu.")
