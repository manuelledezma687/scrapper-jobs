import requests

from bs4 import BeautifulSoup

URL = "https://remoteok.com/remote-qa-jobs"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_remoteok():

    print("Scraping RemoteOK...")

    response = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    rows = soup.select("tr.job")

    for row in rows:

        title_el = row.select_one("h2")
        company_el = row.select_one("h3")
        link_el = row.get("data-href")

        if title_el and company_el and link_el:

            jobs.append({
                "title": title_el.text.strip(),
                "company": company_el.text.strip(),
                "url": f"https://remoteok.com{link_el}",
                "source": "RemoteOK"
            })

    print(f"RemoteOK jobs: {len(jobs)}")

    return jobs

