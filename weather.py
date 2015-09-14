#!/usr/bin/python

################################################################
#
# This project is distributed under the MIT licence, see LICENCE
#
################################################################

import os
import datetime
import time
import random
import sys
from datetime import date

WEATHER_CSV_URL = "http://www.wunderground.com/history/airport/%s/%04d/%02d/%02d/DailyHistory.html?format=1"

if not os.path.exists("weather"):
	raise Exception("weather dir missing")

argc = len(sys.argv)

dateFrom = time.localtime(time.time())
dateTo = time.localtime(time.time())
airport_file = ""
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
	print(airport)

adateFrom = date(dateFrom.tm_year, dateFrom.tm_mon, dateFrom.tm_mday)
adateTo = date(dateTo.tm_year, dateTo.tm_mon, dateTo.tm_mday)

for airportCode in airportCodes:
	print("Beginning scrape of " + airportCode)

	d = adateFrom
	delta = datetime.timedelta(days=1)
	while d <= adateTo:
		print d
		d += delta
