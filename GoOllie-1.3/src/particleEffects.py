#particle effect data for Go Ollie

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


#Format is:
  
  #particle Name = [Image File Name, Next Frame Number, MS this frame visible for, Sound file name,expansion delta,alpha delta,spin

tile_small_explosion = [
              ['smallBoom01',1,10,None,0.03,0,0],
              ['smallBoom02',2,10,None,0.04,0,0],
              ['smallBoom03',3,10,None,0.06,-3,0],
              ['smallBoom04',4,20,None,.07,-5,0],              
              ['end',4,20,None,.03,0,0],    
             ]
              
tile_explosion = [
              ['Boom01',1,10,None,0.03,0,0],
              ['Boom02',2,10,None,0.03,0,0],
              ['Boom03',3,10,None,0.035,0,0],
              ['Boom04',4,20,None,.04,-4,0],              
              ['end',4,20,None,.03,0,0],   
              ]

spell = [
              ['spell01',1,10,None,0.5,-20,0],
              ['spell02',2,10,None,0.5,-20,0],
              ['spell03',3,10,None,0.5,-10,0],
              ['spell04',4,10,None,0.5,-10,0],              
              ['end',4,20,None,0,-8,.001],   
              ]
fairyTrail = [
              ['trail01',1,20,None,0.03,-30,0],
              ['trail02',2,20,None,0.03,-30,0],
              ['trail03',3,20,None,0.03,-30,0],
              ['trail04',4,20,None,0.03,-30,0],              
              ['end',4,20,None,0,-8,.001],   
              ]

fairySparkle1 = [
              ['Starburst01',1,20,None,0.01,-10,0],
              ['Starburst02',2,20,None,0.01,-9,0],
              ['Starburst03',3,30,None,0.01,-8,0],
              ['Starburst04',4,70,None,0.01,-7,0],              
              ['end',4,20,None,0,-8,.001],   
              ]

ghostParticle = [
              ['ghost01',1,20,None,0.01,-10,0],
              ['ghost02',2,20,None,0.01,-9,0],
              ['ghost03',3,30,None,0.01,-8,0],
              ['ghost04',4,70,None,0.01,-7,0],              
              ['end',4,20,None,0,-8,.001],   
              ]

fairyAttack1 = [
              ['CandyStarburst01',1,20,None,0.02,-10,0],
              ['CandyStarburst02',2,20,None,0.02,-9,0],
              ['CandyStarburst01',3,30,None,0.02,-8,0],
              ['CandyStarburst02',4,70,None,0.02,-7,0],              
              ['end',4,20,None,0,-8,.001],   
              ]              
fairyAttack2 = [
              ['CandyStarburst03',1,20,None,0.02,-10,0],
              ['CandyStarburst04',2,20,None,0.02,-9,0],
              ['CandyStarburst03',3,30,None,0.02,-8,0],
              ['CandyStarburst04',4,70,None,0.02,-7,0],              
              ['end',4,20,None,0,-8,.001],   
              ]              
fire1 = [
              ['CandyStarburst01',1,20,None,0.01,-14,0],
              ['CandyStarburst01',2,20,None,0.01,-13,0],
              ['CandyStarburst01',3,30,None,0.01,-12,0],
              ['CandyStarburst01',4,70,None,0.01,-11,0],              
              ['end',4,20,None,0,-8,.001],   
              ]              
fire2 = [
              ['CandyStarburst04',1,20,None,0.01,-14,0],
              ['CandyStarburst04',2,20,None,0.01,-13,0],
              ['CandyStarburst04',3,30,None,0.01,-12,0],
              ['CandyStarburst04',4,70,None,0.01,-11,0],              
              ['end',4,20,None,0,-8,.001],   
              ]  
fairySparkle2 = [
              ['Starburst02',1,20,None,0.01,-10,0],
              ['Starburst04',2,20,None,0.02,-8,0],
              ['Starburst03',3,30,None,0.02,-7,0],
              ['Starburst01',4,70,None,0.02,-6,0],              
              ['end',4,20,None,0,-8,.001],   
              ]

fairyRedTrail = [
              ['redTrail01',1,20,None,0.03,-30,0],
              ['redTrail02',2,20,None,0.03,-30,0],
              ['redTrail03',3,20,None,0.03,-30,0],
              ['redTrail04',4,20,None,0.03,-30,0],              
              ['end',4,20,None,0,-8,.001],   
              ]
              
