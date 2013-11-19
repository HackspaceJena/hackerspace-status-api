#!/usr/bin/python

import urllib2
import json
import time
import logging

fileName = "json"
url = "http://status.hackspace-jena.de/status/button/"

data = None
# Raum Status abrufen
try:
	response = urllib2.urlopen(url, None, 8)
except:
	logging.exception("urllib2")
else:
	# Status lessen 
	data = response.read(1)
	try:
		data = int(data)
	except:
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
state["lastchange"] = str(int(time.time()))
# Status setzen
if data and data == 0:
	state["open"] = "close"
elif data and data == 1:
	state["open"] = "open"
else:
	state["open"] = "null"

# JSON Decodieren und ausgeben
print json.dumps(raw)
