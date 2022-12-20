import ui
import datetime
import time
import lifelpDataBase
import lifelpAUX
import data_objects
import gc

from bank import Bank
from presets import Presets
from custom_view import *
from buttons import *


#############################
#############################
#############################
#     MainView Class      #

#holds all data and functionality
#for the main home view

class MainView:
	def __init__(self):
		self.screenWidth, self.screenHeight = ui.get_screen_size()

		self.today = datetime.date.today()
		self.todayS = str(self.today)
		self.data = lifelpDataBase.getData(self.today)

		self.view = ui.View(background_color = "f0fff5")
		self.nav = ui.NavigationView(self.view)
		self.trashButton = createTrashButton(self)

		self.bank = Bank(self)
		self.presets = Presets(self)
		self.moreViews = MoreViews("r", self, None)
		self.moreViews.finishSetup()

		self.dateButtons = []
		self.sundayIndexViewed = 0
		self.monthBeingViewed = self.todayS[0:7]
		
		self.todayIndex = lifelpAUX.findTodayIndex(self.todayS, self.data)
		self.curDayView = None
		self.createDateButtons()
	
	#creates the date buttons for the main view
	def createDateButtons(self):
		curMonth = self.todayS[0:7]
		mIndex = 1
		daysOfWeek = ["S", "M", "T", "W", "T", "F", "S"]
		self.sundayIndex = int(self.data[curMonth].sundayIndex)
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
				
		needApplyPresets = self.bank.newDay and lifelpAUX.isNewWeek(data[curMonth].dataKeys[self.sundayIndex], self.bank.lastLastLog)
		
		
		#each iteration prepares a day button for the main view
		tempSundInd = self.sundayIndex
		for x in range(0,7):
			#if month ends mid week
			if (tempSundInd + x == len(self.data[curMonth].days)):
				curMonth = lifelpAUX.incrFileKey(curMonth)
				#sundayIndex - 7 to use next month sunday index
				tempSundInd = int(self.data[curMonth].sundayIndex) - 7
				alteredMonths.append(curMonth)
				
			#adds the date button with temporary label to set size
			button = ui.Button(title = "0000000000")
			button.center = (80, (50 + (55*x)))
			button.border_color = "black"
			button.border_width = 1
			button.background_color = "white"
			button.action = self.dateButtonPressed
			self.dateButtons.append(button)
			#highlights current day
			if (self.sundayIndex + x) == (self.todayIndex):
				button.border_color = "#2ce56d"
				button.border_width = 5
		
			#change title of dateButton after being added to view so it can have a consistent size
			button.title = self.data[curMonth].dataKeys[tempSundInd + x]
			self.view.add_subview(button)
			
			
			#figuring out what color to make the dateButton
			day = self.data[curMonth].days[button.title]
			day.buttonIndex = x
			

			#applies presets to day
			if needApplyPresets:
				dayValue = 2**x
				for preset in self.presets.presets:
					if self.presets.presets[preset].frequency & dayValue:
						self.presets.placePreset(preset, x, self.sundayIndex)
						
			lifelpAUX.setDateButtonColor(button, day)

			#adds dayLabel next to dateButton
			dayLabel = ui.Label(text = daysOfWeek[x], font = ('<system-bold>', 20))
			dayLabel.center = (60,  (50 + (55*x)))
			self.view.add_subview(dayLabel)
			
		createPresetButton(self.view, self.presets)
		createMoreViewsButton(self.view, self.moreViews)
		createBankButton(self.view, self.bank)
		createPrevButton(self)
		createNextButton(self)
		
		self.nav.present("fullscreen", hide_title_bar=True)
				
		self.sundayIndexViewed = self.sundayIndex
		
		if needApplyPresets:
			for x in alteredMonths:
				lifelpDataBase.saveData(x, self.data)
		
	
	def changeWeek(self, sender):		
		if sender.title == "prev":
			self.sundayIndexViewed-=7
			if self.sundayIndexViewed < 0:
				mainView.monthBeingViewed = lifelpAUX.decrFileKey(mainView.monthBeingViewed)
				try:
					self.sundayIndexViewed = len(self.data[mainView.monthBeingViewed].days) + self.sundayIndexViewed
				except KeyError:
					self.data[mainView.monthBeingViewed] = lifelpDataBase.loadData(mainView.monthBeingViewed)
					self.sundayIndexViewed = len(self.data[mainView.monthBeingViewed].days) + self.sundayIndexViewed
		else:
			self.sundayIndexViewed+=7
		for x in range(0, len(self.dateButtons)):
			oldLabel = self.dateButtons[x].title
			self.data[oldLabel[0:7]].days[oldLabel].buttonIndex = -1
			#if month ends mid week
			if (self.sundayIndexViewed + x >= len(self.data[mainView.monthBeingViewed].days)):
				mainView.monthBeingViewed = lifelpAUX.incrFileKey(mainView.monthBeingViewed)
				# to use next month sunday index
				try:
					self.sundayIndexViewed = int(self.data[mainView.monthBeingViewed].sundayIndex) - 7
				except KeyError:
					self.data[mainView.monthBeingViewed] = lifelpDataBase.loadData(mainView.monthBeingViewed)
					self.sundayIndexViewed = int(self.data[mainView.monthBeingViewed].sundayIndex) - 7
				if self.sundayIndexViewed == -7:
					self.sundayIndexViewed = 0
			button = self.dateButtons[x]
			button.title = self.data[mainView.monthBeingViewed].dataKeys[self.sundayIndexViewed + x]
			day = self.data[mainView.monthBeingViewed].days[button.title]
			day.buttonIndex = x
			setDateButtonColor(button, day)
			if button.title == self.todayS:
				button.border_width = 5
			else:
				button.border_color = "black"
				button.border_width = 1
				
	#creates a day view object
	#trigger: date button on mainView
	def dateButtonPressed(self, sender):
		month = sender.title[0:7]

		#if from bank info is blank, open day view
		if self.bank.fromBankInfo == "":
			self.curDayView = MyDayView(self, sender)
		else:
			#add new bank-type task to day
			date = sender.title
			self.data[date[0:7]].days[date].tasks[self.bank.fromBankInfo] = dataObjetcs.Task("b", False)
			
			#increase out count for bank task
			self.bank.bank[self.bank.fromBankInfo].outCount+=1
			self.bank.fromBankInfo = ""
			
			#update main view
			self.view.remove_subview(self.trashButton)
			#TODO remove cancel button
			setDateButtonColor(sender, data[date[0:7]].days[date])
			
			#save
			lifelpDataBase.saveData(month, self.data)
			lifelpDataBase.saveBank(self.bank)

	#deletes bank task
	#trigger: trash can button on mainView
	def deleteBankTask(self, sender):
		#delete bank task
		del self.bank.bank[self.bank.fromBankInfo]
		self.bank.bankKeys.remove(self.bank.fromBankInfo)

		self.bank.fromBankInfo = ""

		#hide trash button
		self.view.remove_subview(self.trashButton)

		#save bank
		lifelpDataBase.saveBank(self.bank)
				
				
				
