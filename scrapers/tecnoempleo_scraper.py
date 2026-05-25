import requests

from bs4 import BeautifulSoup

URL = "https://www.tecnoempleo.com/ofertas-trabajo/qa"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_tecnoempleo():

    print("Scraping Tecnoempleo...")

    response = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    offers = soup.select(".oferta")

    for offer in offers:

        title_el = offer.select_one("h2 a")

        company_el = offer.select_one(".empresa")

        if title_el:

            title = title_el.text.strip()

            url = title_el.get("href")

            company = (
                company_el.text.strip()
                if company_el else "Unknown"
            )

            if not url.startswith("http"):
                url = f"https://www.tecnoempleo.com{url}"

            jobs.append({
                "title": title,
                "company": company,
                "url": url,
                "source": "Tecnoempleo"
            })

    print(f"Tecnoempleo jobs: {len(jobs)}")

    return jobs
