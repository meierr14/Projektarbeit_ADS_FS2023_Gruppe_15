# Dieses Python File soll ausgeführt werden, nachdem folgendene Schritte abgeschlossen wurden:
#       1.  Erstellen der Tabellen-Struktur in der DB --> create_tables.py
#       2.  Durchführen des API-Calls und Abspeicherung der Daten in JSON-Files --> football_api   

# Benötigte Imports
import psycopg2
import json


# Funktion, um die Daten über die Mannschaften mittels SQL Abfrage in die DB zu speichern
def table_insert_mannschaften(data_mannschaften):
    insert_query = """
        INSERT INTO bundesliga_mannschaften (team_id, mannschaft)
        SELECT %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM bundesliga_mannschaften WHERE team_id=%s);
    """
    # Abfüllen der Tabelle Mannschaften
    for row in data_mannschaften:
        name = row['teamName']
        id = row['teamId']
        cur.execute(insert_query, (id, name, id))

    conn.commit()

# Funktion, um die Daten über die Punkte und Tore mittels SQL Abfrage in die DB zu speichern
def table_update_mannschaften(data_tabelle):
    for row in data_tabelle:
        id = row['teamInfoId']
        points = row['points']
        goals = row['goals']
        cur.execute(
            f'UPDATE bundesliga_mannschaften SET punkte = {points}, tore = {goals} WHERE team_id = {id}')

    conn.commit()

# Funktion, um die Daten über die einzelnen Spieltage und Tore der Mannschafen mittels SQL Abfrage in die DB zu speichern
def table_insert_result(data_spiele):
    #Vordefinierte Variablen die benötigt werden
    game_nr = 1
    counter = 0
    insert_query = """
        INSERT INTO bundesliga_resultate (match_id, matchday_date, matchday, id_teamh, id_teamg, anzahl_tore, tore_teamh, tore_teamg, winner_team_id)
        SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (SELECT 1 FROM bundesliga_resultate WHERE match_id=%s);
    """
    # For-Schleife, die über alle Daten innerhalb des JSON-Files iteriert
    # Da ein JSON-File wie ein Dictionary aufgebaut ist, kann man mittels der genauen Bezeichnung der exakt benötigte Wert ausgelesen werden (bsp. matchID)
    for row in data_spiele:
        counter += 1
        match_id = row['matchID']
        datum = row['matchDateTime']
        team_heim = row['team1']['teamId']
        team_gast = row['team2']['teamId']
        goals_heim = row['matchResults'][0]['pointsTeam1']
        goals_gast = row['matchResults'][0]['pointsTeam2']
        goals_total = goals_heim + goals_gast

        # Mittels der folgenden If-Schleife soll eine Variable erzeugt werden, die mitgibt welches Team gewonnen hat oder auf 0 gesetzt wird,
        # wenn es sich um ein Unentschieden handelt
        if goals_heim > goals_gast:
            winner_id = team_heim
        elif goals_heim < goals_gast:
            winner_id = team_gast
        else:
            winner_id = 0

        # Ausführen der SQL Abfrage
        cur.execute(insert_query, (match_id, datum, game_nr, team_heim,
                    team_gast, goals_total, goals_heim, goals_gast, winner_id, match_id))
        # Jede Spieltag runde besteht aus 9 Spielen, da dies über die API nicht abgefragt werden kann 
        # wird hier separat gemacht, damit definiert ist, von welcher Spieltagrunde die Daten sind
        if counter == 9:
            counter = 0
            game_nr += 1

    # Speicher der neuen Daten in der DB
    conn.commit()



# Verbindung zur Datenbank aufbauen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

# Cursor erstellen
cur = conn.cursor()

# Öffnen der einzelnen Files und Überführung in eine Variable\Dictionary
with open(f'APIs/JSONData/mannschaften.json', 'r') as file:
    data_mannschaften = json.load(file)

with open(f'APIs/JSONData/tabelle.json', 'r') as file:
    data_tabelle = json.load(file)

with open(f'APIs/JSONData/ganze_saison.json', 'r') as file:
    data_spiele = json.load(file)


# Aufrufen der Funktionen und Übergabe der Dictionaries/JSON-Daten als Input
table_insert_mannschaften(data_mannschaften)
table_update_mannschaften(data_tabelle)
table_insert_result(data_spiele)


# Verbindung schließen
cur.close()
conn.close()