#############################
#############################
#############################
#      MyDayView Class      #
			
#Holds all data and functionality 
#for the curent day being viewed
					
class MyDayView:
	def __init__(self, mainView, sender):
		self.mainView = mainView

		self.editMode = False
		self.textField = ui.TextField(frame = (20, 400, 375, 50))
		self.textField.action = self.createTask
		
		self.taskButtons = []
		self.taskLabels = []

		curDate = sender.title
		month = curDate[0:7]
		
		self.date = curDate
		self.dateButton = sender
		numTasks = 1
		self.view = ui.View()
		self.view.background_color = "#f0fff5"
		
		x = 0
		tasks = self.mainView.data[month].days[curDate].tasks
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
			if lifelpAUX.date1GreaterThan2(self.mainView.bank.lastLastLog, curDate) == False:
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
		#day is only editable if not in the past
		if lifelpAUX.date1GreaterThan2(self.mainView.todayS, curDate) == False:
			createAddTaskButton(self, "task")
			self.editButton = createEditButton(self, "d")
			editMode = False
		self.mainView.nav.push_view(self.view)
	
	def addTask(self, sender):
		self.view.add_subview(self.textField)
	
	def dayEditMode(self, sender):
		if sender.title == "done":
			tasks = self.mainView.data[self.date[0:7]].days[self.date].tasks
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
		self.view.remove_subview(self.textField)
		if textfield.text != "":
			month = self.date[0:7]
			day = self.mainView.data[month].days[self.date]
			numTasks = len(day.tasks) + 1
			day.tasks[textfield.text] = data_objects.Task()
			lifelpDataBase.saveData(month, self.mainView.data)
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
		month = self.date[0:7]
		day = self.mainView.data[month].days[self.date]
		tasks = day.tasks
		taskKeys = list(tasks.keys())
		if sender.title == "🗑️":
			indexToDelete = int(sender.name) - 1
			maxIndex = len(self.taskButtons) - 1
			#can only delete things from present and future days so this is coo
			if tasks[taskKeys[indexToDelete]].type == "b": 
				self.mainView.bank.bank[taskKeys[indexToDelete]].outCount -= 1
				self.mainView.bank.bank[taskKeys[indexToDelete]].dates.remove(day)
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
			lifelpDataBase.saveData(month, self.mainView.data)
			
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
			lifelpAUX.setDateButtonColor(self.dateButton, day)
			for x in tMonths:
				lifelpDataBase.saveData(x, self.mainView.data)
	
	
	
#############################
#############################
#############################
#           main            #

if __name__ == "__main__":
	mainView = MainView()
	
