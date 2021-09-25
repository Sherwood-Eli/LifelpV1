import ui
import datetime
import time
import lifelpDataBase
import lifelpAUX
			


	
	

#############################
#############################
#############################
#Functions shared by classes#


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
			
def activateBoolButton(sender):
	if sender.title == "no":
		sender.title = "yes"
		sender.background_color = "2ce56d"
	elif sender.title == "yes":
		sender.title = "no"
		sender.background_color = "red"




#############################
#############################
#############################
#     MyMainView Class      #

#holds all data and functionality
#for the main home view

class MyMainView:
	def __init__(self):
		self.view = ui.View()
		self.view.background_color = "f0fff5"	
		self.dateButtons = []
		self.sundayIndex = 0
		self.trashButton = createTrashButton(self.view)
		self.todayIndex = lifelpAUX.findTodayIndex(todayS, data)
	
	def createDateButtons(todayS, newDay):
		global data
		global presetWindow
		global bank
		
		curMonth = todayS[0:7]
		mIndex = 1
		daysOfWeek = ["S", "M", "T", "W", "T", "F", "S"]
		self.sundayIndex = int(data[curMonth].sundayIndex)
		alteredMonths = []

		#if month transition is mid week
		if self.sundayIndex > self.todayIndex:
			curMonth = lifelpAUX.decrFileKey(curMonth)
			mIndex = 0
			self.sundayIndex = len(data[curMonth].days) - (7 - self.sundayIndex)
		#else find correct sunday index
		else:
			while self.todayIndex > (self.sundayIndex + 6):
				self.sundayIndex+=7
		
		#at this point lastLog will have been changed to todayS and lastLast log will be the last log but we do not want this to happen more than necesarry so we and it with newDay
		needApplyPresets = newDay and lifelpAux.isNewWeek(data[curMonth].dataKeys[self.sundayIndex], bank.lastLastLog)	
			
		alteredMonths.append(curMonth)

		for x in range(0,7):
			#if month ends mid week
			if (self.sundayIndex + x == len(data[curMonth].days)):
				curMonth = lifelpAUX.incrFileKey(curMonth)
				#sundayIndex - 7 to use next month sunday index
				self.sundayIndex = int(data[curMonth].sundayIndex) - 7
				alteredMonths.append(curMonth)
				
			#adds the date button with temporary label to set size
			button = ui.Button(title = "0000000000")
			button.center = (80, (70 + (55*x)))
			button.background_color = "white"
			button.action = createTaskView
			self.dateButtons.append(button)
			#highlights current day
			if (self.sundayIndex + x) == (self.todayIndex):
				button.border_color = "#2ce56d"
				button.border_width = 5
		
			#change title of dateButton after being added to view so it can have a set space
			button.title = data[curMonth].dataKeys[self.sundayIndex + x]
			data
			self.view.add_subview(button)
			
			if needApplyPresets and x > 0:
				if x % 2 == 0:
					for preset in presetWindow.presets:
						if presetWindow.presets[preset].auto and presetWindow.presets[preset].frequency == "every B day":
							data[curMonth].days[button.title].tasks[preset] = lifelpDataBase.Task()
							data[curMonth].days[button.title].tasks[preset].type = "p"
				else:
					for preset in presetWindow.presets:
						if presetWindow.presets[preset].auto and presetWindow.presets[preset].frequency == "every A day":
							data[curMonth].days[button.title].tasks[preset] = lifelpDataBase.Task()
							data[curMonth].days[button.title].tasks[preset].type = "p"
				for preset in presetWindow.presets:
						if presetWindow.presets[preset].auto and presetWindow.presets[preset].frequency == "every day":
							data[curMonth].days[button.title].tasks[preset] = lifelpDataBase.Task()
							data[curMonth].days[button.title].tasks[preset].type = "p"
			
			#figuring out what color to make the dateButton
			day = data[curMonth].days[button.title]
			day.buttonIndex = x
			setDateButtonColor(button, day)

		

			#adds dayLabel next to dateButton
			dayLabel = ui.Label(text = daysOfWeek[x], font = ('<system-bold>', 20))
			dayLabel.center = (60,  (70 + (55*x)))
			self.view.add_subview(dayLabel)
			
		createPresetButton(self.view)
		createMoreViewsButton(self.view)
		createBankButton(self.view)
		createPrevButton(self.view)
		createNextButton(self.view)
		
		self.view.present("fullscreen")
		
		if needApplyPresets:
			for x in alteredMonths:
				lifelpDataBase.saveData(x, data)
	
	def changeWeek(sender):
		global todayS
		global data
		
		curMonth = todayS[0:7]
		
		if sender.title == "prev":
			self.sundayIndex-=7
			if self.sundayIndex < 0:
				curMonth = lifelpAUX.decrFileKey(curMonth)
				try:
					self.sundayIndex = len(data[curMonth].days) + self.sundayIndex
				except KeyError:
					data[curMonth] = lifelpDataBase.loadData(curMonth)
					self.sundayIndex = len(data[curMonth].days) + self.sundayIndex
		else:
			self.sundayIndex+=7
		for x in range(0, len(self.dateButtons)):
			oldLabel = self.dateButtons[x].title
			data[oldLabel[0:7]].days[oldLabel].buttonIndex = -1
			#if month ends mid week
			if (self.sundayIndex + x >= len(data[curMonth].days)):
				curMonth = lifelpAUX.incrFileKey(curMonth)
				# to use next month sunday index
				try:
					self.sundayIndex = int(data[curMonth].sundayIndex) - 7
				except KeyError:
					data[curMonth] = lifelpDataBase.loadData(curMonth)
					self.sundayIndex = int(data[curMonth].sundayIndex) - 7
				if self.sundayIndex == -7:
					self.sundayIndex = 0
			button = self.dateButtons[x]
			button.title = data[curMonth].dataKeys[self.sundayIndex + x]
			day = data[curMonth].days[button.title]
			day.buttonIndex = x
			setDateButtonColor(button, day)
			if button.title == todayS:
				button.border_width = 5
			else:
				button.border_width = 0
				
				
				
				
