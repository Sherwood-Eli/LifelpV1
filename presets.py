"""
This component holds all of the code for the presets view.
"""

from buttons import *
import lifelpAUX
import lifelpDataBase
import datetime
import data_objects


#############################
#############################
#############################
#       Presets Class       #

#holds all data and functionality
#for the presets section

class Presets:
	def __init__(self, mainView):
		self.mainView = mainView
		self.editMode = False

		self.presets, self.presetKeys = lifelpDataBase.loadPresets()
		self.numPresets = len(self.presetKeys)
		self.view = None
		self.textField = ui.TextField(frame = (20, 400, 375, 50))
		self.textField.action = self.savePreset

	def addPreset(self, sender):
		self.view.add_subview(self.textField)
	
	def showPresetView(self, sender):
		self.editMode = False
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
				
		self.mainView.nav.push_view(self.view)
		
	def presetEditMode(self, sender):
		if sender.title == "edit":
			sender.title = "done"
			self.editMode = True
			self.view.remove_subview(self.freqLabel)
			for preset in self.presets:
				for x in self.presets[preset].frequencyButtons:
					self.view.remove_subview(x)
				self.view.add_subview(self.presets[preset].editButton)
				
		elif sender.title == "done":
			sender.title = "edit"
			self.editMode = False
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
			
			day = self.placePreset(preset, place, self.mainView.sundayIndex)
			
			if day != None:
			
				lifelpAUX.setDateButtonColor(self.mainView.dateButtons[place], day)
		
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
			
			if self.editMode:
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
			self.presets[newPreset] = data_objects.PresetTask(0)
			
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
		today = datetime.date.today()
		todayS = str(today)
		dataKey = todayS[0:7]	
	
		if tempSunInd + place >= len(self.mainView.data[dataKey].days):
			dataKey = lifelpAUX.incrFileKey(dataKey)
			tempSunInd = self.mainView.data[dataKey].sundayIndex - 7
		date = self.mainView.data[dataKey].dataKeys[tempSunInd + place]
		
		if not lifelpAUX.date1GreaterThan2(todayS, date):
			
			day = self.mainView.data[dataKey].days[date]
			
			day.tasks[preset] = data_objects.Task()
			day.tasks[preset].complete = False
			day.tasks[preset].type = "p"
			
			lifelpDataBase.saveData(dataKey, self.mainView.data)
			
			return day
			
		
	
	def removePreset(self, preset, place):
		todayS = str(datetime.date.today())		
		dataKey = todayS[0:7]
		tempSunInd = self.mainView.sundayIndex		
		
		if tempSunInd + place >= len(self.mainView.data[dataKey].days):
			dataKey = lifelpAUX.incrFileKey(dataKey)
			tempSunInd = self.mainView.data[dataKey].sundayIndex - 7
		date = self.mainView.data[dataKey].dataKeys[tempSunInd + place]
		if not lifelpAUX.date1GreaterThan2(todayS, date):
			
			day = self.mainView.data[dataKey].days[date]
		
			if preset in day.tasks:
				del day.tasks[preset]
			
			lifelpAUX.setDateButtonColor(self.mainView.dateButtons[place], day)
			
			lifelpDataBase.saveData(dataKey, self.mainView.data)
