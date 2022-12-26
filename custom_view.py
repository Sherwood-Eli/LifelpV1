from buttons import *
import data_objects
import lifelpDataBase
import lifelpAUX
import gc

#############################
#############################
#############################
#    Setting_Option Class    #

#holds all data and functionality
#for all available options for
#custom views and tasks in the
#more_views section

class Setting_Option:
	def __init__(self, name, type, choices, main_view, more_views):
		self.main_view = main_view
		self.more_views = more_views
		
		self.name = name
		self.type = type
		self.choices = choices
		self.choice_index = 0
		self.helper_button = None
		self.helper_button_active = False
		
	def add_helper_button(self, index):
		kind = self.choices[index]
		if self.helper_button == None:
			button = ui.Button(title = "XXXX")
			button.center = (325, 80 + 45)
			button.background_color = "white"
			button.name = "select"
			self.helper_button = button
		if kind == "view":
			self.helper_button.action = self.more_views.choose_view_link
			self.more_views.custom_task_options_view.add_subview(self.helper_button)
			self.helper_button.title = "none"
			self.helper_button_active = True
		else:
			helper_button_active = False
			self.more_views.custom_task_options_view.remove_subview(self.helper_button)
		
		
	
	def cycle_choice(self, sender):
		self.choice_index+=1
		if self.choice_index%len(self.choices) == 0:
			self.choice_index = 0
		sender.title = self.choices[self.choice_index]
		if self.helper_button_active:
			self.more_views.custom_task_options_view.remove_subview(self.helper_button)
			self.helper_button_active = False
		self.add_helper_button(self.choice_index)


#############################
#############################
#############################
#      More_Views Class      #

#holds all data and funtionality
#for the home view for the
#more views section 

