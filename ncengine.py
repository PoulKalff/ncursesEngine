# -*- coding: utf-8 -*-

import os
import re
import sys
import curses
import locale
import poktools

# --- Variables -----------------------------------------------------------------------------------

version = "v0.05"   # added SelectPath
locale.setlocale(locale.LC_ALL, '')

# --- Classes -------------------------------------------------------------------------------------


class File:
		""" Slave class used by SelectPath """
		def __init__(self, name):
				self.name = name
		def pad(self, data, width):
				return data + ' ' * (width - len(data))
		def render(self, depth, width):
				return self.pad('%s%s %s' % (' ' * 4 * depth, self.icon(), os.path.basename(self.name)), width)
		def icon(self): return '   '
		def traverse(self): yield self, 0
		def expand(self): pass
		def collapse(self): pass


class Dir(File):
		""" Slave class used by SelectPath """

		def __init__(self, name):
				File.__init__(self, name)
				try: self.kidnames = sorted(os.listdir(name))
				except: self.kidnames = None  # probably permission denied
				self.kids = None
				self.expanded = False
		def factory(self, name):    # copy of parent, rather than sending it with object
				if os.path.isdir(name): return Dir(name)
				else: return File(name)
		def children(self):
				if self.kidnames is None: return []
				if self.kids is None:
						self.kids = [self.factory(os.path.join(self.name, kid))
												 for kid in self.kidnames]
				return self.kids
		def icon(self):
				if self.expanded: return '[-]'
				elif self.kidnames is None: return '[?]'
				elif self.children(): return '[+]'
				else: return '[ ]'
		def expand(self): self.expanded = True
		def collapse(self): self.expanded = False
		def traverse(self):
				yield self, 0
				if not self.expanded: return
				for child in self.children():
						for kid, depth in child.traverse():
								yield kid, depth + 1

class SelectPath:
		""" Presents a curses screen where user can select a path / file, returns result """

		def __init__(self, pScreen, startDir="/"):
				self.startDir = startDir
				self.screen = pScreen
				self.selected = False
				mydir = self.factory(self.startDir)
				mydir.expand()
				curidx = 3
				pending_action = None
				pending_save = False
				while 1:
						self.screen.clear()
						line = 0
						offset = max(0, curidx - curses.LINES + 3)
						for data, depth in mydir.traverse():
								if line == curidx:
										self.screen.attrset(curses.color_pair(7) | curses.A_BOLD)
										if pending_action:
												getattr(data, pending_action)()
												pending_action = None
										elif pending_save:
												self.selected = data.name
												return
								else:
										self.screen.attrset(curses.color_pair(0))
								if 0 <= line - offset < curses.LINES - 1:
										self.screen.addstr(line - offset, 0, data.render(depth, curses.COLS))
								line += 1
						pending_save = False
						self.screen.refresh()
						ch = self.screen.getch()
						if ch == curses.KEY_UP: curidx -= 1
						elif ch == curses.KEY_DOWN: curidx += 1
						elif ch == curses.KEY_PPAGE:
								curidx -= curses.LINES
								if curidx < 0: curidx = 0
						elif ch == curses.KEY_NPAGE:
								curidx += curses.LINES
								if curidx >= line: curidx = line - 1
						elif ch == curses.KEY_RIGHT: pending_action = 'expand'
						elif ch == curses.KEY_LEFT: pending_action = 'collapse'
						elif ch == 27 or ch == 113: return    # <return> or 'q'
						elif ch == ord('\n'): pending_save = True
						curidx %= line


		def factory(self, name):
				""" Slave function, to build up path """
				if os.path.isdir(name): return Dir(name)
				else: return File(name)


class nceLabel:
	""" Label object"""

	def __init__(self, _xPos, _yPos, _text, _color, _mWidth, _relativeToCenter):
		self.x = _xPos
		self.y = _yPos
		self.rtc = _relativeToCenter
		self.color = _color
		self.content = [[_text, _color]]
		self.maxWidth = _mWidth
		self.visible = True



class nceDialogBox:
	""" Dialog object, which can only be YES or NO """

	def __init__(self, _xPos, _yPos, _content, _color, _relativeToCenter):
		self.x = _xPos
		self.y = _yPos
		self.rtc = _relativeToCenter
		self.color = _color
		maxLength = max(len(x) for x in _content)
		self.content = []
		_content.append('YES')
		_content.append('NO!')
		maxLength = max(len(x) for x in _content)
		for nr, line in enumerate(_content):
			missing = round((maxLength - len(line)) / 2) if len(line) < maxLength else 0
			pad = missing * ' '
