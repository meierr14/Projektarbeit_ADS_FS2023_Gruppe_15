create_table_resultat = """
    Spieltag_Datum DATE,
    ID_TeamH INTEGER,
    ID_TeamG INTEGER,
    Anzahl_Tore INTEGER,
    Anzahl_Schuesse INTEGER,
    Ballbesitz_TeamH REAL,
    Ballbesitz_TeamG REAL,
    Anzahl_SchuesseH INTEGER,
    Anzahl_SchuesseG INTEGER,    
    Tore_TeamH INTEGER,
    Tore_TeamG INTEGER,
    Fouls_TeamH INTEGER,
    Fouls_TeamG INTEGER,
    Ecken_TeamH INTEGER,
    Ecken_TeamG INTEGER,
    Offsides_TeamH INTEGER,
    Offsides_TeamG INTEGER
"""

create_table_mannschaften = """
    Mannschaft VARCHAR(255),
    ID INTEGER,
    Punkte INTEGER,
    Tore INTEGER,
    Rang INTEGER
"""