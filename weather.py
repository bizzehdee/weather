#!/usr/bin/python

################################################################
#
# This project is distributed under the MIT licence, see LICENCE
#
################################################################

import os, errno
import datetime
import time
import random
import sys
import urllib2
from datetime import date

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise



if not os.path.exists("weather"):
	raise Exception("weather dir missing")

argc = len(sys.argv)

dateFrom = time.localtime(time.time())
dateTo = time.localtime(time.time())
airport_file = "airports.txt"
airportCodes = []

for x in range(0, argc):
	if sys.argv[x] == "-from":
		dateFromStr = sys.argv[x+1]
		dateFrom = time.strptime(dateFromStr, "%Y-%m-%d")
	elif sys.argv[x] == "-to":
		dateToStr = sys.argv[x+1]
		dateTo = time.strptime(dateToStr, "%Y-%m-%d")
	elif sys.argv[x] == "-airport_file":
		airport_file = sys.argv[x+1]
	elif sys.argv[x] == "-airport":
		airportCodes.append(sys.argv[x+1])

if os.path.exists(airport_file):
	#airports file should be a plain txt file with 1 airport code per line only
	airportCodes = [line.rstrip('\n') for line in open(airport_file)]

adateFrom = date(dateFrom.tm_year, dateFrom.tm_mon, dateFrom.tm_mday)
adateTo = date(dateTo.tm_year, dateTo.tm_mon, dateTo.tm_mday)

for airportCode in airportCodes:
	print("Beginning scrape of " + airportCode)

	d = adateFrom
	delta = datetime.timedelta(days=1)
	while d <= adateTo:

		url = "http://www.wunderground.com/history/airport/" + airportCode  + "/" + str(d.year)  + "/" + str(d.month) + "/" + str(d.day) + "/DailyHistory.html?format=1"
		outputFolder = "weather/" + airportCode
		outputFile = outputFolder + "/" + str(d.year)  + "-" + str(d.month) + "-" + str(d.day) + ".csv"
		print("Writing to " + outputFile)

		mkdir_p(outputFolder)
		
		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 'Prefs=SHOWMETAR:1'))
		response = opener.open(url)
		csv = response.read()
		csv = csv.replace("<br />", "")
		
		f = open(outputFile, 'w')
		f.write(csv)
		f.close()
		
		d += delta