#			_content[nr] = pad + line + pad
			self.content.append([pad + line + pad, _color])
		self.frame = []
		self.frame.append(['╭─' + ('─' * (maxLength - 2)) + '─╮', _color])		# Top
		for i in _content:
			self.frame.append(['│ ' + (' ' * (maxLength - 2))  + ' │', _color])
		self.frame.append(['└─' + ('─' * (maxLength - 2)) + '─╯', _color])		# Bottom
		self.maxWidth = maxLength
		self.visible = True
		self.pointer = 0
		self.marked = poktools.FlipSwitch(0)


	def switch(self, _color=200):
		""" Changes the marked selection"""
		self.content[self.marked.get()][1] = self.color
		self.marked.flip()
		self.content[self.marked.get()][1] = _color



	def getCurrentSelection(self):
		""" Return currently selected item and quit """
		return 1



class nceTextBox:
	""" TextBox object """

	def __init__(self, _xPos, _yPos, _content, _color, _mWidth, _frame, _relativeToCenter):
		self.x = _xPos
		self.y = _yPos
		self.rtc = _relativeToCenter
		self.color = _color
		if _frame:
			self.frame = []
			self.frame.append(['╭─' + ('─' * (_mWidth - 2)) + '─╮', _color])		# Top
			for i in _content:
				self.frame.append(['│ ' + (' ' * (_mWidth - 2))  + ' │', _color])
			self.frame.append(['└─' + ('─' * (_mWidth - 2)) + '─╯', _color])		# Bottom
		self.content = []
		for i in _content:
			self.content.append([i, _color])
		self.maxWidth = _mWidth
		self.visible = True
		self.pointer = 0


	def highlight(self, _nr, _color=200):
		""" Set all items to default color and highlight <_nr> """
		for nr, i in enumerate(self.content):
			self.content[nr][1] = self.color
		self.content[_nr][1] =  _color


	def colorFrame(self, _color):
		""" Sets the color of the frame of the object, if object has a frame """
		if hasattr(self, 'frame'):
			for nr, i in enumerate(self.frame):
				self.frame[nr][1] = _color


class NCEngine:
	""" Presents the screen of a program """

	color = { 'white': 0, 'red': 1, 'green' : 2, 'orange' : 3, 'blue' : 4, 'purple' : 5, 'cyan' : 6, 'lightgrey' : 7}	# basic colors
	_borderColor = 0
	lines = []
	objects = {}
	running = True
	screenBorder = False

	def __init__(self):
		self.screen = curses.initscr()
		self.screen.border(0)
		self.screen.keypad(1)
		self.screen.scrollok(0)
		self._getSize()
		self.status = 'Init'
		curses.noecho()
		curses.curs_set(0)
		# init colors
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i, i, -1)
		curses.init_pair(200, curses.COLOR_RED, curses.COLOR_WHITE)			# init 256 colors + 1 special
		self._generateID = self.idGenerator()


	def wts(self, xCord, yCord, txt, col=0):
		""" Write to Screen. Wrapper that tests heigth/width before writing to screen  """
		height, width = self.screen.getmaxyx()
		if xCord > height:
			 self.screen.addstr(1, 1, 'WARNING!! Program tried to write BELOW window! (height=' + str(height) + ', X-coordinate=' + str(xCord) + ')', curses.color_pair(0))
		elif yCord > width:
			 self.screen.addstr(1, 1, 'WARNING!! Program tried to write LEFT OF window! (width=' + str(width) + ', Y-coordinate=' + str(yCord) + ')', curses.color_pair(0))
		else:
			try:
				self.screen.addstr(xCord, yCord, str(txt), curses.color_pair(col))
			except:
				self.exit([xCord, yCord, txt, col])
		return True


	def _getSize(self):
		""" Update height/width/center """
		self.height, self.width = self.screen.getmaxyx()
		self.hcenter = int((self.width - 1) / 2)
		self.vcenter = (self.height - 1) / 2
