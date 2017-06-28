import threading
import os, errno
import datetime
import time
import random
import sys
import csv
import urllib.request
from datetime import date

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

def worker(n,lock):	
	while len(airportCodes) > 0:
		code = airportCodes.pop(-1)

		print (str(n+1) + ': Starting on ' + code)

		d = adateFrom
		delta = datetime.timedelta(days=1)
		while d <= adateTo:
			url = "http://www.wunderground.com/history/airport/" + code  + "/" + str(d.year)  + "/" + str(d.month) + "/" + str(d.day) + "/DailyHistory.html?format=1"
			outputFolder = "weather/" + code
			outputFile = outputFolder + "/" + str(d.year)  + "-" + str(d.month) + "-" + str(d.day) + ".csv"
			print(str(n+1) + ": Fetching " + url)

			mkdir_p(outputFolder)

			response = urllib.request.urlopen(url)
			csv = response.read().decode(response.headers.get_content_charset())

			csv = csv.replace("<br />", "")
			
			f = open(outputFile, 'w')
			f.write(csv)
			f.close()

			d += delta

if not os.path.exists("weather"):
	mkdir_p("weather")

argc = len(sys.argv)

dateFrom = time.localtime(time.time())
dateTo = time.localtime(time.time())
airport_file = ""
airportCodes = []
threadCount = 4
requestData = []

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
	elif sys.argv[x] == "-threads":
		threadCount = int(sys.argv[x+1])

if os.path.exists(airport_file):
	with open(airport_file, 'r') as csvfile:
		airport_file_data = csv.reader(csvfile)
		for row in airport_file_data:
			airportCodes.append(''.join(row))

adateFrom = date(dateFrom.tm_year, dateFrom.tm_mon, dateFrom.tm_mday)
adateTo = date(dateTo.tm_year, dateTo.tm_mon, dateTo.tm_mday)

if threadCount < 1:
	threadCount = 1

print(str(threadCount) + " threads")

lock = threading.Lock()
threads = []
for i in range(threadCount):
	t = threading.Thread(target=worker,args=(i,lock,))
	threads.append(t)
	t.start()
