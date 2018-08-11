#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import locale
from ncengine import NCEngine

# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

obj.borderColor = 1
obj.addLine('v', 50.0)
obj.addLine('v', 30)
obj.addLine('h', 2)
obj.addLine('h', 21.0)

# Add top menus
obj.addLabel(0, 0, 'Menu A', 3, False)
obj.addLabel(50., 0, 'Menu B', 3, False)

# add Menu
obj.addMenu(0, 2, ["First", "Second", "Third", "Fourthflippingfourth", "Motherflippin' fifth", "Sixth"], obj.color['red'], False)
obj.addMenu(20, 10, ["First", "Second", "Third", "Fourthflippingfourth"], obj.color['red'], True)
obj.addMenu(20, 21, ['1', '2', '3'], obj.color['green'], False)
obj.addMenu(25, 20, ['test123'], obj.color['blue'], True)
obj.addTextbox(50., 2, ["-", "-", "-", "-", "-", "-"], obj.color['red'], False)


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

