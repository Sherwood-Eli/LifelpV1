import ui
import datetime
import time
import lifelpDataBase
import lifelpAUX
import gc
			


#move this into preset class later
def setDayFrequency(sender):
	if sender.background_color == (1.0, 0.0, 0.0, 1.0):
		sender.background_color = "2ce56d"
	else:
		sender.background_color = "red"


		
	

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
			
def deleteBankTask(sender):
	global mainView
	global bank
	
	del bank.bank[bank.fromBankInfo]
	bank.bankKeys.remove(bank.fromBankInfo)
	bank.fromBankInfo = ""
	mainView.view.remove_subview(mainView.trashButton)
	lifelpDataBase.saveBank(bank)
			
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
		self.screenWidth, self.screenHeight = ui.get_screen_size()

		self.view = ui.View(background_color = "f0fff5")
		self.nav = ui.NavigationView(self.view)
		
		self.dateButtons = []
		self.sundayIndexViewed = 0
		self.monthBeingViewed = todayS[0:7]
		
		self.trashButton = createTrashButton(self.view)
		self.todayIndex = lifelpAUX.findTodayIndex(todayS, data)
		self.curDayView = None
		self.createDateButtons()
	
	def createDayView(self, sender):
		self.curDayView = MyDayView(sender)
	
	def createDateButtons(self):
		global todayS
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
				
		needApplyPresets = bank.newDay and lifelpAUX.isNewWeek(data[curMonth].dataKeys[self.sundayIndex], bank.lastLastLog)
		
		
		#each iteration prepares a day button for the main view
		tempSundInd = self.sundayIndex
		for x in range(0,7):
			#if month ends mid week
			if (tempSundInd + x == len(data[curMonth].days)):
				curMonth = lifelpAUX.incrFileKey(curMonth)
				#sundayIndex - 7 to use next month sunday index
				tempSundInd = int(data[curMonth].sundayIndex) - 7
				alteredMonths.append(curMonth)
				
			#adds the date button with temporary label to set size
			button = ui.Button(title = "0000000000")
			button.center = (80, (50 + (55*x)))
			button.border_color = "black"
			button.border_width = 1
			button.background_color = "white"
			button.action = self.createDayView
			self.dateButtons.append(button)
			#highlights current day
			if (self.sundayIndex + x) == (self.todayIndex):
				button.border_color = "#2ce56d"
				button.border_width = 5
		
			#change title of dateButton after being added to view so it can have a set space
			button.title = data[curMonth].dataKeys[tempSundInd + x]
			data
			self.view.add_subview(button)
			
			
			#figuring out what color to make the dateButton
			day = data[curMonth].days[button.title]
			day.buttonIndex = x
			

		
			if needApplyPresets:
				dayValue = 2**x
				for preset in presetWindow.presets:
					if presetWindow.presets[preset].frequency & dayValue:
						presetWindow.placePreset(preset, x, self.sundayIndex)
						
			setDateButtonColor(button, day)

			#adds dayLabel next to dateButton
			dayLabel = ui.Label(text = daysOfWeek[x], font = ('<system-bold>', 20))
			dayLabel.center = (60,  (50 + (55*x)))
			self.view.add_subview(dayLabel)
			
		createPresetButton(self.view)
		createMoreViewsButton(self.view)
		createBankButton(self.view)
		createPrevButton(self)
		createNextButton(self)
		
		self.nav.present("fullscreen", hide_title_bar=True)
				
		self.sundayIndexViewed = self.sundayIndex
		
		if needApplyPresets:
			for x in alteredMonths:
				lifelpDataBase.saveData(x, data)
		
	
	def changeWeek(self, sender):
		global todayS
		global data
		
		if sender.title == "prev":
			self.sundayIndexViewed-=7
			if self.sundayIndexViewed < 0:
				mainView.monthBeingViewed = lifelpAUX.decrFileKey(mainView.monthBeingViewed)
				try:
					self.sundayIndexViewed = len(data[mainView.monthBeingViewed].days) + self.sundayIndexViewed
				except KeyError:
					data[mainView.monthBeingViewed] = lifelpDataBase.loadData(mainView.monthBeingViewed)
					self.sundayIndexViewed = len(data[mainView.monthBeingViewed].days) + self.sundayIndexViewed
		else:
			self.sundayIndexViewed+=7
		for x in range(0, len(self.dateButtons)):
			oldLabel = self.dateButtons[x].title
			data[oldLabel[0:7]].days[oldLabel].buttonIndex = -1
			#if month ends mid week
			if (self.sundayIndexViewed + x >= len(data[mainView.monthBeingViewed].days)):
				mainView.monthBeingViewed = lifelpAUX.incrFileKey(mainView.monthBeingViewed)
				# to use next month sunday index
				try:
					self.sundayIndexViewed = int(data[mainView.monthBeingViewed].sundayIndex) - 7
				except KeyError:
					data[mainView.monthBeingViewed] = lifelpDataBase.loadData(mainView.monthBeingViewed)
					self.sundayIndexViewed = int(data[mainView.monthBeingViewed].sundayIndex) - 7
				if self.sundayIndexViewed == -7:
					self.sundayIndexViewed = 0
			button = self.dateButtons[x]
			button.title = data[mainView.monthBeingViewed].dataKeys[self.sundayIndexViewed + x]
			day = data[mainView.monthBeingViewed].days[button.title]
			day.buttonIndex = x
			setDateButtonColor(button, day)
			if button.title == todayS:
				button.border_width = 5
			else:
				button.border_color = "black"
				button.border_width = 1
				
				
				
				
