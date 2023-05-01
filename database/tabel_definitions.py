create_table_resultate = """
    CREATE TABLE IF NOT EXISTS bundesliga_resultate(
        Match_ID INTEGER PRIMARY KEY,
        Spieltag_Datum DATE,
        ID_TeamH INTEGER,
        ID_TeamG INTEGER,
        Anzahl_Tore INTEGER,
        Anzahl_Schuesse INTEGER,
        Ballbesitz_TeamH REAL,
        Ballbesitz_TeamG REAL,
        Anzahl_SchuesseH INTEGER,
        Anzahl_SchuesseG INTEGER,    
        Tore_TeamH INTEGER,
        Tore_TeamG INTEGER,
        Fouls_TeamH INTEGER,
        Fouls_TeamG INTEGER,
        Ecken_TeamH INTEGER,
        Ecken_TeamG INTEGER,
        Offsides_TeamH INTEGER,
        Offsides_TeamG INTEGER
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
        team_name TEXT NOT NULL,
        pass_percentage NUMERIC NOT NULL
    );
"""

create_table_tore_schuesse = '''
    CREATE TABLE IF NOT EXISTS bundesliga_shots_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_name TEXT NOT NULL,
        value NUMERIC NOT NULL
    );
'''

create_table_zweikaempfe = '''
    CREATE TABLE IF NOT EXISTS bundesliga_duels_stats (
        id SERIAL PRIMARY KEY,
        matchday INTEGER NOT NULL,
        team_name TEXT NOT NULL,
        value NUMERIC NOT NULL
    );
'''