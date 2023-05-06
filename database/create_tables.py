import psycopg2
import tabel_definitions

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

# Cursor erstellen
cur = conn.cursor()


cur.execute(tabel_definitions.create_table_mannschaften)
cur.execute(tabel_definitions.create_table_resultate)
cur.execute(tabel_definitions.create_table_pass_stats)
cur.execute(tabel_definitions.create_table_tore_schuesse)
cur.execute(tabel_definitions.create_table_zweikaempfe)

# Änderungen in der DB speichern
conn.commit()

#Verbindung schließen
cur.close()
conn.close()