#		self.wts(self.height - 3, 0, str(self.hcenter), 6)	# Debug

	def idGenerator(self):
		n = 1
		while True:
			yield n
			n += 1

	def generateID(self):
		""" Get the next sequential ID """
		return next(self._generateID)


	def digitsEditor(self, x, y, eString, color):
		""" Edits digits """
		self._getSize()
		xPos = int((x * self.width / 100) + 2 if type(x) == float else x)
		yPos = int((y * self.height / 100) - 1 if type(y) == float else y)
		pointer = poktools.RangeIterator(len(eString) - 1, False)
		keyPressed = ''
		teRunning = True
		self.wts(self.height - 1, 0, 'UP/DOWN cycles digit, ENTER accepts changes', 6)    # Overwrite Status
		self.screen.refresh()
		while teRunning:
			stringSliced = [eString[:pointer.get()], eString[pointer.get()], eString[pointer.get() + 1:]]
			self.wts(yPos, xPos, stringSliced[0], 5)
			self.wts(yPos, xPos + len(stringSliced[0]), stringSliced[1], 1)
			self.wts(yPos, xPos + len(stringSliced[0]) + len(stringSliced[1]), stringSliced[2], 5)
			self.wts(yPos, xPos + len(stringSliced[0]) + len(stringSliced[1]) + len(stringSliced[2]), ' ', 0)    # overwrite last char
			#self.wts(yPos + 2, xPos + 10, str(stringSliced) + ' - ' + str(keyPressed))      # Message output
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


	def boolEditor(self, x, y, value, color):
		""" Edits True/False """
		bValue = 0 if value == 'False' else 1
		pointer = FlipSwitch(bValue)
		self._getSize()
		self.wts(self.height - 9, 0, 'UP/DOWN changes state, ENTER accepts changes', 6)    # Overwrite Status
		xPos = int((x * self.width / 100) + 2 if type(x) == float else x)
		yPos = int((y * self.height / 100) - 1 if type(y) == float else y)
		teRunning = True
		while teRunning:
			self.wts(yPos, xPos, pointer.getString() + ' ', color)
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


	def textEditor(self, x, y, eString, color):
		""" Edits a line of text """
		pointer = poktools.RangeIterator(len(eString) - 1, False)
		keyPressed = ''
		stringSliced = [[], [], []]
		self._getSize()
		xPos = int((x * self.width / 100) + 2 if type(x) == float else x)
		yPos = int((y * self.height / 100) - 1 if type(y) == float else y)
		self.wts(yPos, xPos, eString, 2)     # overwrite line to edit
		editorRunning = True
		while editorRunning:
			if len(eString) > 0:
				stringSliced[0] = eString[:pointer.get()]
				stringSliced[1] = eString[pointer.get()]
				stringSliced[2] = eString[pointer.get() + 1:]
			self.wts(yPos, xPos, stringSliced[0], color)
			self.wts(yPos, xPos + len(stringSliced[0]), stringSliced[1], 200)
			self.wts(yPos, xPos + len(stringSliced[0]) + len(stringSliced[1]), stringSliced[2], color)
			self.wts(yPos, xPos + len(stringSliced[0]) + len(stringSliced[1]) + len(stringSliced[2]), ' ', 3)    # overwrite last char
