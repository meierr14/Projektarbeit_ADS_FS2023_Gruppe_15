# Benötigte imports
import psycopg2
import table_definitions

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

# Cursor erstellen
cur = conn.cursor()

# Druchführen der einzelnen SQL Abfragen, die in tabel_defintions.py vorbereitet wurden
cur.execute(table_definitions.create_table_mannschaften)
cur.execute(table_definitions.create_table_resultate)
cur.execute(table_definitions.create_table_pass_stats)
cur.execute(table_definitions.create_table_tore_schuesse)
cur.execute(table_definitions.create_table_zweikaempfe)
cur.execute(table_definitions.create_table_ballkontrolle)
cur.execute(table_definitions.create_table_laufleistung)
cur.execute(table_definitions.create_table_freekicks)
cur.execute(table_definitions.create_table_corners)

# Änderungen in der DB speichern
conn.commit()

#Verbindung schließen
cur.close()
conn.close()

