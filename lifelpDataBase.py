import lifelpAUX
import datetime

def createData(fileKey):
	global data
	prevFileKey = lifelpAUX.decrFileKey(fileKey)
	try:
		sundayIndex = int(data[prevFileKey].sundayIndex)
	except KeyError:
		data[prevFileKey] = loadData(prevFileKey)
		sundayIndex = int(data[prevFileKey].sundayIndex)
	sundayIndex += 35 - len(data[prevFileKey].days)
	sundayIndex = sundayIndex % 7
	month = fileKey[5:7]
	day = datetime.datetime.strptime(fileKey + "-01",'%Y-%m-%d').date()
	dayS = str(day)
	fileName = fileKey + "-data.txt"
	fileName = "lifelp/" + fileName
	
	with open(fileName, "w") as file:
		file.write(str(sundayIndex))
		file.write("\n")
		while dayS[5:7] == month:
			file.write(dayS)
			file.write("{}")
			file.write("\n")
			day = day + datetime.timedelta(days=1)
			dayS= str(day)

def getData(today):
	todayS = str(today)
	global data
	data = {}
	temp = lifelpAUX.changeMonth(today, -1)
	temp = str(temp)
	temp = temp[0:7]
	data[temp] = loadData(temp)
	temp = todayS
	temp = temp[0:7]
	data[temp] = loadData(temp)
	temp = lifelpAUX.changeMonth(today, 1)
	temp = str(temp)
	temp = temp[0:7]
	data[temp] = loadData(temp)
	return data

class Task:	
	def __init__(self):
		self.complete = False
		self.type = "r"

class MyDay:
	def __init__(self):
		self.tasks = {}
		self.buttonIndex = -1

class MyMonth:
	def __init__(self):
		self.days = {}
		self.sundayIndex = 0
		self.dataKeys = []

def loadData(fileKey):
	fileName = fileKey + "-data.txt"
	fileName = "lifelp/" + fileName
	monthData = MyMonth()
	first = True
	try:
		file = open(fileName, "r", encoding='utf-8')
		for line in file:
			if first:
				monthData.sundayIndex = int(line[0])
				first = False
			else:
				x = 0
				date = ""
				while line[x] != "{":
					date += line[x]
					x+=1
				monthData.days[date] = MyDay()
				monthData.dataKeys.append(date)
				tempTasks = {}
				x+=1
				while line[x] != "}":
					task = ""
					while line[x] != ":":
						task += line[x]
						x+=1
					x+=1
					tempTasks[task] = Task()
					if line[x] == "t":
						tempTasks[task].complete = True
					elif line[x] == "f":
						tempTasks[task].complete = False
					x+=1
					tempTasks[task].type = line[x]
					x+=1
				monthData.days[date].tasks = tempTasks
		file.close()
	except IOError:
		
		createData(fileKey)
		monthData = loadData(fileKey)
	return monthData

def saveData(month, data, encoding='utf-8'):
	fileName = "lifelp/" + month + "-data.txt"
	monthData = data[month]
	with open(fileName, "w") as file:
		file.write(str(monthData.sundayIndex))
		file.write("\n")
		for date in monthData.days:
			file.write(date)
			tempTasks = monthData.days[date].tasks
			file.write("{")
			for task in tempTasks:
				for c in task:
					try:
						file.write(c)
					except UnicodeEncodeError:
						continue
				file.write(":")
				tempTask = tempTasks[task]
				if tempTask.complete == True:
					file.write("t")
				elif tempTask.complete == False:
					file.write("f")
				file.write(tempTask.type)
			file.write("}\n")

def savePresets(presets):
	with open("lifelp/presets.txt", "w", encoding='utf-8') as file:
		for preset in presets:
			for c in preset:
				try:
					file.write(c)
				except UnicodeEncodeError:
					continue
			file.write("{")
			file.write(str(presets[preset].frequency))
			file.write("}")
			file.write("\n")