#############################
#############################
#############################
#      MyDayView Class      #
			
#Holds all data and functionality 
#for the curent day being viewed
					
class MyDayView:
	def __init__(self):	
		self.view = None
		self.taskButtons = []
		self.taskLabels = []
		self.date = ""
		self.dateButton = None
		self.editButton = None
		self.editMode = False
		self.textField = ui.TextField(frame = (20, 400, 375, 50))
		self.textField.action = createTask
	
	
	def addTask(self, sender):
		myDayView.view.add_subview(self.textField)
	
	def dayEditMode(self, sender):
		if sender.title == "done":
			global data
			tasks = data[self.date[0:7]].days[self.date].tasks
			self.editMode = False
			sender.title = "edit"
			x = 0
			for task in tasks:
				button = self.taskButtons[x]
				button.title = button.name
				if tasks[task].complete:
					button.background_color = "#2ce56d"
				else:
					button.background_color = "red"
				x+=1
			
	elif sender.title == "edit":
		self.editMode = True
		sender.title = "done"
		for button in self.taskButtons:
			button.title = "X"
			button.background_color = "#ff591e"
	
	def createTask(textfield):
		global data
		self.view.remove_subview(self.textField)
		if textfield.text != "":
			month = self.date[0:7]
			day = data[month].days[self.date]
			numTasks = len(day.tasks) + 1
			day.tasks[textfield.text] = lifelpDataBase.Task()
			lifelpDataBase.saveData(month, data)
			h = 30 + (40*(numTasks-1))
			button = ui.Button(title = str(numTasks))
			self.taskButtons.append(button)
			button.name = str(numTasks)
			button.flex = "w"
			button.center = (35, h)
			if self.editMode:
				button.title = "X"
				button.background_color = "#ff591e"
			else:
				button.background_color = "red"
			button.action = taskButton
			labelText = textfield.text
			label = ui.Label(text = labelText)
			self.taskLabels.append(label)
			label.center = (125, h+40)
			label.flex = "w"
			label.size_to_fit()
			self.view.add_subview(button)
			self.view.add_subview(label)
			textfield.text = ""
			numTasks+=1
			self.dateButton.background_color = "red"
	
	def taskButton(self, sender):
		global data
		global bank
		month = self.date[0:7]
		day = data[month].days[self.date]
		tasks = day.tasks
		taskKeys = list(tasks.keys())
		if sender.title == "X":
			indexToDelete = int(sender.name) - 1
			maxIndex = len(self.taskButtons) - 1
			#can only delete things from present and future days so this is coo
			if tasks[taskKeys[indexToDelete]].type == "b": 
				bank.bank[taskKeys[indexToDelete]].outCount -= 1
				lifelpDataBase.saveBank(bank)
			del tasks[taskKeys[indexToDelete]]
			del taskKeys[indexToDelete]
			self.view.remove_subview(self.taskButtons[indexToDelete])
			self.view.remove_subview(self.taskLabels[indexToDelete])
			del self.taskButtons[indexToDelete]
			del self.taskLabels[indexToDelete]
			for x in range(indexToDelete, maxIndex):
				self.taskLabels[x].center.y -= 40
				self.taskButtons[x].center.y -= 40
			if maxIndex == 0:
				dayEditMode(self.editButton)
			lifelpDataBase.saveData(month, data)
			
		else:
			index = int(sender.title) - 1
			task = taskKeys[index]
			tMonths = []
			tMonths.append(month)
			if (sender.background_color == (1.0, 0.0, 0.0, 1.0)):
				sender.background_color = "#2ce56d"
				tasks[task].complete = True
				if tasks[task].type == "b":
					for date in bank.bank[task].dates:
						tMonth = date[0:7]
						pastDay = data[tMonth].days[date]
						if tMonth not in tMonths:
							tMonths.append(tMonth)
						pastDay.tasks[task].complete = True
						#if it is -1 then date is not displayed
						if pastDay.buttonIndex != -1:
							
							setDateButtonColor(mainView.dateButtons[pastDay.buttonIndex], pastDay)
					bank.bank[task].complete = True
					lifelpDataBase.saveBank(bank)
			else:
				sender.background_color = "red"
				tasks[task].complete = False
				if tasks[task].type == "b":
					for date in bank.bank[task].dates:
						tMonth = date[0:7]
						pastDay = data[tMonth].days[date]
						if tMonth not in tMonths:
							tMonths.append(tMonth)
						pastDay.tasks[task].complete = False
						if pastDay.buttonIndex != -1:
							setDateButtonColor(mainView.dateButtons[pastDay.buttonIndex], pastDay)
					bank.bank[task].complete = False
					lifelpDataBase.saveBank(bank)
			setDateButtonColor(self.dateButton, day)
			for x in tMonths:
				lifelpDataBase.saveData(x, data)

		
	def createDayView(self, sender):
		global data
		global bank
		global todayS
		self.taskButtons = []
		self.taskLabels = []
		month = sender.title[0:7]
		if bank.fromBankInfo == "":
			curDate = sender.title
			self.date = curDate
			self.dateButton = sender
			numTasks = 1
			self.view = ui.View()
			self.view.background_color = "#f0fff5"
			x = 0
			tasks = data[month].days[curDate].tasks
			for task in tasks:
				h = (30 + 40*x)
				button = ui.Button(title = str(numTasks))
				self.taskButtons.append(button)
				button.name = str(numTasks)
				button.center = (35, h)
				if tasks[task].complete:
					button.background_color = "#2ce56d"
				else:
					button.background_color = "red"
				if date1GreaterThan2(bank.lastLastLog, curDate) == False:
					button.action = taskButton
				label = ui.Label()
				self.taskLabels.append(label)
				label.text = task
				label.center = (125, h)
				label.flex = "w"
				self.view.add_subview(button)
				self.view.add_subview(label)
				numTasks+=1
				x+=1
			if date1GreaterThan2(todayS, curDate) == False:
				createAddTaskButton(self, "task")
				self.editButton = createEditButton(self.view, "d")
				editMode = False
			self.view.present("fullscreen")
		else:
			global mainView
			date = sender.title
			
			data[date[0:7]].days[date].tasks[bank.fromBankInfo] = lifelpDataBase.Task()
			data[date[0:7]].days[date].tasks[bank.fromBankInfo].type = "b"
			
			bank.bank[bank.fromBankInfo].outCount+=1
			bank.fromBankInfo = ""
			
			mainView.view.remove_subview(mainView.trashButton)
			setDateButtonColor(sender, data[date[0:7]].days[date])
			
			lifelpDataBase.saveData(month, data)
			lifelpDataBase.saveBank(bank)	
	

	


