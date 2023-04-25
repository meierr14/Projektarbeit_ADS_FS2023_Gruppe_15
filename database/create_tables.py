import psycopg2
import tabel_definitions
import json

#############################################################
#                                                           #
#     Only run this file once, else you will find double    #
#     entries in the DB                                     #
#                                                           #
#############################################################


def create_tables():
    # Erstellen der Tabellen
    cur.execute(tabel_definitions.create_table_mannschaften)
    cur.execute(tabel_definitions.create_table_resultate)
    conn.commit()


def table_insert_mannschaften(data_mannschaften):
    # Abafüllen der Tabelle Mannschaften
    for row in data_mannschaften:
        name = row['teamName']
        id = row['teamId']
        cur.execute("INSERT INTO mannschaften (mannschaft, id) VALUES (%s, %s)", (name, id))

    conn.commit()


def table_update_mannschaften(data_tabelle):
    for row in data_tabelle:
        id = row['teamInfoId']
        points = row['points']
        goals = row['goals']
        cur.execute(f'UPDATE mannschaften SET punkte = {points}, tore = {goals} WHERE id = {id}')
        
    conn.commit()


def table_insert_result(data_spiele):
    for row in data_spiele:
        datum = row['matchDateTime']
        team_heim = row['team1']['teamId']
        team_gast = row['team2']['teamId']
        goals_heim = row['matchResults'][0]['pointsTeam1']
        goals_gast = row['matchResults'][0]['pointsTeam2']
        goals_total = goals_heim + goals_gast
        cur.execute("INSERT INTO resultate (spieltag_datum, id_teamh, id_teamg, anzahl_tore, tore_teamh, tore_teamg) VALUES (%s, %s, %s, %s, %s, %s)", (datum, team_heim, team_gast, goals_total, goals_heim, goals_gast))    
    
    conn.commit()


# Wird für test verwendet
select_query = "SELECT * FROM Mannschaften;"

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



create_tables()
table_insert_mannschaften(data_mannschaften)
table_update_mannschaften(data_tabelle)
table_insert_result(data_spiele)


#Verbindung schließen
cur.close()
conn.close()