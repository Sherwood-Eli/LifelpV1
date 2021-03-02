import ui
import datetime
import time
import lifelpDataBase
			

def checkForIncompleteTasks(today):
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
	lifelpDataBase.saveBank()

#goes to previous or next week depending on which button calls this function
def changeWeek(sender):
	global buttons
	global sundayIndex
	global data
	global dataKeys
	global viewMain
	today = str(datetime.date.today())
	key = today[0:7]
	if sender.title == "prev":
		sundayIndex-=7
	else:
		sundayIndex+=7
	#if month change is mid week
	if sundayIndex > todayIndex:
		curMonth = loadedMonths[0]
		Mindex = 0
		sundayIndex = len(dataKeys[curMonth]) - (8 - sundayIndex)
	for x in range(0, len(buttons)):
		#if month ends mid week
		if (sundayIndex + x == len(dataKeys[curMonth])):
			Mindex += 1
			curMonth = loadedMonths[Mindex]
			#sundayIndex - 7 to use next month sunday index
			sundayIndex = int(data[curMonth]["S"]) - 7
		button = buttons[x]
		button.title = dataKeys[key][sundayIndex + x]
		setDateButtonColor(button, data[key][button.title])

#Changes the color of a task button to the color that it is not.
#will also change other instances if this task to true/false. (might want to move this to only happen at the beggining of next day potentially)	
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
		lifelpDataBase.saveData(x, data)

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
	viewTasks.add_subview(tTask)

def addPreset(sender):
	viewP.add_subview(tPreset)
	
def createBankView(sender):
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
	
def createTaskView(sender):
	global viewTasks
	global data
	global current
	global numTasks
	global fromBankInfo
	month = sender.title[0:7]
	if fromBankInfo == "":
		current = sender
		curTitle = current.title
		numTasks = 1
		viewTasks = ui.View()
		viewTasks.background_color = "#f0fff5"
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
			viewTasks.add_subview(button)
			viewTasks.add_subview(label)
			numTasks+=1
		createAddTaskButton(viewTasks, "task")
		viewTasks.present("fullscreen")
	else:
		day = sender.title
		data[day][fromBankInfo] = False
		fromBankInfo = ""
		lifelpDataBase.saveData(month, data)
		lifelpDataBase.saveBank()

#Action of the textfield inside viewTask. Creates a new task button and task label
#and places ut in the task View
def createTask(textfield):
	global tTask
	global numTasks
	global data
	global current
	viewTasks.remove_subview(tTask)
	if textfield.text != "":
		month = current.title[0:7]
		temp = data[month][current.title]
		temp[textfield.text] = False
		lifelpDataBase.saveData(month, data)
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
		viewTasks.add_subview(button)
		viewTasks.add_subview(label)
		textfield.text = ""
		numTasks+=1
		current.background_color = "red"
	
def fromBank(sender):
	global bank
	global fromBankInfo
	global viewB
	fromBankInfo = sender.title
	viewB.close()
	temp = "&" + fromBankInfo
	bank[temp] = bank[fromBankInfo]
	del bank[fromBankInfo]
	

def savePreset(sender):
	print(tPreset.text)
	viewTasks.remove_subview(tPreset)
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
		viewTasks.add_subview(button)
		viewTasks.add_subview(label)
		textfield.text = ""
		numTasks+=1
		current.background_color = "red"
	
def createAddTaskButton(view, action):
	button = ui.Button(font = ('<system-bold>', 70), title = "0")
	button.center = (200, 725)
	if action == "task":
		button.action = addTask
	elif action == "preset":
		button.action = addPreset
	view.add_subview(button)
	button.title = "+"
	return button

def createPresetButton(view):
	preset = ui.Button(font = ('<system-bold>',20), title = "presets")
	preset.flex = "LRTB"
	preset.center = (60, 77)
	preset.background_color = "white"
	preset.action = presetView
	view.add_subview(preset)

def createBankButton(view)
	bankBut = ui.Button(font = ('<system-bold>',20), title = "bank")
	bankBut.flex = "LRTB"
	bankBut.center = (35, 77)
	bankBut.background_color = "white"
	bankBut.action = createBankView
	view.add_subview(bankBut)

