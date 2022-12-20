from buttons import *
import data_objects
import lifelpDataBase
import lifelpAUX
import gc

#############################
#############################
#############################
#    SettingOption Class    #

#holds all data and functionality
#for all available options for
#custom views and tasks in the
#moreViews section

class SettingOption:
	def __init__(self, name, type, choices, mainView, moreViews):
		self.mainView = mainView
		self.moreViews = moreViews
		
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
			self.helperButton.action = self.moreViews.chooseViewLink
			self.moreViews.customTaskOptionsView.add_subview(self.helperButton)
			self.helperButton.title = "none"
			self.helperButtonActive = True
		else:
			helperButtonActive = False
			self.moreViews.customTaskOptionsView.remove_subview(self.helperButton)
		
		
	
	def cycleChoice(self, sender):
		self.choiceIndex+=1
		if self.choiceIndex%len(self.choices) == 0:
			self.choiceIndex = 0
		sender.title = self.choices[self.choiceIndex]
		if self.helperButtonActive:
			self.moreViews.customTaskOptionsView.remove_subview(self.helperButton)
			self.helperButtonActive = False
		self.addHelperButton(self.choiceIndex)










#############################
#############################
#############################
#      MoreViews Class      #

#holds all data and funtionality
#for the home view for the
#more views section 

