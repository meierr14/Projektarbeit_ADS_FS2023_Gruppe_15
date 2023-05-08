import psycopg2
import pandas as pd

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

query_tabelle = "SELECT mannschaft, punkte, tore, rang FROM bundesliga_mannschaften"
query_resultate = "SELECT spieltag, id_teamh, id_teamg, tore_teamh, tore_teamg FROM bundesliga_resultate"
query_shots_stats = "SELECT matchday, team_id, value FROM bundesliga_shots_stats"
query_duel_stats = "SELECT matchday, team_id, value FROM bundesliga_duels_stats"
query_pass_stats = "SELECT matchday, team_id, pass_percentage FROM bundesliga_pass_stats"

df_tabelle = pd.read_sql(query_tabelle, conn)
df_resultate = pd.read_sql(query_resultate, conn)
df_shots = pd.read_sql(query_shots_stats, conn)
df_duels = pd.read_sql(query_duel_stats, conn)
df_pass = pd.read_sql(query_pass_stats, conn)

print(df_duels.head())