#############################
#############################
#############################
#        Bank Class         #

#holds all data and functionality
#for the bank section

class Bank:	
	def __init__(self):
		global todayS
		#global data
		#global dataKeys
		self.lastLastLog, self.lastLog, self.bank, self.bankKeys = lifelpDataBase.loadBank()
		self.fromBankInfo = ""
		self.newDay = False
		if self.lastLog != todayS:
			self.checkForIncomplete()
			self.cleanBank()
			self.newDay = True
			self.lastLastLog = self.lastLog
			self.lastLog = todayS
			lifelpDataBase.saveBank(self)
	
	def presentBankView(self, sender):
		self.view = ui.View()
		self.view.background_color = "f0fff5"
		h = 20
		for task in self.bank:
			if self.bank[task].outCount == 0 and self.bank[task].complete == False:
				button = ui.Button(font = ('<system-bold>',20), title = task)
				button.flex = "LRTB"
				button.center = (50, h)
				h+=5
				button.action = self.fromBank
				self.view.add_subview(button)
		self.view.present("fullscreen")
	
	
	def cleanBank(self):
		tasksToDelete = []
		for task in self.bank:
			if self.bank[task].complete:
				dayS = self.bank[task].dates[len(self.bank[task].dates) - 1]
				for date in self.bank[task].dates:
					newKey = task + " " + dayS
					newTask = lifelpDataBase.Task()
					newTask.complete = True
					data[dayS[0:7]].days[date].tasks[newKey] = newTask
					del data[date[0:7]].days[date].tasks[task]
				tasksToDelete.append(task)
		for task in tasksToDelete:
			del self.bank[task]
			self.bankKeys.remove(task)
	
	def checkForIncomplete(self):
		global today
		global todayS
		global data
		day = today
		dayS = str(day)
		while(dayS != self.lastLog):
			day = day - datetime.timedelta(days=1)
			dayS = str(day)
			dataKey = dayS[0:7]
			try:
				curDay = data[dataKey].days[dayS].tasks
			except KeyError:
				data[dataKey] = lifelpDataBase.loadData(dataKey)
				curDay = data[dataKey].days[dayS].tasks
			for task in curDay:
				if curDay[task].complete == False:
					if curDay[task].type == "r":
						self.bankKeys.append(task)
						#if there is another instance of this task somewhere in the future then outCount is inacurate
						curDay[task].type = "b"
						self.bank[task] = lifelpDataBase.BankTask(0, [dayS], False)
					elif curDay[task].type == "b":
						self.bank[task].dates.append(dayS)
						self.bank[task].outCount-=1
			lifelpDataBase.saveData(dataKey, data)
	
	def fromBank(self, sender):
		global mainView
		self.fromBankInfo = sender.title
		mainView.view.add_subview(mainView.trashButton)
		self.view.close()
		
	def deleteBankTask(sender):
		global mainView
		
		del self.bank[bank.fromBankInfo]
		self.bankKeys.remove(self.fromBankInfo)
		self.fromBankInfo = ""
		mainView.view.remove_subview(mainView.trashButton)
		lifelpDataBase.saveBank(self)




#############################
#############################
#############################
#       Presets Class       #

#holds all data and functionality
#for the presets section

