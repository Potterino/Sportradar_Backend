import sqlite3
import json
import database_handler

# Establish a connection with sqlite to the database
conn = sqlite3.connect(database_handler.FINAL_PATH)
cursor = conn.cursor()

# Read the JSON file into the database
with open("sportData.json", "r") as file:
    data = json.load(file)

# Insert matches, stages, teams, and results
for match in data["data"]:
    # Insert teams
    home_team = match["homeTeam"]
    away_team = match["awayTeam"]
    if home_team:
        cursor.execute("""
        INSERT OR IGNORE INTO Teams (name, officialName, slug, abbreviation, teamCountryCode)
        VALUES (?, ?, ?, ?, ?)
        """, (home_team["name"], home_team["officialName"], home_team["slug"], home_team["abbreviation"], home_team["teamCountryCode"]))

        # get homeTeamID
        cursor.execute("SELECT id FROM Teams WHERE slug = ?", (home_team["slug"],))
        home_team_id = cursor.fetchone()[0]
    if away_team:
        cursor.execute("""
        INSERT OR IGNORE INTO Teams (name, officialName, slug, abbreviation, teamCountryCode)
        VALUES (?, ?, ?, ?, ?)
        """, (away_team["name"], away_team["officialName"], away_team["slug"], away_team["abbreviation"], away_team["teamCountryCode"]))

        # get awayTeamID
        cursor.execute("SELECT id FROM Teams WHERE slug = ?", (away_team["slug"],))
        away_team_id = cursor.fetchone()[0]

    # Insert stage if it exists
    stage = match.get("stage")
    stage_id = None
    if stage:
        cursor.execute("""
        INSERT OR IGNORE INTO Stages (name, ordering)
        VALUES (?, ?)
        """, (stage["name"], stage["ordering"]))

        cursor.execute("SELECT id FROM Stages WHERE name = ?", (stage["name"],))
        stage_id = cursor.fetchone()[0]

    # Insert result if it exists
    result = match.get("result")
    if result:
        cursor.execute("""
        INSERT OR IGNORE INTO Results (homeGoals, awayGoals, winner, message)
        VALUES (?, ?, ?, ?)
        """, (
             result["homeGoals"], result["awayGoals"], result["winner"], result["message"]
        ))
    else:
        cursor.execute("""
        INSERT OR IGNORE INTO Results (Id)
        VALUES (NULL)
        """)

    # Insert match
    cursor.execute("""
    INSERT OR IGNORE INTO Matches (season, status, timeVenueUTC, dateVenue, stadium, _homeTeamId, _awayTeamId, _stageId, _resultId, originCompetitionId, originCompetitionName)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, LAST_INSERT_ROWID(), ?, ?)
    """, (
        match["season"], match["status"], match["timeVenueUTC"], match["dateVenue"],
        match["stadium"], home_team_id, away_team_id, stage_id,
        match["originCompetitionId"], match["originCompetitionName"]
    ))

# Save changes and close the connection
conn.commit()
conn.close()

print("Import done")
