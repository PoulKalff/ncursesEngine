#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import curses

# --- Variables -----------------------------------------------------------------------------------


# --- Functions -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------


class FlipSwitch():
    # Represents a switch with on and off-state

    def __init__(self, Ind):
        self._value = Ind

    def flip(self):
        if self._value == 1:
            self._value = 0
        else:
            self._value = 1

    def get(self):
        return self._value


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


class nCursesEngine():
	""" Main class of nCursesEngine, must be inherited """

    def __init__(self):
        self.pointer = RangeIterator(10, False)
        self.running = True
        self.status = 'OK'
        self.frameBuffer = []
        # Start en screen op
        self.screen = curses.initscr()
        self.screen.border(0)
        self.screen.keypad(1)
        curses.noecho()
        curses.start_color()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.loop()


    def loop(self):
        while self.running:
            self.displayScreen()
            self.getInput()
        self.killScreen()
        sys.exit('\n Program terminated normally...\n')


	def getDim(self, dim='BOTH'):
		""" returns the height, width or both, of the current window """
		height, width = self.screen.getmaxyx()
		cPosX = width / 2
		cPosY = height / 2
		if dim.upper() == 'H':
			return height
		elif dim.upper() == 'W':
			return width
		elif dim.upper() == 'HC':
			return cPosY
		elif dim.upper() == 'WC':
			return cPosX
		else:
			return (height, width)


	def addColor(self, c1, c2=curses.COLOR_BLACK):
		""" inits new colour-pair if it does not exist, returns the number of the (new or old) pair """
		pass


	def drawFrame(self):
		""" Draws the current frame and empties the framebuffer """

		self.frameBuffer = []
		pass

	def addData(self, data):
		""" Adds data to the framebuffer """
		pass


    def updateStatus(self, newStatus):
        """ Sets status for loaded objects. Status exists only per session """
        self.status = newStatus



        self. screen.refresh()
        pass
     

    def killScreen(self):
        # Set everything back to normal
        self.screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


    def getInput(self):
        """ Retrieve input from the keyboard and proccess those"""
        pass

    def createMenu(self):
        """ Creates the data used for painting the main menu """
        pass

    def createFrame(self):
        """ Creates the data used for painting the frame """
        pass

    def createConfig(self):
        """ Creates the data used for painting the text """
        pass

        


# --- Main  ---------------------------------------------------------------------------------------

if os.getuid() != 0:
    sys.exit('\n  Must be run with admin priviliges\n')
else:
    objNCE = nCursesEngine()

# --- TODO ---------------------------------------------------------------------------------------
# - 











