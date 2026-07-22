from playwright.sync_api import sync_playwright
import re

# ============================================================================
# SEARCHES FILTRADAS PARA JUNIOR Y MID-LEVEL
# ============================================================================

SEARCHES = [
    # GENERAL QA AUTOMATION (JUNIOR/MID)
    "Junior QA Automation",
    "QA Automation Engineer Junior",
    "Mid-level QA Automation",
    "QA Engineer Junior",
    "Automation Tester Junior",
    "Test Automation Engineer Junior",
    
    # SDET
    "Junior SDET",
    "SDET Mid Level",
    
    # PLAYWRIGHT
    "Junior Playwright QA",
    "Playwright Automation Engineer",
    "QA Playwright Junior",
    
    # SELENIUM
    "Junior Selenium QA",
    "Selenium Python QA Junior",
    "Automation Tester Selenium Junior",
    
    # PYTHON QA
    "Python QA Engineer Junior",
    "Python Automation Tester",
    
    # CYPRESS
    "Junior Cypress QA",
    "Cypress Automation Engineer",
    
    # API TESTING
    "API Automation Tester Junior",
    "API QA Engineer",
    
    # GENERAL (Rejetar senior después)
    "QA Automation",
    "QA Engineer",
    "Automation Tester",
]

WORK_TYPES = {
    "Remote": 2,
    "Hybrid": 3
}

# ============================================================================
# KEYWORDS PARA FILTRAR
# ============================================================================