class More_Views:
	def __init__(self, main_view):
		self.main_view = main_view

		self.edit_mode = False
		self.select_mode = False

		#create home view
		self.view = ui.View()
		self.view.background_color = "f0fff5"

		self.add_task_button = create_add_task_button(self, "custom_view")	
		self.more_view_buttons = []
		self.x = 0
		self.y = 0
		
		#load all view meta data
		self.all_views, self.num_slots, self.available_slots = lifelpDataBase.loadMoreViewsAll()
		
		#create custum_view_view
		self.custom_view_view = ui.View(background_color = "f0fff5")
		self.custom_view_view_title = ui.Button(title = "00000000000000000000", center = (50, 50), action = self.edit_custom_view)
		self.custom_view_view.add_subview(self.custom_view_view_title)
		back_button = ui.Button(title="back", center = (90, 50), action = self.close_custom_view)
		self.custom_view_view.add_subview(back_button)
		home_button = ui.Button(title="home", center = (10, 50), action = self.close_custom_view_view)
		self.custom_view_view.add_subview(home_button)

		self.cur_view = None
		self.view_path = []
		self.open_views = {}

		#create custum_view_view_select_mode
		self.custom_view_view_select = ui.View(background_color = "f0fff5")
		self.custom_view_view_title_select = ui.Button(title = "00000000000000000000", center = (50, 50), action = self.select_custom_view)
		self.custom_view_view_select.add_subview(self.custom_view_view_title)
		back_button = ui.Button(title="back", center = (90, 50), action = self.close_custom_view)
		self.custom_view_view_select.add_subview(back_button)
		home_button = ui.Button(title="home", center = (10, 50), action = self.close_custom_view_view)
		self.custom_view_view_select.add_subview(home_button)

		self.cur_view_select = None
		self.view_path_select = []

		self.place_home_view_links()

	def place_home_view_links(self):
		for view_key in self.all_views:
			if self.all_views[view_key].link_count == 0:
				#create button
				button = ui.Button(title = "00000000000000000000")
				button.center = (105 + 205 * self.x, 40 + 40 * self.y)
				button.background_color = "white"
				button.border_color = "black"
				button.border_width = 1
				button.action = self.open_custom_view
				self.view.add_subview(button)
				button.title = self.all_views[view_key].name
				button.name = view_key
				self.more_view_buttons.append(button)
				self.x+=1
				if self.x%2 == 0:
					self.x = 0
					self.y+=1

	def remove_home_view_links(self):
		self.more_view_buttons = []
		for button in self.more_view_buttons:
			self.view.remove_subview(button)
			del(button)
		gc.collect()

	def refresh_home_view_links(self):
		self.delete_home_view_links()
		self.place_home_view_links()

	def finish_setup(self):
		#view options
		self.chosen_view_options = []
		self.available_view_options = []
		
		#option 1
		self.available_view_options.append(Setting_Option("title", "s", [], self.main_view, self))
		
		#option 2
		self.available_view_options.append(Setting_Option("completable", "b", [], self.main_view, self))
	
		#create the view options view
		self.custom_view_options_view = ui.View(background_color = "f0fff5")

		#create create button and trash button
		self.custom_view_options_create_button = create_create_button(self, "create", "v")
		self.custom_view_options_trash_button = create_options_trash_button("v", self)
		
		#buttons for view deletion sequence
		self.custom_view_options_confirm_delete_label = ui.Label(text="delete view?", center=(80,670))
		self.custom_view_options_confirm_delete_button = ui.Button(title="yes", border_color="black", border_width=1, background_color="white", action=self.confirm_delete, center=(45, 700))
		self.custom_view_options_decline_delete_button = ui.Button(title="no", border_color="black", border_width=1, background_color="white", action=self.decline_delete, center=(80, 700))
		
		#put options on view
		self.put_options_on_view(self.custom_view_options_view, self.available_view_options, self.chosen_view_options)

		
		#task options
		self.chosen_task_options = []
		self.available_task_options = []
		
		#task_option 1
		self.available_task_options.append(Setting_Option("name", "s", None, self.main_view, self))
		
		#Task_Option 2
		self.available_task_options.append(Setting_Option("action", "c", ["view", "note", "distribute"], self.main_view, self))
		
		#create task options view
		self.custom_task_options_view = ui.View(background_color = "f0fff5")
		
		self.custom_task_options_confirm_button = create_create_button(self, "create", "t")
		
		self.put_options_on_view(self.custom_task_options_view, self.available_task_options, self.chosen_task_options)
		
		
	def put_options_on_view(self, view, available_options, chosen_options):
		x = 0
		for option in available_options:
			label = ui.Label(text = option.name, center = (100, 75 + 45*int(x)))
			
			view.add_subview(label)
			#needs boolean value
			if option.type == "b":
				button = ui.Button(title = "XXX")
				button.center = (275, 80 + 45*int(x))
				button.action = lifelpAUX.activate_bool_button
				button.name = "b" + str(x)
				view.add_subview(button)
				button.title = "no"
				button.background_color = "red"
				chosen_options.append(button)
			#needs string value
			elif option.type == "s":
				text_field = ui.Text_Field(frame = (200, 60 + 45*int(x), 150, 35))
				text_field.name = "s" + str(x)
				text_field.text = ""
				view.add_subview(text_field)
				chosen_options.append(text_field)
			elif option.type == "c":
				button = ui.Button(title = "XXXXXXXXX")
				button.center = (250, 80 + 45*int(x))
				button.action = option.cycle_choice
				button.name = "c" + str(x)
				button.background_color = "white"
				view.add_subview(button)
				button.title = option.choices[0]
				option.add_helper_button(0)
				chosen_options.append(button)
			x+=1
		
	def show_home_view(self, sender):
		self.main_view.nav.push_view(self.view)
		
	#called from the task options view, button needing link is the helper button to the link option
	def choose_view_link(self, sender):
		#make home view ready for select mode
		self.select_mode = True
		
		#pop task options view and custom view view
		self.main_view.nav.pop_view()
		self.main_view.nav.pop_view()

			
	def open_custom_view(self, serial_num):
		#clear the old view
		self.clear_custom_view_view()
		#open the new view
		if self.select_mode:
			self.cur_view_select = self.get_a_view(serial_num)
			self.view_path_select.insert(0, serial_num)
		else:
			self.cur_view = self.get_a_view(serial_num)
			self.view_path.insert(0, serial_num)

		#put tasks on view
		self.populate_custom_view_view()


	def close_custom_view(self):
		#pop view to close
		if self.select_mode:
			self.view_path_select.pop(0)
		else:
			self.view_path.pop(0)

		self.clear_custom_view_view()

		#get the next view
		if self.select_mode:
			if len(self.view_path_select) > 0:
				self.cur_view_select = self.get_a_view(self.view_path_select[0])
		else:
			if len(self.view_path) > 0:
				self.cur_view = self.get_a_view(self.view_path[0])

		self.populate_custom_view_view()


	def populate_custom_view_view(self):
		if self.select_mode:
			if self.cur_view_select != None:
				for button in self.cur_view_select.task_buttons:
					self.custom_view_view_select.add_subview(button)
				self.custom_view_view_title_select.title = self.cur_view_select.name
		else:
			if self.cur_view != None:
				for button in self.cur_view.task_buttons:
					self.custom_view_view.add_subview(button)
				self.custom_view_view_title.title = self.cur_view.name


	def clear_custom_view_view(self):
		if self.select_mode:
			if self.cur_view_select != None:
				for button in self.cur_view_select.task_buttons:
					self.custom_view_view_select.remove_subview(button)
		else:
			if self.cur_view != None:
				for button in self.cur_view.task_buttons:
					self.custom_view_view.remove_subview(button)

	
	#gets a view if it is already open, else open a view
	def get_a_view(self, serial_num):
		#i might add some sort of reference counter thing to close ones we dont want after a while to increase efficiency
		if serial_num not in self.open_views:
			self.open_views[serial_num] = Custom_View(serial_num, self, self.main_view)
			
		return self.open_views[serial_num]

		
	def open_custom_view_options(self, mode):
		edit_mode = False
		if mode == "edit":
			edit_mode = True
		x = 0
		for option in self.available_view_options:
			if option.type == "b":
				if not edit_mode or self.cur_view.options[x] == False:
					self.chosen_view_options[x].title = "no"
					self.chosen_view_options[x].background_color = "red"
				elif self.cur_view.options[x] == True:
					self.chosen_view_options[x].title = "yes"
					self.chosen_view_options[x].background_color = "2ce56d"
			elif option.type == "s":
				if edit_mode:
					self.chosen_view_options[x].text = self.cur_view.options[x]
				else:
					self.chosen_view_options[x].text = ""
			x+=1
		if edit_mode:
			self.custom_view_options_confirm_button.title = "save"
			self.custom_view_options_confirm_button.center = (300, 700)
			self.custom_view_options_view.add_subview(self.custom_view_options_trash_button)
			self.custom_view_options_view.remove_subview(self.custom_view_options_confirm_delete_button)
			
			self.custom_view_options_view.remove_subview(self.custom_view_options_confirm_delete_label)
			
			self.custom_view_options_view.remove_subview(self.custom_view_options_decline_delete_button)
		else:
			self.custom_view_options_confirm_button.title = "create"
			self.custom_view_options_confirm_button.center = (210, 700)
			self.custom_view_options_view.remove_subview(self.custom_view_options_trash_button)
		
		self.main_view.nav.push_view(self.custom_view_options_view)
		
		
	def prompt_confirm_delete(self, sender):
		self.custom_view_options_view.remove_subview(self.custom_view_options_trash_button)
		self.custom_view_options_view.add_subview(self.custom_view_options_confirm_delete_label)
		self.custom_view_options_view.add_subview(self.custom_view_options_confirm_delete_button)
		self.custom_view_options_view.add_subview(self.custom_view_options_decline_delete_button)
	
	def confirm_delete(self, sender):
		self.delete_cur_view()
		self.custom_view_options_view.close()
		
		
	def decline_delete(self, sender):
		self.custom_view_options_view.remove_subview(self.custom_view_options_confirm_delete_label)
		self.custom_view_options_view.remove_subview(self.custom_view_options_confirm_delete_button)
		self.custom_view_options_view.remove_subview(self.custom_view_options_decline_delete_button)
		self.custom_view_options_view.add_subview(self.custom_view_options_trash_button)
		
	def delete_cur_view(self):
		serial_num = self.cur_view.serial_num
		self.available_slots.append(serial_num)
		del(self.all_views[serial_num])
		
		#refresh homeview
		self.refresh_home_view_views()
				
		lifelp_data_base.save_more_views_all(self.all_views, self.num_slots, self.available_slots)
		
		gc.collect()
			
	def set_custom_view_settings(self, sender):
		options = [None] * len(self.chosen_view_options)

		#extract option data from chosen options
		for x in self.chosen_view_options:
			index = int(x.name[1])
			kind = x.name[0]
			if kind == "b":
				if x.title == "yes":
					options[index] = True
				elif x.title == "no":
					options[index] = False
			elif kind == "s":
				options[index] = self.chosen_view_options[index].text

		#create mode
		if sender.title == "create":
			if len(self.available_slots) == 0:
				self.num_slots+=1
				serial_num = str(self.num_slots)
			else:
				serial_num = self.available_slots.pop(0)
			
			lifelp_data_base.create_custom_view_data(serial_num, options)
				
			self.all_views[serial_num] = data_objects.Meta_Custom_View(options[0], 0)
			
			lifelpDataBase.saveMoreViewsAll(self.all_views, self.num_slots, self.available_slots)
			
			#then i gotta add the view to the physical home view
			button = ui.Button(title = "00000000000000000000")
			button.center = (105 + 205 * self.x, 40 + 40 * self.y)
			button.background_color = "white"
			button.action = self.open_custom_view_from_home
			button.border_color = "black"
			button.border_width = 1
			self.view.add_subview(button)
			button.title = self.all_views[serial_num].name
			button.name = serial_num
			self.more_view_buttons.append(button)
			self.x+=1
			if self.x%2 == 0:
				self.x = 0
				self.y+=1
				
		else:
			self.cur_view.options = options
			
			#handles a name change
			name = self.cur_view.options[0]
			if self.cur_view.button.title != name:
				self.cur_view.button.title = name
				self.all_views[self.cur_view.serial_num].name = name
				
				lifelpDataBase.saveMoreViewsAll(self.all_views, self.num_slots, self.available_slots)
			
			lifelp_data_base.save_custom_view(self.cur_view.serial_num, self.cur_view.options, self.cur_view.tasks)
		
		self.custom_view_options_view.close()
	
	def more_edit_mode(self, sender):
		if self.edit_mode == False:
			self.edit_mode = True
			for x in self.more_view_buttons:
				x.background_color = "#ff591e"
			sender.title = "done"
		elif self.edit_mode:
			self.edit_mode = False
			for x in self.more_view_buttons:
				x.background_color = "white"
			sender.title = "edit"
				
	def more_select_mode(self, sender):
		if self.select_mode == False:
			self.select_mode = True
			for x in self.more_view_buttons:
				x.background_color = "#2ce56d"
			sender.title = "seek"
		elif self.select_mode:
			self.select_mode = False
			for x in self.more_view_buttons:
				x.background_color = "white"
			sender.title = "select"





