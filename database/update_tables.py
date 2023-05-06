import psycopg2
import json


def table_insert_mannschaften(data_mannschaften):
    insert_query = """
        INSERT INTO bundesliga_mannschaften (team_id, mannschaft) 
        SELECT %s, %s 
        WHERE NOT EXISTS (SELECT 1 FROM bundesliga_mannschaften WHERE team_id=%s);
    """
    # Abafüllen der Tabelle Mannschaften
    for row in data_mannschaften:
        name = row['teamName']
        id = row['teamId']
        cur.execute(insert_query, (id, name, id))

    conn.commit()


def table_update_mannschaften(data_tabelle):
    for row in data_tabelle:
        id = row['teamInfoId']
        points = row['points']
        goals = row['goals']
        cur.execute(f'UPDATE bundesliga_mannschaften SET punkte = {points}, tore = {goals} WHERE team_id = {id}')
        
    conn.commit()


def table_insert_result(data_spiele):
    insert_query = """
        INSERT INTO bundesliga_resultate (id, spieltag_datum, id_teamh, id_teamg, anzahl_tore, tore_teamh, tore_teamg) 
        SELECT %s, %s, %s, %s, %s, %s, %s 
        WHERE NOT EXISTS (SELECT 1 FROM bundesliga_resultate WHERE id=%s);
    """
    for row in data_spiele:
        match_id = row['matchID']
        datum = row['matchDateTime']
        team_heim = row['team1']['teamId']
        team_gast = row['team2']['teamId']
        goals_heim = row['matchResults'][0]['pointsTeam1']
        goals_gast = row['matchResults'][0]['pointsTeam2']
        goals_total = goals_heim + goals_gast
        cur.execute(insert_query, (match_id, datum, team_heim, team_gast, goals_total, goals_heim, goals_gast, match_id))  
    
    conn.commit()


# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

# Cursor erstellen
cur = conn.cursor()

with open('APIs/JSONData/mannschaften.json', 'r') as file:
    data_mannschaften = json.load(file)

with open('APIs/JSONData/tabelle.json', 'r') as file:
    data_tabelle = json.load(file)

with open('APIs/JSONData/ganze_saison.json', 'r') as file:
    data_spiele = json.load(file)



table_insert_mannschaften(data_mannschaften)
table_update_mannschaften(data_tabelle)
table_insert_result(data_spiele)


#Verbindung schließen
cur.close()
conn.close()