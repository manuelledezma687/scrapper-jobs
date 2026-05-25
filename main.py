from database import init_db, save_job, job_exists
from scrapers.remoteok_scraper import scrape_remoteok
from scrapers.tecnoempleo_scraper import scrape_tecnoempleo
from scrapers.linkedin_scraper import scrape_linkedin
from telegram_service import send_telegram_message

all_jobs = []

init_db()

print("===================================")
print("STARTING QA JOB HUNTER BOT")
print("===================================")

try:
    all_jobs.extend(scrape_remoteok())
except Exception as e:
    print(f"RemoteOK Error: {e}")

try:
    all_jobs.extend(scrape_tecnoempleo())
except Exception as e:
    print(f"Tecnoempleo Error: {e}")

try:
    all_jobs.extend(scrape_linkedin())
except Exception as e:
    print(f"LinkedIn Error: {e}")

new_jobs = []

for job in all_jobs:

    if not job_exists(job["url"]):
        save_job(job)
        new_jobs.append(job)

print(f"New jobs found: {len(new_jobs)}")

if new_jobs:

    message = "🔥 NEW QA AUTOMATION JOBS\n\n"

    for idx, job in enumerate(new_jobs, start=1):

        message += (
            f"{idx}. {job['title']}\n"
            f"🏢 {job['company']}\n"
            f"🌍 {job['source']}\n"
            f"{job['url']}\n\n"
        )

    send_telegram_message(message)

print("FINISHED")