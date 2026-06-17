from __future__ import annotations

import sqlite3
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "nayepankh_saathi.db"


def get_connection():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    with get_connection() as conn:

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS volunteers(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                full_name TEXT,

                email TEXT,

                phone TEXT,

                age INTEGER,

                city TEXT,

                preferred_program TEXT,

                preferred_role TEXT,

                skills TEXT,

                availability TEXT,

                motivation TEXT,

                created_at TEXT

            )
            """
        )

        conn.commit()


def add_volunteer(data):

    with get_connection() as conn:

        cursor = conn.execute(
            """
            INSERT INTO volunteers(

                full_name,
                email,
                phone,
                age,
                city,
                preferred_program,
                preferred_role,
                skills,
                availability,
                motivation,
                created_at

            )

            VALUES(?,?,?,?,?,?,?,?,?,?,?)

            """,
            (
                data["full_name"],
                data["email"],
                data["phone"],
                data["age"],
                data["city"],
                data["preferred_program"],
                data["preferred_role"],
                data["skills"],
                data["availability"],
                data["motivation"],
                data["created_at"],
            ),
        )

        conn.commit()

        return cursor.lastrowid


def get_recent_volunteers(search="", limit=25):

    query = "SELECT * FROM volunteers"

    params = []

    if search:

        query += """
        WHERE full_name LIKE ?
        OR email LIKE ?
        OR city LIKE ?
        """

        term = f"%{search}%"

        params = [term, term, term]

    query += " ORDER BY id DESC LIMIT ?"

    params.append(limit)

    with get_connection() as conn:

        rows = conn.execute(query, params).fetchall()

        return [dict(row) for row in rows]


def registrations_by_date():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT

            substr(created_at,1,10) as date,

            COUNT(*) as registrations

            FROM volunteers

            GROUP BY date

            ORDER BY date
            """
        ).fetchall()

        return [dict(r) for r in rows]


def program_distribution():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT

            preferred_program,

            COUNT(*) as count

            FROM volunteers

            GROUP BY preferred_program
            """
        ).fetchall()

        return [dict(r) for r in rows]


def skills_distribution():

    with get_connection() as conn:

        rows = conn.execute(
            """
            SELECT skills
            FROM volunteers
            """
        ).fetchall()

    counter = Counter()

    for row in rows:

        if row["skills"]:

            for skill in row["skills"].split(","):

                counter[skill.strip()] += 1

    return [

        {"skill": skill, "count": count}

        for skill, count in counter.items()

    ]


def get_overview_stats():

    with get_connection() as conn:

        total = conn.execute(
            "SELECT COUNT(*) FROM volunteers"
        ).fetchone()[0]

        cities = conn.execute(
            "SELECT COUNT(DISTINCT city) FROM volunteers"
        ).fetchone()[0]

        programs = conn.execute(
            "SELECT COUNT(DISTINCT preferred_program) FROM volunteers"
        ).fetchone()[0]

    skills = skills_distribution()

    return {

        "total_volunteers": total,

        "unique_cities": cities,

        "unique_programs": programs,

        "unique_skills": len(skills),

    }