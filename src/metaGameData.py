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

class Score:
    name = ''
    score = 0
    time = 0
    
InitialScores = [
    ['Tony',1000000,0],
    ['Victoria',500000,0],
    ['Grace',250000,0],
    ['Joseph',100000,0],
    ['Jarrad',50000,0],
    ['Ed',25000,0],
    ['James',20000,0],
    ['Jon',10000,0],
    ['Michael',5000,0],
    ['Gillian',2500,0],
]


class HighScores:
    scores = []
    pope = 0
    def initialiseScores(self):
        for score in InitialScores:
            newScore = Score()
            newScore.name = score[0]
            newScore.score = score[1]
            newScore.time=scrore[2]
            self.scores.append(newScore)
        
    
def tomato():
    temp = 1