#############################
#############################
#############################
#     Custom_View Class      #

#holds all data and functionality
#for each custom view that was 
#created in the more views section

class Custom_View:
	def __init__(self, serial_num, more_views, main_view):
		self.more_views = more_views
		self.main_view = main_view
		
		self.view = None
		
		self.tasks = []
		task_options, task_completed, task_positions, self.options = lifelpDataBase.load_custom_view(serial_num)
		for x in range(len(task_options)):
			task = Custom_Task(task_positions[x], task_completed[x], task_options[x], more_views)
			self.tasks.append(task)
		
		self.serial_num = serial_num
		self.button = None
		
		self.button_needing_link = None
		
		self.create_view()
		
			
	def create_view(self):
		if self.view != None:
			del self.view
			gc.collect()
		
		
		self.add_task_button = create_add_task_button(self, "custom_task")
		self.edit_button = create_edit_button(self, "c")
		
		#view_option 1
		
		#view_option 2
		self.completable = False
		
		if self.options[1] == True:
			self.completable = True
		
		for task in self.tasks:
			self.view.add_subview(task.button)
			if self.completable:
				completion_button = task.add_completion_button()
				self.view.add_subview(completion_button)
	
			
	def create_task(self, sender):
		self.open_custom_task_options("create", 0)
		
	def edit_task(self, position):
		self.open_custom_task_options("edit", position)
	
	
	def open_custom_task_options(self, mode, p):
		edit_mode = (mode == "edit")
		x = 0
		for option in self.more_views.available_task_options:
			#needs boolean value
			if option.type == "b":
				if edit_mode and self.tasks[p].options[x] == True:
					self.more_views.chosen_task_options[x].title = "yes"
					self.more_views.chosen_task_options[x].background_color = "2ce56d"
				else:
					self.more_views.chosen_task_options[x].title = "no"
					self.more_views.chosen_task_options[x].background_color = "red"
			#needs string value
			elif option.type == "s":
				if edit_mode:
					self.more_views.chosen_task_options[x].text = self.tasks[p].options[x]
				else:
					self.more_views.chosen_task_options[x].text = ""
			elif option.type == "c":
				if edit_mode:
					choice_index = self.tasks[p].options[x][0]
					self.more_views.chosen_task_options[x].title = option.choices[choice_index]
					option.add_helper_button(choice_index)
					option.helper_button.title = self.tasks[p].options[x][1]
				else:
					self.more_views.chosen_task_options[x].title = option.choices[0]
					option.add_helper_button(0)
			x+=1
				
			if edit_mode:
				self.more_views.custom_task_options_confirm_button.title = "save"
				self.cur_task = self.tasks[p]
				#more_views.custom_task_options_confirm_button.center = (55, 70)
			else:
				self.more_views.custom_task_options_confirm_button.title = "create"
				#more_views.custom_task_options_confirm_button.center = (50, 70)
			self.more_views.custom_task_options_confirm_button.action = self.more_views.cur_view.set_custom_task_settings
		
		self.main_view.nav.push_view(self.more_views.custom_task_options_view)
		
		
	def set_custom_task_settings(self, sender):
		options = [None] * len(self.more_views.chosen_task_options)
		for x in self.more_views.chosen_task_options:
			index = int(x.name[1])
			type = x.name[0]
			if type == "b":
				if x.title == "yes":
					options[index] = True
				elif x.title == "no":
					options[index] = False
			elif type == "s":
				options[index] = self.more_views.chosen_task_options[index].text
			elif type == "c":
				options[index] = (int(self.more_views.available_task_options[index].choice_index), self.more_views.available_task_options[index].helper_button.title)
			
		if sender.title == "create":
			task = Custom_Task(len(self.tasks), False, options, self.more_views)
			self.tasks.append(task)
		elif sender.title == "save":
			task = self.cur_task
			self.view.remove_subview(task.button)
			task.set_options(options)
			if self.completable:
				self.view.remove_subview(task.completion_button)
				
		if self.completable:
			completion_button = task.add_completion_button()
			self.view.add_subview(completion_button)
		 
		self.view.add_subview(task.button)

		lifelpDataBase.save_custom_view(self.serial_num, self.options, self.tasks)
		
			#then i guess i should just re-present the physicsl view
		self.more_views.custom_task_options_view.close()	
	
	def custom_edit_mode(self, sender):
		if sender.title == "edit":
			for task in self.tasks:
				if self.completable == False:
					button = task.add_completion_button()
					self.view.add_subview(button)
				task.completion_button.background_color = "#ff591e"
			sender.title = "done"
		else:
			for task in self.tasks:
				button = task.completion_button
				if task.completed:
					button.background_color = "2ce56d"
				else:
					button.background_color = "red"
					
				if self.completable == False:
					self.view.remove_subview(button)
			sender.title = "edit"
		
	def link_view(self, serial_num):
		self.more_views.cur_view.button_needing_link.title = serial_num
		
	def save_self(self):
		lifelpDataBase.save_custom_view(self.serial_num, self.options, self.tasks)


		
	

