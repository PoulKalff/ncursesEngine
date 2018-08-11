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
obj.addTextbox(50., 2, ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6"], obj.color['green'], False)
obj.addMenu(0, 2, ["First", "Second", "Third", "Fourthflippingfourth", "Motherflippin' fifth", "Sixth"], obj.color['orange'], False)
obj.activeObject = 3

#obj.terminate()
#print(obj.objects)
#ys.exit()

# loop and test keys
while obj.running:
	obj.render()		# update screen rendering
	keyPressed = obj.getInput()


obj.terminate()
sys.exit('\n Program terminated normally...\n')






# --- TODO ---------------------------------------------------------------------------------------
# -

