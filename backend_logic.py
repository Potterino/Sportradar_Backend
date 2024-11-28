from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import database_handler


app = Flask(__name__, template_folder=database_handler.PROJECT_PATH)


def fetch_data(filters=None):
    """Fetches data from the database based on a query and optional filters."""
    query = """
        SELECT Matches.season, Matches.status, Matches.dateVenue, Matches.timeVenueUTC, 
		    home_teams.name AS home_team_name, 
		    away_teams.name AS away_team_name, 
		    result_home_goals.homeGoals AS home_goals_result,
		    result_away_goals.awayGoals AS away_goals_result,
		    result_winner.winner AS winner
        FROM Matches
        JOIN Teams AS home_teams ON Matches._homeTeamId = home_teams.id
        JOIN Teams AS away_teams ON Matches._awayTeamId = away_teams.id
        JOIN Results AS result_home_goals ON Matches._resultId = result_home_goals.id
        JOIN Results AS result_away_goals ON Matches._resultId = result_away_goals.id
        JOIN Results AS result_winner ON Matches._resultId = result_winner.id
    """
    conditions = []
    params = []

    # Add filter condition
    if filters:
        if filters.get("season"):
            conditions.append("Matches.season = ?")
            params.append(filters["season"])
        if filters.get("status"):
            conditions.append("Matches.status = ?")
            params.append(filters["status"])
        if filters.get("team_name"):
            conditions.append("(home_teams.name = ? OR away_teams.name = ?)")
            params.extend([filters["team_name"], filters["team_name"]])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Show the next event on top
    query += " ORDER BY Matches.dateVenue"

    # Fetch data from the database
    conn = sqlite3.connect(database_handler.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data


def get_teams():
    """Fetches all the team names from the database"""
    conn = sqlite3.connect(database_handler.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Teams ORDER BY name")
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teams


def add_event(home_team, away_team, date_venue, time_venue, season, stadium=None, originCompetitionId=None, originCompetitionName=None):
    """Adds a new event to the database."""
    conn = sqlite3.connect(database_handler.DATABASE_NAME)
    cursor = conn.cursor()

    # Fetch or create Team IDs
    cursor.execute("SELECT id FROM Teams WHERE name = ?", (home_team,))
    home_team_id = cursor.fetchone()
    if not home_team_id:
        cursor.execute("INSERT INTO Teams (name) VALUES (?)", (home_team,))
        home_team_id = cursor.lastrowid
    else:
        home_team_id = home_team_id[0]

    cursor.execute("SELECT id FROM Teams WHERE name = ?", (away_team,))
    away_team_id = cursor.fetchone()
    if not away_team_id:
        cursor.execute("INSERT INTO Teams (name) VALUES (?)", (away_team,))
        away_team_id = cursor.lastrowid
    else:
        away_team_id = away_team_id[0]

    # Insert default result into Results table
    cursor.execute("""
        INSERT INTO Results (homeGoals, awayGoals, winner) 
        VALUES (?, ?, ?)
    """, (0, 0, None))  # Default result: 0-0, no winner
    result_id = cursor.lastrowid

    # Check if season has a value. If not, use the current year
    if season == "":
        season = 2024

    # Insert new match into Matches table
    cursor.execute("""
        INSERT INTO Matches (season, status, timeVenueUTC, dateVenue, _homeTeamId, _awayTeamId, stadium, originCompetitionId, originCompetitionName, _resultId) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (season, "scheduled", time_venue, date_venue, home_team_id, away_team_id, stadium, originCompetitionId, originCompetitionName, result_id))

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    # Applying filters to the form
    season = request.form.get("season", "")
    status = request.form.get("status", "")
    team_name = request.form.get("team_name", "")

    # Fetch data
    filters = {
        "season": season if season else None,
        "status": status if status else None,
        "team_name": team_name if team_name else None
    }
    matches = fetch_data(filters)
    teams = get_teams()

    # Render HTML page
    return render_template("index.html", matches=matches, filters=filters, teams=teams)


@app.route("/add-event", methods=["POST"])
def add_event_route():
    # Fetches the inserted data from the index page
    home_team = request.form["home_team_name_add"]
    away_team = request.form["away_team_name_add"]
    date_venue = request.form["date_venue"]
    time_venue = request.form["time_venue"]
    season = request.form.get("season_add", None)
    stadium = request.form.get("stadium", None)
    originCompetitionId = request.form.get("originCompetitionId", None)
    originCompetitionName = request.form.get("originCompetitionName", None)

    # Adds the event into the database
    add_event(home_team, away_team, date_venue, time_venue, season, stadium, originCompetitionId, originCompetitionName)

    # redirect back to/refresh the current page
    return redirect(url_for("index"))


app.run(debug=True)
