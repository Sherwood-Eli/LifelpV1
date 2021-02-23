
import ui
import datetime
import time


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
		

def loadData(fileName):
	fileName += "-data.txt"
	fileName = "lifelp/" + fileName
	with open(fileName,"r") as file:
		data = {}
		for line in file:
			x = 0
			key = ""
			task = ""
			while line[x] != "{":
				key += line[x]
				x+=1
			data[key] = {}
			x+=1
			while line[x] != "}":
				task = ""
				while line[x] != ":":
					task += line[x]
					x+=1
				x+=1
				if line[x] == "t":
					data[key][task] = True
				elif line[x] == "f":
					data[key][task] = False
				else:
					data[key] = task
				x+=1
	return data
	
def getData(today):
	output = {}
	outputKeys = {}
	temp = changeMonth(today, -1)
	temp = str(temp)
	temp = temp[0:7]
	output[temp] = loadData(temp)
	outputKeys[temp] = list((output[temp]).keys())
	temp = str(today)
	temp = temp[0:7]
	output[temp] = loadData(temp)
	outputKeys[temp] = list((output[temp]).keys())
	temp = changeMonth(today, 1)
	temp = str(temp)
	temp = temp[0:7]
	output[temp] = loadData(temp)
	outputKeys[temp] = list((output[temp]).keys())
	return output, outputKeys
	
def loadPresets():
	with open("lifelp/presets.txt", "r") as file:
		presets = {}
		for line in file:
			if len(line) > 3:
				x = 0
				key = ""
				while line[x] != ":":
					key+=line[x]
					x+=1
				x+=1
				value = []
				while line[x] != "}":
					temp = ""
					while line[x] != ",":
						temp+=line[x]
						x+=1
					value.append(temp)
					x+=1
				presets[key] = value
	return presets

def saveBank():
	global bank
	bankKeys = list(bank.keys())
	with open("lifelp/bank.txt", "w") as file:
		file.write(bankKeys[0])
		file.write(":,}")
		x = 1
		while x < len(bankKeys):
			temp = bankKeys[x]
			file.write("\n")
			file.write(temp)
			file.write(":")
			for y in bank[temp]:
				file.write(y)
				file.write(",")
			file.write("}")
			x+=1
				

def checkIncomplete(today):
	global bank
	global data
	global bankKeys
	yesterday = str(today - datetime.timedelta(days=1))
	month = yesterday[5:7]
	temp = data[month][yesterday]
	for x in temp:
		if temp[x]:
			if x in bank:
				for y in bank[x]:
					newKey = x + " " + yesterday
					data[y][newKey] = data[y][x]
					del data[month][y][x]
				del bank[x]
		else:
			if x in bank:
				bank[x].append(yesterday)
			else:
				bankKeys.append(x)
				bank[x] = [yesterday]
	bankKeys[0] = str(today)
	saveBank()
	
def readyBank():
	global bank
	for x in bank:
		if x[0] == "&":
			temp = x[1:len(x)]
			bank[temp] = bank[x]
			del bank[x]
	

def loadBank():
	bankKeys = []
	bank = {}
	with open("lifelp/bank.txt") as file:
		for line in file:
			task = ""
			x=0
			while (line[x] != ":"):
				task += line[x]
				x+=1
			bankKeys.append(task)
			bank[task] = []
			x+=1
			while (line[x] != "}"):
				num = ""
				while (line[x] != ","):
					num += line[x]
					x+=1
				bank[task].append(num)
				x+=1
	return bank, bankKeys
				
	

def saveData(month):
	global data
	fileName = "lifelp/" + month + "-data.txt"
	with open(fileName, "w") as file:
		for x in data[month]:
			file.write(x)
			temp = data[month][x]
			file.write("{")
			for y in temp:
				file.write(y)
				file.write(":")
				if type(temp) == dict:
					if temp[y] == True:
						file.write("t")
					elif temp[y] == False:
						file.write("f")
				else:
					file.write("n")
			file.write("}\n")
		

def saveTask(textfield):
	global tTask
	global numTasks
	global data
	global current
	view2.remove_subview(tTask)
	if textfield.text != "":
		month = current.title[0:7]
		temp = data[month][current.title]
		temp[textfield.text] = False
		saveData(month)
		h = -5 + (44*numTasks)
		button = ui.Button(title = str(numTasks))
		button.center = (25.5, h)
		button.background_color = "red"
		button.flex = "LRTB"
		button.action = taskButton
		label = ui.Label()
		label.text = textfield.text
		label.center = (125, h)
		label.flex = "w"
		view2.add_subview(button)
		view2.add_subview(label)
		textfield.text = ""
		numTasks+=1
		current.background_color = "red"

	

def changeButtons(sender):
	global buttons
	global sundayIndex
	global data
	global dataKeys
	global view1
	today = str(datetime.date.today())
	key = today[0:7]
	if sender.title == "prev":
		sundayIndex-=7
	else:
		sundayIndex+=7
	for x in range(0, len(buttons)):
		button = buttons[x]
		button.title = dataKeys[key][sundayIndex + x]
		setDateButtonColor(button, data[key][button.title])

