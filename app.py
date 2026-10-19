
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask import jsonify
from datetime import datetime

app = Flask(__name__)

app.secret_key = "7777777"

DATABASE = "rivals.db"

VALID_ROLES = {"Vanguard", "Duelist", "Strategist"}
VALID_HEROES = {"Spider-Man", "Magik", "Star-Lord", "Mantis"}

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                roles TEXT NOT NULL DEFAULT '',
                heroes TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT ''
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS schedule_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                timezone TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                created_by INTEGER,
                FOREIGN KEY (created_by) REFERENCES profiles(id)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS player_availability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL UNIQUE,
                availability TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
        """)

def get_current_profile():
    profile_id = session.get("profile_id")

    if profile_id is None:
        return None

    with get_db() as db:
        return db.execute(
            "SELECT * FROM profiles WHERE id = ?",
            (profile_id,)
        ).fetchone()


@app.route("/", methods=["GET", "POST"])
def index():
    profile = get_current_profile()


    if request.method == "GET" and profile:
        return redirect(url_for("view_profile"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        description = request.form.get("description", "").strip()

        # Check the submitted values on the server.
        roles = list(dict.fromkeys(request.form.getlist("roles")))
        heroes = list(dict.fromkeys(request.form.getlist("heroes")))

        if not username or len(username) > 30:
            return "Username must be 1–30 characters.", 400

        if len(description) > 500:
            return "Description must be 500 characters or fewer.", 400

        if not set(roles).issubset(VALID_ROLES):
            return "Invalid role selected.", 400

        if not set(heroes).issubset(VALID_HEROES):
            return "Invalid hero selected.", 400

        if len(heroes) > 4:
            return "You can select up to four heroes.", 400

        roles_text = ",".join(roles)
        heroes_text = ",".join(heroes)

        with get_db() as db:
            if profile:
                db.execute("""
                    UPDATE profiles
                    SET username = ?, roles = ?,
                        heroes = ?, description = ?
                    WHERE id = ?
                """, (
                    username, roles_text, heroes_text,
                    description, profile["id"]
                ))
            else:
                cursor = db.execute("""
                    INSERT INTO profiles
                    (username, roles, heroes, description)
                    VALUES (?, ?, ?, ?)
                """, (
                    username, roles_text, heroes_text, description
                ))
                session["profile_id"] = cursor.lastrowid

        return redirect(url_for("view_profile"))

    return render_template(
    "index.html",
    profile=profile,
    heroes_list=HEROES
)

@app.route("/profile")
def view_profile():
    profile = get_current_profile()

    if profile is None:
        return redirect(url_for("index"))

    return render_template(
        "profile.html",
        profile=profile,
        roles=profile["roles"].split(",") if profile["roles"] else [],
        heroes=profile["heroes"].split(",") if profile["heroes"] else []
    )


@app.route("/edit")
def edit_profile():
    profile = get_current_profile()

    if profile is None:
        return redirect(url_for("index"))

    return render_template(
    "index.html",
    profile=profile,
    heroes_list=HEROES
)

@app.route("/team-planner")
def team_planner():
    with get_db() as db:
        profiles = db.execute(
            "SELECT id, username, roles, heroes, description "
            "FROM profiles ORDER BY username COLLATE NOCASE"
        ).fetchall()

    available_profiles = [
        {
            "id": profile["id"],
            "username": profile["username"],
            "roles": profile["roles"].split(",") if profile["roles"] else [],
            "heroes": profile["heroes"].split(",") if profile["heroes"] else [],
            "description": profile["description"]
        }
        for profile in profiles
    ]

    return render_template(
        "team-planner.html",
        available_profiles=available_profiles
    )


HEROES = [
    "Spider-Man",
    "Magik",
    "Star-Lord",
    "Mantis",
    "Iron-Man",
    "Thor",
    "Hulk",
    "Luna Snow",
    "Moon Knight",
    "Psylocke",
    "Scarlet Witch",
    "Venom",
    "Wolverine",
    "Adam",
    "Punisher",
    "Invisible Woman",
    "Human Torch",
    "Jeff TLS",
    "Gorr",
    "Black Panther",
    "Phoenix",
    "Emma Snow",
    "Angela",
    "Blade",
    "CloaknDagger",
    "DareDevil",
    "Steve Rogers",
    "Hawkeye",
    "Loki",
    "Magneto",
    "Squirrel Girl",
    "Ultron",
    "Reed Richards",
    "The Thing",
    "Jubilee",
    "Hood",
    "Rogue",
    "Black Cat",
    "Elsa Bloodstone",
    "Winter Soldier",
    "Black Widow",
    "White Fox",
    "Peni",
    "Cyclops",
    "Iron Fist",
    "Gambit",
    "Groot",
    "Strange",
    "Storm",
    "Rocket",
    "Namor",
    "Deadpool",
    "Hela",
    "Devil Dino",

]

VALID_HEROES = set(HEROES)

@app.route("/api/schedule", methods=["GET", "POST"])
def schedule_api():
    if request.method == "GET":
        with get_db() as db:
            rows = db.execute("""
                SELECT * FROM schedule_events
                ORDER BY event_date, event_time
            """).fetchall()

        return jsonify([dict(row) for row in rows])

    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    event_type = data.get("event_type", "").strip()
    event_date = data.get("event_date", "")
    event_time = data.get("event_time", "")
    timezone = data.get("timezone", "")
    notes = data.get("notes", "").strip()

    try:
        datetime.strptime(event_date, "%Y-%m-%d")
        datetime.strptime(event_time, "%H:%M")
        duration = int(data.get("duration_minutes", 0))
    except (ValueError, TypeError):
        return jsonify(error="Enter a valid date, time, and duration."), 400

    allowed_types = {
        "Practice", "Scrim", "Tournament", "Match", "Review"
    }
    allowed_zones = {
        "America/Chicago",
        "America/New_York",
        "America/Los_Angeles",
        "America/Denver",
        "America/Phoenix",
        "UTC"
    }

    if not name or len(name) > 100:
        return jsonify(error="Event name must be 1–100 characters."), 400

    if event_type not in allowed_types:
        return jsonify(error="Invalid event type."), 400

    if timezone not in allowed_zones:
        return jsonify(error="Select a valid time zone."), 400

    if duration < 1 or duration > 1440:
        return jsonify(error="Duration must be between 1 minute and 24 hours."), 400

    if len(notes) > 2000:
        return jsonify(error="Notes must be 2,000 characters or fewer."), 400

    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO schedule_events
            (name, event_type, event_date, event_time,
             timezone, duration_minutes, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, event_type, event_date, event_time,
            timezone, duration, notes, session.get("profile_id")
        ))

        event = db.execute(
            "SELECT * FROM schedule_events WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

    return jsonify(dict(event)), 201


@app.route("/api/schedule/<int:event_id>", methods=["PUT", "DELETE"])
def schedule_event_api(event_id):
    with get_db() as db:
        event = db.execute(
            "SELECT * FROM schedule_events WHERE id = ?",
            (event_id,)
        ).fetchone()

        if event is None:
            return jsonify(error="Event not found."), 404

        if request.method == "DELETE":
            db.execute(
                "DELETE FROM schedule_events WHERE id = ?",
                (event_id,)
            )
            return jsonify(success=True)

        data = request.get_json(silent=True) or {}

        name = data.get("name", "").strip()
        event_type = data.get("event_type", "").strip()
        event_date = data.get("event_date", "")
        event_time = data.get("event_time", "")
        timezone = data.get("timezone", "")
        notes = data.get("notes", "").strip()

        try:
            datetime.strptime(event_date, "%Y-%m-%d")
            datetime.strptime(event_time, "%H:%M")
            duration = int(data.get("duration_minutes", 0))
        except (ValueError, TypeError):
            return jsonify(error="Enter a valid date, time, and duration."), 400

        if (
            not name or len(name) > 100
            or event_type not in {"Practice", "Scrim", "Tournament", "Match", "Review"}
            or timezone not in {
                "America/Chicago", "America/New_York",
                "America/Los_Angeles", "America/Denver",
                "America/Phoenix", "UTC"
            }
            or not 1 <= duration <= 1440
            or len(notes) > 2000
        ):
            return jsonify(error="Please check the event details."), 400

        db.execute("""
            UPDATE schedule_events
            SET name = ?, event_type = ?, event_date = ?,
                event_time = ?, timezone = ?,
                duration_minutes = ?, notes = ?
            WHERE id = ?
        """, (
            name, event_type, event_date, event_time,
            timezone, duration, notes, event_id
        ))

        updated = db.execute(
            "SELECT * FROM schedule_events WHERE id = ?",
            (event_id,)
        ).fetchone()

    return jsonify(dict(updated))


@app.route("/api/availability", methods=["GET", "POST"])
def availability_api():
    profile = get_current_profile()

    if profile is None:
        return jsonify(error="Create or sign in to a player profile first."), 401

    if request.method == "GET":
        with get_db() as db:
            rows = db.execute("""
                SELECT a.profile_id, a.availability, a.updated_at,
                       p.username
                FROM player_availability a
                JOIN profiles p ON p.id = a.profile_id
                ORDER BY p.username COLLATE NOCASE
            """).fetchall()

        return jsonify([dict(row) for row in rows])

    data = request.get_json(silent=True) or {}
    availability = data.get("availability", "").strip()

    if len(availability) > 2000:
        return jsonify(error="Availability must be 2,000 characters or fewer."), 400

    with get_db() as db:
        db.execute("""
            INSERT INTO player_availability
                (profile_id, availability, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(profile_id) DO UPDATE SET
                availability = excluded.availability,
                updated_at = CURRENT_TIMESTAMP
        """, (profile["id"], availability))

    return jsonify(success=True)


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