#############################
#############################
#############################
#      MyDayView Class      #
			
#Holds all data and functionality 
#for the curent day being viewed
					
class MyDayView:
	def __init__(self, sender):	
		global data
		global bank
		global todayS
		
		self.editMode = False
		self.textField = ui.TextField(frame = (20, 400, 375, 50))
		self.textField.action = self.createTask
		
		
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
				h = (70 + 40*x)
				button = ui.Button(title = str(numTasks))
				self.taskButtons.append(button)
				button.name = str(numTasks)
				button.center = (35, h)
				if tasks[task].complete:
					button.background_color = "#2ce56d"
				else:
					button.background_color = "red"
				if lifelpAUX.date1GreaterThan2(bank.lastLastLog, curDate) == False:
					button.action = self.taskButton
				label = ui.Label()
				self.taskLabels.append(label)
				label.text = task
				label.center = (125, h)
				label.flex = "w"
				self.view.add_subview(button)
				self.view.add_subview(label)
				numTasks+=1
				x+=1
			if lifelpAUX.date1GreaterThan2(todayS, curDate) == False:
				createAddTaskButton(self, "task")
				self.editButton = createEditButton(self, "d")
				editMode = False
			mainView.nav.push_view(self.view)
		else:
			date = sender.title
			
			data[date[0:7]].days[date].tasks[bank.fromBankInfo] = lifelpDataBase.Task()
			data[date[0:7]].days[date].tasks[bank.fromBankInfo].type = "b"
			
			bank.bank[bank.fromBankInfo].outCount+=1
			bank.fromBankInfo = ""
			
			mainView.view.remove_subview(mainView.trashButton)
			setDateButtonColor(sender, data[date[0:7]].days[date])
			
			lifelpDataBase.saveData(month, data)
			lifelpDataBase.saveBank(bank)	
	
	def addTask(self, sender):
		self.view.add_subview(self.textField)
	
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
				button.title = "🗑️"
				button.background_color = "#ff591e"
	
	def createTask(self, textfield):
		global data
		self.view.remove_subview(self.textField)
		if textfield.text != "":
			month = self.date[0:7]
			day = data[month].days[self.date]
			numTasks = len(day.tasks) + 1
			day.tasks[textfield.text] = lifelpDataBase.Task()
			lifelpDataBase.saveData(month, data)
			h = 70 + (40*numTasks)
			button = ui.Button(title = str(numTasks))
			self.taskButtons.append(button)
			button.name = str(numTasks)
			button.flex = "w"
			button.center = (35, h - 40)
			if self.editMode:
				button.title = "🗑️"
				button.background_color = "#ff591e"
			else:
				button.background_color = "red"
			button.action = self.taskButton
			labelText = textfield.text
			label = ui.Label(text = labelText)
			self.taskLabels.append(label)
			label.center = (125, h)
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
		if sender.title == "🗑️":
			indexToDelete = int(sender.name) - 1
			maxIndex = len(self.taskButtons) - 1
			#can only delete things from present and future days so this is coo
			if tasks[taskKeys[indexToDelete]].type == "b": 
				bank.bank[taskKeys[indexToDelete]].outCount -= 1
				bank.bank[taskKeys[indexToDelete]].dates.remove(day)
				lifelpDataBase.saveBank(bank)
			del tasks[taskKeys[indexToDelete]]
			del taskKeys[indexToDelete]
			self.view.remove_subview(self.taskButtons[indexToDelete])
			self.view.remove_subview(self.taskLabels[indexToDelete])
			del self.taskButtons[indexToDelete]
			del self.taskLabels[indexToDelete]
			for x in range(indexToDelete, maxIndex):
				self.taskLabels[x].center.y -= 40
				self.taskLabels[x].name = str(x)
				self.taskButtons[x].center.y -= 40
				self.taskButtons[x].name = str(x)
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
		mainView.nav.push_view(self.view)
	
	def cleanBank(self):
		tasksToDelete = []
		for task in self.bank:
			if self.bank[task].complete:
				dayS = self.bank[task].dates[len(self.bank[task].dates) - 1]
				for date in self.bank[task].dates:
					newKey = task + " " + dayS
					newTask = lifelpDataBase.Task()
					newTask.complete = True
					data[date[0:7]].days[date].tasks[newKey] = newTask
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
		mainView.nav.pop_view()
		




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
		self.view = None
		self.textField = ui.TextField(frame = (20, 400, 375, 50))
		self.textField.action = self.savePreset

	
	def addPreset(self, sender):
		self.view.add_subview(self.textField)
	
	def showPresetView(self, sender):
		global editMode
		editMode = False
		if self.view == None:
			self.view = ui.View(background_color = "f0fff5")
			
			self.freqLabel = ui.Label(text = "Frequency", font = ('<system-bold>',20))
			self.freqLabel.center = (350, 30)
			presetLabel = ui.Label(text = "Task", font = ('<system-bold>',20))
			presetLabel.center = (180, 30)
			
			self.view.add_subview(self.freqLabel)
			self.view.add_subview(presetLabel)
			createAddTaskButton(self, "preset")
			x = 0
			for preset in self.presets:
				h = 70 + (40*x)
				
				labelButton = ui.Button(title = preset, font = ('<system>',20))
				labelButton.action = self.assignPreset
				labelButton.center = (150, h)
				self.view.add_subview(labelButton)
				self.presets[preset].labelButton = labelButton
				
				editButton = ui.Button(title = "X")
				editButton.center = (350, h)
				editButton.background_color = 	"#ff591e"
				editButton.action = self.deletePreset
				editButton.name = str(x)
				self.presets[preset].editButton = editButton
				
					
				days = "smtwtfs"
				place=0
				for day in days:
					button = ui.Button(action = self.setFrequency, frame = (290 + 16*place, h-16, 16, 30))
					if self.presets[preset].frequency & (2**place):
						button.background_color = "2ce56d"
					else:
						button.background_color = "red"
					self.presets[preset].frequencyButtons.append(button)
					self.view.add_subview(button)
					button.title = day
					button.name = str(x) + str(place)
					place+=1
				
				x+=1
			createEditButton(self, "p")
				
		mainView.nav.push_view(self.view)
		
	def presetEditMode(self, sender):
		global editMode
		if sender.title == "edit":
			sender.title = "done"
			editMode = True
			self.view.remove_subview(self.freqLabel)
			for preset in self.presets:
				for x in self.presets[preset].frequencyButtons:
					self.view.remove_subview(x)
				self.view.add_subview(self.presets[preset].editButton)
				
		elif sender.title == "done":
			sender.title = "edit"
			editMode = False
			self.view.add_subview(self.freqLabel)
			for preset in self.presets:
				for x in self.presets[preset].frequencyButtons:
					self.view.add_subview(x)
				
				self.view.remove_subview(self.presets[preset].editButton)
	
		
	def setFrequency(self, sender):
		preset = self.presetKeys[int(sender.name[0])]
		place = int(sender.name[1])
		valueChange = 2**place
		
		if sender.background_color == (1.0, 0.0, 0.0, 1.0):
			sender.background_color = "2ce56d"
			self.presets[preset].frequency+=valueChange
			
			day = self.placePreset(preset, place, mainView.sundayIndex)
			
			if day != None:
			
				setDateButtonColor(mainView.dateButtons[place], day)
		
		else:
			sender.background_color = "red"
			self.presets[preset].frequency-=valueChange
			
			self.removePreset(preset, place)
			
		lifelpDataBase.savePresets(self.presets)
			
	def assignPreset(self, sender):
		if self.presets[sender.title].auto == False:
			self.view.close()
	
	def savePreset(self, sender):
		newPreset = sender.text
		sender.text = ""
		self.view.remove_subview(sender)
		
		if newPreset in self.presets:
			print("there is already a preset with this name")
			
		elif newPreset != "":
			h = 70 + (40*self.numPresets)
			
			editButton = ui.Button(title = "X")
			editButton.center = (350, h)
			editButton.background_color = 	"#ff591e"
			editButton.action = self.deletePreset
			editButton.name = str(self.numPresets)
			
			if editMode:
				self.view.add_subview(editButton)
			
			presetButton = ui.Button(title = newPreset, font = ('<system>',20))
			presetButton.action = self.assignPreset
			presetButton.center = (150, h)
			self.view.add_subview(presetButton)	
			
			frequButtons = []
			days = "smtwtfs"
			place=0
			for day in days:
				button = ui.Button(action = self.setFrequency, background_color = "red", title = day)
				button.frame = (290 + 16*place, h-16, 16, 30)
				button.name = str(self.numPresets) + str(place)
				
				frequButtons.append(button)
				self.view.add_subview(button)
				
				place+=1
			
			self.numPresets+=1
			
			self.presetKeys.append(newPreset)
			self.presets[newPreset] = lifelpDataBase.PresetTask(0)
			
			self.presets[newPreset].labelButton = presetButton
			self.presets[newPreset].editButton = editButton
			self.presets[newPreset].frequencyButtons = frequButtons
			
			
			lifelpDataBase.savePresets(self.presets)
			
	def deletePreset(self, sender):
		indexToDelete = int(sender.name)
		presetToDelete = self.presetKeys[indexToDelete]
		
		self.view.remove_subview(self.presets[presetToDelete].labelButton)
		self.view.remove_subview(self.presets[presetToDelete].editButton)
		
		for b in self.presets[presetToDelete].frequencyButtons:
			self.view.remove_subview(b)
			if b.background_color != (1.0, 0.0, 0.0, 1.0):
					self.removePreset(presetToDelete, int(b.name[1]))
		
		for x in range(len(self.presetKeys) - 1, indexToDelete, -1):
			h = 70 + (40*(x-1))
			preset = self.presets[self.presetKeys[x]]
			
			preset.labelButton.name = str(x-1)
			preset.labelButton.center = (150, h)
			
			preset.editButton.name = str(x-1)
			preset.editButton.center = (350, h)
			
			place = 0
			for b in preset.frequencyButtons:
				b.name = str(x-1)
				b.frame = (290 + 16*place, h-16, 16, 30)
				place+=1
		
		del self.presets[presetToDelete]
		del self.presetKeys[indexToDelete]
		self.numPresets-=1
		
		lifelpDataBase.savePresets(self.presets)
			
	def placePreset(self, preset, place, tempSunInd):
		global data
		global mainView
		today = datetime.date.today()
		todayS = str(today)
		dataKey = todayS[0:7]	
	
		if tempSunInd + place >= len(data[dataKey].days):
			dataKey = lifelpAUX.incrFileKey(dataKey)
			tempSunInd = data[dataKey].sundayIndex - 7
		date = data[dataKey].dataKeys[tempSunInd + place]
		
		if not lifelpAUX.date1GreaterThan2(todayS, date):
			
			day = data[dataKey].days[date]
			
			day.tasks[preset] = lifelpDataBase.Task()
			day.tasks[preset].complete = False
			day.tasks[preset].type = "p"
			
			lifelpDataBase.saveData(dataKey, data)
			
			return day
			
		
	
	def removePreset(self, preset, place):
		global data
		global mainView
		todayS = str(datetime.date.today())		
		dataKey = todayS[0:7]
		tempSunInd = mainView.sundayIndex		
		
		if tempSunInd + place >= len(data[dataKey].days):
			dataKey = lifelpAUX.incrFileKey(dataKey)
			tempSunInd = data[dataKey].sundayIndex - 7
		date = data[dataKey].dataKeys[tempSunInd + place]
		if not lifelpAUX.date1GreaterThan2(todayS, date):
			
			day = data[dataKey].days[date]
		
			if preset in day.tasks:
				del day.tasks[preset]
			
			setDateButtonColor(mainView.dateButtons[place], day)
			
			lifelpDataBase.saveData(dataKey, data)




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
		self.helperButtonActive = False
		
	def addHelperButton(self, index):
		kind = self.choices[index]
		if self.helperButton == None:
			button = ui.Button(title = "XXXX")
			button.center = (325, 80 + 45)
			button.background_color = "white"
			button.name = "select"
			self.helperButton = button
		if kind == "view":
			self.helperButton.action = moreViews.chooseViewLink
			moreViews.customTaskOptionsView.add_subview(self.helperButton)
			self.helperButton.title = "none"
			self.helperButtonActive = True
		else:
			helperButtonActive = False
			moreViews.customTaskOptionsView.remove_subview(self.helperButton)
		
		
	
	def cycleChoice(self, sender):
		self.choiceIndex+=1
		if self.choiceIndex%len(self.choices) == 0:
			self.choiceIndex = 0
		sender.title = self.choices[self.choiceIndex]
		if self.helperButtonActive:
			moreViews.customTaskOptionsView.remove_subview(self.helperButton)
			self.helperButtonActive = False
		self.addHelperButton(choiceIndex)










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
		
		#make view icons
		
		self.allViews, self.numSlots, self.availableSlots = lifelpDataBase.loadMoreViewsAll()
		self.homeViews = lifelpDataBase.loadMoreViewsHome()
		
		self.curView = None
		self.viewPath = []
		self.openViews = {}
	
		for viewKey in self.homeViews:
			button = ui.Button(title = "00000000000000000000")
			button.center = (105 + 205 * self.x, 40 + 40 * self.y)
			button.background_color = "white"
			button.border_color = "black"
			button.border_width = 1
			button.action = self.openCustomViewFromHome
			self.view.add_subview(button)
			button.title = self.homeViews[viewKey]
			button.name = viewKey
			self.moreViewButtons.append(button)
			self.x+=1
			if self.x%2 == 0:
				self.x = 0
				self.y+=1
				
	def finishSetup(self):
		#view options
		self.chosenViewOptions = []
		self.availableViewOptions = []
		
		#option 1
		self.availableViewOptions.append(SettingOption("title", "s", []))
		
		#option 2
		self.availableViewOptions.append(SettingOption("completable", "b", []))
	
		self.customViewOptionsView = ui.View(background_color = "f0fff5")
		self.customViewOptionsConfirmButton = createCreateButton(self.customViewOptionsView, "create", "v")
		
		self.customViewOptionsTrashButton = createOptionsTrashButton("v")
		
		self.customViewOptionsConfirmDeleteLabel = ui.Label(text="delete view?", center=(80,670))
		
		self.customViewOptionsConfirmDeleteButton = ui.Button(title="yes", border_color="black", border_width=1, background_color="white", action=self.confirmDelete, center=(45, 700))
		
		self.customViewOptionsDeclineDeleteButton = ui.Button(title="no", border_color="black", border_width=1, background_color="white", action=self.declineDelete, center=(80, 700))
		
		self.putOptionsOnView(self.customViewOptionsView, self.availableViewOptions, self.chosenViewOptions)

		
		#task options
		self.chosenTaskOptions = []
		self.availableTaskOptions = []
		
		#taskOption 1
		self.availableTaskOptions.append(SettingOption("title", "s", None))
		
		#TaskOption 2
		self.availableTaskOptions.append(SettingOption("action", "c", ["view", "note", "distribute"]))
		
		self.customTaskOptionsView = ui.View(background_color = "f0fff5")
		#we pass v because we need to change action to a method of a specific opjext later on
		self.customTaskOptionsConfirmButton = createCreateButton(self.customTaskOptionsView, "create", "v")
		
		self.putOptionsOnView(self.customTaskOptionsView, self.availableTaskOptions, self.chosenTaskOptions)
		
		
	def putOptionsOnView(self, view, availableOptions, chosenOptions):
		x = 0
		for option in availableOptions:
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
				chosenOptions.append(button)
			#needs string value
			elif option.type == "s":
				textField = ui.TextField(frame = (200, 60 + 45*int(x), 150, 35))
				textField.name = "s" + str(x)
				textField.text = ""
				view.add_subview(textField)
				chosenOptions.append(textField)
			elif option.type == "c":
				button = ui.Button(title = "XXXXXXXXX")
				button.center = (250, 80 + 45*int(x))
				button.action = option.cycleChoice
				button.name = "c" + str(x)
				button.background_color = "white"
				view.add_subview(button)
				button.title = option.choices[0]
				option.addHelperButton(0)
				chosenOptions.append(button)
			x+=1
		
		
	def showView(self, sender):
		if self.editMode:
			self.moreEditMode(self.editButton)
		mainView.nav.push_view(self.view)
		
	def chooseViewLink(self, sender):
		self.curView.buttonNeedingLink = sender
		self.selectView.view.present("fullscreen", hide_title_bar=True)
			
	def openCustomViewFromHome(self, sender):
		if self.editMode:
			self.curView = self.getView(sender.name)
			self.curView.button = sender
			self.openCustomViewOptions("edit")
		else:
			self.openCustomView(sender.name)
			
	#opens a view for viewing
	def openCustomView(self, serialNum):
		if self.selectMode:
			moreViews.curView.linkView(serialNum)
			#closeOtherViews too
			self.view.close()
		else:
			self.curView = self.getView(serialNum)
			mainView.nav.push_view(self.curView.view)
		
		
	#this is old
	def previousView(self, sender):
		nextView = self.getView(self.viewPath.pop())
		if nextView != None:
			
			nextView.view.present("fullscreen")
		self.curView.view.close()
		self.curView = nextView
	
	#gets a view if it is already open, else open a view
	def getView(self, serialNum):
		if serialNum == None:
			return None
		
		#i might add some sort of reference counter thing to close ones we dont want after a while to increase efficiency
		if serialNum not in self.openViews:
			self.openViews[serialNum] = CustomView(serialNum)
			
		return self.openViews[serialNum]
		
	def openCustomViewOptions(self, mode):
		editMode = False
		if mode == "edit":
			editMode = True
		x = 0
		for option in self.availableViewOptions:
			if option.type == "b":
				if not editMode or self.curView.options[x] == False:
					self.chosenViewOptions[x].title = "no"
					self.chosenViewOptions[x].background_color = "red"
				elif self.curView.options[x] == True:
					self.chosenViewOptions[x].title = "yes"
					self.chosenViewOptions[x].background_color = "2ce56d"
			elif option.type == "s":
				if editMode:
					self.chosenViewOptions[x].text = self.curView.options[x]
				else:
					self.chosenViewOptions[x].text = ""
			x+=1
		if editMode:
			self.customViewOptionsConfirmButton.title = "save"
			self.customViewOptionsConfirmButton.center = (300, 700)
			self.customViewOptionsView.add_subview(self.customViewOptionsTrashButton)
			self.customViewOptionsView.remove_subview(self.customViewOptionsConfirmDeleteButton)
			
			self.customViewOptionsView.remove_subview(self.customViewOptionsConfirmDeleteLabel)
			
			self.customViewOptionsView.remove_subview(self.customViewOptionsDeclineDeleteButton)
		else:
			self.customViewOptionsConfirmButton.title = "create"
			self.customViewOptionsConfirmButton.center = (210, 700)
			self.customViewOptionsView.remove_subview(self.customViewOptionsTrashButton)
		
		self.customViewOptionsView.present("fullscreen")
		
		
	def promptConfirmDelete(self, sender):
		self.customViewOptionsView.remove_subview(self.customViewOptionsTrashButton)
		self.customViewOptionsView.add_subview(self.customViewOptionsConfirmDeleteLabel)
		self.customViewOptionsView.add_subview(self.customViewOptionsConfirmDeleteButton)
		
		self.customViewOptionsView.add_subview(self.customViewOptionsDeclineDeleteButton)
	
	def confirmDelete(self, sender):
		self.deleteCurView()
		
		self.customViewOptionsView.close()
		
		
	def declineDelete(self, sender):
		self.customViewOptionsView.remove_subview(self.customViewOptionsConfirmDeleteLabel)
		self.customViewOptionsView.remove_subview(self.customViewOptionsConfirmDeleteButton)
		
		self.customViewOptionsView.remove_subview(self.customViewOptionsDeclineDeleteButton)
		
		self.customViewOptionsView.add_subview(self.customViewOptionsTrashButton)
		
	def deleteCurView(self):
		serialNum = self.curView.serialNum
		self.availableSlots.append(serialNum)
		del(self.allViews[serialNum])
		del(self.homeViews[serialNum])
		
		for button in self.moreViewButtons:
			self.view.remove_subview(button)
			del(button)
			
		for viewKey in self.homeViews:
			button = ui.Button(title = "00000000000000000000")
			button.center = (105 + 205 * self.x, 40 + 40 * self.y)
			button.background_color = "white"
			button.border_color = "black"
			button.border_width = 1
			button.action = self.openCustomViewFromHome
			self.view.add_subview(button)
			button.title = self.homeViews[viewKey]
			button.name = viewKey
			self.moreViewButtons.append(button)
			self.x+=1
			if self.x%2 == 0:
				self.x = 0
				self.y+=1
				
		lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
		lifelpDataBase.saveMoreViewsHome(self.homeViews)
		
		gc.collect()
			
	def setCustomViewSettings(self, sender):
		options = [None] * len(self.chosenViewOptions)
		for x in self.chosenViewOptions:
			index = int(x.name[1])
			type = x.name[0]
			if type == "b":
				if x.title == "yes":
					options[index] = True
				elif x.title == "no":
					options[index] = False
			elif type == "s":
				options[index] = self.chosenViewOptions[index].text
		if sender.title == "create":
			if len(self.availableSlots) == 0:
				self.numSlots+=1
				serialNum = str(self.numSlots)
			else:
				serialNum = self.availableSlots.pop(0)
			
			lifelpDataBase.createCustomViewData(serialNum, options)
				
			self.allViews[serialNum] = options[0]
			self.homeViews[serialNum] = options[0]
			
			lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
			lifelpDataBase.saveMoreViewsHome(self.homeViews)
			
			#then i gotta add the view to the physical home view
			
			button = ui.Button(title = "00000000000000000000")
			button.center = (105 + 205 * self.x, 40 + 40 * self.y)
			button.background_color = "white"
			button.action = self.openCustomViewFromHome
			button.border_color = "black"
			button.border_width = 1
			self.view.add_subview(button)
			button.title = self.homeViews[serialNum]
			button.name = serialNum
			self.moreViewButtons.append(button)
			self.x+=1
			if self.x%2 == 0:
				self.x = 0
				self.y+=1
				
		else:
			self.curView.options = options
			
			#handles a name change
			name = self.curView.options[0]
			if self.curView.button.title != name:
				self.curView.button.title = name
				self.allViews[self.curView.serialNum] = name
				self.homeViews[self.curView.serialNum] = name
				
				lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
				lifelpDataBase.saveMoreViewsHome(self.homeViews)
			
			#this could be improved by having some variable keep track of wether or not anything has actually changed and if not, bypass update
			self.curView.createView()
			lifelpDataBase.saveCustomView(self.curView.serialNum, self.curView.options, self.curView.tasks)
		
			#then i guess i should just re-present the physicsl view
		self.customViewOptionsView.close()
	
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
		self.view = None
		
		self.tasks = []
		taskOptions, taskCompleted, taskPositions, self.options = lifelpDataBase.loadCustomView(serialNum)
		for x in range(len(taskOptions)):
			task = CustomTask(taskPositions[x], taskCompleted[x], taskOptions[x])
			self.tasks.append(task)
		
		self.serialNum = serialNum
		self.button = None
		
		self.buttonNeedingLink = None
		
		self.createView()
		
			
	def createView(self):
		if self.view != None:
			del self.view
			gc.collect()
		
		self.view = ui.View(background_color = "f0fff5")
		self.addTaskButton = createAddTaskButton(self, "customTask")
		self.editButton = createEditButton(self, "c")
		
		#viewOption 1
		
		#viewOption 2
		self.completable = False
		
		if self.options[1] == True:
			self.completable = True
		
		for task in self.tasks:
			self.view.add_subview(task.button)
			if self.completable:
				completionButton = task.addCompletionButton()
				self.view.add_subview(completionButton)
	
			
	def createTask(self, sender):
		self.openCustomTaskOptions("create", 0)
		
	def editTask(self, position):
		self.openCustomTaskOptions("edit", position)
	
	
	def openCustomTaskOptions(self, mode, p):
		editMode = (mode == "edit")
		x = 0
		for option in moreViews.availableTaskOptions:
			#needs boolean value
			if option.type == "b":
				if editMode and self.tasks[p].options[x] == True:
					moreViews.chosenTaskOptions[x].title = "yes"
					moreViews.chosenTaskOptions[x].background_color = "2ce56d"
				else:
					moreViews.chosenTaskOptions[x].title = "no"
					moreViews.chosenTaskOptions[x].background_color = "red"
			#needs string value
			elif option.type == "s":
				if editMode:
					moreViews.chosenTaskOptions[x].text = self.tasks[p].options[x]
				else:
					moreViews.chosenTaskOptions[x].text = ""
			elif option.type == "c":
				if editMode:
					choiceIndex = self.tasks[p].options[x][0]
					moreViews.chosenTaskOptions[x].title = option.choices[choiceIndex]
					option.addHelperButton(choiceIndex)
					option.helperButton.title = self.tasks[p].options[x][1]
				else:
					moreViews.chosenTaskOptions[x].title = option.choices[0]
					option.addHelperButton(0)
			x+=1
				
			if editMode:
				moreViews.customTaskOptionsConfirmButton.title = "save"
				self.curTask = self.tasks[p]
				#moreViews.customTaskOptionsConfirmButton.center = (55, 70)
			else:
				moreViews.customTaskOptionsConfirmButton.title = "create"
				#moreViews.customTaskOptionsConfirmButton.center = (50, 70)
			moreViews.customTaskOptionsConfirmButton.action = moreViews.curView.setCustomTaskSettings
		
		moreViews.customTaskOptionsView.present("fullscreen")
		
		
	def setCustomTaskSettings(self, sender):
		options = [None] * len(moreViews.chosenTaskOptions)
		for x in moreViews.chosenTaskOptions:
			index = int(x.name[1])
			type = x.name[0]
			if type == "b":
				if x.title == "yes":
					options[index] = True
				elif x.title == "no":
					options[index] = False
			elif type == "s":
				options[index] = moreViews.chosenTaskOptions[index].text
			elif type == "c":
				options[index] = (int(moreViews.availableTaskOptions[index].choiceIndex), moreViews.availableTaskOptions[index].helperButton.title)
			
		if sender.title == "create":
			task = CustomTask(len(self.tasks), False, options)
			self.tasks.append(task)
		elif sender.title == "save":
			task = self.curTask
			self.view.remove_subview(task.button)
			task.setOptions(options)
			if self.completable:
				self.view.remove_subview(task.completionButton)
				
		if self.completable:
			completionButton = task.addCompletionButton()
			self.view.add_subview(completionButton)
		 
		self.view.add_subview(task.button)

		lifelpDataBase.saveCustomView(self.serialNum, self.options, self.tasks)
		
			#then i guess i should just re-present the physicsl view
		moreViews.customTaskOptionsView.close()	
	
	def customEditMode(self, sender):
		if sender.title == "edit":
			for task in self.tasks:
				if self.completable == False:
					button = task.addCompletionButton()
					self.view.add_subview(button)
				task.completionButton.background_color = "#ff591e"
			sender.title = "done"
		else:
			for task in self.tasks:
				button = task.completionButton
				if task.completed:
					button.background_color = "2ce56d"
				else:
					button.background_color = "red"
					
				if self.completable == False:
					self.view.remove_subview(button)
			sender.title = "edit"
		
	def linkView(self, serialNum):
		moreViews.curView.buttonNeedingLink.title = serialNum
		
	def saveSelf(self):
		lifelpDataBase.saveCustomView(self.serialNum, self.options, self.tasks)


		
	