# DEBUG		self.wts(20, 2, "Lenght: " + str(len(eString)) + '   Pointer:' + str(pointer.get()) + '   PointerMax:' + str(pointer.max) + '  ' , 4)
# DEBUG		self.wts(21, 2, str(stringSliced) + ' ' , 4)
# DEBUG		self.wts(22, 2, str(len(stringSliced[0])) + ' ' + str(len(stringSliced[1])) + ' ' + str(len(stringSliced[2])) + ' ', 4)
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


	def render(self):
		""" handles resize and displays the data in "data" """
		self._getSize()
		self.screen.clear()
		if self.width < 60 or self.height < 20:
			self.wts(1, 1, "Windows too small to render!" , 1)
		else:
			# check if resized
			if curses.is_term_resized(self.height, self.width):
				curses.resizeterm(self.height, self.width)
				self._getSize()
			# render border
			if self.screenBorder:
				self.drawBorder()
			# render lines
			self.drawLines()
			# render status
			self.wts(self.height - 1, 1, self.status , 1)
			# render objects
			self.drawObjects()
		self.screen.refresh()


	def drawObjects(self):
		""" Draw all objects in object collection """
		for key, o in self.objects.items():
			if o.rtc:	# only horisontal center is supported currently, and only absolute values
				hcenter = int((self.width - 1) / 2)
				posX = hcenter + o.x
			else:
				posX = int((o.x * self.width / 100) if type(o.x) == float else o.x)
			posY = int((o.y * self.height / 100) - 1 if type(o.y) == float else o.y)
			# frame
			if hasattr(o, 'frame'):
				for nr, item in enumerate(o.frame):
					self.wts(posY + nr, posX + 1, item[0], item[1])
			# text
			for nr, item in enumerate(o.content):
				self.wts(posY + nr + 1, posX + 2, item[0], item[1])


	def drawLines(self):
		""" Draw all lines added to object (except border) """
		intersections = [[], []]
		for l in self.lines:
			if l[0] == 'v':
				if len(l) == 3:
					position = l[1] + int((self.width - 1) / 2)
				else:
					position = int((l[1] * self.width / 100) if type(l[1]) == float else l[1])
				intersections[0].append(position)
				for yPos in range(1, self.height - 2):
					self.wts(yPos, position, '│', self._borderColor)
				# endpoints
				self.wts(0, position, '┬',self._borderColor)
				self.wts(self.height - 2, position, '┴', self._borderColor)
			elif l[0] == 'h':
				if len(l) == 3:
					position = l[1] + ((self.height - 1) / 2)
				else:
					position = int((l[1] * self.height / 100) - 1 if type(l[1]) == float else l[1])
				intersections[1].append(position)
				self.wts(position, 1, '─' * (self.width - 2), self._borderColor)
				# endpoints
				self.wts(position, 0, '├', self._borderColor)
				self.wts(position, self.width - 1, '┤', self._borderColor)
		# draw intersections
		for x in intersections[1]:
			for y in intersections[0]:
				self.wts(x, y, '┼', self._borderColor)


	def drawBorder(self):
		""" Draw the staic border of the screen """
		# horizontal lines
		self.wts(0, 0, '╭' + '─' * (self.width - 2) + '╮', self._borderColor)						# Top
		self.wts(self.height - 2, 0, '└' + '─' * (self.width - 2) + '╯', self._borderColor)				# Bottom
		# vertical lines
		for yPos in range(1, self.height - 2):
			self.wts(yPos, 0, '│', self._borderColor)
			self.wts(yPos, self.width - 1, '│', self._borderColor)


	def getInput(self):
		""" Retrieve input and handle internally if understood, else return to calling program """
		keyPressed = self.screen.getch()
		if keyPressed == 113:		# <escape>
			self.terminate()
			self.running = False
		elif keyPressed == 259:		# KEY_UP
			pass
			#self.activeObject.pointer.dec()
		elif keyPressed == 258:		# KEY_DOWN
			pass
			#self.activeObject.pointer.inc()
		elif keyPressed == 260:		# KEY_LEFT
			pass
		elif keyPressed == 261:		# KEY_RIGHT
			pass
		return keyPressed 		# return key for (possible) further action in calling program


	def terminate(self):
		# Set everything back to normal
		self.screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()

	def exit(self, _exitMessage):
		# Set everything back to normal
		self.running = False
		self.screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		if type(_exitMessage) == list:
			print('--- Exit List dump begin -----------------------------')
			for item in _exitMessage:
				print('  ' + str(item))
			print('--- Exit List dump end -------------------------------\n')
		elif type(_exitMessage) == dict:
			print('--- Exit Dict dump begin -----------------------------')
			for key, val in _exitMessage.items():
				print('  ' + str(key) + ' : ' + str(val))
			print('--- Exit Dict dump end -------------------------------\n')
		else:
			sys.exit(str(_exitMessage))


# --- Setter Functions ----------------------------------------------------------------------------

	@property
	def borderColor(self):
		return self._borderColor

	@borderColor.setter
	def borderColor(self, val):
		self._borderColor = self.color[val.lower()] if type(val) == str else val

	def addGridLine(self, type, pos, relativeToCenter=False):
		if relativeToCenter:
			self.lines.append([type, pos, True])
		else:
			self.lines.append([type, pos])

	def addLabel(self, x, y, text, color, rtc=False):
		maxLength = len(text)
		id = self.generateID()
		self.objects[id] = nceLabel(x, y, text, color, maxLength, rtc)
		return id

	def addTextBox(self, x, y, items, color, frame, rtc=False):
		items = list(map(str, items))	# ensure list items are string-type
		maxLength = len(max(items, key=lambda coll: len(coll)))
		id = self.generateID()
		self.objects[id] = nceTextBox(x, y, items, color, maxLength, frame, rtc)
		return id

	def addDialogBox(self, x, y, items, color, rtc=False):
		items = list(map(str, items))	# ensure list items are string-type
		maxLength = len(max(items, key=lambda coll: len(coll)))
		id = self.generateID()
		self.objects[id] = nceDialogBox(x, y, items, color, rtc)
		return id




# --- Main ---------------------------------------------------------------------------------------

if sys.version_info < (3, 0):
	sys.stdout.write("Sorry, requires Python 3.x\n")
	sys.exit(1)



# --- TODO ---------------------------------------------------------------------------------------
# - BUG 	  : Stadigt problemer med scroll/count af bytes..... (??)
# - BUG		  : Crasher stadigt hvis window bliver minimalt I HOEJDE!!
# - Status mangler for alle editors ..... pånær digitseditor
# - En form for funktion hvor man kan tilfoeje colour-init-pairs, ud over default......addColor(c1, c2='Black')
# - Et kald hvor man kan tilfoeje keyboard-keys, og definere hvad der skal ske hvis de bliver kaldt
# - En funktion addData() som tilfoejer data til current frame, og en funktion drawFrame() som tegner denne og tømmer buffer. Boer beregne/optimere data, f.eks. intersects
# - Position objects relative to RIGHT SIDE / BOTTOM / VERTICAL CENTER
# - Dialogbox-type