class Presets:
	def __init__(self):
		self.presets, self.presetKeys = lifelpDataBase.loadPresets()
		self.numPresets = len(self.presetKeys)
		self.viewP = None
		self.textField = ui.TextField(frame = (20, 400, 375, 50))
		self.textField.action = self.savePreset
	
	def addPreset(self, sender):
		self.viewP.add_subview(self.textField)
	
	def showPresetView(self, sender):
		global editMode
		editMode = False
		if self.viewP == None:
			self.viewP = ui.View(background_color = "f0fff5")
			self.autoLabel = ui.Label(text = "Auto", font = ('<system-bold>',20))
			self.autoLabel.center = (275, 70)
			self.freqLabel = ui.Label(text = "Frequency", font = ('<system-bold>',20))
			self.freqLabel.center = (350, 70)
			presetLabel = ui.Label(text = "Task", font = ('<system-bold>',20))
			presetLabel.center = (130, 70)
			self.viewP.add_subview(self.autoLabel)
			self.viewP.add_subview(self.freqLabel)
			self.viewP.add_subview(presetLabel)
			createAddTaskButton(self, "preset")
			x = 0
			for preset in self.presets:
				h = 100 + (40*x)
				
				labelButton = ui.Button(title = preset, font = ('<system>',20))
				labelButton.action = self.assignPreset
				labelButton.center = (100, h)
				self.viewP.add_subview(labelButton)
				self.presets[preset].labelButton = labelButton
				
				autoButton = ui.Button(title = "00")
				autoButton.center = (245, h)
				autoButton.background_color = "red"
				autoButton.action = self.setAuto
				autoButton.name = str(x)
				
				if self.presets[preset].auto:
					autoButton.title = "yes"
					autoButton.background_color = "2ce56d"
					
					frequencyButton = ui.Button(title = "00000000000")
					frequencyButton.center = (350, h)
					frequencyButton.background_color = "white"
					frequencyButton.action = self.setFrequency
					frequencyButton.name = str(x)
					self.viewP.add_subview(frequencyButton)
			
					frequencyButton.title = self.presets[preset].frequency
					
					self.presets[preset].frequencyButton = frequencyButton
				else:
					autoButton.title = "no"
				
				
				self.viewP.add_subview(autoButton)
				self.presets[preset].autoButton = autoButton
				
				x+=1
			createEditButton(self.viewP, "p")
				
				
		self.viewP.present("fullscreen")
		
	def presetEditMode(self, sender):
		global editMode
		if sender.title == "edit":
			sender.title = "done"
			editMode = True
			self.viewP.remove_subview(self.autoLabel)
			self.viewP.remove_subview(self.freqLabel)
			for preset in self.presets:
				if self.presets[preset].auto:
					self.viewP.remove_subview(self.presets[preset].frequencyButton)
				self.presets[preset].autoButton.title = "X"
				self.presets[preset].autoButton.background_color = 	"#ff591e"
		elif sender.title == "done":
			sender.title = "edit"
			editMode = False
			self.viewP.add_subview(self.autoLabel)
			self.viewP.add_subview(self.freqLabel)
			for preset in self.presets:
				if self.presets[preset].auto:
					self.viewP.add_subview(self.presets[preset].frequencyButton)
					self.presets[preset].autoButton.background_color = "2ce56d"
					self.presets[preset].autoButton.title = "yes"
				else:
					self.presets[preset].autoButton.background_color = "red"
					self.presets[preset].autoButton.title = "no"
				
		
	def showFrequencyButton(self, buttonName, task):
		button = ui.Button(title = "00000000000")
		button.center = (350, 100 + 40*int(buttonName))
		button.background_color = "white"
		button.action = self.setFrequency
		button.name = buttonName
		self.viewP.add_subview(button)
		button.title = "every day"
		self.presets[task].frequencyButton = button
		self.presets[task].frequency = button.title
		lifelpDataBase.savePresets(self.presets)
		self.placePreset(task, "every day")
	
	def hideFrequencyButton(self, task):
		button = self.presets[task].frequencyButton
		self.removePreset(task)
		self.viewP.remove_subview(button)
	
	def setAuto(self, sender):
		if sender.title == "no":
			sender.title = "yes"
			sender.background_color = "2ce56d"
			task = self.presetKeys[int(sender.name)]
			self.presets[task].auto = True
			self.showFrequencyButton(sender.name, task)
		elif sender.title == "yes":
			sender.title = "no"
			sender.background_color = "red"
			task = self.presetKeys[int(sender.name)]
			self.presets[task].auto = False
			self.hideFrequencyButton(task)
		elif sender.title == "X":
			indexToDelete = int(sender.name)
			presetToDelete = self.presetKeys[indexToDelete]
			
			self.viewP.remove_subview(self.presets[presetToDelete].labelButton)
			self.viewP.remove_subview(self.presets[presetToDelete].autoButton)
			if self.presets[presetToDelete].auto:
				self.viewP.remove_subview(self.presets[presetToDelete].frequencyButton)
			
			for x in range(len(self.presetKeys) - 1, indexToDelete, -1):
				h = 100 + (40*(x-1))
				preset = self.presets[self.presetKeys[x]]
				
				preset.labelButton.name = str(x-1)
				preset.labelButton.center = (100, h)
				preset.autoButton.name = str(x-1)
				preset.autoButton.center = (245, h)
				if preset.auto:
					preset.frequencyButton.name = str(x-1)
					preset.frequencyButton.center = (350, h)
			
			del self.presets[presetToDelete]
			del self.presetKeys[indexToDelete]
			self.removePreset(presetToDelete)
			self.numPresets-=1
			
			
		lifelpDataBase.savePresets(self.presets)
		
	def setFrequency(self, sender):
		self.removePreset(self.presetKeys[int(sender.name)])
		if sender.title == "every day":
			sender.title = "every A day"
		elif sender.title == "every A day":
			sender.title = "every B day"
		elif sender.title == "every B day":
			sender.title = "every day"
		self.presets[self.presetKeys[int(sender.name)]].frequency = sender.title
		lifelpDataBase.savePresets(self.presets)
		self.placePreset(self.presetKeys[int(sender.name)], sender.title)
			
	def assignPreset(self, sender):
		if self.presets[sender.title].auto == False:
			self.viewP.close()
	
	def savePreset(self, sender):
		newPreset = sender.text
		sender.text = ""
		self.viewP.remove_subview(sender)
		if newPreset in self.presets:
			print("there is already a preset with this name")
			
		elif newPreset != "":
			h = 100 + (40*self.numPresets)
			
			autoButton = ui.Button(title = "no")
			autoButton.center = (245, h)
			autoButton.background_color = "red"
			autoButton.action = self.setAuto
			autoButton.name = str(self.numPresets)
			if editMode:
				autoButton.title = "X"
				autoButton.background_color = "#ff591e"
			
			self.viewP.add_subview(autoButton)
			
			presetButton = ui.Button(title = newPreset, font = ('<system>',20))
			presetButton.action = self.assignPreset
			presetButton.center = (100, h)
			self.viewP.add_subview(presetButton)
			
			
			
			self.numPresets+=1
			
			self.presets[newPreset] = lifelpDataBase.PresetTask(False, "")
			self.presets[newPreset].labelButton = presetButton
			self.presets[newPreset].autoButton = autoButton
			self.presetKeys.append(newPreset)
			lifelpDataBase.savePresets(self.presets)
			
	def placePreset(self, preset, frequency):
		global data
		global mainView
		todayS = str(datetime.date.today())
		
		#for when this is called when not in current week, have there be a global varibld that tells this to be called again when current week is restored.
		start = False
		if frequency == "every day":
			for x in range(0,7):
				date = mainView.dateButtons[x].title
				if date == todayS:
					start = True
				if start:
					day = data[date[0:7]].days[date]
					day.tasks[preset] = lifelpDataBase.Task()
					day.tasks[preset].complete = False
					day.tasks[preset].type = "p"
					setDateButtonColor(mainView.dateButtons[x], day)
		if frequency == "every A day":
			for x in range(0,7):
				date = mainView.dateButtons[x].title
				if date == todayS:
					start = True
				if start and x%2 == 1:
					day = data[date[0:7]].days[date]
					day.tasks[preset] = lifelpDataBase.Task()
					day.tasks[preset].complete = False
					day.tasks[preset].type = "p"
					setDateButtonColor(mainView.dateButtons[x], day)
		if frequency == "every B day":
			for x in range(0,7):
				date = mainView.dateButtons[x].title
				if date == todayS:
					start = True
				if start and x != 0 and x%2 == 0:
					day = data[date[0:7]].days[date]
					day.tasks[preset] = lifelpDataBase.Task()
					day.tasks[preset].complete = False
					day.tasks[preset].type = "p"
					setDateButtonColor(mainView.dateButtons[x], day)
		lifelpDataBase.saveData(todayS[0:7], data)
		if date[5:7] != todayS[5:7]:
			nextMonth = str(lifelpAUX.changeMonth(todayS, 1))
			lifelpDataBase.saveData(nextMonth[0:7], data)
	
	def removePreset(self, preset):
		global data
		global mainView
		todayS = str(datetime.date.today())
		
		start = False
		for x in range(0,7):
			date = mainView.dateButtons[x].title
			if date == todayS:
				start = True
			if start:
				day = data[date[0:7]].days[date]
				if preset in day.tasks:
					del day.tasks[preset]
					setDateButtonColor(mainView.dateButtons[x], day)
		lifelpDataBase.saveData(todayS[0:7], data)
		if date[5:7] != todayS[5:7]:
			nextMonth = str(lifelpAUX.changeMonth(todayS, 1))
			lifelpDataBase.saveData(nextMonth[0:7], data)




