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

