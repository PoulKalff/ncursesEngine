#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import locale
from ncengine import NCEngine

# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

obj.addGridLine('v', 50.0)
obj.addGridLine('v', 30)
obj.addGridLine('h', 2)
obj.addGridLine('h', 21.0)
obj.borderColor = "Red"

# Add top menus
obj.addLabel(0, 0, 'Menu A', 3)
obj.addLabel(50., 0, 'Menu B', 3)

# add Menu
menuID = obj.addMenu(0, 2, ["First", "Second", "Third", "Fourthflippingfourth", "Motherflippin' fifth", "Sixth"], obj.color['red'], False)
obj.addMenu(20, 10, ["First", "Second", "Third", "Fourthflippingfourth"], obj.color['red'], True)
obj.addMenu(20, 21, ['1', '2', '3'], obj.color['green'], False)
obj.addMenu(25, 20, ['test123'], obj.color['blue'], True)
obj.addTextbox(50., 2, ["-", "-", "-", "-", "-", "-"], obj.color['red'], False)
obj.activeObject = menuID


#print(obj._borderColor)
#print(obj.borderColor)
#sys.exit('Killed for DEV')

# loop and test keys
while obj.running:
	obj.render()		# update screen rendering
	key = obj.getInput()
	if key == 113:
		obj.running = False

obj.terminate()
sys.exit('\n Program terminated normally...\n')






# --- TODO ---------------------------------------------------------------------------------------
# -

