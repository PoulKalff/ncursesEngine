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
	""" A menu where the user can choose between lines of text """

	def __init__(self, xPos, yPos, items, color, mWidth, frame):
		self.x = xPos
		self.y = yPos
		self.frame = frame
		self.color = color
		self.items = items
		self.maxWidth = mWidth
		self.visible = True
		self.highlighted =  1
		self.pointer = RangeIterator(len(items) - 1, False)


class Textbox:
	""" A collection of text-lines """

	def __init__(self, xPos, yPos, items, color, mWidth, frame):
		self.x = xPos
		self.y = yPos
		self.frame = frame
		self.color = color
		self.items = items
		self.maxWidth = mWidth
		self.visible = True


class NCEngine:
	""" Presents the screen of a program """

	status = 'Init'
	color = { 'white': 0, 'red': 1, 'green' : 2, 'orange' : 3, 'blue' : 4, 'purple' : 5, 'cyan' : 6, 'lightgrey' : 7}	# basic colors
	_borderColor = False	# no border drawn if no color is set
	lines = []
	objects = []
	running = True


	def __init__(self):
		self.screen = curses.initscr()
		self.screen.border(0)
		self.screen.keypad(1)
		self.screen.scrollok(0) 
		self._getSize()
		curses.noecho()
		curses.curs_set(0)
		# init colors
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i, i, -1)
		curses.init_pair(200, curses.COLOR_RED, curses.COLOR_WHITE)			# init 256 colors + 1 special


	def showColors(self):
		""" Show all colors available with their numbers (helper function) """
		sys.exit('notImplemented')


	def _getSize(self):
		""" Update height/width/center """
		self.height, self.width = self.screen.getmaxyx()
		self.hcenter = int((self.width - 1) / 2)
		self.vcenter = (self.height - 1) / 2


	def render(self):
		""" handles resize and displays the data in "data" """
		self._getSize()
		if self.width > 20 and self.height > 20:
			self.screen.clear()
			# check if resized
			if curses.is_term_resized(self.height, self.width):
				curses.resizeterm(self.height, self.width)
			# render border
			if self._borderColor:
				self.drawBorder()
			# render lines
			self.drawLines()
			# render status
			self.screen.addstr(self.height - 1, 1, self.status , curses.color_pair(1))
			# render objects
			self.drawObjects()
			self.screen.refresh()


	def drawObjects(self):
		""" Draw all objects in object collection """
		for o in self.objects:
			posX = int((o.x * self.width / 100) if type(o.x) == float else o.x)
			posY = int((o.y * self.height / 100) - 1 if type(o.y) == float else o.y)
			# frame
			if o.frame:
				if o.maxWidth + o.x < self.width:
					for nr, item in enumerate(o.items):
						self.screen.addstr(o.y + nr + 1, o.x, '│ ' + (o.maxWidth * ' ')  + ' │', curses.color_pair(o.color))
				self.screen.addstr(o.y, o.x, '╭─' + ('─' * o.maxWidth) + '─╮', curses.color_pair(o.color))						# Top
				self.screen.addstr(o.y + len(o.items) + 1, o.x, '└─' + ('─' * o.maxWidth) + '─╯', curses.color_pair(o.color))		# Bottom
			# text
			for nr, item in enumerate(o.items):
				itemColor = curses.color_pair(o.color)
				if type(o) is Menu:
					if nr == o.highlighted - 1:
						itemColor = curses.color_pair(200)
				self.screen.addstr(posY + nr + 1, posX + 2, item, itemColor)


	def drawLines(self):
		""" Draw all lines added to object (except border) """
		intersections = [[], []]
		for l in self.lines:
			if l[0] == 'v':
				position = int((l[1] * self.width / 100) if type(l[1]) == float else l[1])
				intersections[0].append(position)
				for yPos in range(1, self.height - 2):
					self.screen.addstr(yPos, position, '│', curses.color_pair(self.borderColor))
				# endpoints
				self.screen.addstr(0, position, '┬', curses.color_pair(self.borderColor))
				self.screen.addstr(self.height - 2, position, '┴', curses.color_pair(self.borderColor))
			elif l[0] == 'h':
				position = int((l[1] * self.height / 100) - 1 if type(l[1]) == float else l[1])
				intersections[1].append(position)
				self.screen.addstr(position, 1, '─' * (self.width - 2), curses.color_pair(self.borderColor))
				# endpoints
				self.screen.addstr(position, 0, '├', curses.color_pair(self.borderColor))
				self.screen.addstr(position, self.width - 1, '┤', curses.color_pair(self.borderColor))
		# draw intersections
		for x in intersections[1]:
			for y in intersections[0]:
				self.screen.addstr(x, y, '┼', curses.color_pair(self.borderColor))


	def drawBorder(self):
		""" Draw the staic border of the screen """
		# horizontal lines
		self.screen.addstr(0, 0, '╭' + '─' * (self.width - 2) + '╮', curses.color_pair(self.borderColor))						# Top
		self.screen.addstr(self.height - 2, 0, '└' + '─' * (self.width - 2) + '╯', curses.color_pair(self.borderColor))			# Bottom
		# vertical lines
		for yPos in range(1, self.height - 2):
			self.screen.addstr(yPos, 0, '│', curses.color_pair(self.borderColor))
			self.screen.addstr(yPos, self.width - 1, '│', curses.color_pair(self.borderColor))


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


# --- Setter Functions ----------------------------------------------------------------------------


	@property
	def borderColor(self):
		return self._borderColor

	@borderColor.setter
	def borderColor(self, val):
		self._borderColor = self.color[val.lower()] if type(val) == str else val


	def addGridLine(self, type, coordinate):
		self.lines.append([type, coordinate])


	def addLabel(self, x, y, item, color, frame):
		maxLength = len(item)
		self.objects.append(Textbox(x, y, [item], color, maxLength, frame))


	def addTextbox(self, x, y, items, color, frame):
		maxLength = len(max(items, key=lambda coll: len(coll)))
		self.objects.append(Textbox(x, y, items, color, maxLength, frame))


	def addMenu(self, x, y, items, color, frame):
		maxLength = len(max(items, key=lambda coll: len(coll)))
		self.objects.append(Menu(x, y, items, color, maxLength, frame))





# --- TODO ---------------------------------------------------------------------------------------
# - BUG 	: Stadigt problemer med scroll/count af bytes.....
# - BUG 	: Screen dies if too small for objects.....
# - BUG 	: Rod med menu-farven, 300 kan ikke bruges

# - FEATURE : lave et MIN, så screen ikke renderes hvis objects ikke kan vaere paa skaermen
# - FEATURE : Lave properties til alt, som kan indstilles