#############################
#############################
#############################
#    SettingOption Class    #

#holds all data and functionality
#for all available options for
#custom views and tasks in the
#moreViews section

class SettingOption:
	def __init__(self, name, type, choices):
		self.name = name
		self.type = type
		self.choices = choices
		self.choiceIndex = 0
		self.helperButton = None
		
	def addHelperButton(self, title):
		if title == "view:":
			button = ui.Button(title = "XXXX")
			button.center = (325, 80 + 45)
			button.action = moreViews.chooseViewLink
			button.background_color = "white"
			button.name = "select"
			
			moreViews.curView.optionsView.add_subview(button)
			button.title = "none"
			self.helperButton = button
		
		
	
	def cycleChoice(self, sender):
		self.choiceIndex+=1
		if self.choiceIndex%len(self.choices) == 0:
			self.choiceIndex = 0
		sender.title = self.choices[self.choiceIndex]
		if self.helperButton != None:
			moreViews.curView.optionsView.remove_subview(self.helperButton)
			self.helperButton = None
		self.addHelperButton(sender.title)





#############################
#############################
#############################
#     CustomTask Class      #		

#holds all data and functionality
#for the tasks that are in views
#in the MoreViews section

class CustomTask:
	def __init__(self, options):
		
		
		#option 1
		self.name = option[0]
		
		#option 2
		if self.options[1][0:4] == "view":
			self.attachedView = self.options[1][4:len(self.options[1])]
			button.action = self.openAttachedView




