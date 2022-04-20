#Animation data for Go Ollie

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
  
  #Animation Name = [Image File Name, Next Frame Number, MS this frame visible for, Sound file name(opt)]
jumpSounds = ['jump1','jump2','jump3','jump4','jump5']
deathSounds = ['Death','Death']
swingSounds = ['Death','Death']
walkSounds1 = ['walk1']
walkSounds2 = ['walk2']
bigBatFlap = ['batFlap','batFlap']
smallBat = ['smallBat1',None,'smallBat2',None]
bigBatAlert = ['bigBatAlert',None,None,None]

coinCollected = ['coinCollected']
player_walk = [
              ['player_walk_01',1,13,None,None],
              ['player_walk_02',2,13,None,None],
              ['player_walk_03',3,13,None,None],
              ['player_walk_02',0,13,None,None],
              ]
              
player_land_walk = [
              ['Spider1',1,20,None,None],
              ['Spider2',2,20,None,None],
              ['Spider3',3,20,None,None],
              ['Spider4',4,20,None,player_walk],
              ]
             
player_death = [
              ['player_dead_01',1,20,deathSounds,None],
              ['player_dead_01',2,20,None,None],
              ['player_dead_01',1,20,None,None],
              ]
              
player_swing = [
                ['player_swing_01',1,10,None,None],
                ['player_swing_02',2,10,None,None],
                ['player_swing_03',3,10,None,None],                
                ['player_swing_04',4,10,None,None],                
                ['player_swing_05',5,10,None,None],
                ['player_swing_06',6,10,None,None],
                ['player_swing_07',7,10,None,None],                
                ['player_swing_08',0,10,None,None], 
                ]
                  
player_jump = [
              ['player_jump_01',1,5,jumpSounds,None],
              ['player_jump_02',2,5,None,None],
              ['player_jump_03',3,5,None,None],
              ['player_jump_04',2,5,None,None],

              ]       
              
player_idle = [
              ['player_idle_01',1,130,None,None],
              ['player_idle_01',2,12,None,None],
              ['player_idle_02',3,12,None,None],
              ['player_idle_03',4,12,None,None],
              ['player_idle_04',5,12,None,None],
              ['player_idle_03',6,12,None,None],
              ['player_idle_02',1,12,None,None],
              ]  
              
player_land_idle = [
              ['PlayerLand_02',1,25,None,None],
              ['PlayerLand_02',1,10,None,player_idle],
              ]  
              
player_sub =  [
              ['player_sub_01',1,12,None,None],
              ['player_sub_02',0,12,None,None],
              ]   

player_victory = [

              ['player_jump_01',1,6,None,None],
              ['player_jump_02',2,6,None,None],
              ['player_jump_03',3,6,None,None],
              ['player_jump_04',4,6,None,None],
              ['player_jump_01',5,6,None,None],
              ['player_jump_02',6,6,None,None],
              ['player_jump_03',7,6,None,None],
              ['player_jump_04',8,6,None,None],
              ['player_walk_01',9,6,None,None],
              ['player_walk_02',10,6,None,None],
              ['player_walk_03',11,6,None,None],
              ['player_walk_02',12,6,None,None],
              ['player_walk_01',13,6,None,None],
              ['player_walk_02',14,6,None,None],
              ['player_walk_03',15,6,None,None],
              ['player_walk_02',0,6,None,None],

]
                            
spider_move = [
              ['Spider1',1,20,None,None],
              ['Spider2',2,20,None,None],
              ['Spider3',3,20,None,None],
              ['Spider4',4,20,None,None],
              ['Spider5',5,20,None,None],
              ['Spider4',6,20,None,None],
              ['Spider3',7,20,None,None],
              ['Spider2',0,20,None,None],
              ]  

largespider_attack = [
              ['bigspider01',1,2,None,None],
              ['bigspider02',2,2,None,None],
              ['bigspider03',3,2,None,None],
              ['bigspider04',4,2,None,None],
              ['bigspider05',5,10,None,None],
              ['bigspider04',6,10,None,None],
              ['bigspider03',7,10,None,None],
              ['bigspider02',7,10,None,None],
              ]  
              
largespider_idle = [
              ['bigspider01',1,20,None,None],
              ['bigspider02',2,20,None,None],
              ['bigspider03',3,20,None,None],
              ['bigspider02',0,20,None,None],
              ]  
largespider_move= [
              ['bigspider01',1,20,None,None],
              ['bigspider01',0,20,None,None],
              ]


coin50_loop = [
              ['coin01',1,10,None,None],
              ['coin02',2,10,None,None],
              ['coin03',3,10,None,None],
              ['coin04',4,10,None,None],
              ['coin05',5,10,None,None],
              ['coin06',6,10,None,None],   
              ['coin07',7,10,None,None],
              ['coin08',0,10,None,None],   
              ]   
coin1000_loop = [
              ['1000Coin01',1,10,None,None],
              ['1000Coin02',2,10,None,None],
              ['1000Coin03',3,10,None,None],
              ['1000Coin04',4,10,None,None],
              ['1000Coin05',5,10,None,None],
              ['1000Coin06',6,10,None,None],   
              ['1000Coin07',7,10,None,None],
              ['1000Coin08',0,10,None,None],   
              ] 
coin250_loop = [
              ['250Coin01',1,10,None,None],
              ['250Coin02',2,10,None,None],
              ['250Coin03',3,10,None,None],
              ['250Coin04',4,10,None,None],
              ['250Coin05',5,10,None,None],
              ['250Coin06',6,10,None,None],   
              ['250Coin07',7,10,None,None],
              ['250Coin08',0,10,None,None],   
              ]               
