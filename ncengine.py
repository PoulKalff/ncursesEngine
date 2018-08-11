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
	# (v3) Represents a range of INTs from 0 -> X

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

	def incMax(self, count=1):
		""" Increase both value and max valuse """
		self.max += count
		self.current += count
		self._test()

	def decMax(self, count=1):
		""" Increase both value and max valuse """
		self.max -= count
		self.current -= count
		self._test()

	def _test(self):
		self.max = 0 if self.max < 0 else self.max
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

	def __init__(self, xPos, yPos, content, color, mWidth, frame):
		self.x = xPos
		self.y = yPos
		self.frame = frame
		self.color = color
		self.content = content
		self.maxWidth = mWidth
		self.visible = True
		self.pointer = RangeIterator(len(content) - 1, False)


class Textbox:
	""" A collection of text-lines """

	def __init__(self, xPos, yPos, content, color, mWidth, frame):
		self.x = xPos
		self.y = yPos
		self.frame = frame
		self.color = color
		self.content = content
		self.maxWidth = mWidth
		self.visible = True


class Label:
	""" One simple text-line """

	def __init__(self, xPos, yPos, content, color, mWidth):
		self.x = xPos
		self.y = yPos
		self.color = color
		self.content = content
		self.maxWidth = mWidth
		self.visible = True