KEYWORDS = [
    # CORE
    "qa",
    "automation",
    "testing",
    "tester",
    "sdet",
    "quality",
    
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

# ============================================================================
# PALABRAS CLAVE PARA DETECTAR NIVEL (JUNIOR/MID)
# ============================================================================

JUNIOR_KEYWORDS = [
    r"\bjunior\b",
    r"\bjr\b",
    r"\bentry\s*level\b",
    r"\bentry-level\b",
    r"0-2\s*years",
    r"0-3\s*years",
    r"less than 2",
    r"less than 3",
    r"graduate",
    r"recién\s*graduad",
    r"\bjoven\b",
]

MID_KEYWORDS = [
    r"\bmid\s*level\b",
    r"\bmid-level\b",
    r"\bmiddle\b",
    r"mid-senior",
    r"senior mid",
    r"3-5\s*years",
    r"3-6\s*years",
    r"4-6\s*years",
    r"2-4\s*years",
]

# PALABRAS CLAVE PARA DETECTAR SENIOR (RECHAZAR)
SENIOR_KEYWORDS = [
    r"\bsenior\b",
    r"\bsr\b",
    r"\blead\b",
    r"\bsenior lead\b",
    r"\blead engineer\b",
    r"\barch(?:itect)?\b",
    r"\bprincipal\b",
    r"\bstaff\b",
    r"5\+\s*years",
    r"6\+\s*years",
    r"10\+\s*years",
    r"15\+\s*years",
    r"20\+\s*years",
    r"más de 5",
    r"más de 8",
    r"más de 10",
]

# PALABRAS A RECHAZAR
REJECT_KEYWORDS = [
    "director",
    "manager",
    "vp",
    "cto",
    "head of",
    "chief",
]


# ============================================================================
# FUNCIONES DE FILTRADO
# ============================================================================

def is_senior_position(title: str, description: str = "") -> bool:
    """Detecta si es un cargo Senior/Lead/Principal"""
    text = f"{title} {description}".lower()
    
    for pattern in SENIOR_KEYWORDS:
        if re.search(pattern, text):
            return True
    
    for keyword in REJECT_KEYWORDS:
        if keyword.lower() in text:
            return True
    
    return False


def is_junior_or_mid(title: str, description: str = "") -> bool:
    """Detecta si es Junior o Mid-Level"""
    text = f"{title} {description}".lower()
    
    # Buscar palabras clave de junior
    for pattern in JUNIOR_KEYWORDS:
        if re.search(pattern, text):
            return True
    
    # Buscar palabras clave de mid-level
    for pattern in MID_KEYWORDS:
        if re.search(pattern, text):
            return True
    
    return False


def contains_qa_keywords(text: str) -> bool:
    """Verifica que contenga keywords de QA"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in KEYWORDS)


def filter_job(title: str, company: str, description: str = "") -> tuple[bool, str]:
    """
    Filtra un job según criterios:
    - Rechazar Senior/Lead/Principal
    - Aceptar solo Junior o Mid-Level
    - Contener keywords de QA
    
    Returns: (is_valid, reason)
    """
    
    full_text = f"{title} {company} {description}".lower()
    
    # 1. Rechazar Senior
    if is_senior_position(title, description):
        return False, "❌ Senior/Lead/Principal position"
    
    # 2. Verificar que sea QA
    if not contains_qa_keywords(full_text):
        return False, "❌ No QA keywords found"
    
    # 3. Verificar que sea Junior o Mid
    if not is_junior_or_mid(title, description):
        # Si no detecta explícitamente junior/mid pero es QA, aceptar
        # (podría ser un "QA Automation" sin especificar nivel)
        # Pero mejor ser conservador y rechazar si no especifica
        return False, "⚠️  Level not specified (not Junior/Mid)"
    
    return True, "✅ Valid Junior/Mid QA position"


# ============================================================================
# SCRAPER MEJORADO
# ============================================================================

def scrape_linkedin():
    """
    Scraper de LinkedIn con filtros avanzados:
    - Solo cargos Junior/Mid-Level
    - Solo Barcelona
    - Sin Senior/Lead/Principal
    """
    
    print("=" * 80)
    print("🚀 LINKEDIN QA AUTOMATION SCRAPER - JUNIOR/MID LEVEL ONLY")
    print("=" * 80)
    
    jobs = []
    seen_urls = set()
    rejected_count = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for search in SEARCHES:
            for work_type_name, work_type_value in WORK_TYPES.items():
                
                print(f"\n🔍 Searching: '{search}' | {work_type_name}")
                print("-" * 80)
                
                # URL CON FILTROS MEJORADOS
                search_url = (
                    "https://www.linkedin.com/jobs/search/"
                    f"?keywords={search.replace(' ', '%20')}"
                    "&location=Barcelona%2C%20Spain"  # Barcelona específicamente
                    "&f_AL=true"  # Aplicar filtros de ubicación
                    "&f_TPR=r172800"  # Últimos 24h
                    f"&f_WT={work_type_value}"
                )
                
                try:
                    page.goto(search_url, wait_until="networkidle", timeout=30000)
                    page.wait_for_timeout(3000)
                    
                except Exception as e:
                    print(f"⚠️  Error loading page: {e}")
                    continue
                
                # CARGAR MÁS RESULTADOS
                try:
                    for scroll_attempt in range(5):
                        page.mouse.wheel(0, 5000)
                        page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"⚠️  Error scrolling: {e}")
                
                # EXTRAER TARJETAS
                try:
                    cards = page.locator(".base-card")
                    count = cards.count()
                    print(f"📊 Cards found: {count}")
                    
                except Exception as e:
                    print(f"❌ Error locating cards: {e}")
                    continue
                
                # PROCESAR CADA TARJETA
                for i in range(count):
                    try:
                        card = cards.nth(i)
                        
                        # EXTRAER DATOS BÁSICOS
                        title = card.locator(".base-search-card__title").inner_text().strip()
                        company = card.locator(".base-search-card__subtitle").inner_text().strip()
                        url = card.locator("a").first.get_attribute("href")
                        
                        # EVITAR DUPLICADOS
                        if url in seen_urls:
                            continue
                        
                        seen_urls.add(url)
                        
                        # APLICAR FILTROS
                        is_valid, reason = filter_job(title, company)
                        
                        if is_valid:
                            jobs.append({
                                "title": title,
                                "company": company,
                                "url": url,
                                "source": f"LinkedIn {work_type_name}",
                                "level": "Junior/Mid-Level"
                            })
                            print(f"  ✅ {title} | {company}")
                        else:
                            rejected_count += 1
                            # Descomenta para debug:
                            # print(f"  {reason}: {title} | {company}")
                    
                    except Exception as e:
                        print(f"  ⚠️  Card processing error: {e}")
                        continue
        
        browser.close()
    
    # RESUMEN
    print("\n" + "=" * 80)
    print("📈 SUMMARY")
    print("=" * 80)
    print(f"✅ Valid positions found: {len(jobs)}")
    print(f"❌ Rejected positions: {rejected_count}")
    print(f"📊 Unique URLs processed: {len(seen_urls)}")
    print("=" * 80)
    
    return jobs


# ============================================================================
# EXPORTAR RESULTADOS
# ============================================================================

def export_jobs_to_csv(jobs, filename="linkedin_qa_jobs.csv"):
    """Exporta los jobs a CSV"""
    import csv
    
    if not jobs:
        print("❌ No jobs to export")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'url', 'source', 'level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(jobs)
        
        print(f"✅ Jobs exported to {filename}")
    except Exception as e:
        print(f"❌ Export error: {e}")


def export_jobs_to_json(jobs, filename="linkedin_qa_jobs.json"):
    """Exporta los jobs a JSON"""
    import json
    
    if not jobs:
        print("❌ No jobs to export")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(jobs, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✅ Jobs exported to {filename}")
    except Exception as e:
        print(f"❌ Export error: {e}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    jobs = scrape_linkedin()
    
    # Exportar resultados
    if jobs:
        export_jobs_to_csv(jobs)
        export_jobs_to_json(jobs)
        
        print("\n📋 Sample of found jobs:")
        for job in jobs[:5]:
            print(f"  • {job['title']} @ {job['company']}")