class PresetTask:
	def __init__(self, frequency):
		self.frequency = frequency
		self.labelButton = None
		self.editButton = None
		self.frequencyButtons = []

def loadPresets():
	with open("lifelp/presets.txt", "r") as file:
		presets = {}
		presetKeys = []
		for line in file:
			if len(line) > 1:
				key = ""
				x = 0
				while line[x] != "{":
					key+=line[x]
					x+=1
				presetKeys.append(key)
				x+=1
				frequency = ""
				while line[x] != "}":
					frequency+=line[x]
					x+=1
				frequency = int(frequency)

				presets[key] = PresetTask(frequency)
	return presets, presetKeys

class BankTask:
	def __init__(self, outCount, dates, complete):
		self.outCount = outCount
		self.dates = dates
		self.complete = complete

def loadBank():
	bankKeys = []
	bank = {}
	lastLog = ""
	lastLastLog = ""
	first = True
	with open("lifelp/bank.txt") as file:
		for line in file:
			if first:
				x = 0
				lastLog = ""
				while (line[x] != ":"):
					lastLog+= line[x]
					x+=1
				x+=1
				lastLastLog = ""
				while (line[x] != "}"):
					lastLastLog+= line[x]
					x+=1
				first = False
			else:
				task = ""
				dates = []
				outCount = 0
				x=0
				while (line[x] != ":"):
					task += line[x]
					x+=1
				bankKeys.append(task)
				x+=1
				while (line[x] != ":"):
					date = ""
					while (line[x] != ","):
						date += line[x]
						x+=1
					dates.append(date)
					x+=1
				x+=1
				temp = ""
				while (line[x] != "}"):
					temp+=line[x]
					x+=1
				outCount = int(temp)
				x+=1
				if line[x] == "t":
					complete = True
				else:
					complete = False
				bank[task] = BankTask(outCount, dates, complete)
	return lastLastLog, lastLog, bank, bankKeys

def saveBank(bank):
	with open("lifelp/bank.txt", "w") as file:
		bankKeys = bank.bankKeys
		lastLastLog = bank.lastLastLog
		lastLog = bank.lastLog
		bank = bank.bank
		file.write(lastLog)
		file.write(":")
		file.write(lastLastLog)
		file.write("}")
		x = 0
		while x < len(bankKeys):
			task = bankKeys[x]
			file.write("\n")
			file.write(task)
			file.write(":")
			for y in bank[task].dates:
				file.write(y)
				file.write(",")
			file.write(":")
			file.write(str(bank[task].outCount))
			file.write("}")
			if bank[task].complete:
				file.write("t")
			else:
				file.write("f")
			x+=1
			





			
def createCustomViewData(serialNum, options):
	fileName = "lifelp/moreViews/" + serialNum + ".txt"	
	with open(fileName, "w") as file:
		for option in options:
			if option == True:
				file.write("bt")
			elif option == False:
				file.write("bf")
			else:
				file.write("s")
				file.write(option)
			file.write("_")
		file.write("}")
		
def loadCustomView(serialNum):
	fileName = "lifelp/moreViews/" + serialNum + ".txt"
	#print("opening:", serialNum)	
	options = []
	tasks = []
	positions = []
	completed = []
	taskNum = 0
	with open(fileName, "r") as file:
		first = True
		for line in file:
			x = 0
			if first:
				while line[x] != "}":
					if line[x] == "b":
						if line[x+1] == "t":
							options.append(True)
						else:
							options.append(False)
						x+=3
					elif line[x] == "s":
						x+=1
						string = ""
						while line[x] != "_":
							string += line[x]
							x+=1
						x+=1
						options.append(string)
				first = False
			else:
				taskOptions = []
				aPosition = ""
				if line[x] == "t":
					completed.append(True)
				else:
					completed.append(False)
				x+=1
				while line[x] != "_":
					aPosition += line[x]
					x+=1
				positions.append(int(aPosition))
				x+=1
				while line[x] != "}":
					if line[x] == "b":
						if line[x+1] == "t":
							taskOptions.append(True)
						else:
							taskOptions.append(False)
						x+=3
					elif line[x] == "s":
						x+=1
						string = ""
						while line[x] != "_":
							string += line[x]
							x+=1
						x+=1
						taskOptions.append(string)
					elif line[x] == "c":
						x+=1
						type = ""
						value = ""
						while line[x] != "_":
							type += line[x]
							x+=1
						x+=1
						while line[x] != "_":
							value += line[x]
							x+=1
						x+=1
						taskOptions.append((int(type), value))
						
				tasks.append(taskOptions)
				taskNum+=1
			
							
							
	return tasks, completed, positions, options
			
