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

# add dat to frame/display
obj.frame.append([2, 2,  'Are you sure thatINAL file "' + '1' + '" with its backup?' , 5])
obj.frame.append([2, 3,  'This is a potentially very dangerous operats a potentially very dangerous operats a potentially very dangerous operats a potentially very dangerous operation!!!', 5])
obj.frame.append([2, 4,  'Please type in "doit!" to complete the operation', 5])
obj.frame.append([2, 5,  'Any other command cancels request', 5])
obj.frame.append([2, 32, 'Any other command cancels request', 5])

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

