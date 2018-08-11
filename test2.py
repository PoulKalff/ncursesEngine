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
obj.addLabel(0, 0, 'Movie Files', 6, False)
obj.addLabel(50., 0, 'Actions', 6, False)

# add Menu
obj.addTextbox(50., 2, ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6"], obj.color['green'], False)
obj.addMenu(0, 2, ["First", "Second", "Third", "Fourthflippingfourth", "Motherflippin' fifth", "Sixth"], obj.color['orange'], False)


# loop and test keys
while obj.running:
	obj.render()		# update screen rendering
	keyPressed = obj.getInput()

	if keyPressed == 113:		# <escape>
		obj.running = False
	elif keyPressed == 259:		# KEY_UP
		pass
	elif keyPressed == 258:		# KEY_DOWN
		pass
	elif keyPressed == 260:		# KEY_LEFT
		pass
	elif keyPressed == 261:		# KEY_RIGHT
		pass

obj.terminate()
sys.exit('\n Program terminated normally...\n')






# --- TODO ---------------------------------------------------------------------------------------
# -