#############################
#############################
#############################
#     Custom_Task Class      #		

#holds all data and functionality
#for the tasks that are in views
#in the More_Views section

class Custom_Task:
	def __init__(self, position, completed, options, more_views):
		#position in the display order
		self.position = position
		#is task completed
		self.completed = completed
		self.completion_button = None
		
		self.more_views = more_views
		
		self.set_options(options)
		
		
	def set_task_completion(self, sender):
		if sender.background_color == (1.0, 0.34901960784313724, 0.11764705882352941, 1.0):
			self.more_views.cur_view.edit_task(self.position)
		else:
			if self.completed:
				sender.background_color = "red"
				self.completed = False
			else:
				sender.background_color = "#2ce56d"
				self.completed = True
			self.more_views.cur_view.save_self()
		
	def open_attached_view(self, sender):
		if self.attached_view != "none":
			self.more_views.open_custom_view(self.attached_view)
		
	def set_options(self, options):
		self.options = options
		
		#option 1
		self.name = options[0]
		
		button = ui.Button(title = self.name)
		button.center = (230, 25 + 40 * self.position)
		
		#option 2
		if options[1][0] == 0:
			self.attached_view = options[1][1]
			button.action = self.open_attached_view
		else:
			self.attached_view = "none"
			button.action = None
			
		self.button = button
		
	def add_completion_button(self):
		if self.completion_button == None:
			button = ui.Button(title = str(self.position+1))
			self.completion_button = button
			button.name = str(self.position + 1)
			button.center = (35, 25 + 40 * self.position)
			button.action = self.set_task_completion
			if self.completed:
				button.background_color = "#2ce56d"
			else:
				button.background_color = "red"
		
		return self.completion_button
