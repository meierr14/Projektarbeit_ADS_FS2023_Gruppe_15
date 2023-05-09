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

# Daten aus DB Tabellen lesen
df_tabelle = pd.read_sql(query_tabelle, conn)
df_resultate = pd.read_sql(query_resultate, conn)
df_shots = pd.read_sql(query_shots_stats, conn)
df_duels = pd.read_sql(query_duel_stats, conn)
df_pass = pd.read_sql(query_pass_stats, conn)

# Zusammenfassen aller Daten in ein einziges DataFrame
merged_df = pd.merge(df_resultate[['matchday', 'id_teamh', 'id_teamg', 'tore_teamh', 'tore_teamg', 'winner_team_id']],
                     df_tabelle, left_on='id_teamh', right_on='team_id')
merged_df = pd.merge(merged_df, df_tabelle, left_on='id_teamg', right_on='team_id', suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_shots, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_shots, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_duels, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_duels, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))
merged_df = pd.merge(merged_df, df_pass, left_on=['id_teamh', 'matchday'], right_on=['team_id', 'matchday'])
merged_df = pd.merge(merged_df, df_pass, left_on=['id_teamg', 'matchday'], right_on=['team_id', 'matchday'], suffixes=('_home', '_guest'))

#3print(merged_df.head())

# Selecting appropriate features for machine learning
X = merged_df[['punkte_home', 'punkte_guest', 'tore_home', 'tore_guest',
               'shots_total_home', 'shots_total_guest', 'duels_total_home', 'duels_total_guest',
               'duels_won_home', 'duels_won_guest', 'pass_complete_home', 'pass_complete_guest',
               'pass_failed_home', 'pass_failed_guest', 'pass_total_home', 'pass_total_guest',
               'pass_percentage_home', 'pass_percentage_guest']]
y = merged_df['winner_team_id']

# Create dummy variables for categorical features
merged_df_dummies = pd.get_dummies(merged_df, columns=['mannschaft_home', 'mannschaft_guest'])

# Drop unnecessary columns
merged_df_dummies.drop(['id_teamh', 'id_teamg', 'matchday', 'team_id_home', 'team_id_guest', 'duels_total_home', 'duels_total_guest'], axis=1, inplace=True)


# Create feature matrix X and target vector y
X = merged_df_dummies.drop(['winner_team_id'], axis=1)
y = merged_df_dummies[['winner_team_id']]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tain model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on test set
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
