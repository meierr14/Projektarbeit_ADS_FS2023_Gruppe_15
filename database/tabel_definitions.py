create_table_resultate = """
    CREATE TABLE IF NOT EXISTS bundesliga_resultate(
        Match_ID INTEGER PRIMARY KEY,
        matchday_date DATE,
        matchday INTEGER,
        ID_TeamH INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        ID_TeamG INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        Anzahl_Tore INTEGER,   
        Tore_TeamH INTEGER,
        Tore_TeamG INTEGER,
        Winner_team_id INTEGER
    );
"""

create_table_mannschaften = """
    CREATE TABLE IF NOT EXISTS bundesliga_mannschaften(
        Team_ID INTEGER PRIMARY KEY,
        Mannschaft VARCHAR(255),
        Punkte INTEGER,
        Tore INTEGER,
        Rang INTEGER
    );
"""

create_table_pass_stats = """
    CREATE TABLE IF NOT EXISTS bundesliga_pass_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        pass_complete INTEGER NOT NULL,
        pass_failed INTEGER NOT NULL,
        pass_total INTEGER NOT NULL,
        pass_percentage NUMERIC NOT NULL
    );
"""

create_table_tore_schuesse = '''
    CREATE TABLE IF NOT EXISTS bundesliga_shots_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        shots_total INTEGER NOT NULL
    );
'''

create_table_zweikaempfe = '''
    CREATE TABLE IF NOT EXISTS bundesliga_duels_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        duels_total INTEGER NOT NULL,
        duels_won INTEGER NOT NULL
    );
'''

create_table_ballkontrolle = '''
    CREATE TABLE IF NOT EXISTS bundesliga_touch_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        touches_total INTEGER NOT NULL
    );
'''

create_table_laufleistung = '''
    CREATE TABLE IF NOT EXISTS bundesliga_distance_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
       distance_total NUMERIC NOT NULL
    );
'''

create_table_freekicks = '''
    CREATE TABLE IF NOT EXISTS bundesliga_freekicks (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        freekicks_total INTEGER NOT NULL
    );
'''

create_table_corners = '''
    CREATE TABLE IF NOT EXISTS bundesliga_corners (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_id INT REFERENCES bundesliga_mannschaften(Team_ID) ON DELETE CASCADE,
        corner_left INTEGER NOT NULL,
        corner_right INTEGER NOT NULL,
        corner_total INTEGER NOT NULL
    );
'''