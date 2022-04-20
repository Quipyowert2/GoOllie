# Copyright (C) 2008 Charlie Dog Games

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

import game

class tutorialScreen:
    def render(self):
        game.PC.setColourize(1)
        game.PC.setColour(255,255,255,game.game.tutorialAlpha)
        x = 0
        y = 0
        res = game.JPG_Resources[self.name]  
        game.PC.drawImage(res,x,y)
        
class Tutorial1Class(tutorialScreen):
    name = "tutorialscreen1"

class Tutorial1ClassKeys(tutorialScreen):
    name = "tutorialscreen1Keys"

class Tutorial2Class(tutorialScreen):
    name = "tutorialscreen2"
        
tutorial1 = Tutorial1Class()
Tutorial1Keys = Tutorial1ClassKeys()
tutorial2 = Tutorial2Class()
