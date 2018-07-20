#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from ncengine import NCEngine

# --- Variables -----------------------------------------------------------------------------------

running = True

# --- Functions -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------


# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

# set minimum, before screen blanks
obj.frameMin = [50, 30]
# add dat to frame/display
obj.frame.append([2, 2, 'Are you sure that you want to overwrite the ORIGINAL file "' + '1' + '" with its backup?' , 5])
obj.frame.append([3, 2, 'This is a potentially very dangerous operation!!!', 5])
obj.frame.append([5, 2, 'Please type in "doit!" to complete the operation', 5])
obj.frame.append([5, 18, 'doit!', 6])
obj.frame.append([6, 2, 'Any other command cancels request', 5])

# loop and test keys
while running:
	obj.render()		# update screen rendering
	key = obj.getInput()
	if key == 113:
		running = False

obj.terminate()
sys.exit('\n Program terminated normally...\n')






# --- TODO ---------------------------------------------------------------------------------------
# -

