import sqlite3
from datetime import datetime

DB_FILE = "onboarding.db"


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS countries (
                code        TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                risk_level  TEXT NOT NULL CHECK (risk_level IN ('LOW', 'HIGH'))
            );

            CREATE TABLE IF NOT EXISTS sanctions_list (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name  TEXT NOT NULL UNIQUE,
                added_on   TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS customers (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                name              TEXT    NOT NULL,
                age               INTEGER NOT NULL,
                nationality_code  TEXT    NOT NULL REFERENCES countries(code),
                is_pep            INTEGER NOT NULL,
                id_expiry         TEXT    NOT NULL,
                created_at        TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id  INTEGER NOT NULL REFERENCES customers(id),
                decision     TEXT    NOT NULL,
                decided_at   TEXT    NOT NULL
            );
        """)
        seed(conn)


def seed(conn):
    # Training values only, not a real country risk assessment
    conn.executemany(
        "INSERT OR IGNORE INTO countries (code, name, risk_level) VALUES (?, ?, ?)",
        [
            ("SA", "Saudi Arabia", "LOW"),
            ("SD", "Sudan", "LOW"),
            ("AE", "United Arab Emirates", "LOW"),
            ("XA", "Training Country A", "HIGH"),
            ("XB", "Training Country B", "HIGH"),
        ],
    )
    conn.executemany(
        "INSERT OR IGNORE INTO sanctions_list (full_name, added_on) VALUES (?, ?)",
        [
            ("Omar Khalid", "2026-09-01"),
            ("Salem Nasser", "2026-09-01"),
            ("Tariq Mansour", "2026-09-01"),
        ],
    )

def get_high_risk_countries():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT code FROM countries WHERE risk_level = 'HIGH'"
        ).fetchall()

    codes = []
    for row in rows:
        codes.append(row[0])
    return codes

def get_sanctions_names():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT full_name FROM sanctions_list"
        ).fetchall()

    names  = []
    for row in rows:
        names.append(row[0])
    return names 

def country_exists(code):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM countries WHERE code = ?", (code,)
        ).fetchone()
    return row is not None

def save_application(customer, decision):
    now = datetime.now().isoformat(timespec="seconds")

    with get_conn() as conn:
        cursor = conn.execute(
            """INSERT INTO customers
               (name, age, nationality_code, is_pep, id_expiry, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (customer["name"], customer["age"], customer["nationality"],
             int(customer["is_pep"]), customer["id_expiry"], now),
        )
        customer_id = cursor.lastrowid

        cursor = conn.execute(
            """INSERT INTO decisions (customer_id, decision, decided_at)
               VALUES (?, ?, ?)""",
            (customer_id, decision, now),
        )
        application_id = cursor.lastrowid

    return customer_id, application_id