def saveCustomView(serialNum, options, tasks):
	fileName = "lifelp/moreViews/" + serialNum + ".txt"	
	with open(fileName, "w") as file:
		for option in options:
			if option == True:
				file.write("bt")
			elif option == False:
				file.write("bf")
			else:
				file.write("s")
				file.write(option)
			file.write("_")
		file.write("}")
		file.write("\n")
		for task in tasks:
			if task.completed:
				file.write("t")
			else:
				file.write("f")
			file.write(str(task.position))
			file.write("_")
			for option in task.options:
				if type(option) == type((1,1)):
					file.write("c")
					file.write(str(option[0]))
					file.write("_")
					file.write(option[1])
				elif option == True:
					file.write("bt")
				elif option == False:
					file.write("bf")
				else:
					file.write("s")
					file.write(option)
				file.write("_")
			file.write("}")
			file.write("\n")
			
def loadMoreViewsHome():
	views = {}
	try:
		with open("lifelp/moreViewsHome.txt", "r") as file:
			for line in file:
				x = 0
				key = ""
				while line[x] != ":":
					key+=line[x]
					x+=1
				x+=1
				name = ""
				while line[x] != "}":
					name+=line[x]
					x+=1
				views[key] = name
	except IOError:
		file = open("lifelp/moreViewsHome.txt", "w")
		file.close()
	return views
	
def saveMoreViewsHome(views):
	with open("lifelp/moreViewsHome.txt", "w") as file:
		first = True
		for viewKey in views:
			if first:
				first = False
			else:
				file.write("\n")
			file.write(viewKey)
			file.write(":")
			file.write(views[viewKey])
			file.write("}")
	
	
def loadMoreViewsAll():
	views = {}
	numViews = 0
	availableSlots = []
	try:
		with open("lifelp/moreViewsAll.txt", "r") as file:
			first = True
			for line in file:
				if first:
					numViews = ""
					x = 0
					while line[x] != ":":
						numViews+=line[x]
						x+=1
					numViews = int(numViews)
					slot = ""
					x+=1
					while line[x] != "}":
						while line[x] != ",":
							slot+=line[x]
							x+=1
						availableSlots.append(slot)
						x+=1
					first = False
				else:
					serialNum = ""
					x = 0
					while line[x] != ":":
						serialNum+=line[x]
						x+=1
					x+=1
					linkCount = 0
					linkCountTemp = ""
					while line[x] != ":":
						linkCountTemp+=line[x]
						x+=1
					x+=1
					linkCount = int(linkCount)
					name = ""
					while line[x] != "}":
						name+=line[x]
						x+=1
					views[serialNum] = name
				
	except IOError:
		file = open("lifelp//moreViewsAll.txt", "w")
		file.write("0:}")
		file.close()
	return views, numViews, availableSlots
	
	
def saveMoreViewsAll(views, numViews, availableSlots):
	with open("lifelp//moreViewsAll.txt", "w") as file:
		file.write(str(numViews))
		file.write(":")
		for slot in availableSlots:
			file.write(slot)
			file.write(",")
		file.write("}")
		
		for viewKey in views:
			print(viewKey)
			print(views[viewKey])
			file.write("\n")
			file.write(viewKey)
			file.write(":")
			file.write(views[viewKey].linkCount)
			file.write(":")
			file.write(views[viewKey])
			file.write("}")
	
	
	
	
	
