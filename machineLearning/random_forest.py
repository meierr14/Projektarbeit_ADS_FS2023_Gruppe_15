import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Verbindung zur Datenbank herstellen
conn = psycopg2.connect(
    host="localhost",
    database="PSQL_ADSFS2023Gruppe15",
    user="ADSFS2023Gruppe15",
    password="ADS_FS_2023_G15!?"
)

# SQL Queries für die DB Abfrage
query_tabelle = "SELECT team_id, mannschaft, punkte, tore FROM bundesliga_mannschaften"
query_resultate = "SELECT matchday, id_teamh, id_teamg, tore_teamh, tore_teamg, winner_team_id FROM bundesliga_resultate"
query_shots_stats = "SELECT matchday, team_id, shots_total FROM bundesliga_shots_stats"
query_duel_stats = "SELECT matchday, team_id, duels_total, duels_won FROM bundesliga_duels_stats"
query_pass_stats = "SELECT matchday, team_id, pass_complete, pass_failed, pass_total, pass_percentage FROM bundesliga_pass_stats"
query_corner_stats = "SELECT matchday, team_id, corner_left, corner_right, corner_total FROM bundesliga_corners"
query_distance_stats = "SELECT matchday, team_id, distance_total FROM bundesliga_distance_stats"
query_freekicks_stats = "SELECT matchday, team_id, freekicks_total FROM bundesliga_freekicks"
query_touch_stats = "SELECT matchday, team_id, touches_total FROM bundesliga_touch_stats"

# Daten aus DB Tabellen lesen und in einem Dataframe speichern
df_tabelle = pd.read_sql(query_tabelle, conn)
df_resultate = pd.read_sql(query_resultate, conn)
df_shots = pd.read_sql(query_shots_stats, conn)
df_duels = pd.read_sql(query_duel_stats, conn)
df_pass = pd.read_sql(query_pass_stats, conn)
df_corner = pd.read_sql(query_corner_stats, conn)
df_distance = pd.read_sql(query_distance_stats, conn)
df_freekicks = pd.read_sql(query_freekicks_stats, conn)
df_touch = pd.read_sql(query_touch_stats, conn)


# Zusammenfassen aller Dataframes in ein einziges Dataframe. Dies wird anhand der team_id gemacht, die in jeder Tabelle 
# vorhanden ist und als identifikator alles Teams gilt
merged_df = pd.merge(df_resultate[['matchday', 'id_teamh', 'id_teamg', 'tore_teamh', 'tore_teamg', 'winner_team_id']],
                     df_tabelle, left_on='id_teamh', right_on='team_id')
merged_df = pd.merge(merged_df, df_tabelle, left_on='id_teamg', right_on='team_id', suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_shots, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_shots, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_duels, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_duels, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_pass, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_pass, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_corner, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_corner, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_distance, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_distance, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_freekicks, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_freekicks, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_touch, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_touch, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))

#print(merged_df.head())

# Definition von Merkmalen aus dem Datensetz die für das machinelle lernen benötigt werden
# Die Merkmale dienen als Eingabevariable für das Lernmodell
X = merged_df[['punkte_home', 'punkte_guest', 'tore_home', 'tore_guest',
               'shots_total_home', 'shots_total_guest', 'duels_total_home', 'duels_total_guest',
               'duels_won_home', 'duels_won_guest', 'pass_complete_home', 'pass_complete_guest',
               'pass_failed_home', 'pass_failed_guest', 'pass_total_home', 'pass_total_guest',
               'pass_percentage_home', 'pass_percentage_guest', 'corner_left_home','corner_left_guest',
               'corner_right_home', 'corner_right_guest', 'corner_total_home', 'corner_total_guest',
               'distance_total_home', 'distance_total_guest', 'freekicks_total_home', 'freekicks_total_guest',
               'touches_total_home', 'touches_total_guest']]
# Definition des Merkmals welches als Ausgabevariable
y = merged_df['winner_team_id']

# Erzeugen von neuen Spalten die das Lernmodell benötigt. Für jede neue Kategorie wird hier eine neue Spalte erstellt
# In diesem Fall für jedes Team, welches in der Bundesliga mitmacht wird eine neue Spate erzeugt (1x als Heim und 1x als Gast Mannschaft)
merged_df_dummies = pd.get_dummies(merged_df, columns=['mannschaft_home', 'mannschaft_guest'])

# Durch das zusammenführen der Dataframes in einem vorgehenden Schritt werden einige Spalten doppelt aufgeführt. 
# Da diese unnötig sind werden sie hier entfernt
merged_df_dummies.drop(['id_teamh', 'id_teamg', 'matchday', 'team_id_home', 'team_id_guest', 'duels_total_home', 'duels_total_guest'], axis=1, inplace=True)


# Create feature matrix X and target vector y
X = merged_df_dummies.drop(['winner_team_id'], axis=1)
y = merged_df_dummies[['winner_team_id']]


# Daten werden in Trainings und Test Daten aufgeteilt
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model wird trainiert
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Eine Vorhersage basierend auf den Testdaten machen
y_pred = model.predict(X_test)


# Model performance berechnen
# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
