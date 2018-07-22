#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import locale
from ncengine import NCEngine

# --- Variables -----------------------------------------------------------------------------------

running = True

# --- Functions -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------


# --- Main  ---------------------------------------------------------------------------------------

obj = NCEngine()

# add dat to frame/display
obj.frame.append([2, 2,  'Any other command cancels request', 0])
obj.frame.append([2, 3,  'Any other command cancels request', 1])
obj.frame.append([2, 4,  'Any other command cancels request', 2])
obj.frame.append([2, 5,  'Any other command cancels request', 3])
obj.frame.append([2, 6,  'Any other command cancels request', 4])
obj.frame.append([2, 7,  'Any other command cancels request', 5])
obj.frame.append([2, 8,  'Any other command cancels request', 6])
obj.frame.append([2, 9,  'Any other command cancels request', 7])
obj.frame.append([2, 10,  'Any other command cancels request', 8])
obj.frame.append([2, 11,  'Any other command cancels request', 9])
obj.frame.append([2, 12,  'Any other command cancels request', 10])
obj.frame.append([2, 13,  'Any other command cancels request', 11])
obj.frame.append([2, 14,  'Any other command cancels request', 12])
obj.frame.append([2, 15,  'Any other command cancels request', 13])
obj.frame.append([2, 16,  'Any other command cancels request', 14])
obj.frame.append([2, 17,  'Any other command cancels request', 15])

# add Menu
obj.createMenu(20, 10, ["First", "Second", "Third", "Fourthflippingfourth"], obj.color['red'], True)
obj.createMenu(20, 21, ['1', '2', '3'], obj.color['green'])
obj.createMenu(25, 20, ['test123'], obj.color['blue'])

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

