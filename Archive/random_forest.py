import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


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








##### ANPASSUNGEN JOSP ######

# Hyperparameter-Tuning
# Leistung des Modells durch Hyperparameter-Tuning verbessern. 
# Eine gängige Methode dafür ist GridSearchCV in Scikit-Learn, die wir hier verwenden:


###### VERSION 1 ######
param_grid = {
    'n_estimators': [100, 200, 300, 400],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)
print("Best parameters found: ", grid_search.best_params_)

###### VERSION 2 ######
# Das Modell, das wir optimieren wollen
model = RandomForestClassifier(random_state=42)

# Die Hyperparameter, die wir ausprobieren möchten
param_grid = {
    'n_estimators': [100, 200, 300, 500],   # Anzahl der Bäume
    'max_depth': [None, 10, 20, 30],         # Maximale Tiefe der Bäume
    'min_samples_split': [2, 5, 10],         # Minimale Anzahl von Samples, um einen internen Knoten zu teilen
    'min_samples_leaf': [1, 2, 4]            # Minimale Anzahl von Samples, die an einem Blattknoten benötigt werden
}

# Anwendung von GridSearchCV
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train.values.ravel())

# Ausgabe der besten Parameter
print("Best parameters found: ", grid_search.best_params_)

# Trainieren des Modells mit den besten Parametern
best_model = grid_search.best_estimator_

# Modell Evaluation
y_pred_best = best_model.predict(X_test)
accuracy_best = accuracy_score(y_test, y_pred_best)
print(f'Accuracy of best model: {accuracy_best:.2f}')










# Feature Importance

###### VERSION 1 ######
# Feature Importance analysieren, um zu verstehen, welche Merkmale am meisten zur Vorhersage beitragen:
importance = model.feature_importances_
for i, j in enumerate(importance):
    print(X.columns[i], "=", j)


###### VERSION 2 ######
# Erhalte die Wichtigkeit der Merkmale
importances = best_model.feature_importances_

# Sortiere die Merkmale nach ihrer Wichtigkeit
indices = np.argsort(importances)

# Zeichne ein horizontales Balkendiagramm der Feature Importance
plt.figure(figsize=(10, 12))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()



# Model Evaluation

# Nachdem die Vorhersagen gemacht wurden:
y_pred = model.predict(X_test)

# Verwenden der Funktion classification_report, um einen Textbericht über die wichtigsten Klassifikationsmetriken zu erstellen
print(classification_report(y_test, y_pred))

# Verwenden der Funktion confusion_matrix, um eine Konfusionsmatrix zu erstellen
cm = confusion_matrix(y_test, y_pred)

# Anzeigen der Konfusionsmatrix mit Hilfe von Matplotlib
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.show()




# Cross Validation
# Kreuzvalidierung in Scikit-Learn
# Definieren des Modells
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Ausführen einer 5-fache Kreuzvalidierung
scores = cross_val_score(model, X, y, cv=5)

# Durchschnittliche Genauigkeit über alle 5 Folds ausgeben
print("Average cross-validation score: {:.2f}".format(scores.mean()))






# neuronales Netzwerk mit TensorFlow
# Definieren des Modells
model = Sequential()

# Hinzufügen von Schichten
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid')) # Verwenden Sie 'softmax' für mehr als zwei Klassen

# Kompilieren des Modells
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) # Verwenden Sie 'categorical_crossentropy' für mehr als zwei Klassen

# Trainieren des Modells
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))










# Modell Implementierung und Vorhersagen
# Vorhersagen auf den Testdaten durchführen
y_pred = model.predict(X_test)

# Die Genauigkeit des Modells auf den Testdaten ausgeben
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')


# Modellbewertung 
print(classification_report(y_test, y_pred))

conf_matrix = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix: \n{conf_matrix}')



### spekulativ ob nötig: ####


# auf neuen, unbekannten Daten anwenden, um Vorhersagen zu treffen
# Angenommen, new_data ist ein DataFrame, der Ihre neuen Daten enthält
y_new_pred = model.predict(new_data)

# Nehmen wir an, new_data ist Ihr DataFrame mit den Spielen eines bestimmten Spieltags
new_data = pd.read_sql(query_new_data, conn)

# Stellen Sie sicher, dass new_data die gleiche Struktur hat wie die Trainingsdaten (X_train)
new_data_prepared = preprocess_new_data(new_data)  # Hier müssen Sie die geeignete Vorverarbeitung durchführen

# Führen Sie die Vorhersage aus
y_new_pred = model.predict(new_data_prepared)

# Jetzt enthält y_new_pred die vorhergesagten Gewinner für die Spiele in new_data
print(y_new_pred)
