#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import sys

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


	def render(self):
		""" handles resize and displays the data in "data" """
		self.updatePosition()
		self.screen.clear()
		# check if resized
		if curses.is_term_resized(self.height, self.width):
			curses.resizeterm(self.height, self.width)
		# paint window
		if self.height > self.frameMin[0] and self.width > self.frameMin[1]:    # Match text when populated
			for x, y, text, color in self.frame:
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

