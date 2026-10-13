
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

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
                # Update this browser's existing profile.
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
                # Create a new profile.
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
    return render_template("team-planner.html")



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


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
