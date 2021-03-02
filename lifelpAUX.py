def changeMonth(date, incr):
	date = str(date)
	year = int(date[0:4])
	day = int(date[8:10])
	if date[5] == "0":
		num = int(date[6])
	else:
		num = int(date[5:7])
	num = num + incr
	if num > 9:
		if num > 12:
			num = num - 12
			year+=1
		else:
			num = str(num)		
	elif num < 1:
		num = 12 + num
		year-=1
			
	date = datetime.date(year, num, day)
	return date

def readyBank(bank):
	for x in bank:
		if x[0] == "&":
			temp = x[1:len(x)]
			bank[temp] = bank[x]
			del bank[x]

def findTodayIndex(today):
	month = today[0:7]
	todayIndex = 0
	for x in data[month]:
		if x == today:
			return todayIndex
		todayIndex+=1