clock_loop = [
              ['clock01',1,10,None,None],
              ['clock02',2,10,None,None],
              ['clock03',3,10,None,None],
              ['clock04',4,10,None,None],
              ['clock05',5,10,None,None],
              ['clock06',6,10,None,None],   
              ['clock07',7,10,None,None],
              ['clock08',0,10,None,None],   
              ] 
              
key_loop = [
              ['Key01',1,10,None,None],
              ['Key02',2,10,None,None],
              ['Key03',3,10,None,None],
              ['Key04',4,10,None,None],
              ['Key05',5,10,None,None],
              ['Key06',6,10,None,None],   
              ['Key07',7,10,None,None],
              ['Key08',0,10,None,None],   
              ['Key09',5,10,None,None],
              ['Key10',6,10,None,None],   
              ['Key11',7,10,None,None],
              ['Key12',0,10,None,None],   
              ] 
              
oneUp_loop = [
              ['OneUp_01',1,10,None,None],
              ['OneUp_02',2,10,None,None],
              ['OneUp_03',3,10,None,None],
              ['OneUp_04',4,10,None,None],
              ['OneUp_05',0,10,None,None],
              ] 
                           
bomb_loop = [
              ['Bomb01',1,15,None,None],
              ['Bomb02',0,15,None,None],
              ] 
              
magnet_loop = [
              ['Magnet01',1,15,None,None],
              ['Magnet02',2,15,None,None],
              ['Magnet03',3,15,None,None],
              ['Magnet04',0,15,None,None],              
              ]  
              
snail_move =  [
              ['Snail01',1,10,None,None],
              ['Snail02',2,10,None,None],
              ['Snail03',3,10,None,None],
              ['Snail04',4,10,None,None],
              ['Snail05',5,10,None,None],
              ['Snail06',6,10,None,None],            
              ['Snail07',7,10,None,None],
              ['Snail08',0,10,None,None],   
              ]
largesnail_move =  [
              ['Bigsnail01',1,10,None,None],
              ['Bigsnail02',2,10,None,None],
              ['Bigsnail03',3,10,None,None],
              ['Bigsnail04',4,10,None,None],
              ['Bigsnail05',5,10,None,None],
              ['Bigsnail06',6,10,None,None],            
              ['Bigsnail07',7,10,None,None],
              ['Bigsnail08',0,10,None,None],   
              ]             
wasp_move =   [
              ['Wasp01',1,10,None,None],
              ['Wasp02',0,10,None,None],
            ]
        
Rwasp_move =  [
              ['RWasp01',1,10,None,None],
              ['RWasp02',0,10,None,None],
              ]
            
splash_screen1 = [
              ['BigOllie01',1,12,None,None],
              ['BigOllie02',2,12,None,None],
              ['BigOllie03',3,12,None,None],
              ['BigOllie04',4,18,None,None],
              ['BigOllie03',5,12,None,None],
              ['BigOllie02',0,12,None,None],
              ]   
              
sad_jake = [
              ['Big_SadOllie_01',1,10,None,None],
              ['Big_SadOllie_02',2,10,None,None],
              ['Big_SadOllie_03',3,10,None,None],
              ['Big_SadOllie_04',4,10,None,None],
              ['Big_SadOllie_05',0,150,None,None],
              ]  

smallball_move =  [
              ['SmallBall',1,10,None,None],
              ['SmallBall',0,10,None,None],
              ]

balloonRed_move =  [
              ['BalloonRed',1,10,None,None],
              ['BalloonRed',0,10,None,None],
              ]

balloonBlue_move =  [
              ['BalloonBlue',1,10,None,None],
              ['BalloonBlue',0,10,None,None],
              ]   

balloonYellow_move =  [
              ['BalloonYellow',1,10,None,None],
              ['BalloonYellow',0,10,None,None],
              ]            

bigball_move =  [
              ['BigBall',1,10,None,None],
              ['BigBall',0,10,None,None],
              ]
fairy_move =    [
              ['Fairy01',1,5,None,None],
              ['Fairy02',0,5,None,None],
              ]
              
fairy_spell = [                
              ['FairySpell01',1,10,None,None],
              ['FairySpell02',2,10,coinCollected,None],   
              ['FairySpell03',3,10,None,None],
              ['FairySpell04',0,10,None,None],   
              ]
              
bigBat_move =    [
              ['BigBat01',1,14,None,None],
              ['BigBat02',2,14,bigBatFlap,None],
              ['BigBat03',3,14,None,None],
              ['BigBat02',0,9,None,None],
              ]              
bigBat_attack =    [
              ['BigBat01',1,13,bigBatFlap,None],
              ['BigBat02',0,13,bigBatAlert,None],
              ]      
              
smallBat_move =    [
              ['SmallBat01',1,12,smallBat,None],
              ['SmallBat02',2,12,None,None],
              ['SmallBat03',3,12,None,None],
              ['SmallBat02',0,8,None,None],
              ]              
smallBat_attack =    [
              ['SmallBat01',1,10,None,None],
              ['SmallBat02',0,10,None,None],
              ]                

KillerOrange_move = [
              ['KillerOrange1',1,5,None,None],
              ['KillerOrange2',2,5,None,None],
              ['KillerOrange3',3,5,None,None],
              ['KillerOrange4',0,5,None,None],
              ]
              
HugeBall_move = [
              ['HugeBall',1,10,None,None],
              ['HugeBall',0,10,None,None],
              ]              

Acid_move = [
              ['Acid1',1,5,None,None],
              ['Acid1',0,5,None,None],

              ]