#############################
#############################
#############################
#     CustomTask Class      #		

#holds all data and functionality
#for the tasks that are in views
#in the MoreViews section

class CustomTask:
	def __init__(self, position, completed, options):
		#position in the display order
		self.position = position
		#is task completed
		self.completed = completed
		self.completionButton = None
		
		self.setOptions(options)
		
		
	def setTaskCompletion(self, sender):
		if sender.background_color == (1.0, 0.34901960784313724, 0.11764705882352941, 1.0):
			moreViews.curView.editTask(self.position)
		else:
			if self.completed:
				sender.background_color = "red"
				self.completed = False
			else:
				sender.background_color = "#2ce56d"
				self.completed = True
			moreViews.curView.saveSelf()
		
	def openAttachedView(self, sender):
		global moreViews
		
		if self.attachedView != "none":
			moreViews.openCustomView(self.attachedView)
		
	def setOptions(self, options):
		self.options = options
		
		#option 1
		self.name = options[0]
		
		button = ui.Button(title = self.name)
		button.center = (230, 25 + 40 * self.position)
		
		#option 2
		if options[1][0] == 0:
			self.attachedView = options[1][1]
			button.action = self.openAttachedView
		else:
			self.attachedView = "none"
			button.action = None
			
		self.button = button
		
	def addCompletionButton(self):
		if self.completionButton == None:
			button = ui.Button(title = str(self.position+1))
			self.completionButton = button
			button.name = str(self.position + 1)
			button.center = (35, 25 + 40 * self.position)
			button.action = self.setTaskCompletion
			if self.completed:
				button.background_color = "#2ce56d"
			else:
				button.background_color = "red"
		
		return self.completionButton
	
	

	