#############################
#############################
#############################
#      MoreViews Class      #

#holds all data and funtionality
#for the home view for the
#more views section 

class MoreViews:
	def __init__(self, type):
		self.view = ui.View()
		self.view.background_color = "f0fff5"	
		self.addTaskButton = createAddTaskButton(self, "customView")
		self.editMode = False
		self.selectMode = False
		if type == "r":
			self.editButton = createEditButton(self, "mr")
			self.selectView = MoreViews("s")
			
		elif type == "s":
			self.editButton = createEditButton(self, "ms")
			
		self.moreViewButtons = []
		self.x = 0
		self.y = 0
		
		self.chosenOptions = []
		self.availableOptions = []
		self.optionsView = None
		
		#option 1
		self.availableOptions.append(SettingOption("name", "s", []))
		
		#option 2
		self.availableOptions.append(SettingOption("completable", "b", []))
		
		
		
		self.optionsView = None
		
		self.allViews, self.numSlots, self.availableSlots = lifelpDataBase.loadMoreViewsAll()
		self.homeViews = lifelpDataBase.loadMoreViewsHome()
		
		self.curView = None
		self.viewPath = []
	
		for viewKey in self.homeViews:
			button = ui.Button(title = "00000000000")
			button.center = (55 + 150 * self.x, 50 + 40 * self.y)
			button.background_color = "white"
			button.action = self.openCustomView
			self.view.add_subview(button)
			button.title = self.homeViews[viewKey]
			button.name = viewKey
			self.moreViewButtons.append(button)
			self.x+=1
			if self.x%3 == 0:
				self.x = 0
				self.y+=1
		
	def showView(self, sender):
		if self.editMode:
			self.moreEditMode(self.editButton)
		self.view.present("fullscreen")
		
	def chooseViewLink(self, sender):
		self.curView.buttonNeedingLink = sender
		self.selectView.view.present("fullscreen")
			
	def openCustomView(self, sender):
		if self.curView == None:
			self.viewPath.append(None)
		else:
			self.viewPath.append(self.curView.serialNum)
		self.curView = CustomView(sender.name)
		self.curView.button = sender
		if self.editMode:
			self.openCustomViewOptions("edit")
		elif self.selectMode:
			self.curView.linkView(sender.name)
		else:
			self.curView.view.present("fullscreen")
		
		
		
	def openCustomViewOptions(self, sender):
		self.chosenOptions = []
		
		view = ui.View()
		self.optionsView = view
		view.background_color = "f0fff5"
		
		if sender == "edit":
			x = 0
			for option in self.availableOptions:
				label = ui.Label(text = option.name, center = (100, 75 + 45*int(x)))
				
				view.add_subview(label)
				#needs boolean value
				if option.type == "b":
					button = ui.Button(title = "XXX")
					button.center = (275, 80 + 45*int(x))
					button.action = activateBoolButton
					button.name = "b" + str(x)
					view.add_subview(button)
					if self.curView.options[x] == True:
						button.title = "yes"
						button.background_color = "2ce56d"
					elif self.curView.options[x] == False:
						button.title = "no"
						button.background_color = "red"
					self.chosenOptions.append(button)
				#needs string value
				elif option.type == "s":
					textField = ui.TextField(frame = (200, 60 + 45*int(x), 150, 35))
					textField.name = "s" + str(x)
					textField.text = self.curView.options[x]
					view.add_subview(textField)
					self.chosenOptions.append(textField)
				x+=1
				
			createCreateButton(view, "save", "v")
		else:
			x = 0
			for option in self.availableOptions:
				label = ui.Label(text = option.name, center = (100, 75 + 45*int(x)))
				
				view.add_subview(label)
				#needs boolean value
				if option.type == "b":
					button = ui.Button(title = "XXX")
					button.center = (275, 80 + 45*int(x))
					button.action = activateBoolButton
					button.name = "b" + str(x)
					view.add_subview(button)
					button.title = "no"
					button.background_color = "red"
					self.chosenOptions.append(button)
				#needs string value
				elif option.type == "s":
					textField = ui.TextField(frame = (200, 60 + 45*int(x), 150, 35))
					textField.name = "s" + str(x)
					view.add_subview(textField)
					self.chosenOptions.append(textField)
				x+=1
				
			createCreateButton(view, "create", "v")
		view.present("fullscreen")
		
			
	def setCustomViewSettings(self, sender):
		for x in self.chosenOptions:
			index = int(x.name[1])
			type = x.name[0]
			if type == "b":
				if x.title == "yes":
					self.chosenOptions[index] = True
				elif x.title == "no":
					self.chosenOptions[index] = False
			elif type == "s":
				self.chosenOptions[index] = self.chosenOptions[index].text
		if sender.title == "create":
			if len(self.availableSlots) == 0:
				self.numSlots+=1
				serialNum = str(self.numSlots)
			else:
				serialNum = self.availableSlots.pop(0)
			
			lifelpDataBase.createCustomViewData(serialNum, self.chosenOptions)
				
			self.allViews[serialNum] = self.chosenOptions[0]
			self.homeViews[serialNum] = self.chosenOptions[0]
			
			lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
			lifelpDataBase.saveMoreViewsHome(self.homeViews)
			
			#then i gotta add the view to the physical home view
			
			button = ui.Button(title = "00000000000")
			button.center = (55 + 150 * self.x, 50 + 40 * self.y)
			button.background_color = "white"
			button.action = self.openCustomView
			self.view.add_subview(button)
			button.title = self.homeViews[serialNum]
			button.name = serialNum
			self.moreViewButtons.append(button)
			self.x+=1
			if self.x%3 == 0:
				self.x = 0
				self.y+=1
				
		else:
			self.curView.options = self.chosenOptions
			name = self.curView.options[0]
			if self.curView.button.title != name:
				self.curView.button.title = name
				self.allViews[self.curView.serialNum] = name
				self.homeViews[self.curView.serialNum] = name
				
				lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
				lifelpDataBase.saveMoreViewsHome(self.homeViews)
			lifelpDataBase.saveCustomView(self.curView.serialNum, self.curView.options, self.curView.tasks)
		
			#then i guess i should just re-present the physicsl view
		self.optionsView.close()
	
	def moreEditMode(self, sender):
		if self.editMode == False:
			self.editMode = True
			for x in self.moreViewButtons:
				x.background_color = "#ff591e"
			sender.title = "done"
		elif self.editMode:
			self.editMode = False
			for x in self.moreViewButtons:
				x.background_color = "white"
			sender.title = "edit"
				
	def moreSelectMode(self, sender):
		if self.selectMode == False:
			self.selectMode = True
			for x in self.moreViewButtons:
				x.background_color = "#2ce56d"
			sender.title = "seek"
		elif self.selectMode:
			self.selectMode = False
			for x in self.moreViewButtons:
				x.background_color = "white"
			sender.title = "select"





