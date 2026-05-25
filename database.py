import sqlite3

DB_NAME = "jobs.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            url TEXT UNIQUE,
            source TEXT
        )
    """)

    conn.commit()
    conn.close()

def job_exists(url):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM jobs WHERE url = ?",
        (url,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None

def save_job(job):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs(title, company, url, source)
        VALUES (?, ?, ?, ?)
    """, (
        job["title"],
        job["company"],
        job["url"],
        job["source"]
    ))

    conn.commit()
    conn.close()