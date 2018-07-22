#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import curses
import locale

# --- Variables -----------------------------------------------------------------------------------

version = "v0.03"   # initial development
locale.setlocale(locale.LC_ALL, '')

# --- Classes -------------------------------------------------------------------------------------

class FlipSwitch():
    # (NEW) Represents a switch with on and off-state

    def __init__(self, Ind):
        self._value = bool(Ind)

    def flip(self):
        if self._value == True:
            self._value = False
        else:
            self._value = True

    def get(self):
        return self._value

    def getString(self):
        return str(self._value)


class RangeIterator():
    # (NEW) Represents a range of INTs from 0 -> X

    def __init__(self, Ind, loop=True):
        self.current = 0
        self.max = Ind
        self.loop = loop

    def inc(self, count=1):
        self.current += count
        self._test()

    def dec(self, count=1):
        self.current -= count
        self._test()

    def _test(self):
        if self.loop:
            if self.current > self.max:
                self.current -= self.max + 1
            elif self.current < 0:
                self.current += self.max + 1
        elif not self.loop:
            if self.current >= self.max:
                self.current = self.max
            elif self.current < 0:
                self.current = 0

    def get(self):
        return self.current


class Menu:
    """ A menu object """

    def __init__(self, xPos, yPos, items, pointer):
        self.x = xPos
        self.y = yPos
        self.menuItems = items
        self.highlighted =  None
        self.prevPointer = pointer

    def getCoords(self):
        return (self.x, self.y)



class NCEngine:
	""" Presents the screen of a program """

	frame = []
	menus = []
	color = { 'white': 0, 'red': 1, 'green' : 2, 'orange' : 3, 'blue' : 4, 'purple' : 5, 'cyan' : 6, 'lightgrey' : 7}	# basic colors


	def __init__(self):
		self.screen = curses.initscr()
		self.screen.border(0)
		self.screen.keypad(1)
		self.screen.scrollok(0) 
		self.getSize()
		curses.noecho()
		curses.curs_set(0)
		# init colors
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i, i, -1)
		curses.init_pair(300, curses.COLOR_RED, curses.COLOR_WHITE)			# init 256 colors + 1 special


	def showColors(self):
		""" Show all colors available with their numbers (helper function) """
		sys.exit('notImplemented')


	def getSize(self):
		""" Update height/width/center """
		self.height, self.width = self.screen.getmaxyx()
		self.hcenter = (self.width - 1) / 2
		self.vcenter = (self.height - 1) / 2


	def createMenu(self, posX, posY, items, color, frame = True):
		""" Creates the data used for painting a menu """
		screenData = []
		self.getSize()
		maxLength = len(max(items, key=lambda coll: len(coll)))
		maxHeight = len(items)
		# frame
		if frame:
			for nr, item in enumerate(items):
				screenData.append([posX, posY + nr + 1, '│ ' + (maxLength * ' ')  + ' │', color])
			screenData.append([posX, posY, '╭─' + ('─' * maxLength) + '─╮', color])						# Top
			screenData.append([posX, posY + maxHeight + 1, '└─' + ('─' * maxLength) + '─╯', color])		# Bottom
		# text
		for nr, item in enumerate(items):
			screenData.append([posX + 2, posY + nr + 1, item, color])
		self.menus.append(screenData)


	def render(self):
		""" handles resize and displays the data in "data" """
		self.getSize()
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
		if self.height > 5 and self.width > 5:    # Match text when populated
			for x, y, text, color in dispData:
				if x + len(re.sub('[^\w\s]', '', text)) > self.width:
					text = text[:self.width - 5] + ' ⇨'
				if y < self.height:
					self.screen.addstr(y, x, text, curses.color_pair(color))
				else:
					self.screen.addstr(self.height - 1, x, '⇩' * len(re.sub('[^\w\s]', '', text)), curses.color_pair(color))
		elif self.height > 1 and self.width > 5:
			self.screen.addstr(0, 0, "Window not displayed", curses.color_pair(300))
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
# - BUG : Stadigt problemer med scroll/count af bytes.....