#############################
#############################
#############################
#     CustomView Class      #

#holds all data and functionality
#for each custom view that was 
#created in the more views section

class CustomView:
	def __init__(self, serialNum):
		
		self.view = ui.View()
		self.view.background_color = "f0fff5"	
		
		self.addTaskButton = createAddTaskButton(self, "customTask")
		self.editButton = createEditButton(self, "c")
		
		self.tasks, self.options = lifelpDataBase.loadCustomView(serialNum)
		self.serialNum = serialNum
		self.button = None
		
		self.chosenTaskOptions = []
		self.availableTaskOptions = []
		self.buttonNeedingLink = None
		
		#taskOption 1
		self.availableTaskOptions.append(SettingOption("name", "s", None))
		
		#TaskOption 2
		self.availableTaskOptions.append(SettingOption("action", "c", ["view:", "note", "distribute"]))
		
		
		#viewOption 1
		
		#viewOption 2
		self.completable = False
		
		if self.options[1] == True:
			self.completable = True
		
		numTasks = 1
		for task in self.tasks:
			h = (30 + 40*x)
			if self.completable or self.tasks[task]:
				button = ui.Button(title = str(numTasks))
				self.taskButtons.append(button)
				button.name = str(numTasks)
				button.center = (35, h)
				if self.tasks[task].complete:
					button.background_color = "#2ce56d"
				else:
					button.background_color = "red"
			label = ui.Label()
			self.taskLabels.append(label)
			label.text = task
			label.center = (125, h)
			label.flex = "w"
			self.view.add_subview(button)
			self.view.add_subview(label)
			numTasks+=1
			x+=1
	
	def openCustomTaskOptions(self, sender):
		self.chosenOptions = []
		
		view = ui.View()
		self.optionsView = view
		view.background_color = "f0fff5"
		
		if sender == "edit":
			x = 0
			for option in self.availableTaskOptions:
				label = ui.Label(text = option.name, center = (100, 75 + 45*int(x)))
				
				view.add_subview(label)
				#needs boolean value
				if option.type == "b":
					button = ui.Button(title = "XXX")
					button.center = (275, 80 + 45*int(x))
					button.action = activateBoolButton
					button.name = "b" + str(x)
					view.add_subview(button)
					if self.curView.options[x] == True:
						button.title = "yes"
						button.background_color = "2ce56d"
					elif self.curView.options[x] == False:
						button.title = "no"
						button.background_color = "red"
					self.chosenOptions.append(button)
				#needs string value
				elif option.type == "s":
					textField = ui.TextField(frame = (200, 60 + 45*int(x), 150, 35))
					textField.name = "s" + str(x)
					textField.text = self.curView.options[x]
					view.add_subview(textField)
					self.chosenOptions.append(textField)
				elif option.type == "c":
					button = ui.Button(title = "XXXXXXXXX")
					button.center = (250, 80 + 45*int(x))
					button.action = option.cycleChoice
					button.name = "b" + str(x)
					button.background_color = "white"
					view.add_subview(button)
					button.title = curView.options[x]
				x+=1
				
			createCreateButton(view, "save", "t")
		else:
			x = 0
			for option in self.availableTaskOptions:
				label = ui.Label(text = option.name, center = (100, 75 + 45*int(x)))
				
				view.add_subview(label)
				#needs boolean value
				if option.type == "b":
					button = ui.Button(title = "XXX")
					button.center = (275, 80 + 45*int(x))
					button.action = activateBoolButton
					button.name = "b" + str(x)
					view.add_subview(button)
					button.title = "no"
					button.background_color = "red"
					self.chosenOptions.append(button)
				#needs string value
				elif option.type == "s":
					textField = ui.TextField(frame = (200, 60 + 45*int(x), 150, 35))
					textField.name = "s" + str(x)
					view.add_subview(textField)
					self.chosenOptions.append(textField)
				elif option.type == "c":
					button = ui.Button(title = "XXXXXXXXX")
					button.center = (250, 80 + 45*int(x))
					button.action = option.cycleChoice
					button.name = "b" + str(x)
					button.background_color = "white"
					view.add_subview(button)
					button.title = option.choices[0]
					option.addHelperButton(option.choices[0])
				x+=1
				
			createCreateButton(view, "create", "t")
		view.present("fullscreen")
		
	def setCustomTaskSettings(self, sender):
		for x in self.chosenOptions:
			index = int(x.name[1])
			type = x.name[0]
			if type == "b":
				if x.title == "yes":
					self.chosenOptions[index] = True
				elif x.title == "no":
					self.chosenOptions[index] = False
			elif type == "s":
				self.chosenOptions[index] = self.chosenOptions[index].text
			elif type == "c":
				self.chosenOptions[index] = self.chosenOptions[index].title + self.availableTaskOptions[index].helperButton.title
			
			
			
			
			button = ui.Button(title = "00000000000")
			button.center = (55 + 150 * self.x, 50 + 40 * self.y)
			button.background_color = "white"
			button.action = self.openCustomView
			self.view.add_subview(button)
			button.title = self.homeViews[serialNum]
			button.name = serialNum
			self.moreViewButtons.append(button)
			self.x+=1
			if self.x%3 == 0:
				self.x = 0
				self.y+=1
				
		else:
			self.curView.options = self.chosenOptions
			name = self.curView.options[0]
			if self.curView.button.title != name:
				self.curView.button.title = name
				self.allViews[self.curView.serialNum] = name
				self.homeViews[self.curView.serialNum] = name
				
				lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
				lifelpDataBase.saveMoreViewsHome(self.homeViews)
			lifelpDataBase.saveCustomView(self.curView.serialNum, self.curView.options, self.curView.tasks)
		
			#then i guess i should just re-present the physicsl view
		self.optionsView.close()	
	
	def customEditMode(self, sender):
		print("yo")
		
	def linkView(self, serialNum):
		moreViews.curView.buttonNeedingLink.title = serialNum
	
	
	
		







	
	
	
	
	

	

