from buttons import *



#############################
#############################
#############################
#        Bank Class         #

#holds all data and functionality
#for the bank section

class Bank:	
	def __init__(self, mainView):
		self.mainView = mainView

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
		self.mainView.nav.push_view(self.view)
	
	def cleanBank(self):
		tasksToDelete = []
		for task in self.bank:
			if self.bank[task].complete:
				dayS = self.bank[task].dates[len(self.bank[task].dates) - 1]
				for date in self.bank[task].dates:
					newKey = task + " " + dayS
					newTask = lifelpDataBase.Task()
					newTask.complete = True
					self.mainView.data[date[0:7]].days[date].tasks[newKey] = newTask
					del self.mainView.data[date[0:7]].days[date].tasks[task]
				tasksToDelete.append(task)
		for task in tasksToDelete:
			del self.bank[task]
			self.bankKeys.remove(task)
	
	def checkForIncomplete(self):
		day = today
		dayS = str(day)
		while(dayS != self.lastLog):
			day = day - datetime.timedelta(days=1)
			dayS = str(day)
			dataKey = dayS[0:7]
			try:
				curDay = self.mainView.data[dataKey].days[dayS].tasks
			except KeyError:
				self.mainView.data[dataKey] = lifelpDataBase.loadData(dataKey)
				curDay = self.mainView.data[dataKey].days[dayS].tasks
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
			lifelpDataBase.saveData(dataKey, self.mainView.data)
	
	def fromBank(self, sender):
		self.fromBankInfo = sender.title
		self.master_view.add_subview(self.trashButton)
		self.view.close()