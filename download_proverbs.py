from bs4 import BeautifulSoup
import json
import re

print("Downloading proverbs...")
url = "https://www.pinteric.com/proloc.html"
try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    response.raise_for_status()
    response.encoding = 'windows-1252'
    html = response.text
    with open("raw.html", "w", encoding="utf-8") as f:
        f.write(html)
except Exception as e:
    print(f"Error fetching URL: {e}")
    exit(1)

print("Parsing HTML...")
soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', class_='ordn')
proverbs = []
if table:
    for tr in table.find_all('tr'):
        if tr.find('th'):
            continue
        tds = tr.find_all('td')
        if not tds:
            continue
        if len(tds) == 2:
            latin_td, english_td = tds[0], tds[1]
            
            # Remove contributor links e.g. <a href="..."> (MS) </a>
            for a in latin_td.find_all('a'):
                a.decompose()
            for a in english_td.find_all('a'):
                a.decompose()
                
            latin = latin_td.get_text(separator=' ', strip=True)
            # Remove trailing author in em if present
            for em in latin_td.find_all('em'):
                text = em.get_text()
                if text.startswith('(') and text.endswith(')'):
                    latin = latin.replace(text, '').strip()
            
            english = english_td.get_text(separator=' ', strip=True)
            
            if len(latin) > 2:
                proverbs.append({
                    "latin": latin,
                    "translation": english
                })
        elif len(tds) == 1 and proverbs:
            # Continuation row due to rowspan="2"
            extra = tds[0].get_text(separator=' ', strip=True)
            proverbs[-1]["translation"] += " " + extra

print(f"Extracted {len(proverbs)} proverbs. Writing to JSON...")

with open("latin_proverbs.json", "w", encoding="utf-8") as f:
    json.dump(proverbs, f, indent=4, ensure_ascii=False)

print("Done! Here are the first 3:")
for p in proverbs[:3]:
    print(f" - {p['latin']} : {p['translation']}")
