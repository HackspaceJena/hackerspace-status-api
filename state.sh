#!/bin/sh

# Datei zum Zwischenspeichern
STATEFILE="./tmp/last_state"
# Zieldatei, welche aus dem Internet abrufbar ist
DESTINATION="./tmp/json_new"

/usr/bin/python state.py > $STATEFILE
if [ $? -eq 0 ] # ohne Probleme JSON-Datei erstellt
then
# Veröffentliche JSON-Datei
/bin/cp $STATEFILE $DESTINATION
fi
