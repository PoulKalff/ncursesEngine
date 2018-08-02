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
# obj.objects.append([2, 2,  'Any other command cancels request', 0])
# obj.objects.append([2, 3,  'Any other command cancels request', 1])
# obj.objects.append([2, 4,  'Any other command cancels request', 2])
# obj.objects.append([2, 5,  'Any other command cancels request', 3])
# obj.objects.append([2, 6,  'Any other command cancels request', 4])
# obj.objects.append([2, 7,  'Any other command cancels request', 5])
# obj.objects.append([2, 8,  'Any other command cancels request', 6])
# obj.objects.append([2, 9,  'Any other command cancels request', 7])
# obj.objects.append([2, 10,  'Any other command cancels request', 8])
# obj.objects.append([2, 11,  'Any other command cancels request', 9])
# obj.objects.append([2, 12,  'Any other command cancels request', 10])
# obj.objects.append([2, 13,  'Any other command cancels request', 11])
# obj.objects.append([2, 14,  'Any other command cancels request', 12])
# obj.objects.append([2, 15,  'Any other command cancels request', 13])
# obj.objects.append([2, 16,  'Any other command cancels request', 14])
#obj.objects.append([2, 37,  'Any other command cancels request', 15])

obj.border = True
obj.borderColor = 1
obj.lines.append(['v', 50.0])
obj.lines.append(['v', 30])
obj.lines.append(['h', 2])
obj.lines.append(['h', 21.0])


# add Menu
obj.createMenu(20, 10, ["First", "Second", "Third", "Fourthflippingfourth"], obj.color['red'], True)
obj.createMenu(20, 21, ['1', '2', '3'], obj.color['green'], False)
obj.createMenu(25, 20, ['test123'], obj.color['blue'])
# add top menus
obj.topMenus.append('Menu1')
obj.topMenus.append('Menu2')


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