#############################
#############################
#############################
# Button creation functions #

def createAddTaskButton(viewClass, action):
	button = ui.Button(font = ('<system-bold>', 70), title = "0")
	button.center = (200, 725)
	viewClass.view.add_subview(button)
	if action == "task":
		button.action = viewClass.addTask
	elif action == "preset":
		button.action = viewClass.addPreset
	elif action == "customView":
		button.action = viewClass.openCustomViewOptions
	elif action == "customTask":
		button.action = viewClass.openCustomTaskOptions
	
	button.title = "+"
	return button
	
def createEditButton(view, type):
	button = ui.Button(title = "XXXXXX")
	button.center = (315, 700)
	button.title = "edit"
	
	if type == "p":
		global presetWindow
		button.action = presetWindow.presetEditMode
		view.add_subview(button)
	elif type == "d":
		button.action = dayEditMode
		view.add_subview(button)
	elif type == "c":
		button.action = view.customEditMode
		view.view.add_subview(button)
	elif type == "mr":
		button.action = view.moreEditMode
		view.view.add_subview(button)
	elif type == "ms":
		button.title = "select"
		button.action = view.moreSelectMode
		view.view.add_subview(button)
	return button

def createCreateButton(view, title, type):
	preset = ui.Button(font = ('<system-bold>',30), title = title)
	preset.flex = "LRTB"
	preset.center = (50, 70)
	preset.background_color = "white"
	if type == "v":
		preset.action = moreViews.setCustomViewSettings
	elif type == "t":
		moreViews.curView.setCustomTaskSettings
	view.add_subview(preset)

def createMoreViewsButton(view):
	preset = ui.Button(font = ('<system-bold>',20), title = "more views")
	preset.flex = "LRTB"
	preset.center = (50, 77)
	preset.background_color = "white"
	preset.action = moreViews.showView
	view.add_subview(preset)

def createPresetButton(view):
	preset = ui.Button(font = ('<system-bold>',20), title = "presets")
	preset.flex = "LRTB"
	preset.center = (60, 77)
	preset.background_color = "white"
	preset.action = presetWindow.showPresetView
	view.add_subview(preset)

def createBankButton(view):
	bankBut = ui.Button(font = ('<system-bold>',20), title = "bank")
	bankBut.flex = "LRTB"
	bankBut.center = (35, 77)
	bankBut.background_color = "white"
	bankBut.action = showBankView
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
	
def createTrashButton(view):
	button = ui.Button(font = ('<system-bold>', 40), title = "trash")
	button.action = deleteBankTask
	button.center = (215, 650)
	return button
	

		
	
#############################
#############################
#############################
#           setup           #	
	
def setup():
	global data
	global bank
	global today
	global todayS
	today = datetime.date.today()
	todayS = str(today)
	data = lifelpDataBase.getData(today)
	
	bank = Bank()
	createDateButtons(todayS, bank.newDay)
	
	
	
	
	
#############################
#############################
#############################
#          globals          #

mainView = MyMainView()
moreViews = MoreViews("r")
presetWindow = Presets()
bank = None
myDayView = MyDayView()

today = None
todayS = ""

data = {}
dataKeys = {}


setup()




  
