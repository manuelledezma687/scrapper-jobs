from playwright.sync_api import sync_playwright

SEARCHES = [

    # GENERAL QA AUTOMATION
    "QA Automation",
    "QA Automation Engineer",
    "QA Engineer",
    "Automation Tester",
    "Test Automation Engineer",
    "Software Test Engineer",

    # SDET
    "SDET",
    "Senior SDET",
    "Junior SDET",

    # PLAYWRIGHT
    "Playwright QA",
    "Playwright Engineer",
    "Playwright Automation",
    "QA Playwright",

    # SELENIUM
    "Selenium QA",
    "Selenium Automation",
    "Selenium Python QA",
    "Selenium Java QA",
    "Automation Tester Selenium",

    # PYTHON QA
    "Python QA",
    "Python Automation Tester",
    "QA Python Engineer",

    # CYPRESS
    "Cypress QA",
    "Cypress Automation",
    "QA Cypress Engineer",

    # TESTING
    "Software Tester Automation",
    "Automation QA Tester",
    "QA Testing Automation",

    # API TESTING
    "API Automation Tester",
    "API QA Engineer",
    "Postman QA Automation",

    # MOBILE QA
    "Mobile QA Automation",
    "Appium QA",

    # MANUAL + AUTOMATION HYBRID
    "QA Analyst Automation",
    "QA Consultant Automation",

    # SPANISH SEARCHES
    "QA Automatizacion",
    "Tester Automatizacion",
    "Ingeniero QA",
    "Automation Tester QA",

    # DEV QA
    "Quality Engineer",
    "Software Quality Engineer",

    # HOT KEYWORDS
    "Pytest QA",
    "Robot Framework QA",
    "BDD QA Automation",

]

WORK_TYPES = {
    "Remote": 2,
    "Hybrid": 3
}

KEYWORDS = [

    # CORE
    "qa",
    "automation",
    "testing",
    "tester",
    "sdet",

    # TOOLS
    "selenium",
    "playwright",
    "cypress",
    "appium",
    "postman",
    "pytest",
    "robot framework",

    # LANGUAGES
    "python",
    "java",
    "javascript",
    "typescript",

    # METHODOLOGIES
    "bdd",
    "tdd",

]


def scrape_linkedin():

    print("Scraping LinkedIn...")

    jobs = []

    seen_urls = set()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        for search in SEARCHES:

            for work_type_name, work_type_value in WORK_TYPES.items():

                print(
                    f"Searching: {search} | {work_type_name}"
                )

                search_url = (
                    "https://www.linkedin.com/jobs/search/"
                    f"?keywords={search.replace(' ', '%20')}"
                    "&location=Spain"
                    "&f_AL=true"
                    "&f_TPR=r172800"
                    f"&f_WT={work_type_value}"
                )

                page.goto(search_url)

                page.wait_for_timeout(5000)

                # LOAD MORE RESULTS
                for _ in range(5):

                    page.mouse.wheel(0, 5000)

                    page.wait_for_timeout(2000)

                cards = page.locator(".base-card")

                count = cards.count()

                print(f"Cards found: {count}")

                for i in range(count):

                    try:

                        card = cards.nth(i)

                        title = card.locator(
                            ".base-search-card__title"
                        ).inner_text().strip()

                        company = card.locator(
                            ".base-search-card__subtitle"
                        ).inner_text().strip()

                        url = card.locator(
                            "a"
                        ).first.get_attribute("href")

                        # REMOVE DUPLICATES
                        if url in seen_urls:
                            continue

                        seen_urls.add(url)

                        full_text = (
                            f"{title} {company}"
                        ).lower()

                        # FILTER QA JOBS
                        if not any(
                            keyword in full_text
                            for keyword in KEYWORDS
                        ):
                            continue

                        jobs.append({
                            "title": title,
                            "company": company,
                            "url": url,
                            "source": f"LinkedIn {work_type_name}"
                        })

                    except Exception as e:

                        print(f"Card Error: {e}")

                        continue

        browser.close()

    print(f"LinkedIn jobs: {len(jobs)}")

    return jobs