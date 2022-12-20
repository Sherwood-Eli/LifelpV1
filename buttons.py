import ui

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

def createCreateButton(viewClass, title, type):
	button = ui.Button(font = ('<system-bold>',30), title = title)
	button.center = (200, 700)
	button.background_color = "white"
	button.border_color = "black"
	button.border_width = 1
	if type == "v":
		button.action = viewClass.setCustomViewSettings
		viewClass.customViewOptionsView.add_subview(button)
	elif type == "t":
		#during initialization, curView will be None
		if viewClass.curView != None:
			button.action = viewClass.curView.setCustomTaskSettings
		viewClass.customTaskOptionsView.add_subview(button)
	
	return button

def createMoreViewsButton(view, moreViews):
	button = ui.Button(font = ('<system-bold>',20), title = "more views")
	button.flex = "LRTB"
	button.center = (50, 77)
	button.background_color = "white"
	button.action = moreViews.showView
	button.border_color = "black"
	button.border_width = 1
	view.add_subview(button)

def createPresetButton(view, presets):
	preset = ui.Button(font = ('<system-bold>',20), title = " presets ")
	preset.flex = "LRTB"
	preset.center = (60, 77)
	preset.background_color = "white"
	preset.action = presets.showPresetView
	preset.border_color = "black"
	preset.border_width = 1
	view.add_subview(preset)

def createBankButton(view, bank):
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
	
def createTrashButton(viewClass):
	button = ui.Button(font = ('<system-bold>', 40), title = "🗑️")
	button.action = viewClass.deleteBankTask
	button.center = (215, 650)
	button.border_color = "black"
	button.background_color = "white"
	button.border_width = 1
	return button
	
def createOptionsTrashButton(kind, viewClass):
	button = ui.Button(title = "🗑️")
	button.center = (75, 700)
	button.border_color = "black"
	button.background_color = "white"
	button.border_width = 1
	
	if kind == "v":
		button.action = viewClass.promptConfirmDelete
	elif kind == "t":
		button.action = viewClass.curView.deleteTask
	
	return button
