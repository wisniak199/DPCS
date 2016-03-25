#!/usr/bin/env python3

import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os.path

# the window title
PANELTITLE = "DPCS Settings"

# about DPCS - authors, basic info, licensing and such...
ABOUT_DPCS = """ To be written!
"""

# minimal window width and height
WIDTH = 350
HEIGHT = 400
# settings dictionary
settings = {}
#config file path
FILE = os.path.expanduser('~/.dpcs/.dpcsconfig')

buttonlist = []

def displaypanel():
	""" displays the prefs dialog
	"""
	win = SettingsPanel()
	win.show_all()
	Gtk.main()

def addCheckButton(label, parent): 
	""" add checkbox with label @label to container @parent 
	"""
	checkButton = Gtk.CheckButton.new_with_label(label)
	parent.pack_start(checkButton, False, False, 10)
	buttonlist.append(checkButton)
	return checkButton
		
def save_setting (checkButton): 
	""" saves checkbox value in settings
	"""
	if checkButton.get_active():
		value = 'true'
	else:
		value = 'false'
	settings[checkButton.get_label()] = value

def load_setting (checkButton): 
	""" loads initial value of @checkbutton
	"""	
	if settings[checkButton.get_label()] == 'true' :
		checkButton.set_active(True)
	else:
		checkButton.set_active(False)

class SettingsPanel(Gtk.Window):
	""" The preferences dialog for DPCS
	"""
	
	def __init__(self):
		Gtk.Window.__init__(self, title=PANELTITLE)
		self.set_size_request(WIDTH,HEIGHT)

		maincontainer = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
		self.add(maincontainer)

		notebook = Gtk.Notebook()
		maincontainer.pack_start(notebook, True, True, 0)

		buttonscontainer = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
		maincontainer.pack_start(buttonscontainer, False, False, 0)

		# settings tab

		settingspage = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)

		# add setting boxes here by addCheckButton(Label, Box)
		
		eb = addCheckButton('Enable DPCS', settingspage)
		ab = addCheckButton('test1', settingspage)
		bb = addCheckButton('test2', settingspage)
		gb = addCheckButton('test3', settingspage)
		
		# end of setting boxes

		notebook.append_page(settingspage, Gtk.Label('Settings'))

		# about DPCS tab

		aboutpage = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5)

		acontent = Gtk.Label()
		acontent.set_text(ABOUT_DPCS)
		acontent.set_justify(Gtk.Justification.LEFT)
		aboutpage.pack_start(acontent, True, True, 0)

		notebook.append_page(aboutpage, Gtk.Label('About DPCS'))

		# ok, apply and cancel buttons

		self.ok = Gtk.Button(label="Ok")
		cancel = Gtk.Button(label="Cancel")
		applyb = Gtk.Button(label="Apply")

		buttonscontainer.pack_end(self.ok, False, False, 0)
		buttonscontainer.pack_end(applyb, False, False, 0)
		buttonscontainer.pack_end(cancel, False, False, 0)

		cancel.connect("clicked", Gtk.main_quit)
		applyb.connect("clicked", self.applysettings)
		self.ok.connect("clicked", self.applysettings)
		
		# loads current config
		self.loadconfig()
		self.connect("delete-event", Gtk.main_quit)
		

	def applysettings(self, widget):
		""" writes settings to dpcs.config, exits
		if ok has been pressed
		"""
		os.makedirs(os.path.dirname(FILE), exist_ok=True)
		f = open(FILE, 'w')

		for s in buttonlist:
			save_setting(s)
		json.dump(settings, f, indent=2)
		f.close()
		if widget == self.ok:
			Gtk.main_quit()

	def loadconfig(self):
		""" loads current settings from dpcs.config
		"""
		if os.path.isfile(FILE):
			f = open(FILE, 'r')
			settings.update(json.load(f))
			for b in buttonlist:
				load_setting(b)

			f.close()

if __name__ == "__main__":
	displaypanel()