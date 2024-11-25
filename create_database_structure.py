import sqlite3

# Connect to sqlite main database
conn = sqlite3.connect("main_match_database.db")
cursor = conn.cursor()

# Create tables
# Create Teams table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    officialName TEXT NOT NULL,
    slug TEXT,
    abbreviation TEXT UNIQUE NOT NULL,
    teamCountryCode TEXT NOT NULL,
    stagePosition INTEGER
);
""")

# Create Matches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER,
    status TEXT,
    timeVenueUTC TEXT,
    dateVenue TEXT,
    stadium TEXT,
    _homeTeamId INTEGER,
    _awayTeamId INTEGER,
    _stageId INTEGER,
    _resultId INTEGER,
    originCompetitionId TEXT,
    originCompetitionName TEXT,
    FOREIGN KEY(_resultId) REFERENCES Results(id)
    FOREIGN KEY(_homeTeamId) REFERENCES Teams(id),
    FOREIGN KEY(_awayTeamId) REFERENCES Teams(id),
    FOREIGN KEY(_stageId) REFERENCES Stages(id)
);
""")

# Create Results table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    homeGoals INTEGER,
    awayGoals INTEGER,
    winner TEXT,
    message TEXT
);
""")

# Create Stages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Stages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    ordering INTEGER
);
""")

# Commit changes to databases
conn.commit()



