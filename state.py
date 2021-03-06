#!/usr/bin/python

import urllib2
import json
import time
import logging

fileName = "json"
url = "http://status.krautspace.de/status/button/"

data = None
# Raum Status abrufen
try:
	response = urllib2.urlopen(url, None, 8)
except:
	logging.exception("urllib2")
else:
	# Status lessen 
	data = response.read(1)
	# Data validieren
	if len(data) != 1 or data not in ("0", "1"):
		logging.exception("ungueltigen Zustand gelesen")
		data = None

# JSON Vorlage einlesen
try:
	fp = file(fileName)
	raw = json.load(fp)
	fp.close()
except:
	logging.exception("file")
	exit(1)

# Bereich in dem der Status steht
state = raw["state"]
# letzte Verarbeitungszeit setzen
state["lastchange"] = int(time.time())
# Status setzen
if data:
	if data == "0":
		state["open"] = False
		state["message"] = "no human being on location"
	else:
		state["open"] = True
		state["message"] = "open for public"
else:
	state["open"] = None
	state["message"] = "open for public"

# JSON Decodieren und ausgeben
print json.dumps(raw)
