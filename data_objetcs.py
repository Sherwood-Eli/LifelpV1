class Task:	
	def __init__(self, kind="r", complete=False):
		self.complete = complete
		self.type = kind

class MyDay:
	def __init__(self):
		self.tasks = {}
		self.buttonIndex = -1

class MyMonth:
	def __init__(self):
		self.days = {}
		self.sundayIndex = 0
		self.dataKeys = []

class PresetTask:
	def __init__(self, frequency):
		self.frequency = frequency
		self.labelButton = None
		self.editButton = None
		self.frequencyButtons = []

class BankTask:
	def __init__(self, outCount, dates, complete):
		self.outCount = outCount
		self.dates = dates
		self.complete = complete

class MetaCustomView:
	def __init__(self, name, link_count):
		self.name = name
		self.link_count = link_count