class MoreViews:
	def __init__(self, type, mainView, home_view):
		self.view = ui.View()
		self.mainView = mainView
		if home_view:
			self.home_view = home_view
		self.view.background_color = "f0fff5"	
		self.editMode = False
		self.selectMode = False

		#for creation of regular home view
		if type == "r":
			self.editButton = createEditButton(self, "mr")
			self.selectView = MoreViews("s", self.mainView, self)

		#for creation of select home view	
		elif type == "s":
			self.editButton = createEditButton(self, "ms")

		self.addTaskButton = createAddTaskButton(self, "customView")	
		self.moreViewButtons = []
		self.x = 0
		self.y = 0
		
		#load all view meta data
		self.allViews, self.numSlots, self.availableSlots = lifelpDataBase.loadMoreViewsAll()
		
		self.curView = None
		#CHECK self.viewPath = []
		self.openViews = {}

		self.place_home_view_views()

	def place_home_view_views(self):
		for viewKey in self.allViews:
			if self.allViews[viewKey].link_count == 0:
				#create button
				button = ui.Button(title = "00000000000000000000")
				button.center = (105 + 205 * self.x, 40 + 40 * self.y)
				button.background_color = "white"
				button.border_color = "black"
				button.border_width = 1
				button.action = self.openCustomViewFromHome
				self.view.add_subview(button)
				button.title = self.allViews[viewKey].name
				button.name = viewKey
				self.moreViewButtons.append(button)
				self.x+=1
				if self.x%2 == 0:
					self.x = 0
					self.y+=1

	def delete_home_view_views(self):
		for button in self.moreViewButtons:
			self.view.remove_subview(button)
			del(button)

	def refresh_home_view_views(self):
		self.delete_home_view_views()
		self.place_home_view_views()

	def finishSetup(self):
		#view options
		self.chosenViewOptions = []
		self.availableViewOptions = []
		
		#option 1
		self.availableViewOptions.append(SettingOption("title", "s", [], self.mainView, self))
		
		#option 2
		self.availableViewOptions.append(SettingOption("completable", "b", [], self.mainView, self))
	
		self.customViewOptionsView = ui.View(background_color = "f0fff5")
		self.customViewOptionsConfirmButton = createCreateButton(self, "create", "v")
		
		self.customViewOptionsTrashButton = createOptionsTrashButton("v", self)
		
		self.customViewOptionsConfirmDeleteLabel = ui.Label(text="delete view?", center=(80,670))
		
		self.customViewOptionsConfirmDeleteButton = ui.Button(title="yes", border_color="black", border_width=1, background_color="white", action=self.confirmDelete, center=(45, 700))
		
		self.customViewOptionsDeclineDeleteButton = ui.Button(title="no", border_color="black", border_width=1, background_color="white", action=self.declineDelete, center=(80, 700))
		
		self.putOptionsOnView(self.customViewOptionsView, self.availableViewOptions, self.chosenViewOptions)

		
		#task options
		self.chosenTaskOptions = []
		self.availableTaskOptions = []
		
		#taskOption 1
		self.availableTaskOptions.append(SettingOption("name", "s", None, self.mainView, self))
		
		#TaskOption 2
		self.availableTaskOptions.append(SettingOption("action", "c", ["view", "note", "distribute"], self.mainView, self))
		
		self.customTaskOptionsView = ui.View(background_color = "f0fff5")
		
		self.customTaskOptionsConfirmButton = createCreateButton(self, "create", "t")
		
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
				button.action = lifelpAUX.activateBoolButton
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
		#this edit mode is for editing the home view
		if self.editMode:
			self.moreEditMode(self.editButton)
		self.mainView.nav.push_view(self.view)
		
	def chooseViewLink(self, sender):
		self.curView.buttonNeedingLink = sender
		self.mainView.nav.push_view(self.view)
			
	def openCustomViewFromHome(self, sender):
		if self.editMode:
			self.curView = self.getView(sender.name)
			self.curView.button = sender
			self.openCustomViewOptions("edit")
		else:
			self.openCustomView(sender.name)
			
	def openCustomView(self, serialNum):
		if self.selectMode:
			#link selected view to view that opened select view
			self.home_view.allViews[serialNum].link_count += 1
			self.home_view.curView.linkView(serialNum)
			
			self.view.close()
		else:
			self.curView = self.getView(serialNum)
			self.mainView.nav.push_view(self.curView.view)
	
	#gets a view if it is already open, else open a view
	def getView(self, serialNum):
		if serialNum == None:
			return None
		
		#i might add some sort of reference counter thing to close ones we dont want after a while to increase efficiency
		if serialNum not in self.openViews:
			self.openViews[serialNum] = CustomView(serialNum, self, self.mainView)
			
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
		
		self.mainView.nav.push_view(self.customViewOptionsView)
		
		
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
		
		#refresh homeview
		self.refresh_home_view_views()
				
		lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
		
		gc.collect()
			
	def setCustomViewSettings(self, sender):
		options = [None] * len(self.chosenViewOptions)

		#extract option data from chosen options
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

		#create mode
		if sender.title == "create":
			if len(self.availableSlots) == 0:
				self.numSlots+=1
				serialNum = str(self.numSlots)
			else:
				serialNum = self.availableSlots.pop(0)
			
			lifelpDataBase.createCustomViewData(serialNum, options)
				
			self.allViews[serialNum] = data_objects.MetaCustomView(options[0], 0)
			
			lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
			
			#then i gotta add the view to the physical home view
			button = ui.Button(title = "00000000000000000000")
			button.center = (105 + 205 * self.x, 40 + 40 * self.y)
			button.background_color = "white"
			button.action = self.openCustomViewFromHome
			button.border_color = "black"
			button.border_width = 1
			self.view.add_subview(button)
			button.title = self.allViews[serialNum].name
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
				self.allViews[self.curView.serialNum].name = name
				
				lifelpDataBase.saveMoreViewsAll(self.allViews, self.numSlots, self.availableSlots)
			
			lifelpDataBase.saveCustomView(self.curView.serialNum, self.curView.options, self.curView.tasks)
		
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
	def __init__(self, serialNum, moreViews, mainView):
		self.moreViews = moreViews
		self.mainView = mainView
		
		self.view = None
		
		self.tasks = []
		taskOptions, taskCompleted, taskPositions, self.options = lifelpDataBase.loadCustomView(serialNum)
		for x in range(len(taskOptions)):
			task = CustomTask(taskPositions[x], taskCompleted[x], taskOptions[x], moreViews)
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
		for option in self.moreViews.availableTaskOptions:
			#needs boolean value
			if option.type == "b":
				if editMode and self.tasks[p].options[x] == True:
					self.moreViews.chosenTaskOptions[x].title = "yes"
					self.moreViews.chosenTaskOptions[x].background_color = "2ce56d"
				else:
					self.moreViews.chosenTaskOptions[x].title = "no"
					self.moreViews.chosenTaskOptions[x].background_color = "red"
			#needs string value
			elif option.type == "s":
				if editMode:
					self.moreViews.chosenTaskOptions[x].text = self.tasks[p].options[x]
				else:
					self.moreViews.chosenTaskOptions[x].text = ""
			elif option.type == "c":
				if editMode:
					choiceIndex = self.tasks[p].options[x][0]
					self.moreViews.chosenTaskOptions[x].title = option.choices[choiceIndex]
					option.addHelperButton(choiceIndex)
					option.helperButton.title = self.tasks[p].options[x][1]
				else:
					self.moreViews.chosenTaskOptions[x].title = option.choices[0]
					option.addHelperButton(0)
			x+=1
				
			if editMode:
				self.moreViews.customTaskOptionsConfirmButton.title = "save"
				self.curTask = self.tasks[p]
				#moreViews.customTaskOptionsConfirmButton.center = (55, 70)
			else:
				self.moreViews.customTaskOptionsConfirmButton.title = "create"
				#moreViews.customTaskOptionsConfirmButton.center = (50, 70)
			self.moreViews.customTaskOptionsConfirmButton.action = self.moreViews.curView.setCustomTaskSettings
		
		self.mainView.nav.push_view(self.moreViews.customTaskOptionsView)
		
		
	def setCustomTaskSettings(self, sender):
		options = [None] * len(self.moreViews.chosenTaskOptions)
		for x in self.moreViews.chosenTaskOptions:
			index = int(x.name[1])
			type = x.name[0]
			if type == "b":
				if x.title == "yes":
					options[index] = True
				elif x.title == "no":
					options[index] = False
			elif type == "s":
				options[index] = self.moreViews.chosenTaskOptions[index].text
			elif type == "c":
				options[index] = (int(self.moreViews.availableTaskOptions[index].choiceIndex), self.moreViews.availableTaskOptions[index].helperButton.title)
			
		if sender.title == "create":
			task = CustomTask(len(self.tasks), False, options, self.moreViews)
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
		self.moreViews.customTaskOptionsView.close()	
	
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
		self.moreViews.curView.buttonNeedingLink.title = serialNum
		
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
	def __init__(self, position, completed, options, moreViews):
		#position in the display order
		self.position = position
		#is task completed
		self.completed = completed
		self.completionButton = None
		
		self.moreViews = moreViews
		
		self.setOptions(options)
		
		
	def setTaskCompletion(self, sender):
		if sender.background_color == (1.0, 0.34901960784313724, 0.11764705882352941, 1.0):
			self.moreViews.curView.editTask(self.position)
		else:
			if self.completed:
				sender.background_color = "red"
				self.completed = False
			else:
				sender.background_color = "#2ce56d"
				self.completed = True
			self.moreViews.curView.saveSelf()
		
	def openAttachedView(self, sender):
		if self.attachedView != "none":
			self.moreViews.openCustomView(self.attachedView)
		
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