#############################
#############################
#############################
# Button creation functions #


def createCloseViewButton(viewClass, title, type):
	button = ui.Button(title = title, center = (25, 55),  background_color = "white")
	if type == "c":
		button.action = moreViews.previousView
	elif type == "r":
		button.action = viewClass.closeView
	viewClass.view.add_subview(button)
	


def createAddTaskButton(viewClass, action):
	button = ui.Button(font = ('<system-bold>', 70), title = "0")
	button.center = (200, 750)
	viewClass.view.add_subview(button)
	if action == "task":
		button.action = viewClass.addTask
	elif action == "preset":
		button.action = viewClass.addPreset
	elif action == "customView":
		button.action = viewClass.openCustomViewOptions
	elif action == "customTask":
		button.action = viewClass.createTask
	
	button.title = "+"
	return button
	
def createEditButton(viewClass, type):
	button = ui.Button(title = "XXXXXX")
	button.center = (315, 755)
	viewClass.view.add_subview(button)
	button.title = "edit"
	
	
	if type == "p":
		button.action = viewClass.presetEditMode
	elif type == "d":
		button.action = viewClass.dayEditMode
	elif type == "c":
		button.action = viewClass.customEditMode
	elif type == "mr":
		button.action = viewClass.moreEditMode
	elif type == "ms":
		button.title = "select"
		button.action = viewClass.moreSelectMode
		button.border_color = "black"
		button.border_width = 1
	return button