class NCEngine:
	""" Presents the screen of a program """

	status = 'Init'
	color = { 'white': 0, 'red': 1, 'green' : 2, 'orange' : 3, 'blue' : 4, 'purple' : 5, 'cyan' : 6, 'lightgrey' : 7}	# basic colors
	_borderColor = False	# no border drawn if no color is set
	lines = []
	objects = []
	_activeObject = None
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
		self.generateID = self.idGenerator()


	def idGenerator(self):
		n = 0
		while True:
			yield n
			n += 1


	def getID(self):
		""" Get the next sequential ID """
		return next(self.generateID)


	def boolEditor(self, value, xPos, yPos):
		""" Edits True/False """
		bValue = 0 if value == 'False' else 1
		pointer = FlipSwitch(bValue)
		teRunning = True
		height, width = self.parent.screen.getmaxyx()
		self.screen.addstr(height - 1, 0, 'UP/DOWN changes state, ENTER accepts changes', curses.color_pair(6))    # Overwrite Status
		while teRunning:
			self.screen.addstr(yPos + 4, xPos + 10, pointer.getString() + ' ', curses.color_pair(5))
			self.screen.refresh()
			keyPressed = self.screen.getch()
			if keyPressed == 259 or keyPressed == 258:             # Cursor UP / Down
				pointer.flip()
			elif keyPressed == 260:           # Cursor LEFT
				teRunning = False
			elif keyPressed == 10:           # Return (Select)
				teRunning = False
		strValue = pointer.getString()
		returnValue = strValue + ' ' if len(strValue) == 4 else strValue
		return returnValue


	def digitsEditor(self, eString, xPos, yPos):
		""" Edits digits """
		pointer = RangeIterator(len(eString) - 1, False)
		keyPressed = ''
		teRunning = True
		height, width = self.parent.screen.getmaxyx()
		self.screen.addstr(height - 1, 0, 'UP/DOWN cycles digit, ENTER accepts changes', curses.color_pair(6))    # Overwrite Status
		while teRunning:
			stringSliced = [eString[:pointer.get()], eString[pointer.get()], eString[pointer.get() + 1:]]
			self.screen.addstr(yPos + 4, xPos + 10, stringSliced[0], curses.color_pair(5))
			self.screen.addstr(yPos + 4, xPos + 10 + len(stringSliced[0]), stringSliced[1], curses.color_pair(1))
			self.screen.addstr(yPos + 4, xPos + 10 + len(stringSliced[0]) + len(stringSliced[1]), stringSliced[2], curses.color_pair(5))
			self.screen.addstr(yPos + 4, xPos + 10 + len(stringSliced[0]) + len(stringSliced[1]) + len(stringSliced[2]), ' ', curses.color_pair(0))    # overwrite last char
			#self.screen.addstr(yPos + 6, xPos + 10, str(stringSliced) + ' - ' + str(keyPressed), curses.color_pair(0))      # Message output
			self.screen.refresh()
			keyPressed = self.screen.getch()
			focusedChar = int(stringSliced[1])
			if keyPressed == 259:             # Cursor UP
				if focusedChar < 9:
					stringSliced[1] = str(focusedChar + 1)
			elif keyPressed == 258:           # Cursor DOWN
				if focusedChar > 0:
					stringSliced[1] = str(focusedChar - 1)
			if keyPressed == 261:           # Cursor RIGHT
				pointer.inc()
				if len(stringSliced[2]) > 0 and stringSliced[2][0] == ':':
					pointer.inc()
			elif keyPressed == 260:           # Cursor LEFT
				if pointer.get() == 0:
					returnFile = stringSliced[0] + stringSliced[1] + stringSliced[2]
					teRunning = False
				else:
					pointer.dec()
					if len(stringSliced[0]) > 0 and stringSliced[0][-1] == ':':
						pointer.dec()
			elif keyPressed == 10:           # Return (Select)
				returnFile = stringSliced[0] + stringSliced[1] + stringSliced[2]
				teRunning = False
			elif keyPressed > 47 and keyPressed < 58:   # 0-9
				stringSliced[1] = chr(keyPressed)
				pointer.inc()
				if len(stringSliced[2]) > 0 and stringSliced[2][0] ==  ':':
					pointer.inc()
			eString = stringSliced[0] + stringSliced[1] + stringSliced[2]
		return returnFile



	def textEditor(self, x, y, eString, color):
		""" Edits a line of text """
		pointer = RangeIterator(len(eString) - 1, False)
		keyPressed = ''
		editorRunning = True
		stringSliced = [[], [], []]
		xPos = int((x * self.width / 100) + 2 if type(x) == float else x)
		yPos = int((y * self.height / 100) - 1 if type(y) == float else y)
		self.screen.addstr(yPos, xPos, eString, curses.color_pair(2))     # overwrite line to edit
		while editorRunning:
			if len(eString) > 0:
				stringSliced[0] = eString[:pointer.get()]
				stringSliced[1] = eString[pointer.get()]
				stringSliced[2] = eString[pointer.get() + 1:]
			self.screen.addstr(yPos, xPos, stringSliced[0], curses.color_pair(color))
			self.screen.addstr(yPos, xPos + len(stringSliced[0]), stringSliced[1], curses.color_pair(200))
			self.screen.addstr(yPos, xPos + len(stringSliced[0]) + len(stringSliced[1]), stringSliced[2], curses.color_pair(color))
			self.screen.addstr(yPos, xPos + len(stringSliced[0]) + len(stringSliced[1]) + len(stringSliced[2]), ' ', curses.color_pair(3))    # overwrite last char
# Debug:
			self.screen.addstr(20, 2, "Lenght: " + str(len(eString)) + '   Pointer:' + str(pointer.get()) + '   PointerMax:' + str(pointer.max) + '  ' , curses.color_pair(4))
			self.screen.addstr(21, 2, str(stringSliced) + ' ' , curses.color_pair(4))
			self.screen.addstr(22, 2, str(len(stringSliced[0])) + ' ' + str(len(stringSliced[1])) + ' ' + str(len(stringSliced[2])) + ' ', curses.color_pair(4))
