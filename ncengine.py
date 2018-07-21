#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import curses
import locale

# --- Variables -----------------------------------------------------------------------------------

version = "v1.03"   # added support for relaoding from .log
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# --- Classes -------------------------------------------------------------------------------------

class NCEngine:
	""" Presents the screen of a program """

	frame = []
	frameMin = [10,10]
	menus = []

	def __init__(self):
		self.screen = curses.initscr()
		self.screen.border(0)
		self.screen.keypad(1)
		self.updatePosition()
		curses.noecho()
		curses.start_color()
		curses.curs_set(0)
		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)			# more generic... have 2 standard, and other must be custom?
		curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)


	def updatePosition(self):
		self.height, self.width = self.screen.getmaxyx()
		self.center = (self.width - 1) / 2


	def createMenu(self, posX, posY, items):
		""" Creates the data used for painting a menu """
		screenData = []
		self.updatePosition()
		maxLength = len(max(items, key=lambda coll: len(coll)))
		maxHeight = len(items)
		screenData.append([posX, posY, '╭─' + ('─' * maxLength) + '─╮', 5])					# Top
		for nr, item in enumerate(items):
			missingSpace = maxLength - len(item)
			screenData.append([posX, posY + nr + 1, '│ ' + item + (missingSpace * ' ')  + ' │', 5])
		screenData.append([posX, posY + maxHeight + 1, '└─' + ('─' * maxLength) + '─╯', 5])		# Bottom
		self.menus.append(screenData)


	def lastMenuSpecs(self):
		""" Get specifications of the last menu """
		pass	# Use this to build next menu


	def render(self):
		""" handles resize and displays the data in "data" """
		self.updatePosition()
		self.screen.clear()
		# check if resized
		if curses.is_term_resized(self.height, self.width):
			curses.resizeterm(self.height, self.width)
		# collect data
		dispData = self.frame
		for menu in self.menus:
			for line in menu:
				dispData.append(line)
		# paint window
		if self.height > self.frameMin[0] and self.width > self.frameMin[1]:    # Match text when populated
			for x, y, text, color in dispData:
				totalLength = x + len(text)
				if totalLength > self.width:
					text = text[:self.width - 6] + ' >>'
				if y < self.height:
					self.screen.addstr(y, x, str(text), curses.color_pair(color))
				else:
					self.screen.addstr(self.height - 1, 2, '^ ' * (self.width / 2 - 2), curses.color_pair(color))
		elif self.height > 1 and self.width > 5:
			self.screen.addstr(0, 0, "Window not displayed", curses.color_pair(1))
		self.screen.refresh()


	def getInput(self):
		""" Retrieve input from the keyboard and return those"""
		keyPressed = self.screen.getch()
		return keyPressed


	def terminate(self):
		# Set everything back to normal
		self.screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()





# --- TODO ---------------------------------------------------------------------------------------
# -