def createCreateButton(view, title, type):
	button = ui.Button(font = ('<system-bold>',30), title = title)
	button.center = (200, 700)
	button.background_color = "white"
	button.border_color = "black"
	button.border_width = 1
	if type == "v":
		button.action = moreViews.setCustomViewSettings
	elif type == "t":
		button.action = moreViews.curView.setCustomTaskSettings
	view.add_subview(button)
	return button

def createMoreViewsButton(view):
	button = ui.Button(font = ('<system-bold>',20), title = "more views")
	button.flex = "LRTB"
	button.center = (50, 77)
	button.background_color = "white"
	button.action = moreViews.showView
	button.border_color = "black"
	button.border_width = 1
	view.add_subview(button)

def createPresetButton(view):
	preset = ui.Button(font = ('<system-bold>',20), title = " presets ")
	preset.flex = "LRTB"
	preset.center = (60, 77)
	preset.background_color = "white"
	preset.action = presetWindow.showPresetView
	preset.border_color = "black"
	preset.border_width = 1
	view.add_subview(preset)

def createBankButton(view):
	bankBut = ui.Button(font = ('<system-bold>',20), title = "bank")
	bankBut.flex = "LRTB"
	bankBut.center = (35, 77)
	bankBut.background_color = "white"
	bankBut.action = bank.presentBankView
	bankBut.border_color = "black"
	bankBut.border_width = 1
	view.add_subview(bankBut)