def createPrevButton(view):
	prev = ui.Button(font = ('<system-bold>',15), title = "prev")
	prev.background_color = "white"
	prev.action = changeWeek
	prev.center = (30, 460)
	view.add_subview(prev)

def createNextButton(view):
	next = ui.Button(font = ('<system-bold>',15), title = "next")
	next.background_color = "white"
	next.action = changeWeek
	next.center = (100, 460)
	view.add_subview(next)
	
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
		
		
		

	

def createDateButtons(today):
	global viewMain
	global dataKeys
	global buttons
	global todayIndex
	global sundayIndex

	loadedMonths = list(dataKeys.keys())
	curMonth = loadedMonths[1]
	Mindex = 1
	daysOfWeek = ["S", "M", "T", "W", "T", "F", "S"]
	sundayIndex = int(data[curMonth]["S"])

	#if month transition is mid week
	if sundayIndex > todayIndex:
		curMonth = loadedMonths[0]
		Mindex = 0
		sundayIndex = len(dataKeys[curMonth]) - (8 - sundayIndex)
	#else find correct sunday index
	else:
		while todayIndex > (sundayIndex + 6):
			sundayIndex+=7

	for x in range(0,7):
		#if month ends mid week
		if (sundayIndex + x == len(dataKeys[curMonth])):
			Mindex += 1
			curMonth = loadedMonths[Mindex]
			#sundayIndex - 7 to use next month sunday index
			sundayIndex = int(data[curMonth]["S"]) - 7
			
		#adds the date button with temporary label to set size
		button = ui.Button(title = "0000000000")
		button.center = (80, (70 + (55*x)))
		button.background_color = "white"
		button.action = createTaskView
		buttons.append(button)
		#highlights current day
		if (sundayIndex + x) == (todayIndex):
			button.border_color = "#2ce56d"
			button.border_width = 5
		#figuring out what color to make the dateButton
		temp = data[curMonth][button.title]
		setDateButtonColor(button, temp)
		viewMain.add_subview(button)

		#change title of dateButton after being added to view so it can have a set space
		button.title = dataKeys[curMonth][sundayIndex + x]

		#adds dayLabel next to dateButton
		dayLabel = ui.Label(text = daysOfWeek[x], font = ('<system-bold>', 20))
		dayLabel.center = (60,  (70 + (55*x)))
		viewMain.add_subview(dayLabel)
		
	createPresetButton(viewMain)
	createBankButton(viewMain)
	createPrevButton(viewMain)
	createNextButton(viewMain)
	
	viewMain.present("fullscreen")

	

	
def setup():
	global bankKeys
	global data
	global dataKeys
	global todayIndex
	today = datetime.date.today()
	todayS = str(today)
	
	
	if todayS != bankKeys[0]:
		#lifelpAUX.readyBank(bank)
		if todayS[8:10] == "01":
			lifelpDataBase.createData(today)
		#checkForIncompleteTasks(today)
	data, dataKeys = lifelpDataBase.getData(today)
	todayIndex = lifelpAUX.findTodayIndex(todayS)
	
	
	
	createDateButtons(todayS)



viewMain = ui.View()
viewMain.background_color = "#f0fff5"
viewTasks = ui.View()
viewTasks.background_color = "#f0fff5"
viewB = ui.View()
viewB.background_color = "#f0fff5"
viewP = ui.View()
viewP.background_color = "f0fff5"

buttons = []

numTasks = 0
dataIndex = 0
current = ""
data = {}
dataKeys = {}
tTask = ui.TextField(frame = (20, 400, 375, 50))
tTask.action = createTask
tPreset = ui.TextField(frame = (20, 400, 375, 50))
tPreset.action = savePreset
bank, bankKeys = lifelpDataBase.loadBank()
presets = loadPresets()
fromBankInfo = ""
sundayIndex = ""

setup()



#THOUGHTS:
	#i can probably make a function that creates the buttons with the nice presets that take parameters for most of this button making

	#I can put all of my global variables in a function and declare them all there if i want


  