# Debug:
			self.screen.refresh()
			keyPressed = self.screen.getch()
			if keyPressed == 261:            # Cursor RIGHT
				if len(stringSliced[2]) > 0:
					pointer.inc()
			elif keyPressed == 260:          # Cursor LEFT
				if len(stringSliced[0]) > 0:
					pointer.dec()
			elif keyPressed == 10:           # Return (Select)
				editorRunning = False
				return eString.strip()
			elif keyPressed == 330:          # Del
				if stringSliced[2] != ' ':
					stringSliced[1] = stringSliced[2][:1]
					stringSliced[2] = stringSliced[2][1:]
					if stringSliced[2] == '':
						stringSliced[2] = ' '
				elif stringSliced[2] == ' ':
				   stringSliced[1] = ''
				   stringSliced[2] = ' '
			elif keyPressed == 263:          # Backspace
				stringSliced[0] = stringSliced[0][:-1]
				pointer.decMax()
			elif keyPressed < 256 and chr(keyPressed) in ',./-abcdefghijklmnopqrstuvwqyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ':
				stringSliced[1] = chr(keyPressed) + stringSliced[1]
				pointer.incMax()
			if type(stringSliced) == list:
				eString = ''.join(stringSliced)


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
		if not self.activeObject:
			self.terminate()
			sys.exit('Cannot start program loop without active object. Please set .activeObject')
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
			if type(o) is not Label:
				if o.frame:
					if o.maxWidth + o.x < self.width:
						for nr, item in enumerate(o.content):
							self.screen.addstr(o.y + nr + 1, o.x, '│ ' + (o.maxWidth * ' ')  + ' │', curses.color_pair(o.color))
					self.screen.addstr(o.y, o.x, '╭─' + ('─' * o.maxWidth) + '─╮', curses.color_pair(o.color))						# Top
					self.screen.addstr(o.y + len(o.content) + 1, o.x, '└─' + ('─' * o.maxWidth) + '─╯', curses.color_pair(o.color))		# Bottom
			# text
			for nr, item in enumerate(o.content):
				itemColor = curses.color_pair(o.color)
				if type(o) is Menu:
					if nr == o.pointer.get():
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
		""" Retrieve input and handle internally if understood, else return to calling program """
		keyPressed = self.screen.getch()
		if keyPressed == 113:		# <escape>
			self.terminate()
			self.running = False
		elif keyPressed == 259:		# KEY_UP
			self.objects[self.activeObject].pointer.dec()
		elif keyPressed == 258:		# KEY_DOWN
			self.objects[self.activeObject].pointer.inc()
		elif keyPressed == 260:		# KEY_LEFT
			pass
		elif keyPressed == 261:		# KEY_RIGHT
			pass
		else:
			return [keyPressed]


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


	@property
	def activeObject(self):
		return self._activeObject

	@activeObject.setter
	def activeObject(self, val):
		self._activeObject = val if val < len(self.objects) else None
		if not self._activeObject:
			sys.exit('No object number ' + str(val))


	def addGridLine(self, type, coordinate):
		self.lines.append([type, coordinate])


	def addLabel(self, x, y, item, color):
		maxLength = len(item)
		self.objects.append(Label(x, y, [item], color, maxLength))
		return len(self.objects) - 1


	def addTextbox(self, x, y, items, color, frame):
		maxLength = len(max(items, key=lambda coll: len(coll)))
		self.objects.append(Textbox(x, y, items, color, maxLength, frame))
		return len(self.objects) - 1 


	def addMenu(self, x, y, items, color, frame):
		maxLength = len(max(items, key=lambda coll: len(coll)))
		self.objects.append(Menu(x, y, items, color, maxLength, frame))
		return len(self.objects) - 1





# --- TODO ---------------------------------------------------------------------------------------
# - BUG 	: Stadigt problemer med scroll/count af bytes.....
# - BUG 	: Rod med menu-farven, 300 kan ikke bruges
# - BUG 	: obecjt ID er noget rod.... passer ikke hvis objekter fjernes!


# - FEATURE : lave et MIN, så screen ikke renderes hvis objects ikke kan vaere paa skaermen
# - FEATURE : Lave properties til alt, som kan indstilles
# - FEATURE : Test digitsEditor
# - FEATURE : Test boolEditor

