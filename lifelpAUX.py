import datetime

def turnToInt(string):
	if string[0] == "0":
		string = string[1]
	return int(string)

def isNewWeek(sunday, lastLog):
	if date1GreaterThan2(sunday, lastLog):
		return True
	return False

def date1GreaterThan2(date1, date2):
	if (int(date1[0:4]) > int(date2[0:4])):
		return True
	elif (int(date1[0:4]) == int(date2[0:4])):
		if (turnToInt(date1[5:7]) > turnToInt(date2[5:7])) or (turnToInt(date1[5:7]) >= turnToInt(date2[5:7])) and (turnToInt(date1[8:10]) > turnToInt(date2[8:10])):
			return True
	return False



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
		return str(newYear) + "-" + "01"
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

	
def setDateButtonColor(button, day):
	button.background_color = "white"
	if len(day.tasks):
		good = True
		for task in day.tasks:
			good = good and day.tasks[task].complete
		if good:
			button.background_color = "2ce56d"
		else:
			button.background_color = "red"
	else:
		if day.buttonIndex == 0:
			button.background_color = "2ce56d"