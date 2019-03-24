# Poul Kalff python programming module
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import logging as log

# --- Variables ----------------------------------------------------------------------------------

# --- Functions ----------------------------------------------------------------------------------

def ensurePackage(package):
    """ Check whether APT package exists, installs if it not """
    if not checkPackage(package):
        installPackage(package)
    return True


def checkPackage(package):
    """ Check whether APT package exists """
    if ' ' in package:
        return -1       # Please specify one pacakge only
    raw_output = runExternal("dpkg -l " + package)
    lines = raw_output.split('\n')
    if len(lines) == 1:
        return False
    else:
        return True


def installPackage(package):
    """ Installs package via apt """
    reply = runExternal('sudo apt install ' + str(package) + ' -y')
    return reply


def readFileContents(self, fil):
    """ Read and return file contnts """
    f = open(fil,'r')
    data = f.read()
    f.close()
    return data


def writeFileContents(self, file, content):
    """ Write data to file """
    counter = 0
    while os.path.exists(self.file + '_BACKUP' + str(counter)):
        counter += 1
    shutil.copy(self.file, self.file + '_BACKUP' + str(counter))
    # write file
    nr = 0
    f = open(self.file, 'w')
    for p in self.posts:
        if p.valid:
            nr += 1
            f.writelines(p.toFile(nr))
    f.close()


def runExternal(command):
    """ Runs external process and returns output """
#    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, stderr=open(os.devnull, 'w'))
 #   output, err = process.communicate()
    output = subprocess.getoutput(command)      # New to Python3, untested!
    return output



# --- Classes ------------------------------------------------------------------------------------

class FlipSwitch():
    """ Represents a switch with on and off-state """

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


# --- Main Program -------------------------------------------------------------------------------

# Module cannot be called directly

# --- TODO ---------------------------------------------------------------------------------------
# - Skla have en log-function i en klasse... skal/boer fungere som i movietools



