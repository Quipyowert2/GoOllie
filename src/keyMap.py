# Copyright (C) 2008 Charlie Dog Games
# Changes for GNU/Linux port Copyright (C) 2008 W.P. van Paassen

# This file is part of Go Ollie.

# Go Ollie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Go Ollie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Go Ollie.  If not, see <http://www.gnu.org/licenses/>.

class key_def:
    def __init__(self, value, string):
        self.keyValue = value
        self.keyString = string

import Pycap

leftKey = key_def(Pycap.getKeyCode("LEFT"),'leftKey')
rightKey = key_def(Pycap.getKeyCode("RIGHT"),'rightKey')           
upKey = key_def(Pycap.getKeyCode("UP"),'upKey')
downKey = key_def(Pycap.getKeyCode("DOWN"),'downKey')
enterKey = key_def(Pycap.getKeyCode("RETURN"),'enterKey')
fireKey = key_def(Pycap.getKeyCode("RETURN"),'fireKey')
editorKey = key_def(Pycap.getKeyCode("e"),'editorKey')
newObjectKey = key_def(Pycap.getKeyCode("o"),'newObjectKey')
escapeKey = key_def(Pycap.getKeyCode("ESCAPE"),'escapeKey')
deleteKey = key_def(Pycap.getKeyCode("DELETE"),'deleteKey')
leftCursorKey = key_def(Pycap.getKeyCode("LEFT"), 'leftCursorKey')
rightCursorKey = key_def(Pycap.getKeyCode("RIGHT"),'rightCursorKey')
downCursorKey = key_def(Pycap.getKeyCode("DOWN"),'downCursorKey')
upCursorKey = key_def(Pycap.getKeyCode("UP"),'upCursorKey')
tabKey = key_def(Pycap.getKeyCode("TAB"),'tabKey')
reloadKey = key_def(Pycap.getKeyCode("r"),'reloadKey')
rightShiftKey = key_def(Pycap.getKeyCode("RSHIFT"),'rightShiftKey')
leftShiftKey = key_def(Pycap.getKeyCode("LSHIFT"),'leftShiftKey')
backSpace = key_def(Pycap.getKeyCode("BACKSPACE"),'backSpace')
highScore = key_def(Pycap.getKeyCode("1"),'highScore')
pauseKey = key_def(Pycap.getKeyCode("P"),'pauseKey')
optionsKey = key_def(Pycap.getKeyCode("2"),'optionsKey')
leftControlKey = key_def(Pycap.getKeyCode("LCONTROL"),'leftControlKey')
rightControlKey = key_def(Pycap.getKeyCode("RCONTROL"),'rightControlKey')
cheatKey = key_def(Pycap.getKeyCode("C"),'cheat Key')
hintKey = key_def(Pycap.getKeyCode("H"),'hint Key')
spaceKey = key_def(Pycap.getKeyCode("SPACE"),'space Key')
dashKey = key_def(Pycap.getKeyCode("D"),'dash Key')
smashKey = key_def(Pycap.getKeyCode("S"),'smash Key') 

configurableKeys = [leftKey,rightKey,upKey,downKey,fireKey,pauseKey]

namedKeys = [
[222,'"'],
[191,'/'],
[Pycap.getKeyCode("RETURN"),'Enter'],
[Pycap.getKeyCode("ESCAPE"),'Escape'],
[Pycap.getKeyCode("DELETE"),'Delete'],
[Pycap.getKeyCode("LEFT"),'Left-Cursor'],
[Pycap.getKeyCode("RIGHT"),'Right-Cursor'],
[Pycap.getKeyCode("DOWN"),'Down-Cursor'],
[Pycap.getKeyCode("UP"),'Up-Cursor'],
[Pycap.getKeyCode("TAB"),'Tab'],
[Pycap.getKeyCode("RSHIFT"),'Shift'],
[Pycap.getKeyCode("SPACE"),'Space'],
[Pycap.getKeyCode("RCONTROL"),'Ctrl'],
[Pycap.getKeyCode("LATL"),'Alt'],
[Pycap.getKeyCode("INSERT"),'Ins'],
[20,'Caps-Lock'],
[Pycap.getKeyCode("F1"),'F1'],
[Pycap.getKeyCode("F2"),'F2'],
[Pycap.getKeyCode("F3"),'F3'],
[Pycap.getKeyCode("F4"),'F4'],
[Pycap.getKeyCode("F5"),'F5'],
[Pycap.getKeyCode("F6"),'F6'],
[Pycap.getKeyCode("F7"),'F7'],
[Pycap.getKeyCode("F8"),'F8'],
[Pycap.getKeyCode("F9"),'F9'],
[Pycap.getKeyCode("F10"),'F10'],
[Pycap.getKeyCode("F11"),'F11'],
[Pycap.getKeyCode("F12"),'F12'],
[Pycap.getKeyCode("BACKSPACE"),'Back-Space'],
]

def saveKeysRegistry():
    import Pycap
    Pycap.writeReg( leftKey.keyString, str(leftKey.keyValue))
    Pycap.writeReg( rightKey.keyString, str(rightKey.keyValue))
    Pycap.writeReg( upKey.keyString, str(upKey.keyValue))
    Pycap.writeReg( downKey.keyString, str(downKey.keyValue))    
    Pycap.writeReg( fireKey.keyString, str(fireKey.keyValue)) 
    Pycap.writeReg( pauseKey.keyString, str(pauseKey.keyValue)) 
    
def loadKeysRegistry():
    import Pycap
    value = Pycap.readReg(leftKey.keyString)
    if(value):
        leftKey.keyValue = int(value)
    value = Pycap.readReg(rightKey.keyString)
    if(value):
        rightKey.keyValue = int(value)        
    value = Pycap.readReg(upKey.keyString)
    if(value):
        upKey.keyValue = int(value)        
    value = Pycap.readReg(downKey.keyString)
    if(value):
        downKey.keyValue = int(value)       
    value = Pycap.readReg(fireKey.keyString)
    if(value):
        fireKey.keyValue = int(value)          
    value = Pycap.readReg(pauseKey.keyString)
    if(value):
        pauseKey.keyValue = int(value) 
