#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import locale
from ncengine import NCEngine

# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

obj.borderColor = 1
obj.addGridLine('v', 50.0)
obj.addGridLine('h', 2)

# Add top menus
obj.addLabel(0, 0, 'Movie Files', 6)
obj.addLabel(50., 0, 'Actions', 6)

# add Menu
textBoxID = obj.addTextbox(50., 2, ["Text1", "Text2", "127.0.0.1", "2a80:1093:2ab1:12a1:1231:42bc", "False", "Text6"], obj.color['cyan'], False)
obj.addMenu(0, 2, ["First", "Second", "Third", "Fourthflippingfourth", "Motherflippin' fifth", "Sixth"], obj.color['orange'], False)
obj.activeObject = 3

# loop and test keys
while obj.running:
	obj.render()		# update screen rendering
	keyPressed = obj.getInput()
	# handle unknown keystrokes
	if type(keyPressed) is list:
		if keyPressed == [10]:	# KEY_ENTER
			yPosition = obj.objects[obj.activeObject].pointer.get()
			textToEdit = obj.objects[textBoxID].content[yPosition]
			editedText = obj.textEditor(50., yPosition + 3, textToEdit, 2)
			obj.objects[textBoxID].content[yPosition] = editedText
obj.terminate()
print('return value')






# --- TODO ---------------------------------------------------------------------------------------
# -

