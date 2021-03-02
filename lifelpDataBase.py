import lifelpAUX

def createData(day):
	day = lifelpAUX.changeMonth(day, 1)
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

def saveData(month, data):
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

def saveBank(bank):
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