def createPrevButton(viewClass):
	prev = ui.Button(font = ('<system-bold>',15), title = "prev")
	prev.background_color = "white"
	prev.action = viewClass.changeWeek
	prev.center = (30, 460)
	prev.border_color = "black"
	prev.border_width = 1
	viewClass.view.add_subview(prev)

def createNextButton(viewClass):
	next = ui.Button(font = ('<system-bold>',15), title = "next")
	next.background_color = "white"
	next.action = viewClass.changeWeek
	next.center = (100, 460)
	next.border_color = "black"
	next.border_width = 1
	viewClass.view.add_subview(next)
	
def createTrashButton(view):
	button = ui.Button(font = ('<system-bold>', 40), title = "🗑️")
	button.action = deleteBankTask
	button.center = (215, 650)
	button.border_color = "black"
	button.background_color = "white"
	button.border_width = 1
	return button
	
def createOptionsTrashButton(kind):
	button = ui.Button(title = "🗑️")
	button.center = (75, 700)
	button.border_color = "black"
	button.background_color = "white"
	button.border_width = 1
	
	if kind == "v":
		button.action = moreViews.promptConfirmDelete
	elif kind == "t":
		button.action.moreViews.curView.deleteTask
	
	return button
	

		

	
	
	
	
	
#############################
#############################
#############################
#     set up and globals    #

today = datetime.date.today()
todayS = str(today)

data = lifelpDataBase.getData(today)




bank = Bank()
presetWindow = Presets()
moreViews = MoreViews("r")
moreViews.finishSetup()
mainView = MyMainView()
	
