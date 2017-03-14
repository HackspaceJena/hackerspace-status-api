#!/usr/bin/python

import urllib2
import json
import time
import logging

fileName = "json"
url = "http://status.krautspace.de/status/button/"
laststateFile = 'lastState.txt'

data = None
# Raum Status abrufen
try:
	response = urllib2.urlopen(url, None, 8)
except:
	logging.exception("urllib2")
else:
	# Status lesen
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

try:
	fp = file(laststateFile)
	lastState, oldTimestamp = fp.readline().split()
	fp.close()
except:
	logging.exception("file")
	exit(1)

# Status setzen
if data:
	if lastState != data:
		currentTimestamp = int(time.time())
		if data == "0":
			state["lastchange"] = currentTimestamp
			state["open"] = False
			state["message"] = "no human being on location"
		else:
			state["lastchange"] = currentTimestamp
			state["open"] = True
			state["message"] = "open for public"
		try:
			fp = open( laststateFile, 'w' )
			fp.write(data + ' ' + str(currentTimestamp))
			fp.close()
		except:
			logging.exception("file")
			exit(1)
	else:
		state["lastchange"] = oldTimestamp
else:
	state["open"] = None
	state["message"] = "open for public"
	state["lastchange"] = oldTimestamp

# JSON Decodieren und ausgeben
print json.dumps(raw)