spell_explosion = [
              ['spell01',1,10,'spell_hit',1,-10,0],
              ['spell02',2,10,None,1,-10,0],
              ['spell03',3,10,None,1,-5,0],
              ['spell04',4,10,None,1,-5,0],              
              ['end',4,20,None,0,-8,.001],   
              ]

clock_explosion = [
              ['clock01',1,60,None,1,-10,0],
              ['clock01',2,60,None,1,-4,0],
           
              ['end',2,20,None,.03,0,0],   
              ]
              
big_explosion = [
              ['smallBoom01',1,10,"bombExplosion",0.5,-1,0],
              ['smallBoom02',2,10,None,1,-2,0],
              ['smallBoom03',3,10,None,1,-3,0],
              ['smallBoom04',4,30,None,2,-8,0],           
              ['end',4,20,None,.03,0,0],   
              ]    
              
vBig_explosion = [
              ['smallBoom01',1,10,None,0.5,-1,0],
              ['smallBoom02',2,10,None,1.5,-2,0],
              ['smallBoom03',3,10,None,1.5,-3,0],
              ['smallBoom04',4,30,None,2.5,-8,0],           
              ['end',4,20,None,.03,0,0],   
              ]  
debris = [
          ['smallBoom01',1,200,None,0,0,0.001],
          ['smallBoom01',0,200,None,0,0,0.001],
          ]
          
fruit = [
          ['smallBoom01',1,200,None,0.005,0,0.0],
          ['smallBoom01',0,200,None,0.005,0,0.0],
          ] 

lock = [
          ['PadlockOpen',1,5,None,0.005,0,0.0],
          ['PadlockOpen',0,5,None,0.005,0,0.0],
          ['PadlockOpen',0,200,None,0.005,0,0.0],
          ]
          
dustPuff = [
          ['DustPuff01',1,10,None,0.3,-20,0],
          ['DustPuff02',2,10,None,0.3,-20,0],
          ['DustPuff03',3,10,None,0.3,-20,0],
          ['DustPuff04',0,10,None,0.3,-20,0],
]

hitEffect = [
          ['HitEffect01',1,20,None,0.1,-4,0],
          ['HitEffect02',2,20,None,0.1,-10,0],
          ['HitEffect03',3,20,None,0.1,-30,0],
          ['HitEffect04',4,50,None,0.1,-50,0],
          ['end',4,20,None,.03,0,0], 
]

fireWork1 = [
          ['coin01',1,10,None,0.001,-1,0],
          ['coin02',2,10,None,0.001,-1.5,0],
          ['coin03',3,10,None,0.001,-1.5,0],
          ['coin04',4,10,None,0.001,-1.5,0],
          ['coin05',5,10,None,0.001,-1.5,0],
          ['coin06',6,10,None,0.001,-1.5,0],
          ['coin07',7,10,None,0.001,-1.5,0],
          ['coin08',0,10,None,0.001,-1.5,0],
          ['end',2,20,None,.03,0,0], 
]

fireWork2 = [
          ['250Coin01',1,10,None,0.001,-1,0],
          ['250Coin02',2,10,None,0.001,-1.5,0],
          ['250Coin03',3,10,None,0.001,-1.5,0],
          ['250Coin04',4,10,None,0.001,-1.5,0],
          ['250Coin05',5,10,None,0.001,-1.5,0],
          ['250Coin06',6,10,None,0.001,-1.5,0],
          ['250Coin07',7,10,None,0.001,-1.5,0],
          ['250Coin08',0,10,None,0.001,-1.5,0],
          ['end',2,20,None,.03,0,0], 
]
fireWork3 = [
          ['1000Coin01',1,10,None,0.001,-1,0],
          ['1000Coin02',2,10,None,0.001,-1.5,0],
          ['1000Coin03',3,10,None,0.001,-1.5,0],
          ['1000Coin04',4,10,None,0.001,-1.5,0],
          ['1000Coin05',5,10,None,0.001,-1.5,0],
          ['1000Coin06',6,10,None,0.001,-1.5,0],
          ['1000Coin07',7,10,None,0.001,-1.5,0],
          ['1000Coin08',0,10,None,0.001,-1.5,0],
          ['end',2,20,None,.03,0,0], 
]

acid = [
       ['Acid',1,10,None,0.002,-4.0,0],
       ['Acid',0,10,None,0.002,-4.0,0],
       ]
