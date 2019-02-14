#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import locale
from ncengine import NCEngine

# --- Variables -----------------------------------------------------------------------------------

initialValues = {	"First" 				: "Text1",
			"Second" 				: "Text2",
			"Third" 				: "127.0.0.1",
			"Fourthflippingfourth" 			: "2a80:1093:2ab1:12a1:1231:42bc",
			"Motherflippin' fifth" 			: "False",
			"Sixth" 				: "247824"
		}

valueType =	[	'text',
			'text',
			'ipv4',
			'ipv6',
			'bool',
			'digits'
		]

# --- Functions  ----------------------------------------------------------------------------------

def checkType(inText, inType):
    """ Checks that a certain texts adheres to a certain standard """
    if inType == 'digits':
        if inText.isdigit():
            return True
    elif inType == 'bool':
        if inText == 'True' or inText == 'False':
            return True
    elif inType == 'ipv4':
        if inText.count('.') == 3 and (inText.replace('.','')).isdigit():
            return True
    elif inType == 'ipv6':
        if inText.count(':') == 5 and len(inText) == 29:
            return True
    return False

# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

obj.borderColor = 1
obj.addGridLine('v', 50.0)
obj.addGridLine('h', 2)

# Add top menus
obj.addLabel(0, 0, 'Movie Files', 6)
obj.addLabel(50., 0, 'Actions', 6)
obj.status = 'spark mig!'

# add Menu
menuID = obj.addMenu(0, 2, list(initialValues.keys()), obj.color['orange'], False)
textBoxID = obj.addTextbox(50., 2, list(initialValues.values()), obj.color['cyan'], False)
obj.activeObject = menuID

# loop and test keys
while obj.running:
	obj.render()		# update screen rendering
	keyPressed = obj.getInput()
	# handle unknown keystrokes
	if keyPressed == 10:	# KEY_ENTER
		textToEdit = obj.objects[textBoxID].content[obj.pointer]
#		if 'False' in textToEdit or 'True' in textToEdit:

		if valueType[obj.pointer] == 'bool':
			editedText = obj.boolEditor(50., obj.pointer + 3, textToEdit, 2)
		elif valueType[obj.pointer] == 'digits':
			editedText = obj.digitsEditor(50., obj.pointer + 3, textToEdit, 2)
		else:
			editedText = obj.textEditor(50., obj.pointer + 3, textToEdit, 2)

		if checkType(editedText, valueType[obj.pointer]):
			obj.objects[textBoxID].content[obj.pointer] = editedText
		else:
			pass	# Set status that type failed




print(obj.objects[textBoxID].content)	# Should be reconstructed to match initialValues

for k in initialValues.keys():
    print(k)


# --- TODO ---------------------------------------------------------------------------------------
# -



