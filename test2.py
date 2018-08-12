#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import locale
from ncengine import NCEngine

# --- Variables -----------------------------------------------------------------------------------

values = {	"First" 				: "Text1", 
			"Second" 				: "Text2", 
			"Third" 				: "127.0.0.1", 
			"Fourthflippingfourth" 	: "2a80:1093:2ab1:12a1:1231:42bc", 
			"Motherflippin' fifth" 	: "False", 
			"Sixth" 				: "Text6"
		 }

# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

obj.borderColor = 1
obj.addGridLine('v', 50.0)
obj.addGridLine('h', 2)

# Add top menus
obj.addLabel(0, 0, 'Movie Files', 6)
obj.addLabel(50., 0, 'Actions', 6)

# add Menu
menuID = obj.addMenu(0, 2, list(values.keys()), obj.color['orange'], False)
textBoxID = obj.addTextbox(50., 2, list(values.values()), obj.color['cyan'], False)
obj.activeObject = menuID

# loop and test keys
while obj.running:
	obj.render()		# update screen rendering
	keyPressed = obj.getInput()
	# handle unknown keystrokes
	if type(keyPressed) is list:
		if keyPressed == [10]:	# KEY_ENTER
			y = obj.getObject(menuID).pointer.get()
			textToEdit = obj.getObject(textBoxID).content[y]
			editedText = obj.textEditor(50., y + 3, textToEdit, 2)
			obj.getObject(textBoxID).content[y] = editedText
			values[y] = editedText


print(values)






# --- TODO ---------------------------------------------------------------------------------------
# -

