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

class tileClass:
    def __init__(self,idleTime,idleFrames,rotateTime,rotateFrames,hintTime,hintFrames,removeTime,removeFrames,lineTime,lineFrames,value,bonusRotation,chance,linePenalty):
      
        self.idleFrames = idleFrames
        self.rotateFrames = rotateFrames
        self.hintFrames = hintFrames
        self.removeFrames = removeFrames
        self.lineFrames = lineFrames
        
        self.idleTime = idleTime
        self.rotateTime = rotateTime
        self.hintTime = hintTime
        self.removeTime = removeTime
        self.lineTime = lineTime
        self.value = value
        self.bonusRotation = bonusRotation
        self.chance = chance
        self.linePenalty = linePenalty
        
character1 = tileClass(
      40,
      ["blue"], 
      40,
      ["blue"],
      40,
      ["blue"],
      40,
      ["blue"],
      40,
      ["blue"],
      5,
      0,
      100,
      0
      )
      
character2 = tileClass(
      40,
      ["darkgreen"], 
      40,
      ["darkgreen"],
      40,
      ["darkgreen"],
      40,
      ["darkgreen"],
      40,
      ["darkgreen"],
      5,
      1,
      100,
      0
      )
      
character3 = tileClass(
      40,
      ["green"], 
      40,
      ["green"],
      40,
      ["green"],
      40,
      ["green"],
      40,
      ["green"],
      5,
      2,
      100,
      0
      )
      
character4 = tileClass(
      40,
      ["greyskull"], 
      40,
      ["greyskull"],
      40,
      ["greyskull"],
      40,
      ["greyskull"],
      40,
      ["greyskull"],
      0,
      -1,
      20,
      10  #This is how many of these take out the entire bar - e.g. 20 skull lines kills the player always 
      )
      
character5 = tileClass(
      40,
      ["orange"], 
      40,
      ["orange"],
      40,
      ["orange"],
      40,
      ["orange"],
      40,
      ["orange"],
      5,
      3,
      100
      ,0
      )        
      
character6 = tileClass(
      40,
      ["pink"], 
      40,
      ["pink"],
      40,
      ["pink"],
      40,
      ["pink"],
      40,
      ["pink"],
      5,
      0,
      100,
      0
      ) 
      
character7 = tileClass(
      40,
      ["purple"], 
      40,
      ["purple"],
      40,
      ["purple"],
      40,
      ["purple"],
      40,
      ["purple"],
      10,
      1,
      70,
      0
      ) 

character8 = tileClass(
      40,
      ["redgem"], 
      40,
      ["redgem"],
      40,
      ["redgem"],
      40,
      ["redgem"],
      40,
      ["redgem"],
      25,
      2,
      60,
      0
      ) 
      
character9 = tileClass(
      40,
      ["yellowmoon"], 
      40,
      ["yellowmoon"],
      40,
      ["yellowmoon"],
      40,
      ["yellowmoon"],
      40,
      ["yellowmoon"],
      50,
      3,
      50,
      0
      ) 
      
character10 = tileClass(
      40,
      ["yellowstar"], 
      40,
      ["yellowstar"],
      40,
      ["yellowstar"],
      40,
      ["yellowstar"],
      40,
      ["yellowstar"],
      100,
      1,
      40,
      0
      ) 

character11= tileClass(
      40,
      ["wildcard03"], 
      40,
      ["wildcard03"],
      40,
      ["wildcard03"],
      40,
      ["wildcard03"],
      40,
      ["wildcard03"],
      50,
      -1,
      15,
      0
      ) 

inert= tileClass(
      40,
      ["blackbox"], 
      40,
      ["blackbox"],
      40,
      ["blackbox"],
      40,
      ["blackbox"],
      40,
      ["blackbox"],
      0,
      -1,
      3,
      0
      ) 


tileList = [character1,character2,character3,character5,character6,character7,character11,character4,character8,character9,character10,inert]


class faceClass:
    def __init__(self,speed,animation1):
        self.animation1 = animation1
        self.speed = speed
        
idle =  faceClass(10,["idle01"])          
eye_bite =  faceClass(10,["eye_bite01","eye_bite02"])  
eye_blink =  faceClass(8,["eye_blink01","eye_blink02","eye_blink03","eye_blink04"]) 
eye_cheek =  faceClass(30,["eye_cheek01","eye_cheek02"])
eye_grit =  faceClass(10,["eye_grit01","eye_grit02"])
eye_happy = faceClass(10,["eye_happy01","eye_happy02"]) 
eye_huh = faceClass(10,["eye_huh01","eye_huh02"])
eye_ohnoes = faceClass(10,["eye_ohnoes01","eye_ohnoes02"]) 
eye_tongue = faceClass(8,["eye_tongue01","eye_tongue02","eye_tongue01","eye_tongue02","eye_tongue01","eye_tongue02","eye_tongue01","eye_tongue02"]) 
eye_why = faceClass(30,["eye_why01","eye_why02"]) 
eye_wild = faceClass(30,["eye_wild01","eye_wild02"]) 
eye_inert = faceClass(30,["eye_inert"]) 
randomExpressionList = [eye_bite,eye_blink,eye_cheek,eye_grit,eye_happy,eye_huh,eye_why]