def getMonth(today):
	return(today[5:7])

#junk func
def findSunday(today):
	global dataKeys
	global dataIndex
	temp = today[0:7]
	tempKeys = dataKeys[temp]
	for x in range(0,len(tempKeys)):
		if today == tempKeys[x]:
			dataIndex = x
			temp = x - 3
			for y in range(0,7):
				if ((temp - y)%7) == 0:
					return (x-y)

def findTodayIndex(today):
	month = today[0:7]
	todayIndex = 0
	for x in data[month]:
		if x == today:
			return todayIndex
		todayIndex+=1
		
def taskButton(sender):
	global current
	global data
	global bank
	month = current.title[0:7]
	temp = data[month][current.title]
	keys = list(temp.keys())
	index = int(sender.title) - 1
	task = keys[index]
	bankKey = "&" + task
	tMonths = []
	tMonths.append(month)
	if (sender.background_color == (1.0, 0.0, 0.0, 1.0)):
		sender.background_color = "#2ce56d"
		temp[task] = True
		if bankKey in bank:
			for x in bank[bankKey]:
				tMonth = x[0:7]
				if tMonth not in tMonths:
					tMonths.append(tMonth)
				data[tMonth][x][task] = True
	else:
		sender.background_color = "red"
		temp[task] = False
		if bankKey in bank:
			for x in bank[bankKey]:
				tMonth = x[0:7]
				if tMonth not in tMonths:
					tMonths.append(tMonth)
				data[tMonth][x][task] = False
	setDateButtonColor(current, temp)
	for x in tMonths:
		saveData(x)

def setDateButtonColor(button, tasks):
	button.background_color = "white"
	if len(tasks):
		good = True
		for x in tasks:
			good = good and tasks[x]
		if good:
			button.background_color = "2ce56d"
		else:
			button.background_color = "red"
	
def addTask(sender):
	global tTask
	view2.add_subview(tTask)
	
def dateButton(sender):
	global view2
	global data
	global current
	global numTasks
	global fromBankInfo
	month = sender.title[0:7]
	if fromBankInfo == "":
		current = sender
		curTitle = current.title
		numTasks = 1
		view2 = ui.View()
		view2.background_color = "#f0fff5"
		hb = 13
		hl = -5
		temp = data[month][curTitle]
		for x in temp:
			hb += (4)
			hl += (44)
			button = ui.Button(title = str(numTasks))
			button.center = (17, hb)
			if temp[x]:
				button.background_color = "#2ce56d"
			else:
				button.background_color = "red"
			button.flex = "LRTB"
			button.action = taskButton
			label = ui.Label()
			label.text = x
			label.center = (125, hl)
			label.flex = "w"
			view2.add_subview(button)
			view2.add_subview(label)
			numTasks+=1
		createAddTaskButton(view2, "task")
		view2.present("fullscreen")
	else:
		day = sender.title
		data[day][fromBankInfo] = False
		fromBankInfo = ""
		saveData(month)
		saveBank()

def decrMonth():
	if today[5] == "0":
		month = int(today[6])
		if month == 1:
			month = "12"
		else:
			month-=1
			month = "0" + str(month)
	else:
		month = int(today[5:7])
		if month == 10:
			month = "09"
		else:
			month-=1
			month = str(month)
	
def fromBank(sender):
	global bank
	global fromBankInfo
	global viewB
	fromBankInfo = sender.title
	viewB.close()
	temp = "&" + fromBankInfo
	bank[temp] = bank[fromBankInfo]
	del bank[fromBankInfo]

def addPreset(sender):
	viewP.add_subview(tPreset)
	

def savePreset(sender):
	print(tPreset.text)
	view2.remove_subview(tPreset)
	if sender.text != "":
		h = -5 + (44*len(presets))
		button = ui.Button(title = str(numTasks))
		button.center = (25.5, h)
		button.background_color = "red"
		button.action = taskButton
		label = ui.Label()
		label.text = textfield.text
		label.center = (125, h)
		label.flex = "w"
		view2.add_subview(button)
		view2.add_subview(label)
		textfield.text = ""
		numTasks+=1
		current.background_color = "red"
	
def createAddTaskButton(view, action):
	button = ui.Button(font = ('<system-bold>', 70), title = "0")
	button.center = (50,375)
	button.flex = "wh"
	if action == "task":
		button.action = addTask
	elif action == "preset":
		button.action = addPreset
	view.add_subview(button)
	button.title = "+"
	return button
	
	
def presetView(sender):
	global presets
	autoLabel = ui.Label(text = "Auto", font = ('<system-bold>',20))
	autoLabel.center = (275, 70)
	freqLabel = ui.Label(text = "Frequency", font = ('<system-bold>',20))
	freqLabel.center = (350, 70)
	viewP.add_subview(autoLabel)
	viewP.add_subview(freqLabel)
	createAddTaskButton(viewP, "preset")
	#for x in range(0, len(presets)):
	viewP.present("fullscreen")
		
		
		

