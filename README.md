# Dokumentverwaltungssystem

## Was ist das?
Das System speichert Dokumente in einer Vektordatenbank (und in einem Ordner) und macht sie durchsuchbar mithilfe der Embeddings. Hierbei gibt es auch ein primitives User-System. Jeder neue User erhält einen Token, mithilfe dessen nur die Dokumente, die
von diesem User hinterlegt sind, auch gesucht und zurückgegeben werden.
Es nutzt ChromaDB für Dokumente und SQLite für das User-System als Datenbanken, sowie FastAPI für die REST-Schnittstelle.

## Noch nicht implementiert
- Passwörter werden noch im Klartext in der Datenbank gespeichert. Hashing schafft hier Abhilfe.
- Das User-System ist primitiv und User können noch nicht gelöscht werden. Sicherheitstechnisch empfehle ich, einen offenen Standard wie OAUTH2 zu verwenden.
- Token laufen nicht ab und sind unveränderlich.

## Wie starte ich das Programm?
1. Ein neues Python-Environment erstellen.
2. pip install -r requirements.txt
3. python main.py

Dies setzt die Ordner auf und startet einen lokalen Uvicorn-Server. Der Inhalt der Ordner wird jedes Mal beim letzten Befehl gelöscht (heißt die Datenbanken zurückgesetzt), dies ist durch das manuelle Starten des Uvicorn-Servers über den uvicorn-Befehl vermeidbar.

## Wie nutze ich das Programm?
Eine umfassende Dokumentation der Nutzung aller Endpunkte ist nach dem Starten des Servers unter http://127.0.0.1:8000/docs erhältlich. Hier finden sich auch die respektiven Curl-Befehle. Ich empfehle, hierüber alle Befehle auszuführen ("Try it out" bei jedem Endpunkt).
Das User-System funktioniert wie folgt:
1. Einen Nutzer unter POST /api/users erstellen (username und password Parameter im Body)
2. Den Nutzer unter PUT /api/users einloggen (username und password Parameter im Body)
3. Der letzte Befehl gibt einen Token zurück, der bei den Dokumentbefehlen als URL-Parameter angegeben wird (Sicherheitstechnisch nicht für die Produktion geeignet, siehe oben.)

