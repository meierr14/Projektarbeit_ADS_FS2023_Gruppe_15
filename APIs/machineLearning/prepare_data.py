import psycopg2
import pandas as pd

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

query_tabelle = "SELECT team_id, mannschaft, punkte, tore FROM bundesliga_mannschaften"
query_resultate = "SELECT matchday, id_teamh, id_teamg, tore_teamh, tore_teamg FROM bundesliga_resultate"
query_shots_stats = "SELECT matchday, team_id, shots_total FROM bundesliga_shots_stats"
query_duel_stats = "SELECT matchday, team_id, duels_total, duels_won FROM bundesliga_duels_stats"
query_pass_stats = "SELECT matchday, team_id, pass_complete, pass_failed, pass_total, pass_percentage FROM bundesliga_pass_stats"

df_tabelle = pd.read_sql(query_tabelle, conn)
df_resultate = pd.read_sql(query_resultate, conn)
df_shots = pd.read_sql(query_shots_stats, conn)
df_duels = pd.read_sql(query_duel_stats, conn)
df_pass = pd.read_sql(query_pass_stats, conn)

merged_df = pd.merge(df_resultate, df_tabelle, left_on='id_teamh', right_on='team_id')
merged_df = pd.merge(merged_df, df_tabelle, left_on='id_teamg', right_on='team_id', suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_shots, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_shots, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_duels, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_duels, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_pass, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_pass, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))



print(merged_df.head())