def bankView(self):
	global bank
	global viewB
	viewB = ui.View()
	viewB.background_color = "f0fff5"
	h = 15
	for x in bank:
		if "&" not in x:
			button = ui.Button(font = ('<system-bold>',20), title = x)
			button.flex = "LRTB"
			button.center = (50, h)
			h+=5
			button.action = fromBank
		viewB.add_subview(button)
	viewB.present("fullscreen")
		

def loadButtons(today,month):
	global view1
	global dataKeys
	global buttons
	global todayIndex
	global sundayIndex
	loadedMonths = list(dataKeys.keys())
	curMonth = loadedMonths[1]
	Mindex = 1
	daysOfWeek = ["S", "M", "T", "W", "T", "F", "S"]
	sundayIndex = int(data[curMonth]["S"])
	if sundayIndex > todayIndex:
		curMonth = loadedMonths[0]
		Mindex = 0
		sundayIndex = len(dataKeys[curMonth]) - (sundayIndex-8)
	else:
		while todayIndex > (sundayIndex + 6):
			sundayIndex+=7
	for x in range(0,7):
		if (sundayIndex + 1 == len(dataKeys[curMonth])):
			sundayIndex = 1
			Mindex += 1
			curMonth = loadedMonths[Mindex]
		button = ui.Button(title = "0000000000")
		button.center = (80, (70 + (55*x)))
		button.background_color = "white"
		
		
		button.action = dateButton
		buttons.append(button)
		m = ui.Label(text = daysOfWeek[x], font = ('<system-bold>', 20))
		m.center = (60,  (70 + (55*x)))
		view1.add_subview(m)
		if (sundayIndex + x) == (todayIndex):
			button.border_color = "#2ce56d"
			button.border_width = 5
		view1.add_subview(button)
		#change after being added to view so it can have a set space
		button.title = dataKeys[curMonth][sundayIndex + x]
		temp = data[curMonth][button.title]
		if len(temp) > 0:
			button.background_color = "#2ce56d"
			for y in temp:
				if temp[y] == False:
					button.background_color = "red"
		
	preset = ui.Button(font = ('<system-bold>',20), title = "presets")
	preset.flex = "LRTB"
	preset.center = (60, 77)
	preset.background_color = "white"
	preset.action = presetView
	view1.add_subview(preset)
	bankBut = ui.Button(font = ('<system-bold>',20), title = "bank")
	bankBut.flex = "LRTB"
	bankBut.center = (35, 77)
	bankBut.background_color = "white"
	bankBut.action = bankView
	view1.add_subview(bankBut)
	
	prev = ui.Button(font = ('<system-bold>',15), title = "prev")
	prev.background_color = "white"
	prev.action = changeButtons
	prev.center = (30, 460)
	view1.add_subview(prev)
	
	next = ui.Button(font = ('<system-bold>',15), title = "next")
	next.background_color = "white"
	next.action = changeButtons
	next.center = (100, 460)
	view1.add_subview(next)
	
	view1.present("fullscreen")
	
def createData(day):
	day = changeMonth(day, 1)
	fileName = str(day)
	dayS = fileName
	month = fileName[5:7]
	fileName = fileName[0:7]
	fileName = fileName + "-data.txt"
	fileName = "lifelp/" + fileName
	with open(fileName, "w") as file:
		while dayS[5:7] == month:
			file.write(dayS)
			file.write("{}")
			file.write("\n")
			day = day + datetime.timedelta(days=1)
			dayS= str(day)
	
def setup():
	global bankKeys
	global data
	global dataKeys
	global todayIndex
	global month
	today = datetime.date.today()
	todayS = str(today)
	data, dataKeys = getData(today)
	todayIndex = findTodayIndex(todayS)
	month = getMonth(todayS)
	if todayS != bankKeys[0]:
		#readyBank()
		if todayS[8:10] == "01":
			createData(today)
		#checkIncomplete(today)
	
	
	
	loadButtons(todayS, month)

view1 = ui.View()
view1.background_color = "#f0fff5"
view2 = ui.View()
view2.background_color = "#f0fff5"
viewB = ui.View()
viewP = ui.View()
viewP.background_color = "f0fff5"
buttons = []
numTasks = 0
dataIndex = 0
current = ""
data = {}
dataKeys = {}
tTask = ui.TextField(frame = (20, 400, 375, 50))
tTask.action = saveTask
tPreset = ui.TextField(frame = (20, 400, 375, 50))
tPreset.action = savePreset
bank, bankKeys = loadBank()
presets = loadPresets()
fromBankInfo = ""
sundayIndex = ""

setup()



#THOUGHTS:
	#i can probably make a function that creates the buttons with the nice presets that take parameters for most of this button making



  
