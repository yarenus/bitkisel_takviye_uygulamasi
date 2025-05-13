import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = "https://www.ilacprospektusu.com"

# Örnek ilaç linkleri (başlangıç için 3 ilaç)
ilac_url_list = [
    "/ilac/6117-parol-film-tablet",
    "/ilac/5290-augmentin-bid-tablet",
    "/ilac/1561-nexium-40-mg-enterik-kapli-tablet"
]

def yan_etkileri_cek(url_ek):
    tam_url = BASE_URL + url_ek
    response = requests.get(tam_url)
    soup = BeautifulSoup(response.content, "html.parser")

    prospektus = soup.find("div", class_="prospektus")
    if not prospektus:
        return "Prospektüs bulunamadı."

    paragraphs = prospektus.find_all("p")
    etkiler = []
    found = False

    for p in paragraphs:
        text = p.get_text(strip=True).lower()
        if "yan etki" in text or "yan etkiler" in text:
            found = True
            continue
        if found:
            if p.find("strong"):  # Yeni başlığa geçtiyse dur
                break
            etkiler.append(p.get_text(strip=True))

    return " ".join(etkiler) if etkiler else "Yan etkiler bilgisi bulunamadı."

# Verileri tutmak için liste
veriler = []

for url in ilac_url_list:
    ilac_adi = url.split("/")[-1]
    print(f"{ilac_adi} için veriler çekiliyor...")
    yan_etkiler = yan_etkileri_cek(url)
    veriler.append([ilac_adi, yan_etkiler])
    time.sleep(2)  # siteyi yormamak için bekleme süresi

# CSV olarak kaydet
with open("ilac_yan_etkileri.csv", "w", newline="", encoding="utf-8") as dosya:
    writer = csv.writer(dosya)
    writer.writerow(["İlaç Adı", "Yan Etkiler"])
    writer.writerows(veriler)

print("✅ Veri çekme tamamlandı. 'ilac_yan_etkileri.csv' dosyası hazır.")
