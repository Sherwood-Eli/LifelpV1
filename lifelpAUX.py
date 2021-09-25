import datetime

def changeMonth(date, incr):
	date = str(date)
	year = int(date[0:4])
	day = int(date[8:10])
	if date[5] == "0":
		month = int(date[6])
	else:
		month = int(date[5:7])
	month = month + incr
	if month > 9:
		if month > 12:
			month = month - 12
			year+=1
	elif month < 1:
		month = 12 + month
		year-=1
			
	date = datetime.date(year, month, 1)
	return date

def getFirstOfMonth(fileKey):
	year = int(fileKey[0:4])
	if fileKey[5] == "0":
		month = int(fileKey[6])
	else:
		month = int(fileKey[5:7])
	return datetime.datetime(year, month, 1)

def decrFileKey(key):
	if key[5] == "0":
		temp = int(key[6])
	else:
		temp = int(key[5:7])
	temp-=1
	if temp < 1:
		newYear = int(key[0:4])
		newYear-=1
		return str(newYear) + "-" + "12"
	elif temp < 10:
		return key[0:5] + "0" + str(temp)
	else:
		return key[0:5] + str(temp)
		
def incrFileKey(key):
	if key[5] == "0":
		temp = int(key[6])
	else:
		temp = int(key[5:7])
	temp+=1
	if temp > 12:
		newYear = int(key[0:4])
		newYear+=1
		return str(newYear) + "-" + "12"
	elif temp < 10:
		return key[0:5] + "0" + str(temp)
	else:
		return key[0:5] + str(temp)

def findTodayIndex(today, data):
	month = today[0:7]
	todayIndex = 0
	for x in data[month].days:
		if x == today:
			return todayIndex
		todayIndex+=1

	
