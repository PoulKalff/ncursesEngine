#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

# --- Variables -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------

class NCEngine:
	""" Presents the screen of a program """

	frame = []
	frameMin = [10,10]

	def __init__(self):
		self.screen = curses.initscr()
		self.screen.border(0)
		self.screen.keypad(1)
		self.updatePosition()
		curses.noecho()
		curses.start_color()
		curses.curs_set(0)


	def updatePosition(self):
		self.height, self.width = self.screen.getmaxyx()
		self.center = (self.width - 1) / 2


	def createMenu(self, posX, posY, items):
		""" Creates the data used for painting a menu """
		screenData = []
		self.updatePosition()
		# horizontal lines
		screenData.append([yCord + 3, xCord, '╭' + '─' * 21 + '╮', 5])
		screenData.append([yCord + 9, xCord, '└' + '─' * 21 + '╯', 5])
		# vertical lines
		screenData.append([yCord + 4, xCord, '│                     │', 5])
		screenData.append([yCord + 5, xCord, '│                     │', 5])
		screenData.append([yCord + 6, xCord, '│                     │', 5])
		screenData.append([yCord + 7, xCord, '│                     │', 5])
		# text
		col = [4, 4, 4]
		screenData.append([yCord + 5, xCord + 5, 'Add New Item', col[0]])
		screenData.append([yCord + 6, xCord + 5, 'Purge Backups', col[1]])
		screenData.append([yCord + 7, xCord + 5, 'Switch View', col[2]])
		return screenData


	def validate(self):
		""" checks the data in self.frame, ensures that no data exists outside borders """
		pass


	def render(self):
		""" handles resize and displays the data in "data" """
		self.validate()
		self.screen.clear()
		# check if resized
		self.updatePosition()
		if curses.is_term_resized(self.height, self.width):
			curses.resizeterm(self.height, self.width)
		# paint window
		if self.height > self.frameMin[0] and self.width > self.frameMin[0]:    # Match text when populated
			for x, y, text, color in self.frame:
				try:
					self.screen.addstr(x, y, str(text), curses.color_pair(color))
				except Exception as inst:
					sys.exit(str(inst))
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

