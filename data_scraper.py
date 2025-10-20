import requests
from bs4 import BeautifulSoup
import csv
import time



def scrape_website(url, max_pages=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    all_headlines = []
    page = 1

    while True:
        try:
            response = requests.get(f"{url}?page={page}", headers=headers, timeout = 10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            
            #collecting headline text from <article> tags if present
            for article in soup.find_all("article"):
                #finding the first headline in the article
                heading = article.find(["h1", "h2", "h3"])
                if heading and heading.get_text(strip=True):
                    all_headlines.append((heading.get_text(strip=True), article.get('href')))
                    
            #Collecting standalone headlines        
            for tag in soup.find_all(["h1", "h2"]):
                text = tag.get_text(strip=True)
                if text:
                    all_headlines.append((text, None))
                    
            #anchor tags that may represent headlines        
            for a in soup.find_all("a", class_=lambda c: any(cls for cls in c.split() if "head" in cls.lower() or "title" in cls.lower()) if c else False):
                txt = a.get_text(strip= True)
                if txt:
                    all_headlines.append((txt, a['href'] if a.get('href') else None))
                    
            if len(all_headlines) < 10 or page >= max_pages:
                break
            
            time.sleep(2)
            
            page +=1

        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"An Error Occured: {e}")
            break
        
    return all_headlines

url = input("Enter the website URL: ")
headlines = scrape_website(url)
print("\nTop headlines:")
for headline, link in headlines[:10]:
    print(f"{headline} {'[' + link + ']' if link else ''}")



#common headline containers
candidates = []    

            
seen = set()
headlines = []
for h in candidates:
    if h not in seen:
        seen.add(h)
        headlines.append(h)

# 7. Show top N headlines (example N = 10)
top_headlines = headlines[:10]