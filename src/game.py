# All Game code Copyright (C) 2008-2009 Charlie Dog Games
# Changes for GNU/Linux port Copyright (C) 2008-2009 W.P. van Paassen

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

currentVersion = 30
showNonFreeLogos = 0
showLogo = 1
gridType = 1
demoGame = 0
testCutScene = -1
renderDetailLevel = 2
finalLevel = 48
levelsPerArcadeSegment = 8
segmentsInArcade = 4
levelsInArcde = levelsPerArcadeSegment * segmentsInArcade
localAppData = None
renderMode = 1
superior = 0
editorEnabled = 1

availableLanguageNames = ["English","Spanish"]
#enumerated list
English,Spanish = list(range(2))

#to check which language is selected you can do something like:

#if profiles[currentProfile].currentLanguage == English:
#   etc
# or you could use profiles[currentProfile].currentLanguage as an index into an array of translated strings...
#to add another languge add the new name to both lists.

# normal imports
import random, math
import animationSets
import keyMap
import messages
import levelData
import particleEffects
import cutScenes
import WorldTypes
import config
import copy
import os
#import PycapRes
import webbrowser

copywrite1 = "all game code is copywrite Charlie Dog Games 2008-2009"        

###########################################
# Application initialization data 
###########################################
appIni = {
    "mProdName"                 : "Go Ollie",
    "mProductVersion"   : "1.3",
    "mCompanyName"      : "CDG",
    "mFullCompanyName"  : "Charlie Dog Games",
    "mTitle"                    : "Go Ollie",
    "mRegKey"                   : "GoOllie",
    "mWidth"                    : 800,
    "mHeight"                   : 600,
    "mWaitForVSync"             : 1,
    "mAutoEnable3D"             : 0,
    "mTest3D"           : 1,
    "mVSyncUpdates"             : 1,
    "mWindowIconBMP": "extraResources/Logos/icon.bmp"
    }

class timeWarpClass:
    counter = 0
    initialValue = 1000.0
    def start(self,initialTime):
        if speedEnabled:
            self.counter = self.initialValue * initialTime
       #     print "setting counter",self.counter        
    def stop(self):
        counter = 0
      
    def tick(self,delta):
        self.counter -= delta
        if self.counter <0:
            self.counter = 0
        
        if speedEnabled ==1 and self.counter>0:
            if(globalPlayer):
                globalPlayer.showGhost = 5
            return 0.3
        else:
            return 1  
    def enabled(self):
        if speedEnabled ==1:
            return self.counter
        else:
            return 0
            
timeWarp = timeWarpClass()     


class backDropManagerClass:
    backDropLoaded = ""
    backDropResource = -1
    
    def checkAndReload(self,thisBackDrop):
        if self.backDropLoaded != thisBackDrop:
        #    print"reloading backdrop",thisBackDrop
            if self.backDropResource != -1:
                PCR.unloadImage(self.backDropResource)
            self.backDropResource = PCR.loadImage('extraResources/backDrops/'+thisBackDrop)
            self.backDropLoaded = thisBackDrop
  
backDropManager = backDropManagerClass()  
  


class smartBombClass:

    timer = 0 
    running = 0
    endValue = 30
    
    def tick(self,delta):
        global cameraX
        global cameraY
        self.timer += 1
        if self.timer >= self.endValue:
            self.stop()
        if self.running:
            cameraX += math.sin(self.timer/1)*7
            cameraY += math.sin(self.timer*1.2)*7
            if int(self.timer)%5 == 0:
                x = random.randint(100,700)
                y = random.randint(100,500)
                particleController.addItem(bigExplosion(),x,y,1)
        return 0
        
    def render(self):
        return 0
        
    def start(self):
        global smartUsed
        if speedEnabled:
            smartUsed = 1
            self.timer = 0
            self.running = 1
    
    def stop(self):
        global cameraX
        global cameraY
        self.running = 0
        cameraY = 0
        
    def active(self):
        return self.running
        
smartBomb =  smartBombClass()       

class Medalion:
    Hang,Smash,Stun,Dash,Speed,Fairy = list(range(6))
    graphicsBig = ["BigAmuletUnited01","BigAmuletUnited02","BigAmuletUnited03","BigAmuletUnited04","BigAmuletUnited05","BigAmuletUnited06"]
    graphicsSmall = ["SmlAmuletUnited01","SmlAmuletUnited02","SmlAmuletUnited03","SmlAmuletUnited04","SmlAmuletUnited05","SmlAmuletUnited06"]
    active = []
    resBig = []
    emptyBig= []
    resSmall = []
    emptySmall= []
    x = 360
    y = 5
    rotation = 0
    flash = 0
    lr = 255
    lg = 255
    lb = 100
    la = 90
    visible = 0
   
    def render(self,x,y,scaled,forcedOn = 0):
        self.visible = 0
        PC.drawmodeNormal()
        PC.setColour( 255, 255, 255, 255)
        if forcedOn:
            self.visible = 1
        else:
            for segmentActive in self.active:
                if segmentActive:
                    self.visible = 1

 #       if(comboLevel>0 or scaled==0 or scaled == 2):  #always want to flash if in Menu screen
        test = random.randint(0,6)      
        index = 0
        for segmentActive in self.active:
            if scaled and forcedOn == 0:
                if segmentActive or forcedOn == 1:
                    newRes = self.resSmall[index]
                else:
                    newRes = self.emptySmall[index]
                if self.visible  or metaGame != menuItems.game:
                    if index == self.Speed and smartUsed and forcedOn == 0:
                        newRes = self.emptySmall[index]
                        PC.drawImage(newRes, x, y)                        
                    else:
                        PC.drawImage(newRes, x, y)               
                        if(segmentActive or forcedOn) and test == index:
                            PC.drawmodeAdd()
                            PC.drawImage(newRes, x, y)
                            PC.drawmodeNormal()
            else:
                if segmentActive or forcedOn == 1:
                    newRes = self.resBig[index]
                else:
                    newRes = self.emptyBig[index]
                PC.drawImage(newRes, x, y)               
                if segmentActive and test == index:
                    PC.drawmodeAdd()
                    PC.drawImage(newRes, x, y)
                    PC.drawmodeNormal()
              
              
            index += 1
 
    def setSegmentStatus(self,segment,status):
        self.active[segment]=status
     
    def __init__(self):
        self.resBig = []
        self.active = []
        self.emptyBig = []
        self.emptySmall = []
        self.resSmall = []
        for segmentName in self.graphicsBig:  
            self.resBig.append(JPG_Resources[segmentName])
            self.active.append(0)
            self.emptyBig.append(JPG_Resources[segmentName+'Empty'])
            
        for segmentName in self.graphicsSmall:  
            self.resSmall.append(JPG_Resources[segmentName])
            self.emptySmall.append(JPG_Resources[segmentName+'Empty'])     
            
    def tick(self,delta):
        self.flash += delta
        self.rotation -= delta/400.0 * comboLevel
        return 0

class LevelMetaDataClass:
    title = "temp"
    RandomTiles = 0
    DayTime = 0
    RandomSpawns = 0
    currentSection = None
    currentSectionNumber = 0
    currentLevelFile = None
    gridDeath = 0
    platformSet = None
    jewelSet = None
    BackDrop = None
    introMusic = None
    sequence = 0
    instructions = None
    midInstructions = None
    winMusic = None
    loseMusic = None
    scrollSpeed = 0
    randomSpawnEnemy = 0
    nextEnemySpawn = 0
    levelNumber = 0
    
    UpperScenery = []         #This is a sequential list of all the scenery on the bottom - stored as a structure with a name and an X
    LowerScenery = []         #This is a sequential list of all the scenery on the bottom 
    LastX = 10000                    #mock up of the last X coordinate
    title = ""

def setUpPredictionTable(Gy,Vx,Vy):
    table = []
    YMax = 0
    firstEntry=0
    for x in range(800):
        value1 = x/Vx
        value2 = value1*Gy/2.0
        value3 = value1*(Vy+value2)
        if value3<-600:
            break
        if value3 >= YMax:
            YMax = value3
        else:
            if firstEntry ==0:
                table.append(x)
                #print("table offset",table[0])
                firstEntry = x
           # print("prediction table entry",x,value3)
            table.append(value3)
    return table

def setUpPredictionTableSimple(Gy,Vx,Vy):
    table = []
    table.append(0)     #reserve first value for max
    YMax = 0
    firstEntry=0
    for x in range(800):
        value1 = x/Vx
        value2 = value1*Gy/2.0
        value3 = value1*(Vy+value2)
        if value3 >= YMax:
            YMax = value3
        else:
            if(table[0] == 0):
                table[0] = x
        if value3<-600:
            break
        table.append(value3)
    return table

def getTableValueSimple(x,table,range,flag):
    if x<0:
        x *= -1
    maximumY = table[0]
    if(flag and x<int((1-range)*maximumY)):
        return table[table[0]]-(range*160.0)
    
    if x+1+(range*maximumY)>= len(table):
        return -10000
    else:
        return table[x+1+int(range*maximumY)]-table[1+int(range*maximumY)]
        
def findMaxY(table):
    return table[0]
    
def findYinJumpTable(targetY,table,range):
    x = 0

    maximumY = table[0]
    #print "maximumY",maximumY
    for y in table[maximumY:]:
        if y-(table[1+int(maximumY*range)]) < targetY:
            return x+maximumY-(maximumY*range)
        x += 1
    #print"bollox"
    return  - 10000
        
def getTableValue(x,table):
  if x<0:
      x *= -1
  x = x-table[0] #index 0 of table is offset so correct for offset
  if(x<=0):
      return table[1] #index 1 is always maximum y
  elif x >= len(table)-1:
      return -10000 # off end of table so return stupidly low value
  else:
      #need to add on 1 becuase table starts at index 1
      return table[int(x+1)]
 
def findJumpLookUp(table):
    height = comboLevel+1/2
    if(height>2):
        height=2
    if(height<0):
        height = 0
    if smashEnabled:
        height += 6
    if globalPlayer.onTrampoline:
        height = 3 + globalPlayer.onTrampoline.jumpTableOffset
    #height = 2
    thisTable = jumpArray[height]
    return thisTable[table]

class MouseOver:
    function = None
    parameter = None
    
whereIsSnakyJake = -1   
charlieBark = -1
tutorialsOn = 1
thisLevelTutioral = 0
editorScrollBar = 0
maxEditorScrollBar = 60
editorScrolled = 0
double1DownCount = 0
double1Down = 0
double2DownCount = 0
double2Down = 0
pointerSizeX = 8
mouseOverMessage =MouseOver()
iconsWide = 4
iconWidth = 50
editorWidth = iconsWide*iconWidth
gridFillRight=1 #set this to one to put the grid on the right of the screen
maxJumpLookUp0=setUpPredictionTable(-0.15,2.2*1.7,4.0*1.3)
jumpLookUp0 = setUpPredictionTableSimple(-0.15,2.2*1.7,4.0*1.3)
maxJumpLookUp1=setUpPredictionTable(-0.20,2.2*1.6,6.0*1.3)
jumpLookUp1 = setUpPredictionTableSimple(-0.20,2.2*1.6,6.0*1.3)
maxJumpLookUp2=setUpPredictionTable(-0.23,2.2*1.5,7.5*1.3)
jumpLookUp2 = setUpPredictionTableSimple(-0.23,2.2*1.5,7.5*1.3)

maxJumpLookUp0a=           setUpPredictionTable(-0.17,2.2*1.7,5.0*1.3)
jumpLookUp0a =       setUpPredictionTableSimple(-0.17,2.2*1.7,5.0*1.3)

maxJumpLookUp1a=     setUpPredictionTable(-0.20,2.2*1.6,6.5*1.3)
jumpLookUp1a = setUpPredictionTableSimple(-0.20,2.2*1.6,6.5*1.3)

maxJumpLookUp2a=     setUpPredictionTable(-0.25,2.2*1.5,8.0*1.3)
jumpLookUp2a = setUpPredictionTableSimple(-0.25,2.2*1.5,8.0*1.3)

maxTrampolineLookUpBig=setUpPredictionTable(-0.25,2.2*1.6,11.3*1.3)
trampolinLookUpBig = setUpPredictionTableSimple(-0.25,2.2*1.6,11.3*1.3)
maxTrampolineLookUpMed=setUpPredictionTable(-0.20,2.2*1.5,8.5*1.3)
trampolinLookUpMed = setUpPredictionTableSimple(-0.20,2.2*1.5,8.5*1.3)
maxTrampolineLookUpSmall=setUpPredictionTable(-0.15,2.2*1.5,5.5*1.3)
trampolinLookUpSmall = setUpPredictionTableSimple(-0.15,2.2*1.5,5.5*1.3)
jumpArray = [[maxJumpLookUp0,jumpLookUp0],[maxJumpLookUp1,jumpLookUp1],[maxJumpLookUp2,jumpLookUp2],[maxTrampolineLookUpBig,trampolinLookUpBig],[maxTrampolineLookUpMed,trampolinLookUpMed],[maxTrampolineLookUpSmall,trampolinLookUpSmall],[maxJumpLookUp0a,jumpLookUp0a],[maxJumpLookUp1a,jumpLookUp1a],[maxJumpLookUp2a,jumpLookUp2a]]
#Global Variables.  Don't initialise anything in here which needed per game
VERTICAL = 0
HORIZONTAL = 1
globalPlayer = None #dirty trick so we can find the player
globalFairy = None
doExit = 0 # flag specifying whether or not the game should continue to run (not a hook)
allGraphicFiles=[]
allGraphicFilesNames=[]
allSoundFiles=[]
allSoundFilesNames=[]
allLevelFiles=[]
allLevelFilesNames=[]
font8 = None
font22 = None
font23 = None
font36 = None
font38 = None
PC = None
time = 0
rotation = 0
oldCameraX = 0
cameraX=0
cameraY = 0
#gameSpeed = 0
x_max = 800
x_min = 0
y_max = 600
y_min = 0
gravity = 0
lives = 0
score = 0
displayScore = 0
GameOverDelay = 0
startGame = 1  #Game sits in the start up screen until this is cleared
canStart = 0 #hack to allows to check that the enter key is raised between end and start games
grid = []
gridRight = 0
gridLeft = 800
gridLeftTarget = 800
gridRightTarget=0
RemoveCount = 50       # really a constant
nextID = 0
#All the objects in the world
objects = []
solidObjects = [] #list of solid objects which is populated at the beginning of the update loop
unusedObjects = [] # list of all objects which have been created but are not now used
platformsToSpawn = 0
StaticPlatformXRange = 250
StaticPlatformXspeed = 1.5
GridPitchY = 50
PlatformPitchY = 25
GridPitchX = 40
levelMetaData = LevelMetaDataClass()
Enabled = 0

#JPG_resources is populated with all the JPG in the res directory
JPG_Resources = {}
WAV_Resources = {}
map_Resources = {}
MIDI_Resources = {}
map_Section = {}
map_Jewels = {}
inEditor = 0
InEditorKeyUP = 0
CursorY = 0
nextObjectIndex = 0
ObjectStarts = []
editorToggle = 0
playerInWorld = 0
PCR = None
levelNumber = 1
FinishFlag = 0
ExitFlag = 0
FinishTimer = 0
EndLength = 3000
BlocksRemaining = 0
scoreBonus = 0
scoreMultiplier = .5
combo = 0
ScreenMessages = None
comboLevel = 0
comboScale = .4
editorMoveSpeed = 2
keyArray = list(range(512))
keyRepeatArray = list(range(512))
downKey= 0
matchedTiles = []
metaGame= 4
gamePaused = 0
minimumMatch = 3

oldMetaGame =99999
scorePos = -1
newGame = 0
fullRotation = 44.0/7.0
tempDelta = 0
totalTimePlayed = 0
comboTimer = 0
startComboTimer = 8000
mdx = 0
mdy = 0
mdn = 0
mousex = 0
mousey = 0
mouseWheelPos = 0
mouseDelta = 0
editorAddObject =0
inGUI = 0
bonusGame = 0  #set to true if the player was awarded a bonus game
tilesOver=0
riskIncrement = 20.0
maximumRisk = 240.0
dataIsLoaded=0
loadingScreen = None
loadingBar = None
fileIndex = 0
gameOver = 1
scoreX = 5 # postion of score on the screen for printing and moving the coins
scoreY = 45
gridSettled = 0
bombExplosion=0 #set this to true to refill grid after removing tile
startLevelTimer = 0
arcadeMode = 0 
fullScreenMode = 0
delayRefill = 0
currentProfile = 0      #this needs saving and loading in the registry
startingLevelCampaign = 1
finishLevelCampaign = 48
stunJumpEnabled = 0
smashEnabled = 0
hangEnabled = 0
dashEnabled = 0
fairyEnabled = 0
speedEnabled = 1
smartUsed = 0

StagingFlag = 0
forcePause =0
continousWorldXOffset = 0
coinsCollected = 0
coinsSpawned = 0
crittersCollected = 0
crittersSpawned = 0
levelTime = 0
levelTimeDelta = 0
hangSpriteHeight = 80
button1Down = 0
ghostSpawnX=0
ghostSpawnY=300
medalion = None
trampolinePlayerY = 0
startLives = 3
levelQueued = 0
continousTime = 0       #incremented each frame
nextLifeScoreTarget = 0
cursorEnabled = 0
finishPlaformRight = 100000 #absolute furthest right of the world.
magnetOn = 0
magnetRange = 260
magnetRangeSq = magnetRange* magnetRange
smartBombCount = 0
replacementAttackDelay = 160
instructionWait = 0
finishOn = 0
thisHighScoreIDX=100
quietMusic = 0.25
globalDebug1 = 0
missedCoin = 0
globalOldPlatformOn = None
removeTrailCountStart = 1800
removeTrailCount = 0

# Initialises all global variables in here.  Called at the start of every new game
###########################################
def initialiseGame():
    #print("initializing Game")
    global mouseEnabled
    global gamePaused
    global metaGame
    global lives
    global score
    global displayScore
    global grid
    global gridRight
    global levelNumber  
    global time 
    global ScreenMessages  
    global objects
    global keyArray
    global keyRepeatArray
    global gridRightTarget
    global oldMetaGame
    global scorePos
    global newGame
    global gameOver
    global startGame
    global arcadeMode 
    global medalion
    global thisHighScoreIDX
    global renderMode
    thisHighScoreIDX = 100

    for key in range(512):
        keyArray[key] = 0
        keyRepeatArray[key] = 0 

    gameOver = 1
    mouseEnabled= 1
    oldMetaGame=0
    scorePos=-1
    time = 0
    #score = 0 can't be cleared here becuase we need it for meta game
    objects = []  #Clear all the existing objects in the world
    random.seed(1)
    #grid=[
    #[],[],[],[],[],[],[],[],
    #[],[],[],[],[],[],[],[],
   # [],[],[],[],[],[],[],[]
    #]
    grid=[
    [],[],[],[],[],[],[],[],
    [],[],[],[]
    ]
    gridRight = 0
    gridRightTarget=0
    #levelNumber  = config.levelStart
    ScreenMessages = ScreenMessagesClass()
    #initialiseLevel()   #Then initialise the actual level
    newGame = 1
    gamePaused = 0      
    startGame = 1
    arcadeMode = 0 
    medalion = Medalion()
    fadeManager.fadeDown(menuItems.nameCanvas)
   # renderMode = PC.getRenderMode()
    

###########################################
# Initialises all global variables in here.  Called at the start of every new game
def ressetCoins():
  global coinsCollected
  global coinsSpawned
  coinsCollected = 0
  coinsSpawned = 0
  
def ressetCritters():  
  global crittersCollected
  global crittersSpawned
  crittersCollected = 0
  crittersSpawned = 0  

def initialiseLevel():
#    print("initializing level",levelNumber)
    global rotation 
    global cameraX
    global cameraY
    global x_max
    global x_min
    global y_max
    global y_min
    global gravity
    global objects
    global GameOverDelay
    global startGame
    global canStart
    global inEditor
    global CursorY
    global inEditor
    global editorToggle
    global playerInWorld
    global FinishTimer
    global scoreBonus
    global nextObjectIndex
    global platformsToSpawn
    global combo
    global matchedTiles
    global comboTimer
    global bonusGame
    global tilesOver
    global oldMetaGame
    global comboLevel 
    global stunJumpEnabled
    global smashEnabled
    global hangEnabled
    global dashEnabled
    global continousWorldXOffset
    global forcePause
    global speedEnabled
    global gridLeft
    global levelQueued
    global oldCameraX 
    global finishPlaformRight
    global magnetOn
    global smartUsed
    global thisLevelTutioral
    global tutorialsOn
    global finishOn 
    global missedCoin
    global globalFairy
    adaptive.setGameMode()
    globalFairy = None
    thisLevelTutioral = 0
    smartUsed = 0
    finishPlaformRight = 1000000  #stupidly large value 
    oldCameraX = 0
    cameraX = 0
    forcePause =0 #set to true if a game generated event wants the action to halt for a while
    comboLevel =0
#    oldMetaGame =99999
    x_max = 800
    gridLeft = x_max
    x_min = 0
    y_max = 600
    y_min = 0
    gravity = .15
    GameOverDelay = 600
    canStart = 0
    inEditor = 0
    CursorY = 300
    inEditor = 0
    editorToggle = 0
    FinishTimer = EndLength
    scoreBonus = 0
    ScreenMessages.clearMessages()
    LoadLevelData()
    ressetToStartOfLevel()
    levelQueued = 1
    continousWorldXOffset = 0
    escapeMenu.active = 0
    magnetOn = 0
    trailGame.initialise()
    tutorialsOn = checkIfTutorialsEnabled()
    if globalPlayer:
        globalPlayer.PlatformOn = None
    finishOn = 0
    missedCoin = 0
arcadeMusicList = ["Level1.ogg","Level2.ogg","Level3.ogg","Level4.ogg"]
arcadeMusicWin = ["level1Win","level2Win","level3Win","level4Win"]
arcadeMusicLose = ["level1Lose","level2Lose","level3Lose","level4Lose"]
#triggers the first time into the level tick
def firstTickLevel():
    global levelQueued
    if levelQueued == 1:
        levelQueued = 0
        fadeManager.fadeUpIfReady()    
      #  if(arcadeMode):
     #       ScreenMessages.setMessageScroll(messages.ArcadeGame,None)
     #       ScreenMessages.setMessageScroll(messages.Arcade2,None)
     #   else:
           # ScreenMessages.setMessageScroll(messages.Level,None,str(levelNumber))
         #   ScreenMessages.setMessageScroll(messages.Blank36,None,levelMetaData.title)  
        if arcadeMode:
            tuneIDX = int((levelNumber-1)/levelsPerArcadeSegment)
            if tuneIDX <0:
                tuneIDX = 0
            if tuneIDX > 3:
                tuneIDX = 3
            playTuneOgg (arcadeMusicList[tuneIDX],1)
            levelMetaData.winMusic = arcadeMusicWin[tuneIDX]
            levelMetaData.loseMusic = arcadeMusicLose[tuneIDX]
        else:
            playTuneOgg (levelMetaData.introMusic,1)
        if arcadeMode:
            launchArcadeToken()

levelToSpawnTokens = [3,5,10,13,20,26]
tokenToSpawn = [WorldTypes.ArcadePowerUpStunJump,WorldTypes.ArcadePowerUpHang,WorldTypes.ArcadePowerUpDash,WorldTypes.ArcadePowerUpSmash,WorldTypes.ArcadePowerUpFairy,WorldTypes.ArcadePowerUpSpeed]

def launchArcadeToken():  
#    print"starting launchtoken"
    count= 0
    for nextSpawnLevel in levelToSpawnTokens:
        if levelNumber >= nextSpawnLevel:
 #           print "check to see if we already got this one"
            if arcadePowerUpGot(tokenToSpawn[count])==0:
#                print "spawning token",tokenToSpawn[count]
                y = 280
                x = cameraX+2000
                token = tokenToSpawn[count]
                index = addObject(nextID,x,y,token)
                index.centreTrack = y
                return
        else:
            return
        count += 1
            
  
def ressetToStartOfLevel():
#    print "ressetToStartOfLevel"
    global rotation 
    global cameraX
    global cameraY
    global GameOverDelay
    global playerInWorld
    global FinishFlag
    global ExitFlag
    global FinishTimer
    global scoreBonus
    global nextObjectIndex
    global platformsToSpawn
    global combo
    global matchedTiles
    global comboTimer
    global bonusGame
    global tilesOver
    global oldMetaGame
    global objects
    global startLevelTimer
    global delayRefill
    global levelTime
    global levelTimeDelta
    startLevelTimer = 200
    combo = 0 
    FinishFlag = 0
    ExitFlag = 0
    playerInWorld = 0
    nextObjectIndex = 0
    comboTimer = 0       
    rotation = 0
    cameraX=0
    cameraY = 0    
    nextObjectIndex = 0
    platformsToSpawn = 0 
    objects = []
    ressetCoins()
    ressetCritters()
    spawnObjectOnScroll() # initialise the first batch of objects
    matchedTiles = []
    bonusGame = 0
    tilesOver=0
    if arcadeMode == 0:
        trailGame.emptytrail()
        EmptyGrid()
    scrollManager.ressetScroll()  
    delayRefill = 0   
    levelTime = 0
    levelTimeDelta = 0
  
###########################################
# mouseEnter
#
# Notifier called whenever the mouse enters
# the app window
#
###########################################
def mouseEnter():
        global gamePaused
        if(gamePaused==1):
            gamePaused = 0
        #forceSoundUpdate()
        #if(escapeMenu.active):
        #    escapeMenu.active = 0

###########################################
# mouseLeave
#
# Notifier called whenever the mouse leaves
# the app window
#
###########################################
def mouseLeave():
        global gamePaused
        gamePaused = 1
        #if escapeMenu.active == 0:
         #   escapeMenu.toggle()

###########################################
# mouseMove
#
# Notifier called whenever the mouse moves
# inside the app window
#
###########################################
def mouseMove( x, y ):
        # store for render
        global mousex, mousey
        mousex = x
        mousey = y
        if(inEditor):
            moveSelected(x,y)
#        if(inGUI):
        if ScreenMessages != None:
            ScreenMessages.mouseInput(x,y,-1)

def makeSparkleParticle(x,y,deltaX,deltaY,maxSize=1):
    deltaX += 0.5-(random.randint(0,10)/10.0)
    deltaY -= (random.randint(0,10)/20.0)
    size = .5 + (random.randint(0,10)/100.0)
    size *= maxSize
    particleChosenIndex = random.randint(1,2)
    if particleChosenIndex==1:
        particleChosen = fairySparleParticle1()
    else:
        particleChosen = fairySparleParticle2()
    particleController.addItem(particleChosen,x,y,size,deltaX,deltaY)
 
def makeGhostParticle(x,y,deltaX,deltaY,maxSize,diameter):
    deltaX += 0.5-(random.randint(0,10)/10.0)
    deltaY -= (random.randint(0,10)/20.0)
    angle = random.randint(0,100) * 44/700.00
    x += diameter/2*math.sin(angle)
    y += diameter/2* math.cos(angle)
    size = 1.0
    particleChosen = ghostParticle()
    particleController.addItem(particleChosen,x,y,size,deltaX,deltaY)

def makeAttackParticle(x,y,deltaX,deltaY,maxSize,h_bias,v_bias):
    deltaX += -1.5 + (random.randint(0,30)/10.0)
    deltaY -= (random.randint(0,30)/10.0)
    size = .5 + (random.randint(0,10)/20.0)
    x += (h_bias * -0.5) + random.randint(0,int(h_bias))
    y += (v_bias * -0.5) + random.randint(0,int(v_bias))
    size *= maxSize
    particleChosenIndex = random.randint(1,2)
    if particleChosenIndex==1:
        particleChosen = fairyAttackParticle1()
    else:
        particleChosen = fairyAttackParticle2()
    particleController.addItem(particleChosen,x,y,size,deltaX,deltaY)
    
def makeFireWorkParticle(x,y,deltaX,deltaY,maxSize,h_bias,v_bias): 
    deltaX += -1.5 + (random.randint(0,30)/10.0)
    deltaY -= (random.randint(0,30)/10.0)
    size = .5 + (random.randint(0,10)/20.0)
    x += (h_bias * -0.5) + random.randint(0,int(h_bias))
    y += (v_bias * -0.5) + random.randint(0,int(v_bias))
    size *= maxSize
    particleChosenIndex = random.randint(1,100)
    if particleChosenIndex<70:
        particleChosen = fireWorkParticle1()
    elif particleChosenIndex<92:
        particleChosen = fireWorkParticle2()
    else:
        particleChosen = fireWorkParticle3()
    particleController.addItem(particleChosen,x,y,size,deltaX,deltaY)
    
class pointer:
    image1 = None
    image2 = None
    xSize = 60
    ySize = 60
    xOffset = -18
    yOffset = -30
    enabled = 1
    targetAlpha = 255
    currentAlpha = 0
    oldX = 0
    oldY = 0
    deltaX = 0
    deltaY = 0
    clicked = 0
    nextSparkle = 10
    oldCameraX = 0
    
    def tick(self,delta):
        size = 0.25
        scrollDelta = (cameraX - self.oldCameraX)/delta
        self.oldCameraX = cameraX
        if self.clicked>0:
            size *= 4.0
            particle = fairyTrailParticle()
            self.clicked -= delta
        else:
            particle = fairyRedTrailParticle()
            if self.clicked <0:
                self.clicked = 0
        #distance = math.sqrt((self.deltaX * self.deltaX) + (self.deltaY * self.deltaY))
        deltaX = (mousex - self.oldX)/8.0
        deltaY = (mousey - self.oldY)/8.0
        if dataIsLoaded and gamePaused ==0 and self.enabled and renderDetailLevel>0:
            particleController.addItem(particle,cameraX+self.oldX,self.oldY,size,deltaX+ scrollDelta,deltaY)
            self.nextSparkle -= delta
            if self.nextSparkle<0:
                self.nextSparkle = 5
                makeSparkleParticle(cameraX+self.oldX,self.oldY,deltaX+scrollDelta,deltaY)

        if self.enabled == 0:
            self.targetAlpha = 0
        else:
            self.targetAlpha = 255
        if self.currentAlpha > self.targetAlpha:
            self.currentAlpha -= delta*10
        if self.currentAlpha < 0:
            self.currentAlpha = 0
        if self.currentAlpha < self.targetAlpha :
            self.currentAlpha += delta*10
        if self.currentAlpha > 255:
            self.currentAlpha = self.targetAlpha     

    def stop(self):
        self.targetAlpha = 0
        self.currentAlpha = 0
        self.enabled = 0

    def render(self):
        x = mousex
        y = mousey
        self.deltaX = self.oldX-x
        self.deltaY = self.oldY-y
        self.oldX = x
        self.oldY = y
        direction = 1
        xOffset = self.xOffset
        if gamePaused ==0:  #mouse has left the game
            PC.setColourize(0)
            pointerName = self.image1
            if continousTime%10>5:
                pointerName = self.image2
            frame = JPG_Resources[pointerName]
            PC.setColourize(1)
            PC.setColour(255,255,255,int(self.currentAlpha))
            if globalPlayer != None and metaGame == menuItems.game: 
                if x+cameraX < globalPlayer.x+(self.xSize+globalPlayer.width)/2:
                    direction = -1
                    xOffset = -2*self.xOffset
            PC.drawImageScaled(frame, x+xOffset, y+self.yOffset,direction*self.xSize,self.ySize )  
            PC.setColourize(0)
            
class fairyPointerClass(pointer):
    image1 = "Mouse01"
    image2 = "Mouse02"
    xSize = 32
    ySize = 40
    xOffset = -2
    yOffset = -9
    
class arrowPointerClass(pointer):
    image1 = "Mouse02"
    image2 = "Mouse02"
    xSize = 30
    ySize = 30
    xOffset = 0
    yOffset = 0    
    enabled = 0

fairyPointer = fairyPointerClass()
arrowPointer = arrowPointerClass()

def tickCursors(delta):
    fairyPointer.tick(delta)
    arrowPointer.tick(delta)

def renderCursors():
    fairyPointer.render()
    arrowPointer.render()
    
mouseToggle = 0
def moveSelected(mx,my):
    global objects
    for object in objects:
        if object.Selected:
            object.x = mx+object.mouseXoffset+cameraX
            object.y = my+object.mouseYoffset+cameraY
            
def updateSelection(mx,my,selection):
    global objects
    for object in objects:
        if(selection):
            x = object.x 
            y = object.y
            w = object.width
            h = object.height
            if(object.name == "BigWheel" or object.name == "CoinWheel" or object.name == "SmallWheel"or object.name == "SmallCoinWheel"):
                x+= (w/2)-25
                y+= (h/2)-25
                w = 50
                h = 50
            if(x<mx+cameraX and x+w>mx+cameraX and y<my and y+h>my and object.canBeSaved):
                if(object.Selected == 0):
                    object.mouseXoffset = object.x-(mx+cameraX)
                    object.mouseYoffset = object.y-(my+cameraY)
                    object.Selected = 1                
                else: 
                    object.Selected = 0

globalOldPlatformOn = None
def checkforPlatform(mx,my,mdn,double1Down):
    if FinishFlag:
        return
    if  my< 80 and mx>360 and mx < 440 and double1Down==1:
        smartBomb.start()

        return
    platformsFound = []
    noneSolid = []
    for object in objects:
        if object.inRange or object == globalPlayer:
            x = object.x 
            y = object.y
            w = object.width* object.scale
            h = (object.height* object.scale)# + object.selectExtension
            y += object.height- h 
            
            if(x<mx+pointerSizeX+cameraX and x+w>mx-pointerSizeX+cameraX and y-object.selectExtensionUp<my and y+h+object.selectExtensionDown>my):
                global globalOldPlatformOn
                if object == globalPlayer and globalPlayer.PlatformOn:
                    globalOldPlatformOn = globalPlayer.PlatformOn                 
                if object.solid:
                    platformsFound.append(object)
                elif object != globalPlayer:
                    noneSolid.append(object)
    if len(noneSolid)>0:
        # if we have selected a none solid item then do this one in preference to any other
        thisTest =  noneSolid
    else:
        thisTest = platformsFound
    for object in  thisTest:     
        x = object.x 
        y = object.y
        w = object.width* object.scale
        h = object.height* object.scale 
        y += object.height- h       
        if (mdn==0 or mdn ==1) and (globalPlayer.doingJump==0 or globalPlayer.onTrampoline):
            if mdn == 1 and object.inAttackRange:
                return
            if globalPlayer.onTrampoline==0:  
                globalPlayer.trampolineTarget = None            
                globalPlayer.moveTargetObject = object 
                if double1Down:
                    globalPlayer.thisTargetJump = 0
                else:
                    globalPlayer.thisTargetJump = 2
                globalPlayer.clickType = mdn 
                targetX = mousex
                if targetX+(globalPlayer.width*globalPlayer.scale/2) > gridLeft-12:
                    targetX = gridLeft - (globalPlayer.width*globalPlayer.scale/2)-12
                globalPlayer.moveTargetX = targetX+cameraX-x #relative x coordinate
                if globalPlayer.moveTargetX<(globalPlayer.width*globalPlayer.scale)/2:
                    globalPlayer.moveTargetX = (globalPlayer.width*globalPlayer.scale)/2
                if globalPlayer.moveTargetX+(globalPlayer.width*globalPlayer.scale)/2>object.width:
                    globalPlayer.moveTargetX = object.width - (globalPlayer.width*globalPlayer.scale)/2
            else:
                globalPlayer.trampolineTarget = object
                globalPlayer.moveTargetObject = object 
                globalPlayer.clickType = mdn 
#tony- currently trampolines don't work properly - player gets                
                targetX = mousex
                if targetX+(globalPlayer.width*globalPlayer.scale/2) > gridLeft-12:
                    targetX = gridLeft - (globalPlayer.width*globalPlayer.scale/2)-12
                globalPlayer.moveTargetX = targetX+cameraX-x #relative x coordinate
                if globalPlayer.moveTargetX<(globalPlayer.width*globalPlayer.scale)/2:
                    globalPlayer.moveTargetX = (globalPlayer.width*globalPlayer.scale)/2
                if globalPlayer.moveTargetX+(globalPlayer.width*globalPlayer.scale)/2>object.width:
                    globalPlayer.moveTargetX = object.width - (globalPlayer.width*globalPlayer.scale)/2
               # print "move target",globalPlayer.moveTargetX


                        

def openWebPage(address):                        
    webbrowser.open_new(address)
          
###########################################
# mouseDown
#
# Notifier called whenever a mouse button
# is pressed
#
###########################################def mouseDown( x, y, i ):
        # store for render
def mouseDown( x, y, i ):
        global mdx, mdy, mdn,mouseToggle
        global editorAddObject
        global button1Down
        global double1DownCount
        global double1Down
        global double2DownCount
        global double2Down
        global smartBombCount
        global instructionWait

        if instructionWait==1:
            instructionWait = 0
        doubleClickDelay = 30
        mdx = x
        mdy = y
        mdn = i
        button1Down = 0
        button2Down = 0
        double1Down = 0
        double2Down = 0
        if mdn == 0:
            button1Down = 1
            if double1DownCount> 0:
                double1Down = 1
                if globalOldPlatformOn and smashEnabled:
                    globalPlayer.smashSelected = 1
                    return
#            else: 
#                double1Down = 0
            double1DownCount = doubleClickDelay  
        if mdn == 1 and dashEnabled:
            if double2DownCount> 0:
                double2Down = 1
                if globalOldPlatformOn:
                    globalPlayer.dashSelected = 1
                    return
#            else: 
#                double2Down = 0
            double2DownCount = doubleClickDelay 
            double1DownCount = 0
        if fairyPointer:
            fairyPointer.clicked = 3
        if globalPlayer!= None:
            if(inEditor):
                if(mdn == 0 and mouseToggle ==0 and x>editorWidth): #left button
                    updateSelection(x,y,1)
                    mouseToggle = 1
            elif(inGUI==0 and globalPlayer.getOntoPlatformCount==0):
                checkforPlatform(x,y,mdn,double1Down)
        if(mdn ==0):    #check to see if player is clicking on a message
            if ScreenMessages:
                ScreenMessages.mouseInput(x,y,1)

###########################################
# mouseUp
#
# Notifier called whenever a mouse button
# is released
#
###########################################
def mouseUp( x, y, i ):
        # store for render
        global mux, muy, mun,mouseToggle
        global inGui
        global button1Down
        global instructionWait
        mux = x
        muy = y
        mun = i
        button1Down = 0
        mouseToggle = 0
        if(inEditor and mdn == 0): #left button
                updateSelection(x,y,0)

class StringInput:
    thisString = ''
    length = 128
    def addChar(self,char):
        if(char == keyMap.backSpace.keyValue):
            self.thisString = self.thisString[:-1]
        elif(char == keyMap.spaceKey.keyValue): #space pressed
            self.thisString = self.thisString+chr(32)
        else:
            if ( (len(self.thisString)<self.length-1) and (char >= ord("a") and char <= ord("z") ) or ( char >= ord("A") and char <= ord("Z") ) or ( char >= ord("0") and char <= ord("9") ) ):
                if(char>=ord('a') and char <=ord('z')):
                    if((checkKey(keyMap.leftShiftKey.keyValue)==0) and (checkKey(keyMap.rightShiftKey.keyValue)==0) ):
                        self.thisString = self.thisString+chr(char).lower()
                    else:
                        self.thisString = self.thisString+chr(char).upper()
                else:
                    self.thisString = self.thisString+chr(char)
    def clearString(self):
        self.thisString=''
        
    def getDisplayString(self):
        string = self.thisString
        if continousTime%100<50:
            string += "___________________"
        return string[:self.length-1]
  
workingString = StringInput()

def scoreWithIcon(x,y,worth):
    incScore(worth)

class ghostImage:
    x=0
    y=0
    facing=0
    frame = 0
    alpha = 200

class WorldObject:
    isTrampoline = 0
    collisionYBias = 0
    thisVolume = 1
    selectExtensionUp = 6
    selectExtensionDown = 6
    validStart = 0
    moveTargetObject = None
    canBeSaved = 1
    spawner = 0
    hangable=0
    rotated = 0
    tickDelay = 0
    worth = 50  #base value of enemy
    attacktimer = 0
    hitPoints = 0    # if zero then thing can't be attacked.
    baseFriction = 1 #overload this to change the friction cooefficiet of the surface
    friction = 1
    collected = 0
    placeable = 1   #set to 0 if not placeale
    scale = 1
    targetScale = 1
    scaleChangeSpeed = .002
    hint = 0
    solid = 1           #By default all objects are solid and can be stood on
    Selected = 0
    ID = 0
    type = 0
    name = ''
    x = 0
    y = 0
    z = 100             #by default in the middle
    oldX = 0
    oldY = 0
    res = None
    animation = None   #None by default
    frameNumber = 0
    animationSwitch = 0
    facing = 1
    rotation = 0
    height = 0
    width = 0
    life = 0
    x_speed = 0
    y_speed = 0
    xDeltaSpeed=0
    yDeltaSpeed=0
    target_x_speed=0
    target_y_speed=0
    base_speed = 0
    x_acceleration = 0.19
    onGround = 0
    max_Xspeed = 2.2
    graphic = 'player'
    tintr = 255
    tintg = 255
    tintb = 255
    tinta = 255
    colourize = 0
    mouseXoffset = 0
    mouseYoffset = 0
    GUIElement = 0
    killed = 0
    deathTimer = 0
    targetX = 0
    targetY = 0
    deltaX=0
    deltaY=0
    speed = 0
    topExtent=0
    ghostImages = []
    numberGhosts = 0
    showGhost = 0
    ghostOffsetX = 0
    ghostOffsetY = 0
    inRange = 0
    inHangRange = 0
    inAttackRange = 0
    dynamic = 0
    thisPanning = 1
    animationFrameRes = None
    
    def makeOnGroundSound(self):
        return 0
    
    def editorTick(self,delta):
        return 0

    def hit(self,points):
        #prototype function
        self.hitPoints -= points
        self.targetX = scoreX+160.0
        self.targetY = scoreY-100
        self.killed = 1
        self.speed = 2.0
        deltaX= self.targetX+cameraX-self.x
        deltaY = self.targetY-self.y
#        print "enemy hit",self.targetY,cameraY,self.y,deltaY
        distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
        self.deltaX = deltaX/distance
        self.deltaY = deltaY/distance  
 #       print "enemy delta",self.deltaX,self.deltaY
        if smartBomb.active() == 0 and gameOver == 0 and FinishFlag==0:
            playSimpleSoundList (['gotcha','haha'])  
        particleX = self.x + (self.width/2)
        particleY = self.y + (self.height/2.0)
        xSpeed = 0
        ySpeed = 0
        particle = hitEffectParticle()
        size = 0.1
        numberParticles = 6
        particleController.addItem(particle,particleX,particleY,size,xSpeed,ySpeed)
        if(self.hitPoints > 0) and self.killReplacement:
            self.setUpReplacment()
    def render(self):
        global cameraX
        if(self.colourize):
            PC.setColourize(1)
            PC.setColour(int(self.tintr),int(self.tintg),int(self.tintb),int(self.tinta))
        else:
            PC.setColourize(0)
        tempx = self.x-cameraX
        tempY = self.y + self.height - (self.height*self.scale)-cameraY
        if(self.facing<0):
            tempx+= (self.width*self.scale)
        if(self.animation==None):
            frame = self.res
        else:
        #    name = self.animation[self.frameNumber][0]  #Tony - used to get this here now it's cached
        #    frame = JPG_Resources[name]
            frame = self.animationFrameRes
        PC.drawmodeNormal()
        if(self.deathTimer==0):
            if(self.rotated==0):  #used to allow for rotating wasps and other animals
                #if we have a trail to show then render it before the main image
                if len(self.ghostImages)>0 and self.showGhost>0:
                    PC.setColourize(1)
                    for ghost in self.ghostImages:
                        gtempx = ghost.x-cameraX
                        if(ghost.facing<0):
                            gtempx+= (self.width*self.scale)
                        PC.setColour(255,100,100,int(ghost.alpha))
                        ghost.alpha -= 17
                        PC.drawImageScaled(ghost.frame, gtempx, ghost.y,ghost.facing,self.height*self.scale)
                if(self.colourize):
                    PC.setColourize(1)
                    PC.setColour(int(self.tintr),int(self.tintg),int(self.tintb),int(self.tinta))
                else:
                    PC.setColourize(0)
                PC.drawImageScaled(frame, tempx, tempY,self.facing * self.width*self.scale,self.height*self.scale)
                if self.numberGhosts >0:
                    self.addGhost(self.x+self.ghostOffsetX,tempY+self.ghostOffsetY,frame,self.facing * self.width*self.scale,120)
                    self.ghostOffsetX = 0       #these are not currently used but can be set up to displace the ghost
                    self.ghostOffsetY = 0
            else:
                if(self.colourize):
                    PC.setColourize(1)
                    PC.setColour(int(self.tintr),int(self.tintg),int(self.tintb),int(self.tinta))
                else:
                    PC.setColourize(0)
                PC.drawImageRot(frame, tempx, tempY,self.rotated)
        else:
            if(self.colourize):
                PC.setColourize(1)
                PC.setColour(int(self.tintr),int(self.tintg),int(self.tintb),int(self.tinta))
            else:
                PC.setColourize(0)
            PC.drawImageRot(frame, tempx, tempY,self.deathTimer/5.0)
          
        #PC.drawImageScaled( self.res, self.x-cameraX, self.y, self.width, self.height)
        if(self.Selected):
            PC.setColour( 128, 128, 128, 128)
            PC.fillRect( self.x-cameraX-10, tempY-10, (self.width*self.scale)+20, (self.height*self.scale)+20 )
            
    def tick(self,delta):
        self.thisPanning = (self.x-cameraX-400)/100
        if(self.scale<self.targetScale):
            self.scale+=(self.scaleChangeSpeed*delta)
            if self.scale> self.targetScale:
                self.scale =  self.targetScale
        elif(self.scale>self.targetScale):
            scaleDelta = (self.scale - self.targetScale) * 0.05
            self.scale-= scaleDelta
            if self.scale < self.targetScale:
                self.scale =  self.targetScale
        self.controlAnimation(delta)
        self.oldX = self.x
        self.oldY = self.y
        self.life += delta
    def controlAnimation(self,delta):
        if(self.animation != None):
            if(self.animationSwitch< self.life):
                self.animationFrameRes = JPG_Resources[self.animation[self.frameNumber][0]]
                self.frameNumber = self.animation[self.frameNumber][1]
                self.animationSwitch += self.animation[self.frameNumber][2]
                playSimpleSoundList(self.animation[self.frameNumber][3],volume = self.thisVolume,panning = self.thisPanning)
            
    def doAnimation(self,newAnimation,animationSpeed):
        #print"do animation",self.name
        name = self.animation[self.frameNumber][0]
        frame = JPG_Resources[name]
        #store the old height so we can move the character up if required
        oldHeight = PCR.imageHeight(frame) 
        if( (newAnimation!= None) and (self.animation !=newAnimation)):
            self.animation=newAnimation
            self.frameNumber = 0
            self.animationSwitch = self.animation[self.frameNumber][2]
            playSimpleSoundList(self.animation[self.frameNumber][3],panning = self.thisPanning)
        #    print"sound playing",self.animation[self.frameNumber][3]
        else:    
            self.animationSwitch -= animationSpeed;
            if(self.animationSwitch<= 0):
                self.frameNumber = self.animation[self.frameNumber][1]
                nextAnimation = self.animation[self.frameNumber][4]
                if nextAnimation != None:
#                    print" switching animations"
                    self.frameNumber = 0
                    self.animation = nextAnimation
                self.animationSwitch = self.animation[self.frameNumber][2]
                playSimpleSoundList(self.animation[self.frameNumber][3],panning = self.thisPanning)
        name = self.animation[self.frameNumber][0]
        #need to compensate for the fact thqat different frames are different heights
        frame = JPG_Resources[name]
        self.height = PCR.imageHeight(frame)  
        self.width = PCR.imageWidth(frame) 
        heightDelta = oldHeight-self.height
        self.animationFrameRes = frame
        if(self.hangMode==0 ):   #if we are hanging then we don't compensate for a change in height
            self.y += heightDelta
    def spawn(self):
        return 0                #by default doesn't have a death
        
    def Death(self,delta):
        return 0
        
    def isCollected(self):      #by detault does nothing
        return 0
        
    def stoodOn(self):          #by default does nothing
        return 0
        
    def isSmash(self):          #by default does nothing
        return 0
        
    def setUpGraphics(self):   #by default sets up using graphic
        self.res = JPG_Resources[self.graphic]
        self.height = PCR.imageHeight( self.res )
        self.width= PCR.imageWidth( self.res ) 
        if self.animation:
            self.animationFrameRes = JPG_Resources[self.animation[self.frameNumber][0]]
        
    def canBePlaced(self):          #by default returns true
        return 1
        
    def __init__(self):
      self.ghostImages = [] 
    
    def getGraphic(self):              #by default returns graphic or animation
        if self.animation:
            name = self.animation[0][0]
        #need to compensate for the fact thqat different frames are different heights
            #frame = JPG_Resources[name]
            return name
        return self.graphic
      
    def addGhost(self,x,y,frame,facing,alpha):
        ghost = ghostImage()
        ghost.x = x
        ghost.y = y
        ghost.facing = facing
        ghost.frame = frame
        ghost.alpha = alpha
        self.ghostImages.append(ghost)
        #clamp at number of ghosts
        self.ghostImages = self.ghostImages[-self.numberGhosts:]  
          
    def getcollisionList(self):
        return solidObjects
        
def spawnPlayer():
    global playerInWorld
    object = addObject(nextID,cameraX+40,50,WorldTypes.Player)  # add in the player
#    object = addObject(nextID,cameraX+40,50,WorldTypes.Player)  # add in the player
    playerInWorld= 1
    return object


class PlayerSubGame(WorldObject):
    name = 'playerSubGame'
    graphic = 'player_sub_01'
    y_speed = 2
    y_max_speed = 6
    acceleration = 1
    nextBlock = 'Red'
    firstTime = 1
    placeable = 0  #set to 0 if not placeale
    def render(self):
        self.facing = 1
        if(self.nextBlock !='None'):
            tileName = self.nextBlock+'Tile'
            graphic = JPG_Resources[tileName]
            x = self.x-cameraX -40
            y = self.y            
            PC.drawImageScaled( graphic, x, int(((y+30)/GridPitchY)*GridPitchY), GridPitchY, GridPitchY)
        WorldObject.render(self)
    def tick(self,delta):
        WorldObject.doAnimation(self,animationSets.player_sub,delta)#sequence the animation 
        self.targetScale = 1+(math.sqrt(comboLevel)*comboScale)
        if(self.firstTime):
           # self.nextBlock = Checkcolours(); //this is broekn
            self.firstTime = 0
        if checkKey(keyMap.upKey.keyValue):
            self.y_speed -= self.acceleration
            if(self.y_speed<-1 * self.y_max_speed):
                self.y_speed = -1 * self.y_max_speed   
        elif checkKey(keyMap.downKey.keyValue):
            self.y_speed += self.acceleration
            if(self.y_speed>self.y_max_speed):
                self.y_speed = self.y_max_speed  
        else:
            self.y_speed = 0
        self.y += self.y_speed 
        if(self.y < y_min):
            self.y = y_min
        if(self.y > y_max-self.height):
            self.y = y_max-self.height
#        if(checkKeyNoRepeat(keyMap.fireKey.keyValue)):  #tony - this all needs rewriting now
 #           if(self.nextBlock != 'None'):
#                AddToGrid(self.nextBlock,self.y+30+40,1)
 #           self.nextBlock = Checkcolours()
        WorldObject.tick(self,delta)

class physicsObject(WorldObject):
    collisionObjects = []
    maximum_y_speed = 6
    jumpSpeed = -4.0 #was 6
    deathTimer = 0
    PlatformOn = None   #copy of the platform we are currently standing on
    oldPlatformOn = None
    onBottom = 0
    tempbase_speed = 0
    tempy_speed = 0

    def tick(self,delta):
        global lives
        self.tickDelay-=delta
        if(self.tickDelay>0):
            return
        else:
            self.tickDelay = 0
        self.onGround -= delta
        if(self.onGround < 0):
            self.onGround = 0
            self.oldPlatformOn=self.PlatformOn
        self.PlatformOn = None
        self.collisionObjects = [] # clear the array
        self.y_speed += gravity*delta
        if(self.y_speed > self.maximum_y_speed):
           self.y_speed = self.maximum_y_speed
        deltaSpeed = self.x_speed - (self.target_x_speed+self.base_speed)
        self.xDeltaSpeed = self.x_speed - self.base_speed
        if(deltaSpeed>0.3):
            self.x_speed -= self.x_acceleration*self.friction
        elif(deltaSpeed<-0.3):
            self.x_speed += self.x_acceleration*self.friction
        else:
            self.x_speed = self.target_x_speed+self.base_speed
        self.x += self.x_speed *delta
        self.y += self.y_speed*delta
        #now do collision
        selfX = self.x
        selfY = self.y+ self.height-(self.height*self.scale)
        selfW = self.width*self.scale
        selfH = self.height*self.scale
        
        thisBottom = selfY + selfH
        thisRight = selfX + selfW
        self.onBottom = 0
        if(selfY > (y_max - selfH+cameraY) ):
            self.onBottom = 1
            selfY = y_max - selfH+cameraY
            self.y = selfY+selfH-self.height
            if(self.y_speed > 0 and self.name == "player"):
                self.y_speed = 0
                self.painCount = -1
                self.invulnerable = -1
                self.Death(delta)
                trailGame.emptytrail(1)
            self.onGround = 3.0
            self.base_speed = 0
        self.doCollision(delta)
        if self.onGround:
            if self.PlatformOn:
                selfY = self.PlatformOn.y-selfH
                self.y = selfY+selfH-self.height+1
                self.base_speed = self.tempbase_speed
                self.friction = self.baseFriction*self.PlatformOn.baseFriction
                self.y_speed = self.tempy_speed
                #print "on platform",self.PlatformOn.name,self.PlatformOn.y_speed
        WorldObject.tick(self,delta)
        
    def doCollision(self,delta):
        selfX = self.x
        selfY = self.y+ self.height-(self.height*self.scale)
        selfW = self.width*self.scale
        selfH = self.height*self.scale      
        selfY_Speed = self.y_speed
        thisBottom = selfY + selfH
        thisRight = selfX + selfW
        collisionObjectList = self.getcollisionList()
        for thisObject in collisionObjectList:
            if(thisObject != self and self.deathTimer==0):  #don't collide with self
                if thisObject.scale==1:
                    thisObjectH = thisObject.height
                    thisObjectW = thisObject.width
                    thisObjectY = thisObject.y
                else:
                    thisObjectH = thisObject.height*thisObject.scale
                    thisObjectW = thisObject.width*thisObject.scale
                    thisObjectY = thisObject.y + thisObject.height-(thisObject.height*thisObject.scale)                  
                thisObjectX = thisObject.x
                if(thisRight > thisObjectX):
                    thisObjectRight = thisObjectX + thisObjectW
                    if(selfX < thisObjectRight):
                        if(thisBottom > thisObjectY-1):
                            thisObjectBottom = thisObjectY + thisObjectH                          
                            if(selfY < thisObjectBottom):
                                self.collisionObjects.append(thisObject)
                                #OK we are colliding with this platform
                                if(thisObject.solid == 1):
                                    if(thisBottom - thisObjectY < 10):
                                        deltaY = selfY_Speed - thisObject.y_speed
                                        if(deltaY>0):
                                            if self == globalPlayer:
                                                if self.doingJump == 0:
                                                    if self.onGround == 0:
                                                        self.makeOnGroundSound(deltaY)
                                                    self.onGround = 2
                                            else:
                                                self.onGround = 2
                                            if self.PlatformOn:
                                                if self.moveTargetObject == thisObject:
                                                    self.PlatformOn = thisObject
                                            else:
                                                self.PlatformOn = thisObject
                                            self.tempy_speed = self.PlatformOn.y_speed
                                            self.tempbase_speed = self.PlatformOn.x_speed
                                            if scrollManager.slowDown and self == globalPlayer:
                                                self.tempbase_speed /= 4.0
                                                #self.y_speed = self.PlatformOn.y_speed
                                #now check to see if we can kill an alien
                                if(thisObject.hitPoints > 0 and self.attacktimer>0 and stunJumpEnabled):
                                    if(thisBottom - thisObjectY < 40):
                                        deltaY = selfY_Speed - thisObject.y_speed
                                        if(deltaY>0):
                                            self.onGround = 2
                                            self.PlatformOn = thisObject
                                            self.tempy_speed = self.jumpSpeed-((self.scale-1)*1.4)
                                            self.tempbase_speed = self.x_speed
                                            thisObject.hit(comboLevel+1)
                                            #self.invulnerable= 150
                                            self.trampolineTargetLocal=0
                                            self.trampolineTarget=None                            

allowEnemyAtDifficulty = 1
minSpawnRange = 400
lastSpawnedEnemyX = 0

class enemy(physicsObject):
    z = 75
    deathSpeed = 0
    targetX = 0
    targetY = 0
    spawnNoted = 0
    tint = 255
    targetTint = 255
    inRange = 0
    killReplacement = 0
    hitPoints = 1
    attackDelta = 1
    attackDelay = 0
    solid = 0
    collisionWidth = 0.4
    collisionHeight = 0.3
    thisPanning = 0
    thisVolume = 1
    inPhysics = 1
    
    def tick(self,delta):
        global crittersCollected
        global crittersSpawned

        self.attackDelay -= delta
        volume = 1
        self.thisPanning = (self.x-cameraX-400)/100
        if self.thisPanning < -4:
            volume = 0
        elif self.thisPanning > 4:
            volume = 0

        self.thisVolume = volume
        if self.attackDelay < 0:
            self.attackDelay = 0
        if(self.spawnNoted==0):
            crittersSpawned += 1
            self.spawnNoted = 1
        if self.killed:
            self.x_speed = self.deltaX * self.speed
            self.y_speed = self.deltaY * self.speed
           # print "enemydead",self.name,self.x_speed,self.y_speed,self.y
            self.x += self.x_speed
            self.y += self.y_speed
            self.speed += 0.2  
            self.deathTimer += delta
            if(self.y<20 and self.x>cameraX-100):
                scoreWithIcon(self.x,self.y,self.worth)
                crittersCollected += 1
                self.x = -600
        else:
            if self.inPhysics:
            #    print "enemy in phyics",self.name
                physicsObject.tick(self,delta)
            if (self.x+self.width)-cameraX>0 and self.x-cameraX<800 and smartBomb.active():
                self.hit(10000) #deal huge amount of damage!
            if globalPlayer:
                thisObject = globalPlayer
                if self.attackDelay==0:
                    #now we have to scale down the enemy collisio volume to make it less sensitivve
                    widthReduction = self.width*self.collisionWidth
                    heightReduction = self.height*self.collisionHeight
                    enemyX = self.x+(widthReduction/2)
                    enemyWidth = self.width-widthReduction
                    enemyY = self.y+(heightReduction/2)
                    enemyHeight = self.height-heightReduction
                    enemyRight = enemyX + enemyWidth
                    enemyBottom = enemyY + enemyHeight
                    playerX = thisObject.x
                    playerY = thisObject.y+ thisObject.height-(thisObject.height*thisObject.scale)
                    playerW = thisObject.width*thisObject.scale
                    playerH = thisObject.height*thisObject.scale
                    playerBottom = playerY + playerH
                    playerRight = playerX + playerW
                    if (playerX < enemyRight) and (playerRight > enemyX):
                        if (playerY < enemyBottom) and (playerBottom > enemyY):
                            if thisObject.dashMode or thisObject.doingSmash:
                                self.hit(10000) #deal huge amount of damage!
                            elif globalFairy:
                                if globalFairy.attackingThis(self)==0:
                                    thisObject.Death(delta,self.attackDelta)
                            else:
                                thisObject.Death(delta,self.attackDelta)
                                if self.name == "Acid":
                                    self.hitPlayer()
        self.isSelectable(delta)


    def isSelectable(self,delta):
        self.inRange = 0
        if(stunJumpEnabled==0 or self.hitPoints == 0):
            self.tint = 255
            self.inRange = 0
            self.inAttackRange = 0
        else:
            #first only allow enemy on the screen to be selected
            if (self.x<cameraX+x_max) and (self.x+self.width>cameraX):
                if globalPlayer != None:
                    localPlayer = globalPlayer
                    if localPlayer.PlatformOn or localPlayer.onTrampoline:
                        playerCenterX = localPlayer.x+(localPlayer.width/2*localPlayer.scale)
                        selfCentreX = self.x+(self.width/2)
                        distanceX = playerCenterX- selfCentreX
                        if(profiles[currentProfile].mouseControl==1):
                            maxJumpLookUp=findJumpLookUp(0)
                            YAfterJump = getTableValue(distanceX,maxJumpLookUp)
                            if localPlayer.hangMode==0:
                                playerHeight = self.height
                            else:
                                playerHeight = hangSpriteHeight
                            if(localPlayer.onTrampoline):
                                yDelta = trampolinePlayerY+playerHeight-self.y
                            else:
                                yDelta = localPlayer.y+playerHeight-self.y
                            yDelta += self.collisionYBias
                            if(YAfterJump>yDelta):
                                self.inRange = 1
                                self.inAttackRange = 1
            
    def render(self):
        WorldObject.render(self)
        self.colourize = 1
        if(self.killed):
            PC.setColour( 60,200,0,256,)
            PC.setFont( font36 )
            string = str(self.worth)
            x = self.x+(self.width/2)-cameraX-10
            PC.drawString(string, x, self.y+60-cameraY )
            
        if(globalPlayer!= None):
            if(globalPlayer.PlatformOn!= None):
                if self.inRange==1:
                    self.tint = 155+ (math.sin(self.life/10.0)*130)
                    if self.tint>255:
                        self.tint = 255
                    if self.tint<50:
                        self.tint = 50
                else:
                    self.tint = 255
        if(profiles[currentProfile].mouseControl==0):
            self.tint = 255
        self.tintr = 255
        self.tintg = self.tint
        self.tintb = self.tint
        self.tinta = 255

class KillerOrange(enemy):
    hitPoints = 1
    solid = 0
    name = 'killerOrange1'
    graphic = 'HugeBall'
    maximum_y_speed = 20
    animation = animationSets.HugeBall_move
    bounceSound = "bigBounce"
    global objects
    def tick(self,delta):
        self.rotated += delta*0.1
        self.target_x_speed = -2.0       
        tempY = self.y_speed
        self.x_speed = -2.0
        enemy.tick(self,delta)       #tick the parent class  
        if(self.onGround and tempY > 0):
            #if we've hit a platform then invert movement
            self.y_speed = -tempY
            thisVolume = tempY/15.0
            #print "bounce volume",thisVolume
            if thisVolume>1:
                thisVolume = 1
            if thisVolume <0:
                thisVolume = 0
           # print "bounce volume",thisVolume            
            playSimpleSound (self.bounceSound,volume = thisVolume,panning = self.thisPanning) 
    

               
class Spider(enemy):
    hitPoints = 1
    solid = 0
    name = 'Spider'
    graphic = 'Spider1'
    maximum_y_speed = 0.6
    y_dir = 1
    animation = animationSets.spider_move
    webGraphic = 'ThinWeb'
    global objects
    
    def render(self):
        #render the web
        if self.killed == 0:
            webX = self.x + self.width/2
            webY = self.topExtent        
            PC.setClipRect(0,self.topExtent,800,self.y-self.topExtent+5)
            frame = JPG_Resources[self.webGraphic]
            PC.drawImage(frame,webX-cameraX,webY-cameraY)
            PC.clearClipRect()
        enemy.render(self)
    
    def tick(self,delta):
        temp = self.y
        tempx = self.x  #we don't want physics to move spider in the X if it hits a platform
        enemy.tick(self,delta)       #tick the parent class  
        if self.killed == 0:
            #only do the following stuff if we are not dead
            self.x = tempx
            if(self.onGround and self.y_dir>0):
                #if we've hit a platform then invert movement
                self.y_dir = -1
                playSimpleSound ('smallSpiderDown',panning = self.thisPanning) 
            if(self.y_dir>0):
                self.y =  temp+(self.maximum_y_speed*delta)
            else:
                self.y =  temp-((self.maximum_y_speed*delta)*1.5)
            if(self.y<=self.topExtent and self.y_dir<0):
                self.y_dir = 1
                playSimpleSound ('smallSpiderUp',panning = self.thisPanning) 
                
class LargeSpider(Spider):
    hitPoints = 2
    name='bigspider'
    graphic='bigspider01'    
    webGraphic = 'ThickWeb'
    animation = animationSets.largespider_idle
    maximum_y_speed = 1.5 
    y_dir =0
    visionRangeX = 40   
    platformBelow = None
    worth = 250
    killReplacement = WorldTypes.Spider
    PlatformSetUp = 0
    
    def setUpBelowPlatform(self):
        currentY = 600
  #      print "spawning Spider",self.x,self.width 
        self.PlatformSetUp = 1
        for object in objects:
            if object.x < self.x+self.width and object.x+object.width>self.x:
                if (object.y < currentY) and (object.y > self.y+self.height) and object.solid:
                    self.platformBelow = object
                    currentY = object.y
    
    def tick(self,delta):
        temp = self.y
        tempx = self.x  #we don't want physics to move spider in the X if it hits a platform
        enemy.tick(self,delta)       #tick the parent class 
        if self.life>10 and self.PlatformSetUp==0:
            self.setUpBelowPlatform()
        if self.killed == 0:
            self.y = temp
            #only do the following stuff if we are not dead
            self.x = tempx
            if(self.onGround and self.y_dir>0):
                self.animation = animationSets.largespider_attack
                playSimpleSound ('spiderGrab',panning = self.thisPanning) 
                #if we've hit a platform then invert movement
                self.y_dir = -1
            if(self.y_dir>0):
                self.y =  temp+(self.maximum_y_speed*delta*2.5)
            elif(self.y_dir<0):
                self.y =  temp-((self.maximum_y_speed*delta)*1)
            if(self.y<=self.topExtent and self.y_dir<0):
                self.y_dir = 0
            visionMinimumX = self.x-self.visionRangeX
            visionMaximumX = self.x+self.width+self.visionRangeX
            if globalPlayer!= None and self.platformBelow != None:
                playerMinX = globalPlayer.x
                playerMaxX = globalPlayer.x+globalPlayer.width
                if self.y+self.height>globalPlayer.y and self.y_dir>0:
                    self.animation = animationSets.largespider_attack                    
                if(visionMinimumX<playerMaxX and visionMaximumX>playerMinX and self.y_dir==0 and globalPlayer.PlatformOn == self.platformBelow and globalPlayer.hangMode==0):
                    self.animation = animationSets.largespider_move
                    playSimpleSound ('spiderDown',panning = self.thisPanning)                    
                    self.frameNumber= 0
                    self.y_dir = 1
                    self.visionRangeX -= 20
                    if self.visionRangeX<0:
                        self.visionRangeX =0 
    def setUpReplacment(self):
        index = addObject(nextID,self.x-25,self.topExtent,self.killReplacement)
        index.y += 20
        index.attackDelay = replacementAttackDelay
        index = addObject(nextID,self.x+25,self.topExtent,self.killReplacement)
        index.y += 40
        index.attackDelay = replacementAttackDelay

balloonTypes = [ animationSets.balloonBlue_move,animationSets.balloonRed_move,animationSets.balloonYellow_move]

class Balloon(enemy):
    hitPoints = 1
    name = "Balloon"
    graphic = "BalloonYellow"
    animation = None
    startDelay = 0
    target_y_speed = -2.5
    minX = 0
    maxX = 0
    x_dir = 0
    x_acceleration = 0.02
    x_dir = x_acceleration    
    stringRes = None
    stringWidth = 0
    solid = 0
    
    def render(self):
        enemy.render(self)
        if inEditor == 0:
            stringY = self.y+self.height-cameraY
            stringX = self.x + (self.width/2) - (self.stringWidth/2)-cameraX+2
            PC.drawmodeNormal()
            PC.setColourize(0)
            PC.drawImage(self.stringRes,stringX,stringY)
            PC.drawmodeNormal()        
        
        
    def tick(self,delta):
        if self.y < -100.0:
            self.x = -300
        if self.x < cameraX+x_max:
            self.startDelay -= delta
        if self.startDelay < 0:
            self.startDelay = 0
        
        if self.startDelay:
            #do idle animation here
            temp = 0
        else:
            self.y_speed -= 0.02
            self.x_speed += self.x_dir
            self.x += self.x_speed*delta
            if self.x > self.maxX:
                self.x_dir = -self.x_acceleration
            if self.x < self.minX:
                self.x_dir = self.x_acceleration
            if self.y_speed < self.target_y_speed:
                self.y_speed = self.target_y_speed
        temp_y_speed = self.y_speed
        temp_x_speed = self.x_speed
        enemy.tick(self,delta)
        self.y_speed = temp_y_speed
        self.x_speed = temp_x_speed

    def spawn(self):
        self.startDelay = random.randint(100,260)
        self.target_y_speed += random.randint(0,100)/100.0
        self.minX = self.x - 10
        self.maxX = self.x + 10
        type = random.randint(0,2)
        self.animation = balloonTypes[type]
        name = self.animation[self.frameNumber][0]
        frame = JPG_Resources[name]
        self.width = PCR.imageWidth(frame)
        self.height = PCR.imageHeight(frame)
        self.stringRes = JPG_Resources["string"]
        self.stringWidth = PCR.imageWidth(self.stringRes)
        self.res = frame
        self.animationFrameRes = frame

class SmallBall(enemy):
    hitPoints = 1
    solid = 0
    active = 0
    name = 'SmallBall'
    graphic = 'SmallBall'
    facing = 1
    animation = animationSets.smallball_move
    damping = -0.95
    bounces = 0
    ballOldPlatformOn = None
    x_acceleration=0.04
    target_x_speed = -2.5
    bounceSound = "smallBounce"
    global objects
    def tick(self,delta):
        if(self.x<cameraX+x_max):
            self.active = 1
        if self.active ==0:
            return
        if self.onGround and self.ballOldPlatformOn!= None:
            if self.ballOldPlatformOn != self.PlatformOn:
                self.target_x_speed = self.target_x_speed * -1
        if self.onGround:
            self.ballOldPlatformOn = self.PlatformOn       
        self.rotated -= self.x_speed/20.0
        tempY = self.y_speed
        enemy.tick(self,delta)       #tick the parent class  
        if(self.onGround and tempY>=0):
            self.bounces+=1
            if tempY<0.25 :
                self.y_speed = 0
            else:
                self.y_speed = tempY*self.damping 
                thisVolume = tempY/15.0
                #print "bounce volume",thisVolume
                if thisVolume>1:
                    thisVolume = 1
                if thisVolume <0:
                    thisVolume = 0
               # print "bounce volume",thisVolume  
                thisVolume *= self.thisVolume
                if thisVolume>0:
                    playSimpleSound (self.bounceSound,volume = thisVolume,panning = self.thisPanning) 

class BigBall(SmallBall):
    name = "BigBall"
    graphic = "BigBall"
    rotationSpeed = 0.2
    damping = -0.7
    animation = animationSets.bigball_move
    target_x_speed = -2
    bounceSound = "bigBounce"
 
class Acid(SmallBall):
    placeable = 0
    name = "Acid"
    graphic = "Acid1"
    maxXSpeed = -2.0
    rotationSpeed = 0.2
    damping = -0.98
    animation = animationSets.Acid_move
    y_speed = -2
    attackDelta = 20
    
    def tick(self,delta):
        if(self.bounces >0):
            spawnAcidParticles(self.x,self.y,self.thisPanning)
            self.x = -300   
        oldDelta = delta
        delta /= 1.5
        SmallBall.tick(self,delta)
        delta = oldDelta
        
    def hitPlayer(self):
        spawnAcidParticles(self.x,self.y,self.thisPanning)
        self.x = -300     
    
    def spawn(self):
        self.y_speed = -2 -(random.randint(1,3))
 
def spawnAcidParticles(x,y,thisPanning): 
    playSimpleSound ('acidSplat',panning = thisPanning)
    deltaX = random.randint(10,20)/-20.0
    particleController.addItem(acidParticle(),x+2,y+30,1,deltaX,-1.2)
    particleController.addItem(acidParticle(),x+2,y+30,1,0,-1.4)
    deltaX = random.randint(10,20)/20.0
    particleController.addItem(acidParticle(),x+2,y+30,1,deltaX,-1.2)
 
class Snail(enemy):
    hitPoints = 1
    solid = 0
    name = 'Snail'
    graphic = 'Snail01'
    maxXSpeed = 1.0
    target_x_speed = -maxXSpeed
    facing = -1
    animation = animationSets.snail_move
    directionSound = 'snailDirection'
    0.1
    global objects
    def tick(self,delta):
        #self.target_x_speed = self.maxXSpeed   
        if self.x>cameraX+850:
            return
        if globalPlayer:
            if delta != 0:
                if globalPlayer.platformSmashed==self.PlatformOn and self.PlatformOn:
                    self.PlatformOn = None
                    self.hit(10000)
        enemy.tick(self,delta)       #tick the parent class 
        if self.killed:
            return
        #if(self.onGround):    
        if(self.PlatformOn==None):
            if delta != 0:
               # self.x = -300
                temp = 1
         #       if(self.oldPlatformOn != None):
        #            self.oldPlatformOn = None
         #           self.hit(10000)
 #               print "Warning! snail on ground"
        else:
            self.inPhysics = 0
            if(self.PlatformOn.x >self.x):
                self.target_x_speed = self.maxXSpeed
                if self.facing == -1:
                    playSimpleSound (self.directionSound,panning = self.thisPanning)
                self.facing = 1
            if(self.PlatformOn.x+ self.PlatformOn.width < self.x+self.width):
                self.target_x_speed = -self.maxXSpeed
                if self.facing == 1:
                    playSimpleSound (self.directionSound,panning = self.thisPanning)
                self.facing = -1
        if self.inPhysics ==0:
            WorldObject.tick(self,delta)
            if self.PlatformOn != None:
                self.base_speed = self.PlatformOn.x_speed
                deltaSpeed = self.x_speed - (self.target_x_speed+self.base_speed)
                self.xDeltaSpeed = self.x_speed - self.base_speed
                if(deltaSpeed>0.3):
                    self.x_speed -= self.x_acceleration*self.friction
                elif(deltaSpeed<-0.3):
                    self.x_speed += self.x_acceleration*self.friction
                else:
                    self.x_speed = self.target_x_speed+self.base_speed
                self.x += self.x_speed *delta
            
class LargeSnail(Snail):
    collisionYBias = -20
    hitPoints = 2
    name='LargeSnail'
    graphic='Bigsnail01'
    animation = animationSets.largesnail_move 
    maxXSpeed = 1.5
    target_x_speed = maxXSpeed
    attackClock=0
    x_acceleration = 0.04
    canAttack = 1
    worth = 250
    waitTillAttack = 0
    killReplacement = WorldTypes.Snail
    seenPlayer = 0
    directionSound = 'snailDirectionLarge'
    
    def tick(self,delta):
        self.attackClock += delta
        self.waitTillAttack -= delta
        if self.waitTillAttack<0:
            self.waitTillAttack = 0
        if self.PlatformOn!=None:
            if globalPlayer != None:
                if self.PlatformOn == globalPlayer.PlatformOn and globalPlayer.hangMode ==0:
                    if self.seenPlayer == 0:
                        playSimpleSound ('snailAlert',panning = self.thisPanning)                     
                    self.seenPlayer = 1
                    self.colourize = 1
                    attackValue = math.sin(self.attackClock/10)
                    self.tintg = 120+(attackValue*120)
                    if self.x < globalPlayer.x:
                        self.target_x_speed = self.maxXSpeed/4
                        self.facing = 1
                    elif self.x > globalPlayer.x:
                        self.target_x_speed = -self.maxXSpeed/4
                        self.facing = -1
                    if(attackValue>0.8 and self.canAttack and self.waitTillAttack == 0):
                        self.canAttack = 0
                        type = WorldTypes.Acid 
                        index = addObject(nextID,0,0,type)
                        index.x = self.x
                        if(self.facing>0):
                            index.x += self.width-10
                        else:
                            index.x -= 10
                        index.y = self.y+self.height-20
                        index.maxXSpeed = self.facing*(random.randint(3,6))
                        index.x_speed = index.maxXSpeed
                        
                    if(attackValue<0):
                        self.canAttack = 1
                else:
                    self.seenPlayer = 0
                    if self.facing > 0:
                        self.target_x_speed = self.maxXSpeed
                    else:
                        self.target_x_speed = -self.maxXSpeed
                    self.canAttack = 0
                    self.attackClock = 0
                    self.waitTillAttack = 30
        Snail.tick(self,delta) 
        
    def setUpReplacment(self):
            index = addObject(nextID,self.x-10,self.y+2,self.killReplacement)
            index.target_x_speed = index.maxXSpeed
            index.facing = 1
            index.attackDelay = replacementAttackDelay
            index = addObject(nextID,self.x+10,self.y+2,self.killReplacement)
            index.target_x_speed = index.maxXSpeed*-1
            index.facing = -1
            index.attackDelay = replacementAttackDelay


maxDistanceToPlayer = 300 

class Fairy(physicsObject):   
    speed = 5
    placeable = 0
    z = 40
    hitPoints = 1
    solid = 0
    name = 'Fairy'
    graphic = 'Fairy01'
    target_x_speed = 0
    target_y_speed = 0
    facing = -1
    x_acceleration = 0.1
    animation = animationSets.fairy_move 
    attackTarget = None
    checkIndex = 0
    attackCount = 0
    
    def attackingThis(self,enemy):
        if self.attackTarget:
            if self.attackTarget == enemy:
                if self.attackCount:
                    return 1
        return 0
    
    def tick(self,delta):     
        self.y_speed = 0
        if(globalPlayer!=None):
#              if arcadeMode:
#                  print "fairy running",self.x,self.y
              if self.attackTarget:
                  if self.attackTarget.x+self.attackTarget.width < cameraX-1 or self.attackTarget.x > cameraX+801:
                      self.attackTarget = None
              if self.x < cameraX-200:
                  self.x = cameraX -200
              if self.x > cameraX + 1000:
                  self.x = cameraX + 1000
              if self.attackTarget== None:
                  distanceInFront = 220
                  distanceAbove = 70
                  self.attackCount = 0
                  if comboLevel == 0:
                      deltaX = cameraX-200- self.x
                      deltaY = 300 - self.y
                  else:
                      self.checkTarget(delta)
                      self.checkCoin(delta)
                      distanceInFront = 180* (math.sin(-self.life/110.0))
                      distanceAbove = 180* (math.cos(-self.life/110.0))
                      deltaX = (globalPlayer.x+distanceInFront) - self.x
                      deltaY = (globalPlayer.y+distanceAbove) - self.y
                  distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
                  if distance == 0:
                      deltaX = 0
                      deltaY = 0
                  else:
                      deltaX = deltaX/distance
                      deltaY = deltaY/distance
                  if deltaX < 0:
                      self.facing = 1
                  else:
                      self.facing = -1
                  self.speed = (distance-20)/30
                  if self.speed>15:
                      self.speed = 15
                  if(distance>10):
                      self.x += deltaX*self.speed
                      self.y += deltaY*self.speed
              else:
                  deltaX = (self.attackTarget.x+self.attackTarget.width/2) - (self.x+self.width/2)
                  deltaY = (self.attackTarget.y+self.attackTarget.height/2) - (self.y+self.height/2)
                  distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
                  if distance > 0:
                      deltaX = deltaX/distance
                      deltaY = deltaY/distance
                  else:
                      deltaX = 0
                      deltaY = 0
                  if deltaX < 0:
                      self.facing = 1
                  else:
                      self.facing = -1
                  self.speed = (distance+200)/40
                  if self.speed>25:
                      self.speed = 25
                  self.x += deltaX*self.speed
                  self.y += deltaY*self.speed
                  if distance < 20:
                      self.facing = -1
                      self.attackCount +=1
                      attackComplete = 35
                      if self.attackCount > attackComplete:
                          self.attackTarget.hit(1000)
                          self.attackTarget = None
                      elif distance < 10:
                          self.x = (self.attackTarget.x+self.attackTarget.width/2) - (self.width/2)
                          self.y = (self.attackTarget.y+self.attackTarget.height/2) - (self.height/2)
                  else:
                      self.attackCount = 0
                  if distance > maxDistanceToPlayer + 100:
                      self.attackTarget = None
                      
              particle = fairyRedTrailParticle()
              x = self.x-cameraX
              y = self.y + 54-cameraY
              if(self.facing<0):
                  x += 80
              else:
                  x += 0
              if self.attackCount==0:
                  #particleController.addItem(particle,cameraX+x,y,0.3,0,0)
                  makeSparkleParticle(cameraX+x,y,0,0,2)
              if self.attackCount>0 and self.attackTarget:
                  x = self.attackTarget.x+self.attackTarget.width/2
                  y = self.attackTarget.y+self.attackTarget.height/2
                  makeAttackParticle(x,y,0,0,2,self.attackTarget.width/2.0,self.attackTarget.height/3.0)     
                 
        tempY = self.y
        physicsObject.tick(self,delta)
        self.y = tempY
        
    def checkCoin(self,delta):
        right = self.x+(self.width*self.scale)-15
        left = self.x+15
        top = self.y+15
        bottom = self.y + (self.height * self.scale)-15
        for object in objects:
            if right >object.x and left < object.x + object.width:
              if bottom >object.y and top < object.y + object.height:        
                  object.isCollected()
    
    def checkTarget(self,delta):

        deltaX = globalPlayer.x - self.x
        deltaY = globalPlayer.y - self.y
        distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
        if distance > maxDistanceToPlayer:
            return
        fairyAttackDistance = 250
        if self.checkIndex >= len(objects):
            self.checkIndex = 0 
        nextTarget = objects[self.checkIndex]
        if nextTarget != globalPlayer and nextTarget != globalFairy and nextTarget.hitPoints and nextTarget.killed==0:
            if nextTarget.x+nextTarget.width > cameraX and nextTarget.x < cameraX + x_max:
                if nextTarget.y+nextTarget.height > cameraY and nextTarget.y< cameraY+y_max:
                    deltaX = nextTarget.x - self.x
                    deltaY = nextTarget.y - self.y        
                    distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))    
                    if distance < fairyAttackDistance:
                        if nextTarget.name != "RWasp":
                            self.attackTarget = nextTarget
                        else:
                            if nextTarget.waspActive:
                                self.attackTarget = nextTarget
        self.checkIndex += 1       
    
    def render(self):
        self.scale = 0.75
        lightRes = JPG_Resources["gradedCircle100"]
        centreX = self.x+(self.width/2*self.scale)
        centreY = self.y+(self.height*self.scale)
        lightWidth = 200
        lightHeight = 200
        x = centreX- lightWidth/2
        y = centreY - lightHeight/2
        PC.setColourize(1)
        if self.attackCount:
            alpha = 200
            red = 200
            alpha += 55 * math.sin(self.attackCount)
            red += 55 * math.sin(self.attackCount)
            PC.drawmodeAdd()
            PC.setColour(int(red),34,34,int(alpha))
            PC.drawImageScaled(lightRes,x-cameraX,y-cameraY,lightWidth,lightHeight)
            PC.drawmodeNormal()
        else:
            PC.setColour(130,255,100,100)
            PC.drawImageScaled(lightRes,x-cameraX,y-cameraY,lightWidth,lightHeight)
        PC.setColourize(0)
        WorldObject.render(self)
        
def launchFairy():
    global globalFairy
#    print "launching fairy",x,y
    x = cameraX - 200
    y = 300
#    if arcadeMode:
#        print "launching fairy",x,y
    type = WorldTypes.Fairy
    object = addObject(nextID,x,y,type)
    globalFairy = object

    
        
class fireBall(enemy):
    name = 'fireBall'
    graphic = 'KillerOrange1'
    max_y_speed = 0.8
    fire_y_speed = 0.8
    max_x_speed = 0.8
    fire_x_speed = 0.8
    x_direction = 1
    y_direction = 1
    acceleration = 0.012
    x_max_distance = 1000
    hitPoints = 0
    attackCount = 0
    solid = 0
    initial_x = 300     #only used for CS
    worth = 1000
    firstSeen = 1
    #animation = animationSets.KillerOrange_move
    def render(self):
        if inEditor:
           enemy.render(self)
        else:     
            lightRes = JPG_Resources["gradedCircle100"]
            centreX = self.x+self.width/2
            centreY = self.y+self.height/2
            lightWidth = 200
            lightHeight = 200
            x = centreX- lightWidth/2
            y = centreY - lightHeight/2
            PC.setColourize(1)
            if self.attackCount:
                alpha = 120
                blue = 180
                alpha += 120 * math.sin(self.attackCount)
                blue += 75 * math.sin(self.attackCount)
                PC.drawmodeAdd()
                PC.setColour(34,34,int(blue),int(alpha))
                PC.drawImageScaled(lightRes,x-cameraX,y-cameraY,lightWidth,lightHeight)
                PC.drawmodeNormal()
            else:
                PC.setColour(130,130,255,140)
                PC.drawImageScaled(lightRes,x-cameraX,y-cameraY,lightWidth,lightHeight)
            PC.setColourize(0)   

        if self.killed:
            PC.setColour( 60,200,0,256,)
            PC.setFont( font36 )
            string = str(self.worth)
            x = self.x+(self.width/2)-cameraX-10
            PC.drawString(string, x, self.y+60-cameraY )
           
    def spawn(self):
        self.initial_x = self.x
        self.x_direction = 1
        self.x_speed = 0
        
    def tick(self,delta):
        if self.x < cameraX+760 and self.firstSeen:
            self.ghostSound()
            self.firstSeen = 0
        if smartBomb.active():
            enemy.hit(self,1000)
        if self.killed:
            self.x_speed = self.deltaX * self.speed
            self.y_speed = self.deltaY * self.speed
           # print "enemydead",self.name,self.x_speed,self.y_speed,self.y
            self.x += self.x_speed
            self.y += self.y_speed
            self.speed += 0.2  
            self.deathTimer += delta
            if(self.y<20 and self.x>cameraX-100):
                scoreWithIcon(self.x,self.y,self.worth)
                #crittersCollected += 1
                self.x = -600
        else:
            deltaX = self.initial_x - self.x
            if deltaX < 0:
                deltaX *= -1
            if deltaX > self.x_max_distance:
                self.x = -300
            self.rotated = self.fire_x_speed/-6.0
            tempY = self.y 
            tempX = self.x
            enemy.tick(self,delta)       #tick the parent class  
            self.x=tempX + self.fire_x_speed*delta
            if finishOn==0:
                self.x += scrollManager.getScrollSpeed(delta)
            self.y = tempY+ self.fire_y_speed*delta
            makeGhostParticle(self.x+self.width/2,self.y+self.height/2,0,0,2,15)    
            #print "ghost",self.x,cameraX,x_max
            #print "ghost print",self.fire_x_speed
            if self.x < cameraX+80 and self.x_direction == -1:
                self.ghostSound()
                self.x_direction = 1
               # print "changing direction",self.x,cameraX
            if self.x+self.width > cameraX+x_max-80 and self.x_direction == 1:
                self.x_direction = -1
                self.ghostSound()
              #  print "changing direction",self.x,cameraX
            if self.x_direction == 1:
                if self.fire_x_speed < self.max_x_speed:
                    self.fire_x_speed += delta *self.acceleration
            if self.x_direction == -1:
                if self.fire_x_speed >  - self.max_x_speed: 
                    self.fire_x_speed -= delta *self.acceleration        
            
            if self.y < cameraY+80 and self.y_direction == -1:
                self.y_direction = 1
                self.ghostSound()
            if self.y+self.height > cameraY+y_max-80 and self.y_direction == 1:
                self.y_direction = -1
                self.ghostSound()
            if self.y_direction == 1:
                if self.fire_y_speed < self.max_y_speed:
                    self.fire_y_speed += delta *self.acceleration
            if self.y_direction == -1:
                if self.fire_y_speed >  - self.max_y_speed: 
                    self.fire_y_speed -= delta *self.acceleration  
                    
    def ghostSound(self):
        playSimpleSoundList(["ghost1","ghost2","ghost3"],panning =self.thisPanning, volume = self.thisVolume)
                    
    def hit(self,points):
        return 0

waspSoundDelay = 0
                
class Wasp(enemy):
    hitPoints = 1
    solid = 0
    name = 'Wasp'
    graphic = 'Wasp01'
    target_x_speed = 0
    target_y_speed = 0
    facing = 1
    x_acceleration = 0.05
    current_y_speed = 0.5
    hitLastFrame = 0
    animation = animationSets.wasp_move
    worth = 200
    collisionWidth = 0.5
    collisionHeight = 0.4
    global objects
    def tick(self,delta):
        global waspSoundDelay
        if self.x+100>cameraX and self.x < cameraX+810:
            if waspSoundDelay<=0:
                #playSimpleSound ("wasp5")    
                waspSoundDelay= 25
        self.rotated = self.x_speed/-6.0
        tempY = self.y 
        tempYS = self.y_speed
        enemy.tick(self,delta)       #tick the parent class  
        if(self.killed==0):
            if self.y <= 20:
                self.current_y_speed = 1.0
                self.target_y_speed = self.current_y_speed
            if self.y >= 450:
                self.current_y_speed = -1.0
                self.target_y_speed = self.current_y_speed
            self.y = tempY
            self.y_speed = tempYS
            if(self.y_speed > self.target_y_speed):
                self.y_speed -= 0.005
            elif(self.y_speed < self.target_y_speed):
                self.y_speed += 0.005
            for thisObject in self.collisionObjects: 
                if(thisObject != globalPlayer):
                    if self.hitLastFrame == 0:
                        self.hitLastFrame = 1
                        self.current_y_speed *= -1
                    self.x_speed = 0
                    self.target_y_speed = self.current_y_speed
                    self.target_x_speed = 0 
            if(len(self.collisionObjects)==0):
                self.hitLastFrame = 0  
                if(self.x<cameraX+750):
                    self.target_x_speed = -2
                    self.target_y_speed = 0
                else:
                    self.target_y_speed = self.current_y_speed/100
            self.y += self.y_speed*delta
            self.x += self.x_speed*delta
        
class RWasp(Wasp):
    facing = 1
    waspActive = 0
    name = "RWasp"
    animation = animationSets.Rwasp_move
    x_acceleration = -0.05
    
    def tick(self,delta):
        if self.x + self.width < cameraX:
            self.x += 2.0
            self.waspActive = 1
        if self.waspActive:
            Wasp.tick(self,delta)
            if self.x > cameraX+1200:
                self.x = cameraX-1000
                self.x_speed = 0
    def render(self):
        if self.waspActive or inEditor:
            Wasp.render(self)

class Bat(enemy):
    solid = 0
    target_x_speed = 0
    target_y_speed = 0
    facing = 1
    x_acceleration = 0.01
    centreX = 0
    centreY = 0
    rotation = 0
    currentDistance = 150
    patrolRotationSpeed = .005
    rotationSpeed = .0075
    attackDistance = 150
    attackSpeed = 1.0
    worth = 250
    attackDelta = 0.4
    
    def spawn(self):
        self.centreX = self.x
        self.centreY = self.y
        return 0
        
    def tick(self,delta):
        self.rotation += delta*self.rotationSpeed
        tempY = self.y 
        tempYS = self.y_speed
        enemy.tick(self,delta)       #tick the parent class  
        self.y_speed = 0
        if(self.killed==0):
            oldX = self.x
            oldY = self.y
            self.x = self.centreX + (math.sin(self.rotation)*self.currentDistance)
            self.y = self.centreY + (math.cos(self.rotation)*self.currentDistance) 
            if(self.x>oldX):
                self.facing = -1
            else:
                self.facing = 1

class BigBat(Bat):
    name = 'BigBat'
    graphic = 'BigBat01'
    animation = animationSets.bigBat_move
    moveAnimation = animationSets.bigBat_move
    attackAnimation = animationSets.bigBat_attack
    hitPoints = 2
    killReplacement = WorldTypes.SmallBat
    rotationSpeed = 0
    patrolRotationSpeed = 0
    attackSpeed = 1.6
    worth = 500
        
    def tick(self,delta):
        Bat.tick(self,delta)
        if self.killed == 0:
            self.tryAttackPlayer(delta)
        
    def tryAttackPlayer(self,delta):
        if globalPlayer != None:
            deltaX = self.x-globalPlayer.x
            deltaY = self.y-globalPlayer.y
            distancePlayer = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
            if distancePlayer<self.attackDistance:
                unitX = deltaX/distancePlayer
                unitY= deltaY/distancePlayer
                attackVectorX = unitX*self.attackSpeed*delta
                attackVectorY = unitY*self.attackSpeed*delta 
                self.centreX -= attackVectorX  
                self.centreY -= attackVectorY 
                self.rotationSpeed = 0
                if self.animation != self.attackAnimation:
                    playSimpleSound ("bigBatAlert",volume = self.thisVolume,panning = self.thisPanning) 
                self.animation = self.attackAnimation
                self.patrolRotationSpeed = .005
                if self.frameNumber>1: #tony = horrible hack
                    self.frameNumber = 0
            else:
                self.rotationSpeed = self.patrolRotationSpeed
                self.animation = self.moveAnimation
                
    def setUpReplacment(self):
        index = addObject(nextID,self.x,self.y+20,self.killReplacement)
        index.centreX = self.x - self.currentDistance+10
        index.rotation = 0.5 * (22.0/7.0)
        index.centreY = self.y+20
        index.attackDelay = replacementAttackDelay
        index = addObject(nextID,self.x,self.y+20,self.killReplacement)
        index.centreX = self.x + self.currentDistance-10
        index.centreY = self.y+20   
        index.rotation = 1.5 *(22.0/7.0)
        index.attackDelay = replacementAttackDelay
        
class SmallBat(Bat):
    hitPoints = 1
    solid = 0
    name = 'SmallBat'
    graphic = 'SmallBat01'
    animation = animationSets.smallBat_move
    moveAnimation = animationSets.smallBat_move
    attackAnimation = animationSets.smallBat_attack
    worth = 100
    rotationSpeed = .0075
    currentDistance = 120

#not used anymore
class Web(physicsObject):
    placeable = 0   #set to 0 if not placeale
    name = 'Web'
    graphic = 'Web'
    solid = 0
    maximum_y_speed = 0
    length = 0 #special variable used to control length of web
    def render(self):
        PC.setClipRect(0,0,800,self.y+self.length)
        WorldObject.render(self)
        PC.clearClipRect()

class PlayerGhostUp(WorldObject):
    z = 45      #in front of player
    placeable = 0   #set to 0 if not placeale
    name = 'ghostUp' 
    graphic = 'player_walk_01'
    speed = 8
    solid = 0
    def tick(self,delta):
        if(globalPlayer!=None):
            deltaX = globalPlayer.x - self.x
            deltaY = globalPlayer.y - self.y
            distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
            deltaX = deltaX/distance
            deltaY = deltaY/distance
            self.x += deltaX*self.speed
            self.y += deltaY*self.speed 
            if deltaX<0:
                self.facing = -1
            else:
                self.facing = 1
            if(distance<20):
                global comboLevel
                comboLevel += 1
                self.x = -500
 
    def render(self):
        PC.drawmodeAdd()
        PC.setColourize(1)
        PC.setColour( 255, 255, 255, 96 )
        frame = JPG_Resources[self.graphic]
        width = PCR.imageWidth(frame)
        height = PCR.imageHeight(frame)
        x = self.x-cameraX
        if self.facing <0:
            x += width
        PC.drawImageScaled(frame, x, self.y-cameraY,width*self.facing,height)
        PC.drawmodeNormal()
        PC.setColourize(0)
        
def decComboLevel(inc):
    global comboLevel
    if cheatCanvas.AllPowerOn == 0:  
        comboLevel -= inc
        if(globalPlayer!=None):
            type = WorldTypes.PlayerGhostDown 
            addObject(nextID,globalPlayer.x,globalPlayer.y,type)

                
def removeAllCombo():
    global comboLevel
    if cheatCanvas.AllPowerOn == 0:  
       # print "removing combo"
        if(globalPlayer!=None):
            for count in range(comboLevel):
                type = WorldTypes.PlayerGhostDown 
                ghost  = addObject(nextID,globalPlayer.x,globalPlayer.y,type)
                ghost.y_speed += count
                if count % 2:
                    ghost.x_speed = -(count-1)/4.0
                else:
                    ghost.x_speed = (count-1)/4.0
        comboLevel = 0
    
class PlayerGhostDown(PlayerGhostUp):
    placeable = 0   #set to 0 if not placeale
    name = 'ghostDown' 
    graphic = 'player_walk_01'
    y_speed = 2
    solid = 0
    def tick(self,delta):
        self.y -= self.y_speed
        self.speed+=0.3
        self.x += self.x_speed
        if(self.y < -100):
            self.x = -300

tryForSmash = 0
startJumpTimer = 16
endJumpTimer = 6
maxDashSpeed = 10
maxDashTap = 20        #how long player has for double tap on dash
maxDashTime = 50        #Maximum time we can dash for
dashJumpImpulse = -5
hack = 2
oldX = 0 

class Player(physicsObject):
    onTrampoline = 0
    smashSelected = 0
    dashSelected = 0
    z = 50
    numberGhosts = 6
    tickDelay = 0
    placeable = 0   #set to 0 if not placeale
    name = 'player'
    baseFriction = 2
    graphic = 'player_walk_01'
    animation = animationSets.player_walk
    solid =0
    invulnerable = 0
    painCount=0
    scale = 1
    targetScale = 1
    colourize = 1
    needToRestartLevel = 0
    jumptimer = 0
    stunJump = 0
    jumpedFrom = None   #This is the platform the player jumped from
    hangMode = 0
    hangTakeOffSpeedX = 1.5
    dashSpeed = 0             #speed at which we dash
    dashTapTimer = 0
    dashSpeedTimer = 0
    dashMode = 0
    dashBegun = 0     #set so we know when to put in an up impulse
    oldYSpeed = 0

    moveTargetX = 50
    simulation = 1
    destinationX = 0
    doingJump = 0
    tableEnd = 0
    jumpTimer = 0
    deltaScale = 1
    platformOffset = 0
    jumpRange = 0
    hangTarget = 0      #this flag tells us if the target is a hang target or not
    smashSpeed = -9.5
    #jumpSpeed = -6     #commented this out on the 8th August
    trampolineTargetLocal=0
    trampolineTarget=None
    platformSmashed = None
    clickType = 0
    doingHangDrop = 0
    doingSmash = 0
    tempmoveTargetObject = None
    moveSpeedScale = 1.0
    thisTargetJump = 0
    getOntoPlatformCount = 0
    doingGetOntoPlatform = 0
    preHangDropY = 0

    def tick(self,delta): 
        self.showGhost -= delta #this is used to activate the ghost trail
        if self.showGhost<0:
            self.showGhost = 0
        global globalPlayer
       # global cameraX
       # cameraX = self.x - 400
        self.jumptimer -=delta

        self.oldYSpeed = self.y_speed
        if FinishFlag:
            self.x += delta*1.5
            WorldObject.tick(self,delta)
            self.facing = 1
            return
        if self.jumptimer<0:
            self.jumptimer = 0
        globalPlayer = self
        if tilesOver*riskIncrement>maximumRisk:
            global lives
            global comboLevel
            global bombExplosion
            global delayRefill
            global gridFillHeight
            global targetGridFillHeight
            global cameraX
            comboLevel = 0
            self.invulnerable = 0
            self.painCount = 0
            self.deathTimer = 0
            self.Death(delta)
            if bombExplosion == 0:
                startGridExplosion()
            bombExplosion = 1
            if lives <=0:
                delayRefill = 1
                self.needToRestartLevel = 1 #force level to restart
            detonateGrid()
            #self.needToRestartLevel = 1 #force level to restart
            gridFillHeight=0
            targetGridFillHeight=0

        self.attacktimer -= delta
        if self.attacktimer <0:
            self.attacktimer =0
        self.targetScale = 1+(math.sqrt(comboLevel)*comboScale)
        if(self.deathTimer):
            self.playerDead(delta)
            if(self.y < (y_max - self.height+cameraY) ):
                if(self.simulation):
                    physicsObject.tick(self,delta)       #tick the parent class
                else:
                    WorldObject.tick(self.delta)
            if(self.x < gridRight + cameraX):
                self.x = gridRight + cameraX
            if(self.x+self.width>gridLeft+cameraX):
                self.x = gridLeft+cameraX-self.width
            return
        else:
            if(self.invulnerable>0):
                self.invulnerable -= delta
                #now tint the player
                tintCount = self.invulnerable%32
                if(tintCount>16):
                    tintCount =32-tintCount
                self.tintg=0+(tintCount*16)
                self.tintb=0+(tintCount*16)
            elif(self.dashSpeedTimer>0):
                self.tintr=255-self.dashSpeedTimer*4 
                self.tintg=255
                self.tintb=255-self.dashSpeedTimer*4              
            else:
                self.tintr=255
                self.tintg=255 
                self.tintb=255                
                self.invulnerable = 0
        self.res = JPG_Resources[self.graphic]
        self.painCount+=1
        if(self.painCount>8):
            self.painCount =8
        if(0==0):
            scrollManager.setADSpeed(self.x,delta) #tony - disabled Adaptive changing of scroll speed
            if profiles[currentProfile].mouseControl:
                self.getMouseControl(delta)
            else:
                self.getKeyBoardControl(delta)   
            if(self.x < gridRight + cameraX):
                self.x = gridRight + cameraX
                if self.PlatformOn == None:
                    self.hangMode = 0
                elif self.x+40>self.PlatformOn.x+self.PlatformOn.width:
                    self.hangMode = 0       #always cancel hangmode if pushed of edge of screen

            rightDelta = (self.x+(self.width*self.scale)) -(cameraX + gridLeft)
            if rightDelta > 0 :
                cameraX += math.sqrt(rightDelta)
            if(self.x < x_min + cameraX):
                self.x = x_min + cameraX  
            
            if(self.hangMode ==1):
                #note we don't run physics when hanging
                if(self.PlatformOn != None):
                    self.PlatformOn.stoodOn()
                    self.base_speed = self.PlatformOn.x_speed
                    self.x_speed = self.base_speed
                    self.y_speed = self.PlatformOn.y_speed
                    self.x += self.x_speed*delta
                    self.y += self.y_speed*delta
                else:
                    self.hangMode = 0
                WorldObject.tick(self,delta)
            else:
                if(self.doingJump==0):  #don't tick physics if in jump mode (canned)
                    physicsObject.tick(self,delta)       #tick the parent class
                else:
                   # physicsObject.tick(self,delta)
                    temp = self.PlatformOn 
                    self.doCollision(delta)
                    self.PlatformOn  = temp
                    WorldObject.tick(self,delta)                  
            for thisObject in self.collisionObjects:  
                thisObject.isCollected()
            if(self.onGround and self.PlatformOn): #might be the floor
                self.PlatformOn.stoodOn()


    def getcollisionList(self):
        return objects
        
    def findInCollisionObjects(self,platform):
        for thisPlat in self.collisionObjects:
            if thisPlat == platform:
                return 1
            else:
                return 0
          
    def getMouseControl(self,delta):
        global globalOldPlatformOn
        #don't let the player go beyond the finish platform
       # oldX = self.x

#        if self.moveTargetObject:
#            setglobalDebug1(self.moveTargetObject.x)
        #setglobalDebug1(0)        
        if checkKeyNoRepeat(keyMap.dashKey.keyValue) and dashEnabled:
            globalOldPlatformOn = globalPlayer.PlatformOn
            globalPlayer.dashSelected = 1
            
        if  checkKeyNoRepeat(keyMap.smashKey.keyValue) and smashEnabled:
            globalOldPlatformOn = globalPlayer.PlatformOn
            globalPlayer.smashSelected = 1

        if self.x +(self.width*self.scale)> finishPlaformRight: 
            self.x = finishPlaformRight - (self.width*self.scale)
            self.target_x_speed = 0
            self.x_speed = 0
            self.dashMode = 0
            self.dashSpeedTimer = 0
        if dashEnabled:
            self.moveSpeedScale = 1.1
        else:
            self.moveSpeedScale = 0.85
        centreX = (self.x+(self.width/2 * self.scale))
        bottomy = self.y + self.height
        getOntoPlatform = 0
        if self.getOntoPlatformCount>0:
            self.getOntoPlatformCount-= delta
            if self.getOntoPlatformCount<=0:
                self.getOntoPlatformCount = 0
                getOntoPlatform = 1
        if getOntoPlatform:
            if self.PlatformOn != None:
                self.moveTargetObject = self.PlatformOn
                if self.doingJump == 0: 
                    self.setUpMouseHangJump(delta,centreX,self.PlatformOn)
                    self.doingGetOntoPlatform = 1
            self.getOntoPlatformCount = 0
           # self.PlatformOn = None
        elif self.doingHangDrop:
            self.doHangDrop(delta,centreX,self.moveTargetObject)
        elif(self.onTrampoline):
            if(self.doingJump == 0):
                #On trampoline Ready to start new bounce
                if(self.trampolineTarget ==None):
                    #CONTINUE TO BOUNCE ON THIS TRAMPOLINE
                    self.trampolineTargetLocal = self.PlatformOn
                else:
                    self.trampolineTargetLocal = self.trampolineTarget                    
                self.setUpMouseJump(delta,centreX,self.trampolineTargetLocal)
                #self.moveTargetObject = None
                self.trampolineTarget = None
            else:
                self.doingMouseJump(delta,centreX,self.trampolineTargetLocal)
        elif(self.dashMode):
            self.dashBegun = 0                     
            self.x_speed = self.dashSpeed
            self.dashSpeedTimer -= delta
            if(self.dashSpeedTimer <0):
                self.dashSpeedTimer = 0
                self.dashMode = 0
                self.target_x_speed = 0
                self.doingJump = 0
                self.invulnerable= 100
        
        elif self.doingSmash:
            if self.y_speed>-0.5:
                self.doingSmash = 0
                self.invulnerable= 100
        elif self.smashSelected:
            self.smashSelected = 0
            if smashEnabled:
                if globalOldPlatformOn:
                    self.doingSmash = 1
                    self.platformSmashed = globalOldPlatformOn
                    globalOldPlatformOn.isSmash()
                    self.y_speed = self.smashSpeed*(1+((self.scale-1)*.4))
                    self.PlatformOn = None
                    self.onGround = 0
                    self.showGhost = 30
                    self.moveTargetObject = None
                    self.x_speed = 0
                    self.target_x_speed = 0
                    self.doingJump = 0
                    #if(comboLevel>0):
                    #    decComboLevel(1)
                    thisPanning = (self.x-cameraX-400)/100
                    playSimpleSound("smash",panning =thisPanning)
                
        elif self.dashSelected:
            self.dashSelected = 0
            if dashEnabled and self.PlatformOn:
                if self.hangMode:
                    self.y -= 150
                elif self.doingHangDrop:
                    self.y = self.preHangDropY
                self.y_speed = dashJumpImpulse
                self.moveTargetObject = None
                self.PlatformOn = None
                self.hangTarget = 0
                self.onGround = 0
                self.showGhost = 40
                self.dashMode = 1
                self.facing = 1
                self.doingJump = 0
                self.dashSpeed = maxDashSpeed * self.facing
                self.dashSpeedTimer = 30
                self.hangMode = 0
                thisPanning = (self.x-cameraX)/100
                playSimpleSound("dash",panning =thisPanning)
        elif self.moveTargetObject:
            #setglobalDebug1(1)
            if self.moveTargetObject == self.PlatformOn:
                #setglobalDebug1(1)
                if self.thisTargetJump ==0:
                    self.setUpSamePlatformJump(delta,centreX,self.moveTargetObject)
                    self.thisTargetJump =1
                elif self.thisTargetJump ==1:
                    self.doingMouseJump(delta,centreX,self.moveTargetObject)
                elif self.moveTargetObject.x+self.moveTargetObject.width<cameraX or self.moveTargetObject.x > cameraX+gridLeft:
                    self.moveTargetObject = None
                elif self.hangMode and self.clickType == 0:
                    self.setUpMouseHangJump(delta,centreX,self.moveTargetObject)
                elif self.hangMode==0 and self.clickType == 1 and hangEnabled:
                    self.setUpMouseDropHang(delta,centreX,self.moveTargetObject)
                    self.preHangDropY = self.y
                else:
                  #  setglobalDebug1(self.moveTargetX)
                    self.doingWalk(delta,centreX)
            else:
                if(self.doingJump):
                 #   oldX = self.x
                    self.doingMouseJump(delta,centreX,self.moveTargetObject)
                  #  print "mouseControl",int(self.x-oldX)
                else:
                    self.setUpMouseJump(delta,centreX,self.moveTargetObject)
        else:
            if self.facing < 0:
                #8 is a constant wich makes Jake turn slightly sooner
                if mousex+cameraX > self.x + (self.width*self.scale)-8:
                    self.facing = 1
            else:
                if mousex+cameraX < self.x+8:
                    self.facing = -1
#        print "mouseControl",int(self.x-oldX)
                
    def doingWalk(self,delta,centreX):
        self.getOntoPlatformCount = 0
        moveTargetX = self.moveTargetX+self.moveTargetObject.x
        deltaX = moveTargetX - centreX
        maxSpeed = 1+(self.scale*2)
        maxSpeed *= self.moveSpeedScale
        if deltaX > 0 :
            if deltaX>3:
                self.facing = 1
                self.target_x_speed = deltaX/8
                if(self.target_x_speed>maxSpeed):
                    self.target_x_speed = maxSpeed
            else:
                self.x = moveTargetX - (self.width/2*self.scale)                    
                self.moveTargetObject = None
                self.target_x_speed = 0
                self.x_speed = 0
        else:
            if deltaX < -3:
                self.facing = -1
               # print("target_x_speed",self.target_x_speed)
                self.target_x_speed = deltaX/8
                if(self.target_x_speed<-1*maxSpeed):
                    self.target_x_speed = -1*maxSpeed
            else:
                self.x = moveTargetX  - (self.width/2* self.scale)                  
                self.moveTargetObject = None
                self.target_x_speed = 0  
                self.x_speed = 0                 
    
    def doingMouseJump(self,delta,centreX,moveTargetObject):
        self.getOntoPlatformCount = 0
      #called if a jump has already been startedt
        self.destinationY = moveTargetObject.y - self.height
        if(self.hangTarget==1 or  (self.clickType == 1 and hangEnabled)):
            self.destinationY += (hangSpriteHeight *self.scale)       
        speed = 3.0
        velocityX = delta*speed                    
        if(self.x<=cameraX):        #if we are at edge of screen clip
            self.x = cameraX
        elif(self.x+self.width>=cameraX+gridLeft):
            self.x = cameraX+gridLeft-self.width
            table = 0
        oldY = self.y
        self.y = self.deltaY+self.destinationY-getTableValueSimple(int(self.jumpTimer),self.jumpLookUp,self.jumpRange,0)+4
  #      print "doingMouse Jump",moveTargetObject.x,self.platformOffset,self.deltaX,self.jumpTimer
        self.x = moveTargetObject.x+ self.platformOffset -self.deltaX
        self.x+= (self.jumpTimer)*self.deltaScale
        self.x_speed =(self.jumpTimer)*0.02 #for animation 
        sound_y_speed = self.y-oldY
        timerDelta  = delta*self.jumpSpeed*-1
        timerDelta *= self.moveSpeedScale
        self.jumpTimer += timerDelta
        if(self.jumpTimer > self.tableEnd):
            if moveTargetObject.inAttackRange:
                #print("in attack range")
                self.attacktimer=20
            if  moveTargetObject.hitPoints:
                self.moveTargetObject = None
            self.doingGetOntoPlatform  = 0
            self.x = moveTargetObject.x+ self.platformOffset
            self.y = self.destinationY
            self.doingJump = 0
            self.onGround = 1
            #self.controlAnimation(delta)
            self.x_speed = 0
            self.thisTargetJump = 2
            self.onTrampoline = 0
            self.makeOnGroundSound(sound_y_speed/8.0)
            if self.hangTarget and self.clickType == 0:
                self.getOntoPlatformCount = 10 #was 10
            if hangEnabled and (self.hangTarget or (self.clickType == 1 and sound_y_speed) ):
                self.moveTargetObject = None
                self.hangMode = 1
                self.onGround = 0
                self.PlatformOn = moveTargetObject
                self.base_speed = moveTargetObject.x_speed
                self.x_speed = self.base_speed #note that we don't run physics on the player whilst hanging
                self.y_speed = moveTargetObject.y_speed
                #force Jake into the correct position in the Y (always 10 from top of platform)
                topJake = moveTargetObject.y-15
                topJake = topJake + ((self.height+30)* self.scale) - self.height
                self.y = topJake
                #need to make a compensation for the hanging animation being off centre
                if(centreX > moveTargetObject.x+moveTargetObject.width-30):
                    self.x = moveTargetObject.x+moveTargetObject.width-30-(self.width/2*self.scale)                
            elif self.moveTargetObject:
                if self.moveTargetObject.x+self.moveTargetObject.width<cameraX or self.moveTargetObject.x > cameraX+gridLeft:
                    self.moveTargetObject = None
                elif self.moveTargetObject.y_speed>0:  #tony - nasty hack
                    self.y_speed = 2  #we need a downward speed to garantee hitting the platform                
    def setUpMouseHangJump(self,delta,centreX,moveTargetObject):

        self.getOntoPlatformCount = 0
        self.hangTarget = 0
      #called when player selects another platform so a jump has to be initiallised
        #clear speed
        self.hangMode =0  
        self.onGround = 0
        self.x_speed = 0      
        self.target_x_speed = 0
        self.y_speed = 0
        self.deltaX = 0
        self.deltaY = (160*self.scale) - 80
        self.doingJump = 1
        self.platformOffset = self.x- self.moveTargetObject.x
        self.jumpRange = 0
        self.jumpTimer = 0
        self.tableEnd = findMaxY(findJumpLookUp(1))#always do the maximum jump when jumping onto the platform
        self.deltaScale = 0
        self.PlatformOn = None
        self.jumpLookUp = findJumpLookUp(1)

        
    def setUpMouseDropHang(self,delta,centreX,moveTargetObject):  
        self.getOntoPlatformCount=0
        self.hangTarget = 0
      #called when player selects another platform so a jump has to be initiallised
        #clear speed
        self.hangMode =0  
        self.onGround = 0
        self.x_speed = 0      
        self.target_x_speed = 0
        self.y_speed = 0
        self.deltaX = 0
        self.deltaY = 80
        self.doingJump = 1
        self.platformOffset = self.x- self.moveTargetObject.x
        self.jumpRange = 0
        self.jumpTimer = 0
        self.tableEnd = findYinJumpTable(self.deltaY,findJumpLookUp(1),1)
        self.deltaScale = 0
        self.doingHangDrop = 10+(self.height*self.scale)
        self.moveTargetObject = self.PlatformOn
        self.PlatformOn = None  
        
    def doHangDrop(self,delta,centreX,moveTargetObject):
        dropSpeed = 5
        self.getOntoPlatformCount = 0
        self.doingHangDrop -= delta*dropSpeed
        if self.doingHangDrop<0:
            self.doingHangDrop = 0
            self.hangMode = 1
            self.onGround = 0
            self.doingJump = 0
            self.PlatformOn = moveTargetObject
            self.base_speed = moveTargetObject.x_speed
            self.x_speed = self.base_speed #note that we don't run physics on the player whilst hanging
            self.y_speed = moveTargetObject.y_speed
            #force Jake into the correct position in the Y (always 10 from top of platform)
            topJake = moveTargetObject.y-15
            topJake = topJake + ((self.height+30) * self.scale) - self.height
            self.y = topJake
            #need to make a compensation for the hanging animation being off centre
            if(centreX > moveTargetObject.x+moveTargetObject.width-30):
                self.x = moveTargetObject.x+moveTargetObject.width-30-(self.width/2*self.scale)  
            self.moveTargetObject = None  
            self.x = moveTargetObject.x+ self.platformOffset            
        else:
            self.y += delta*dropSpeed
            temp = 0 
        self.jumpLookUp = findJumpLookUp(1) 
        

    def setUpSamePlatformJump(self,delta,centreX,moveTargetObject):
        self.getOntoPlatformCount=0
        self.hangTarget = moveTargetObject.inHangRange
      #called when player selects another platform so a jump has to be initiallised
        #clear speed
        self.PlatformOn = None
        self.hangMode =0  
        self.onGround = 0
        self.x_speed = 0
        self.target_x_speed = 0
        self.y_speed = 0
        deltaX = centreX-(self.moveTargetX+self.moveTargetObject.x)
        maxJumpX = 200
        if deltaX>0:
            deltaX -= maxJumpX
            if deltaX <0:
                deltaX =0
        if deltaX<0:
            deltaX += maxJumpX
            if deltaX >0:
                deltaX =0
        self.platformOffset =  self.moveTargetX-(self.width/2*self.scale)+deltaX
        self.destinationX = self.platformOffset+self.moveTargetObject.x
        self.deltaX = self.destinationX - self.x    
        
        self.destinationY = moveTargetObject.y - self.height 
        self.deltaY = self.y-self.destinationY #negated cos table is
        self.doingJump = 1
        self.jumpRange = 0
        #now find the table range.
        self.tableEnd = findYinJumpTable(self.deltaY,findJumpLookUp(1),self.jumpRange)
        self.jumpTimer = 0
        if self.tableEnd==0:
        #    print ("error Self.tableEnd is zero deltaT,jumpRange",self.deltaY,self.jumpRange)
            self.tableEnd = 1 #tony = fudge just in case of an error
        self.deltaScale = self.deltaX/self.tableEnd     
        self.jumpLookUp = findJumpLookUp(1)   
        #print "delta X",self.deltaScale
        
    def setUpMouseJump(self,delta,centreX,moveTargetObject):
        self.getOntoPlatformCount=0
        self.hangTarget = moveTargetObject.inHangRange
      #called when player selects another platform so a jump has to be initiallised
        #clear speed
        #self.PlatformOn = None
        self.hangMode =0  
        self.onGround = 0
        self.x_speed = 0
        self.target_x_speed = 0
        self.y_speed = 0
        self.destinationY = moveTargetObject.y - self.height
        self.deltaY = self.y-self.destinationY #negated cos table is
#        if self.onTrampoline:
 #           self.moveTargetObject =self.PlatformOn
        self.PlatformOn = None
        if  moveTargetObject.isTrampoline:
            if moveTargetObject.jumpTableOffset==0:
                self.platformOffset = 75 - self.width/2
            elif moveTargetObject.jumpTableOffset==1:
                self.platformOffset = 55 - self.width/2    
            elif moveTargetObject.jumpTableOffset==2:
                self.platformOffset = 36 - self.width/2                 
        else:
            if(centreX < moveTargetObject.x ):
                    self.platformOffset = - (self.width/2*self.scale)
            elif(centreX > moveTargetObject.x + moveTargetObject.width):
                self.platformOffset = moveTargetObject.width-(self.width/2*self.scale)
            else:
                maxJumpX = 200 - (self.deltaY/2)
                #self.platformOffset = - moveTargetObject.x+self.x
                self.platformOffset = self.moveTargetX-(self.width/2*self.scale)
                deltaX = centreX-(self.platformOffset+moveTargetObject.x)
                if deltaX>0:
                    deltaX -= maxJumpX
                    if deltaX <0:
                        deltaX =0
                if deltaX<0:
                    deltaX += maxJumpX
                    if deltaX >0:
                        deltaX =0
                self.platformOffset +=deltaX
                #tony - need to put range limit in here!
        self.destinationX = moveTargetObject.x + self.platformOffset
       # self.destinationY = moveTargetObject.y - self.height 
        if self.hangTarget==1 or (self.clickType == 1 and hangEnabled):
            self.destinationY = moveTargetObject.y+10 - self.height + (self.height*self.scale)
            self.deltaY = self.y-self.destinationY #negated cos table is
            #self.destinationY = 0
            #print("hangSpriteHeight",hangSpriteHeight)         
        #clicking on platform other than the one we are standing on
        self.doingJump = 1
        #calculate the trajectory
        self.deltaX = self.destinationX - self.x
        if(self.deltaX <0):
            self.facing = -1
        else:
            self.facing = 1
        #find appropriate table:                  
       # self.deltaY = self.y-self.destinationY #negated cos table is
        self.jumpRange = 1
        testY = getTableValueSimple(int(self.deltaX),findJumpLookUp(1),self.jumpRange,1)
        if(testY<self.deltaY):
            self.jumpRange = .6
            testY = getTableValueSimple(int(self.deltaX),findJumpLookUp(1),self.jumpRange,1)
            if(testY<self.deltaY):
                self.jumpRange = .4
                testY = getTableValueSimple(int(self.deltaX),findJumpLookUp(1),self.jumpRange,1)
                if(testY<self.deltaY):
                    self.jumpRange = .2
                    testY = getTableValueSimple(int(self.deltaX),findJumpLookUp(1),self.jumpRange,1)
                    if(testY<self.deltaY):
                        self.jumpRange = 0
        if self.onTrampoline:
            self.jumpRange = 0
        #now find the table range.
        self.tableEnd = findYinJumpTable(self.deltaY,findJumpLookUp(1),self.jumpRange)
        self.jumpTimer = 0
        if self.tableEnd==0:
        #    print ("error Self.tableEnd is zero deltaT,jumpRange",self.deltaY,self.jumpRange)
            self.tableEnd = 1 #tony = fudge just in case of an error
        self.deltaScale = self.deltaX/self.tableEnd     
        self.jumpLookUp = findJumpLookUp(1)         
      
    def getKeyBoardControl(self,delta):
        self.dashTapTimer -= delta
        if(self.dashTapTimer <0):
            self.dashTapTimer = 0
        if(self.dashSpeedTimer>maxDashTime):
            self.dashSpeedTimer=maxDashTime

        #print("dash enabled",dashEnabled)
        if dashEnabled and self.onGround and (checkKeyNoRepeat(keyMap.leftKey.keyValue) or checkKeyNoRepeat(keyMap.rightKey.keyValue)):
            if self.dashMode:
                self.dashMode =0
            elif(self.dashTapTimer>0):
                self.dashMode = 1
                self.dashTapTimer = 0
            else:
                self.dashTapTimer = maxDashTap
        if checkKey(keyMap.leftKey.keyValue):
            self.facing = -1
            if(self.onGround):
                if(self.dashMode):
                    self.dashBegun = 1
                    self.dashSpeed = -maxDashSpeed
                    self.dashSpeedTimer += delta/2.0
                    self.target_x_speed = 0
                else:
                    self.target_x_speed = -1 * self.max_Xspeed
            else:
                self.base_speed -= delta/20.0 #added for better air control
                self.target_x_speed = 0 #added for better air control
                #old air control: self.target_x_speed = -.5 * self.max_Xspeed
        elif checkKey(keyMap.rightKey.keyValue):
            self.facing = +1
            if(self.onGround):  
                if(self.dashMode):
                    self.dashBegun = 1
                    self.dashSpeed = maxDashSpeed
                    self.dashSpeedTimer += delta/2.0
                    self.target_x_speed = 0
                else:  
                    self.target_x_speed = self.max_Xspeed
            else:
                self.base_speed += delta/40.0 #added for better air control
                self.target_x_speed = 0 #added for better air control
                #old air control: self.target_x_speed = .5 * self.max_Xspeed
        else:
            if(self.dashMode):
                if(self.dashBegun):
                    self.y_speed = dashJumpImpulse
                self.dashBegun = 0 
                #print("dash mode",self.dashTimer)                     
                self.x_speed = self.dashSpeed
                self.dashSpeedTimer -= delta
                self.showGhost = 30
                if(self.dashSpeedTimer <0):
                    self.dashSpeedTimer = 0
                    self.dashMode = 0
            else:
                self.target_x_speed = 0
                self.dashSpeedTimer = 0



        if(self.hangMode ==1):
         #see if player has released the hang key...               
            if checkKeyUp(keyMap.upKey.keyValue):
                #if they have then let go and give jake an impulse
                self.hangMode = 0
                if checkKey(keyMap.leftKey.keyValue):
                    self.base_speed = -self.hangTakeOffSpeedX
                if checkKey(keyMap.rightKey.keyValue):
                    self.base_speed = self.hangTakeOffSpeedX
                self.y_speed = (self.jumpSpeed-((self.scale-1)*1.5))*1.7
            else: 
                #if player is still hanging on check if platform is still valid
                self.checkForHangObject()
                if(self.hangMode == 0):
                    #if not then Jake just drops
                    self.y_speed = 0
                    self.x_speed = 0
                    self.base_speed = self.x_speed
                
        if checkKeyNoRepeat(keyMap.upKey.keyValue):
            if self.onGround==0:    #make sure we are not on the ground when grabbing
                self.checkForHangObject()
          
            if self.hangMode==0 and self.onGround or (self.stunJump and self.y_speed<0 and self.y_speed>-2.5):
                #self.dashMode = 0 #kill dash mode for now if we try to jump
                if self.dashBegun and speedEnabled:
                    self.y_speed = (self.jumpSpeed-((self.scale-1)*1.5))*self.dashSpeedTimer/15.0
                    self.showGhost = 30
                else:
                    self.dashMode = 0
                    self.dashSpeedTimer = 0
                    if(self.onGround):
                        self.stunJump = 0
                        self.jumpedFrom = self.PlatformOn  #keep a record ofr what we jumped of
                    self.jumptimer = startJumpTimer                    #tony - test particle system
                    #particleController.addItem(debris("platform100Wood"),self.x,self.y,1)
                    self.jumpSpeedKey = self.jumpSpeed-((self.scale-1)*1.5)
                    self.y_speed = self.jumpSpeedKey
                    self.base_speed = self.x_speed
                    self.onGround =0
                    if(self.stunJump==0):
                        #if stunJumpEnabled:
                        self.stunJump = 1
                    else:
                        self.stunJump= 0                    
            else:
                self.attacktimer = 20
                #hang mode

            if self.jumptimer>0 and self.jumptimer < startJumpTimer and smashEnabled:
                if self.jumpedFrom:
                    self.jumpedFrom.isSmash()
                    self.jumpedFrom = None 
        if self.jumptimer>endJumpTimer and checkKey(keyMap.upKey.keyValue):
            self.y_speed = self.jumpSpeedKey 
            self.jumpSpeedKey -= 0.1


    def checkForHangObject(self):                    
        self.hangMode = 0
        if hangEnabled==0:
            return
        for thisObject in self.collisionObjects: 
            if thisObject.hangable:             
              #need to do collision for head
                collisionSize = 25
                if self.y_speed >0:
                    adjustment = self.y_speed*4.0
                else:
                    adjustment = self.y_speed* -4.0
                collisionSize += (self.y_speed*5.0) #scale collision volume according to speed to makke it a bit eaasier
                topJake = self.y+self.height - (self.height * self.scale)
                headBottom = topJake + collisionSize
                if(topJake-collisionSize<thisObject.y+thisObject.height):
                    if(headBottom>thisObject.y):
          #compensate for the fact that the head is not in the centre of the sprite whilst jumping!
                        width = self.width/2    
          #for now we'll assume that only half the sprite is collidable - this is very graphic specic!
                        if(self.facing<1):
                            x = self.x
                        else:
                            x = self.x + self.width/2
                        if(x<thisObject.x+thisObject.width) and (x+width>thisObject.x):
                            self.hangMode = 1  
                            self.base_speed = thisObject.x_speed
                            self.x_speed = self.base_speed 
                  #note that we don't run physics on the player whilst hanging
                            self.y_speed = thisObject.y_speed
                  #force Jake into the correct position in the Y (always 10 from top of platform)
                            topJake = thisObject.y + 10
                            topJake = topJake + (self.height * self.scale) - self.height
                            self.y = topJake
                            jakeWidth = self.width * self.scale
                            centreX = self.x+(jakeWidth/2)
                  #Force Jake into the correct position in the X (never closer than 10 from edges)
                            if(centreX<thisObject.x+10):
                                self.x = thisObject.x+10-jakeWidth/2
                            if(centreX> thisObject.x+thisObject.width-10):
                                self.x = thisObject.x+thisObject.width-10-jakeWidth/2
              
    def Death(self,delta,increment = 1):
        global comboLevel
        global lives
       # print"death",self.deathTimer
        if(self.invulnerable<=0):
            self.painCount -=1
            self.painCount -= increment
            if(self.painCount<=0):
                self.painCount = 0
                if(self.deathTimer<=0):
                    if(comboLevel>0):
                        if arcadeMode:
                            adaptive.doingBadly(30) #lost a shield so adjust difficulty
                        #decComboLevel(1)
                        removeAllCombo()
                        playSimpleSound ('ouch') 
                        if(self.y+(self.height*self.scale)>=y_max):
                            self.deathTimer = 60
                    else:
                        if arcadeMode:
                            adaptive.doingBadly(80) #lost a life so doing really badly!
                        decrementLives()
                        playSimpleSound ('Death') 
                        self.deathTimer = 300
                        self.x_speed = 0
                        self.y_speed = -8
                        self.hangMode = 0
                        self.doingHangDrop = 0
                    self.invulnerable = 300
    
    def playerDead(self,delta): 
        global playerInWorld
        #delta = 1.3 #tony remove
        self.moveTargetObject = None
        self.target_x_speed = 0
        if(self.deathTimer>1):
            self.y += delta/2.0
            self.deathTimer -= delta
        else:
            self.deathTimer=0
            if(lives<=0):
                killPlayer()
            else:
                global tilesOver

                tilesOver = 0
                if(self.needToRestartLevel):
                    ressetToStartOfLevel()
                    self.needToRestartLevel = 0
                self.moveTargetObject = None
                self.doingJump = 0
                self.hangMode = 0
                self.trampolineTarget = None
                self.getOntoPlatformCount = 0
                self.doingGetOntoPlatform  =0 
                self.restartPlayer()

    def restartPlayer(self):
        minimumX = cameraX+gridLeft
        startOffset = 180
        if oldCameraX == cameraX or oldCameraX == 0:
            startOffset = 50
        for platform in objects:
            if platform.x + platform.width>cameraX+startOffset:
                if platform.x < minimumX:
                    if platform.validStart:
                        minimumX = platform.x
        if minimumX != cameraX+gridLeft:
            self.x = minimumX
            self.y = -20
            self.invulnerable = 300
            #self.y_speed = -13
            self.y_speed = 10
            self.onTrampoline = 0
            if self.x<cameraX:
                self.x = cameraX
        else:
            self.deathTimer = 1 #No platform available so don't spawn yet
        
    def controlAnimation(self,delta):   
        if(delta ==0):  # if we are paused then no change to animation
            return
        if (FinishFlag):
            WorldObject.doAnimation(self,animationSets.player_victory,delta)
        elif(self.deathTimer>0 or lives==0):
            #for time based animations use delta to control speed
            WorldObject.doAnimation(self,animationSets.player_death,delta)
        elif(self.onGround):
            # use delta between current speed and speed of surface standing on to control animation
            Xdelta = self.xDeltaSpeed
            if(Xdelta==0):
                if self.animation == animationSets.player_jump:
                    WorldObject.doAnimation(self,animationSets.player_land_idle,delta)
                   # print "landed"
                elif self.animation == animationSets.player_walk:
                    WorldObject.doAnimation(self,animationSets.player_idle,delta)
                else:
                    WorldObject.doAnimation(self,None,delta)          
            else:
                if self.animation == animationSets.player_jump:
                    WorldObject.doAnimation(self,animationSets.player_land_idle,delta)
                if(Xdelta<0):
                    Xdelta = -Xdelta
                if self.animation == animationSets.player_idle:
                    WorldObject.doAnimation(self,animationSets.player_walk,Xdelta)
                else:
                    WorldObject.doAnimation(self,None,Xdelta)
        elif(self.hangMode):           
            WorldObject.doAnimation(self,animationSets.player_swing,delta)
        else:
            Xdelta = self.x_speed*0.5
            if(Xdelta<0):
                Xdelta = -Xdelta
            WorldObject.doAnimation(self,animationSets.player_jump,Xdelta)
            
    def makeOnGroundSound(self,deltaY):
       # print "deltaY",deltaY
        thisVolume = deltaY/2.0
        if thisVolume>1:
            thisVolume = 1
        if thisVolume < 0:
            thisVolume = 0
       # print "thisVolume",thisVolume
        thisPanning = (self.x-cameraX-400)/100
        playSimpleSoundList(["land1","land2"],panning =thisPanning, volume = thisVolume)
        #playSimpleSound("land1")



class CellarWheel(WorldObject):
    coins = 0
    solid = 0
    z = 200 # right at the back
    name = 'BigWheel'
    graphic = 'bar' 
    speed1 = 0.003
    speed2 = 0.006
    distance1 = 160.0
    distance2 = 110.0
    angle1 = 0
    angle2 = 0
    dynamic = 1
    numberPlatforms = 8.0
    platforms = []
    centre1X = 0
    centre1Y = 0
    centre2X = 0
    centre2Y = 0
    graphic2 = "smallBar"
    smallRes = None
    widthSmall = 0
    heightSmall = 0
    def spawn(self):
        self.platforms = []
        for platform in range(int(self.numberPlatforms)):
            type = WorldTypes.CellarRotatingPlatform #tony - for now we'll not bother with random here
            object = addObject(nextID,0,0,type)
            self.platforms.append(object)
            object.x = self.x
            object.y = self.y + 300 

        if self.coins:
            self.tick(0)      #do one tick to set up the platforms
            count = 0
            for platform in self.platforms:
                if count%2 ==0:
                    type = WorldTypes.Coin250 
                    offset = 30
                else:
                    type = WorldTypes.Coin1000
                    offset = 35
                centreX = platform.x+platform.width/2 - offset
                centreY = platform.y 
                x = centreX
                y = centreY-(offset*2.0)
                object = (addObject(nextID,x,y,type))
                global coinsSpawned
                coinsSpawned += 1
                count += 1
                
        self.smallRes = JPG_Resources[self.graphic2]
        self.widthSmall = PCR.imageWidth(self.smallRes)
        self.heightSmall = PCR.imageHeight(self.smallRes)
        
    def render(self):
        if PC.getIs3DAccelerated():
            x = self.x-cameraX
            y = self.y-cameraY
            PC.drawImageRot(JPG_Resources[self.graphic],x,y,self.angle1+fullRotation/4 )
            if self.smallRes != None:
                x = self.centre1X-cameraX - self.widthSmall/2
                y = self.centre1Y-cameraY - self.heightSmall/2
                PC.drawImageRot(self.smallRes,x,y,self.angle2)
                x = self.centre2X-cameraX - self.widthSmall/2
                y = self.centre2Y-cameraY - self.heightSmall/2
                PC.drawImageRot(self.smallRes,x,y,self.angle2)
        if(self.Selected):
            #selectable region is much smaller than the wheel to make selecting objects on top of it easier
            PC.setColour( 128, 128, 128, 128)
            PC.fillRect( x+(self.width/2-25), y+(self.height/2-25), 50, 50 )
            
    def tick(self,delta):
        #delta = 1.6666
        #print "rotating wheel",delta,self.speed1,self.speed2,self.angle1,self.angle2
        if(delta>0):
            self.angle1 += self.speed1*delta
            self.angle2 += self.speed2*delta
        #rotate us
        if self.speed1>0:
            if(self.angle1>=fullRotation):
                self.angle1 -= fullRotation
            if(self.angle2>=fullRotation):
                self.angle2 -= fullRotation          #rotate us
        else:
            if(self.angle2<0):
                self.angle2 += fullRotation
            if(self.angle1<0):
                self.angle1 += fullRotation
        #rotate us           
        self.centre1X = self.x+(self.width/2) + self.distance1*math.sin(self.angle1)
        self.centre1Y = self.y+(self.height/2) + self.distance1*math.cos(self.angle1)
        self.centre2X = self.x+(self.width/2) - self.distance1*math.sin(self.angle1)
        self.centre2Y = self.y+(self.height/2) - self.distance1*math.cos(self.angle1)  
        for platform in range(int(self.numberPlatforms)):   
            oldX = self.platforms[platform].x
            oldY = self.platforms[platform].y
            thisAngle = platform/(self.numberPlatforms/2.0)*fullRotation
            if platform < (self.numberPlatforms/2.0):
                x = self.centre1X
                y = self.centre1Y
            else:
                x = self.centre2X
                y = self.centre2Y
            x += self.distance2*math.sin(self.angle2+thisAngle)
            y += self.distance2*math.cos(self.angle2+thisAngle)
            x -= self.platforms[platform].width/2
            y -= self.platforms[platform].height/2
            self.platforms[platform].x = x
            self.platforms[platform].y = y
            if(delta>0):
                self.platforms[platform].y_speed = (self.platforms[platform].y - oldY) /delta 
                self.platforms[platform].x_speed = (self.platforms[platform].x - oldX) /delta
                
class CoinCellarWheel(CellarWheel):  
    name = 'CoinWheel'  
    coins = 1
    speed1 = -0.003
    speed2 = -0.006
    angle1 = 11.0/7.0
    
class DoubleCellarWheel(CoinCellarWheel):
    name = 'doubleWheel'
    speed1 = -0.005
    speed2 = -0.007
    def spawn(self):
        CellarWheel.spawn(self)
        type = WorldTypes.CellarWheel #tony - for now we'll not bother with random here
        object = addObject(nextID,0,0,type)
        object.x = self.x
        object.y = self.y
        object.speed1 = self.speed1
        object.speed2 = self.speed2


class SmallCellarWheel(WorldObject):
    coins = 1
    solid = 0
    z = 200 # right at the back
    name = 'SmallWheel'
    graphic = 'smallBar' 
    speed1 = 0.009
    distance1 = 110.0
    angle1 = 0
    dynamic = 1
    numberPlatforms = 4.0
    platforms = []
    centre1X = 0
    centre1Y = 0
    def spawn(self):
        self.platforms = []
        for platform in range(int(self.numberPlatforms)):
            type = WorldTypes.CellarRotatingPlatform #tony - for now we'll not bother with random here
            object = addObject(nextID,0,0,type)
            self.platforms.append(object)
            object.x = self.x
            object.y = self.y + 300 

        if self.coins:
            self.tick(0)      #do one tick to set up the platforms
            count = 0
            for platform in self.platforms:
                if count%2 ==0:
                    type = WorldTypes.Coin250 
                    offset = 30
                else:
                    type = WorldTypes.Coin1000
                    offest = 35
                centreX = platform.x+platform.width/2 - offset
                centreY = platform.y 
                x = centreX
                y = centreY-(offset*2.2)
                object = (addObject(nextID,x,y,type))
                global coinsSpawned
                coinsSpawned += 1
                count += 1
        
    def render(self):
        x = self.x-cameraX
        y = self.y-cameraY
        PC.drawImageRot(JPG_Resources[self.graphic],x,y,self.angle1+fullRotation/4 )
        if(self.Selected):
            #selectable region is much smaller than the wheel to make selecting objects on top of it easier
            PC.setColour( 128, 128, 128, 128)
            PC.fillRect( x+(self.width/2-25), y+(self.height/2-25), 50, 50 )
            
    def tick(self,delta):
        #delta = 1.6666
        #print "rotating wheel",delta,self.speed1,self.speed2,self.angle1,self.angle2
        if(delta>0):
            self.angle1 += self.speed1*delta
        #rotate us
        if self.speed1>0:
            if(self.angle1>=fullRotation):
                self.angle1 -= fullRotation         #rotate us
        else:
            if(self.angle1<0):
                self.angle1 += fullRotation
        #rotate us           
        self.centre1X = self.x+(self.width/2)
        self.centre1Y = self.y+(self.height/2)  
        for platform in range(int(self.numberPlatforms)):   
            oldX = self.platforms[platform].x
            oldY = self.platforms[platform].y
            thisAngle = platform/(self.numberPlatforms)*fullRotation
            x = self.centre1X
            y = self.centre1Y

            x += self.distance1*math.sin(self.angle1+thisAngle)
            y += self.distance1*math.cos(self.angle1+thisAngle)
            x -= self.platforms[platform].width/2
            y -= self.platforms[platform].height/2
            self.platforms[platform].x = x
            self.platforms[platform].y = y
            if(delta>0):
                self.platforms[platform].y_speed = (self.platforms[platform].y - oldY) /delta 
                self.platforms[platform].x_speed = (self.platforms[platform].x - oldX) /delta
                







class RotatingPlatformSpawn(WorldObject):
    solid = 0
    z = 200 # right at the back
    name = 'BigWheel'
    graphic = 'wheel' 
    speed = 0.002
    distance = 210.0
    angle = 0
    dynamic = 1
    numberPlatforms = 8.0
    def spawn(self):
        for platform in range(int(self.numberPlatforms)):
           # if(levelMetaData.RandomTiles==0):
            type = WorldTypes.RotatingPlatform #tony - for now we'll not bother with random here
           # else:
           #     type = WorldTypes.RotatingPlatformRed + (platform%levelMetaData.RandomTiles)
            index = objects.index(addObject(nextID,0,0,type))
            objects[index].angle = platform*(fullRotation)/self.numberPlatforms
            #print("wheel angle index",index)
            objects[index].centreX = self.x+self.width/2
            objects[index].centreY = self.y+self.height/2 
            objects[index].distance = self.distance             
            objects[index].speed = self.speed 
            objects[index].tickDelay = 100
            #print("wheel",index,objects[index].name,objects[index].x,objects[index].y)           
        return 1
    def render(self):
        if PC.getIs3DAccelerated():
            x = self.x-cameraX
            y = self.y-cameraY
            PC.drawImageRot(JPG_Resources[self.graphic],x,y,self.angle)
            if(self.Selected):
                #selectable region is much smaller than the wheel to make selecting objects on top of it easier
                PC.setColour( 128, 128, 128, 128)
                PC.fillRect( x+(self.width/2-25), y+(self.height/2-25), 50, 50 )
        
    def tick(self,delta):
        if(delta>0):
            self.angle += self.speed*delta
        #rotate us
        if(self.angle>fullRotation):
            self.angle -= fullRotation
            
class SmallWheel(RotatingPlatformSpawn):
    name = 'SmallWheel'
    graphic = 'wheelSmall' 
    speed = -0.0025
    distance = 130.0
    angle = 0
    dynamic = 1
    numberPlatforms = 5.0
            
class CoinWheel(RotatingPlatformSpawn):
    name = 'CoinWheel'
    
    def spawn(self):
        count = 0
        global coinsSpawned
        for platform in range(int(self.numberPlatforms)):
            type = WorldTypes.RotatingPlatform #tony - for now we'll not bother with random here
            index = objects.index(addObject(nextID,0,0,type))
            objects[index].angle = platform*(fullRotation)/self.numberPlatforms
            objects[index].centreX = self.x+self.width/2
            objects[index].centreY = self.y+self.height/2 
            objects[index].distance = self.distance             
            objects[index].speed = self.speed 
            objects[index].tickDelay = 50
            
           # if count%2==0:
            type = WorldTypes.Coin50 
            angle = platform*(fullRotation)/self.numberPlatforms
            centreX = self.x+self.width/2
            centreY = self.y+self.height/2 
            x = centreX + (math.sin(angle)*self.distance)-25
            y = centreY + (math.cos(angle)*self.distance)-80
            object = (addObject(nextID,x,y,type))
            coinsSpawned += 1
            object.tickDelay = 30  
           # count += 1
            
class SmallCoinWheel(CoinWheel):
    name = 'SmallCoinWheel'
    graphic = 'wheelSmall' 
    speed = -0.0025
    distance = 130.0
    angle = 0
    dynamic = 1
    numberPlatforms = 5.0

class smashable(WorldObject):
    debris1 = None
    debris2 = None
    def isSmash(self):
        if(self.x>cameraX):
            if(self.debris1):
                x = self.x
                particleController.addItem(debris(self.debris1,-0.01),x,self.y+15,1)
            if(self.debris2):
                debrisWidth =  PCR.imageWidth( JPG_Resources[self.debris2] ) 
                x = self.x+self.width-debrisWidth
                particleController.addItem(debris(self.debris2,0.01),x,self.y+15,1)
        self.x = -10000

class Platform(smashable):
    selectExtensionUp = 30
    selectExtensionDown = 0
    hangable = 1
    platformIDX=levelData.platform200   #default!
    graphic = 'RandomPlatform100' #default - never used
    mouseOver = 0
    tint  = 255
    targetTint = 255
    forceTint = 0
    platformParticleStrobe = 0
    def setUpGraphics(self):
        if(self.platformIDX != -1):
            #overloaded to set up using hte platformIDX
            self.graphic = levelMetaData.platformSet[self.platformIDX][0]
            if len(levelMetaData.platformSet[self.platformIDX])>1:
                #if there is debris for this platform then set it up
                self.debris1 = levelMetaData.platformSet[self.platformIDX][1]
                self.debris2 = levelMetaData.platformSet[self.platformIDX][2]
        self.res = JPG_Resources[self.graphic]
        self.width= PCR.imageWidth( self.res ) 
        self.height = PCR.imageHeight( self.res )
    def getGraphic(self):  
        self.setUpGraphics()
        return self.graphic
        
    def tick(self,delta):
        smashable.tick(self,delta)
        self.inRange = 0
        self.inHangRange = 0
        standingOnThisPlatform  = 0
        accessible = 1
        if(self.tint<self.targetTint):
            self.tint += delta*4
            if(self.tint>self.targetTint):
                self.tint = self.targetTint
        if(self.tint>self.targetTint):
            self.tint -= delta*4
            if(self.tint<self.targetTint):
                self.tint = self.targetTint
        #first only allow platforms on the screen to be selected
        if (self.x<cameraX+gridLeft) and (self.x+self.width>cameraX):
            if globalPlayer != None:
                if globalPlayer.PlatformOn or globalPlayer.onTrampoline:
                    if(globalPlayer.onTrampoline):
                        playerPlatform = globalPlayer.onTrampoline
                    else:
                        playerPlatform = globalPlayer.PlatformOn
                    playerCenterX = globalPlayer.x+(globalPlayer.width/2*globalPlayer.scale)
                    if playerCenterX > self.x+self.width:
                        #this platform is to the left
                        distanceX = playerCenterX-(self.x+self.width)
                        if distanceX <0:
                            distanceX = 0
                        #print("distance on left",distanceX)
                        direction = -1
                    elif globalPlayer.x+globalPlayer.width<self.x+self.width:
                        #this platform is to the right
                        distanceX = (self.x)-(globalPlayer.x+(globalPlayer.width/2*globalPlayer.scale))
                        if distanceX<0:
                            distanceX = 0
                        direction = 1
                        #print("distance on right",distanceX)
                    else:
                        direction = 0
                        distanceX = 0                 
                    if playerPlatform==self :
                        direction = 0
                        distanceX = 0    #this is the platform the player is currently standing on!
                        standingOnThisPlatform = 1
                    if(profiles[currentProfile].mouseControl==1):
                        if accessible == 1:
                            if standingOnThisPlatform:
                                self.inRange = 1
                            else:
                                maxJumpLookUp=findJumpLookUp(0)
                                YAfterJump = getTableValue(distanceX,maxJumpLookUp)
                                if globalPlayer.hangMode==0:
                                    playerHeight = self.height
                                else:
                                    playerHeight = hangSpriteHeight
                                if(globalPlayer.onTrampoline):
                                    yDelta = trampolinePlayerY+playerHeight-self.y
                                else:
                                    yDelta = globalPlayer.y+playerHeight-self.y
                                if(YAfterJump>yDelta):
                                    self.inRange = 1
                                    #now check to see if hang will work
                                elif ( YAfterJump> (yDelta - hangSpriteHeight)) and hangEnabled==1:
                                    self.inHangRange = 1
                                    self.inRange = 1
    
    def render(self):
        PC.drawmodeNormal()
        self.colourize = 1
        if(globalPlayer!= None):
            if(globalPlayer.PlatformOn!= None):
                if self.inRange==1:
                    self.targetTint = 255
                else:
                    self.targetTint = 70
        if(profiles[currentProfile].mouseControl==0):
            self.tint = 255
        self.tintr = self.tint
        self.tintg = self.tint
        self.tintb = self.tint
        if(inEditor == 0 and self.forceTint == 0): #otherwise we can't ghost none selectable platforms
            self.tinta = 255 
        PC.setColourize(1)        
        PC.setColour(int(self.tintr),int(self.tintg),int(self.tintb),int(self.tinta))
        PC.drawImage(self.res,self.x-cameraX,self.y+cameraY)
        PC.setColourize(0)
        if(self.Selected):
            PC.setColour( 128, 128, 128, 128)
            PC.fillRect( self.x-cameraX, self.y, self.width, self.height )
            
        if self.targetTint == 255 and mousex+pointerSizeX+cameraX> self.x and mousex+cameraX-pointerSizeX < self.x+self.width:
            if mousey > self.y-self.selectExtensionUp and mousey < self.y + self.height+self.selectExtensionDown and forcePause==0 and FinishFlag ==0 and escapeMenu.active==0:
                self.platformParticleStrobe += 1
                if self.platformParticleStrobe%2:              
                    x = random.randint(int(self.x),int(self.x+self.width))
                    y = self.y+5 
                    scrollDelta = 0
                    makeSparkleParticle(x,y,scrollDelta,0,2)                
                PC.drawmodeAdd()
                PC.setColourize(1) 
                if button1Down:
                  PC.setColour( 200, 200, 200, 200)
                else:
                    PC.setColour( 200, 200, 200, 128)
                PC.drawImage(self.res,self.x-cameraX,self.y+cameraY)
                PC.drawmodeNormal()
                PC.setColourize(0)

class Conveyor(WorldObject):
    name = "conveyor"
    graphic = "Conveyor400"
    numberPlatforms = 4.0
    speed = 1.0
    placeable = 0
    def spawn(self):
        for platform in range(int(self.numberPlatforms)):
            type = WorldTypes.ConveyorPlatform 
            object = addObject(nextID,0,0,type)
            object.x= self.x + (platform/self.numberPlatforms * self.width)
            object.y = self.y
            object.maxLeft = self.x
            object.maxRight = self.x+self.width            
            object.speed = self.speed 
            object.tickDelay = 50   
        self.y += 10
    
class ConveyorPlatform(Platform):
    placeable = 0
    maxLeft = 0
    maxRight = 0
    platformIDX=-1   #disable want it to always look like the trampoline
    graphic = "ConveyorPlatform"

    def tick(self,delta):
        rightLimit = 30
        self.x += self.speed* delta
        if self.x > self.maxRight:
            self.x = self.maxLeft
            self.solid = 1
        if self.x > self.maxRight-rightLimit:
            #self.solid = 0
            if globalPlayer.PlatformOn == self:
                globalPlayer.PlatformOn = None
        Platform.tick(self,delta)

class SwingLong(Platform):
    solid = 1
    hangable=1
    graphic = 'JVineBase'
    vine = "JVineLong"
    platformIDX=-1   #disable want it to always look like the trampoline
    vineRes = 0
    vineLength = 210.0
    angle = 0
    x_centre = 0
    y_centre = 0
    swingSpeed = 0.018
    counter = 0
    vineX=0
    vineY=0
    swingRange = 0.65
    rotatedVine=0
    dynamic = 1
    name = "medVine"
    vineIdx=2
    platformIdx = 5
    vineWidth = 0
    compensation = 0
    def spawn(self):
        self.vineRes = JPG_Resources[self.vine]
        self.vineWidth = PCR.imageWidth(self.vineRes)
        self.compensation = self.width/2- self.vineWidth/2
        self.vineLength = PCR.imageHeight(self.vineRes)
        self.x_centre = self.x
        self.y_centre = self.y-self.vineLength
        return 0 
        
    def tick(self,delta):   
        oldX = self.x
        oldY = self.y
        Platform.tick(self,delta)
        self.counter += delta
        self.rotatedVine = math.sin(self.counter*self.swingSpeed)*self.swingRange
        self.vineX = self.x_centre+(math.sin(self.rotatedVine)*self.vineLength/2)
        self.vineY = self.y_centre+(math.cos(self.rotatedVine)*self.vineLength/2)-self.vineLength*0.5
        self.x = self.x_centre+(math.sin(self.rotatedVine)*self.vineLength)-(self.compensation)
        self.y = self.y_centre+(math.cos(self.rotatedVine)*self.vineLength)-(self.height/8)
        if delta!=0:
            self.x_speed = (self.x-oldX)/delta
            self.y_speed = (self.y-oldY)/delta
        else:
            self.x_speed = 0
            self.y_speed = 0

    def render(self):
        if(inEditor!=1):
            PC.drawmodeNormal()
            PC.setColourize(0)
            PC.drawImageRot(self.vineRes,self.vineX-cameraX,self.vineY+cameraY,self.rotatedVine)
        Platform.render(self)
        
    def setUpGraphics(self):
        self.graphic = levelMetaData.platformSet[11][self.platformIdx]
        self.vine = levelMetaData.platformSet[11][self.vineIdx]
        self.res = JPG_Resources[self.graphic]
        self.width= PCR.imageWidth( self.res ) 
        self.height = PCR.imageHeight( self.res )


            
    def isSmash(self):
        return
        
    def stoodOn(self):
        #need to stop player walking of edge of platform
        centreX = globalPlayer.x+(globalPlayer.width/2)
        if centreX < self.x:
            globalPlayer.x = self.x-(globalPlayer.width/2)
        if centreX > self.x + self.width:
            globalPlayer.x = self.x + self.width -(globalPlayer.width/2)            


class SwingMedium(SwingLong):
    vine = "JVineMed"
    name = "shortVine"
    platformIDX=-1   #disable want it to always look like the trampoline
    swingSpeed = 0.023
    vineIdx=1
    platformIdx = 4

class SwingVeryLong(SwingLong):
    vine = "JVineVLong"
    name = "LongVine"
    platformIDX=-1   #disable want it to always look like the trampoline
    swingSpeed = 0.015
    swingRange = 0.50
    vineIdx=3
    platformIdx = 0

class BigTrampoline(Platform):  
    validStart = 1
    jumpTableOffset = 0
    placeable = 1   #set to 0 if not place
    hangable = 0
    name = 'BigTrampoline'
    graphic = 'Trampoline150'
    trampgraphic = 'Trampoline150'
    trampgraphicDown = 'Trampoline150Down'
    trampgraphicUp = 'Trampoline150Up'
    trampRes = None
    trampDownRes = None
    trampUpRes = None
    platformIDX=-1   #disable want it to always look like the trampoline
    bounceCount = 0
    bounceSound = "bigTrampBounce"
    isTrampoline = 1
    
    def stoodOn(self):
        global trampolinePlayerY
        startBounce = 40
        self.bounceCount = startBounce
        if(globalPlayer.onTrampoline==0):
            globalPlayer.onTrampoline = self
            trampolinePlayerY = globalPlayer.y
            thisVolume = 1           
            thisPanning = (self.x-cameraX-400)/100
            playSimpleSound (self.bounceSound,volume = thisVolume,panning = thisPanning) 
        return 0
            
    def isSmash(self):
        return 0
        
        
    def render(self):
        if inEditor:
            self.res = JPG_Resources[self.trampgraphic]
            Platform.render(self) 
            return
        tempY = self.y
        originalHeight = PCR.imageHeight(self.trampRes)
        if self.bounceCount == 0:
            self.res = self.trampRes  
        elif self.bounceCount > 20:
            self.res = self.trampDownRes
        else:
            self.res = self.trampRes
        newHeight = PCR.imageHeight(self.res)
        self.y += originalHeight-newHeight
        Platform.render(self)
        self.y = tempY
        
    def spawn(self):
        self.trampRes = JPG_Resources[self.trampgraphic]
        self.trampDownRes = JPG_Resources[self.trampgraphicDown]
#        self.trampUpRes = JPG_Resources[self.trampgraphicUp]
        
    def tick(self,delta):
        self.bounceCount -= delta
        if self.bounceCount<0:
            self.bounceCount = 0
        Platform.tick(self,delta)
        
class MedTrampoline(BigTrampoline):
    jumpTableOffset = 1
    name = 'MedTrampoline'
    graphic = 'Trampoline113'
    trampgraphic = 'Trampoline113'
    trampgraphicDown = 'Trampoline113Down'
    trampgraphicUp = 'Trampoline113Up'
    bounceSound = "medTrampBounce"
    
class SmallTrampoline(BigTrampoline):
    jumpTableOffset = 2
    name = 'SmallTrampoline'
    graphic = 'Trampoline75'
    trampgraphic = 'Trampoline75'
    trampgraphicDown = 'Trampoline75Down'
    trampgraphicUp = 'Trampoline75Up'
    bounceSound = "smallTrampBounce"
    
class RotatingPlatform(Platform):
    placeable = 0   #set to 0 if not placeale    
    hangable = 1
    centreX = 0
    centreY = 0
    angle = 0.0
    distance = 0.0
    speed = 0.0
    tickDelay = 100
    platformIDX=-1   #disable want it to always look like the trampoline
    name = 'platform'
    graphic = 'WaterwheelPlatform'
    dynamic = 1

    def tick(self,delta):
        #print("rotating platform tick",self,self.x,self.y)
        self.tickDelay -= delta
        if(self.tickDelay<=0):
            self.tickDelay = 0
            if(delta>0):   
                self.angle += self.speed*delta
            if(self.angle>fullRotation):
                self.angle =- fullRotation
        oldX =  self.x 
        oldY = self.y
        #calculate the position in the world
        self.x = self.centreX + (math.sin(self.angle)*self.distance)-self.width/2
        self.y = self.centreY + (math.cos(self.angle)*self.distance)-self.height/2
        #cheap differentiation becuase I don't want to do the calculus
        if(delta>0):
            tempDelta = delta
            self.y_speed = (self.y - oldY) /tempDelta 
            self.x_speed = (self.x - oldX) /tempDelta
            
        #self.hint = AddToGrid(self.name,self.y,0)

        Platform.tick(self,delta)
        
    def isSmash(self):
        return 0 


class CellarRotatingPlatform(Platform):
    placeable = 0   #set to 0 if not placeale    
    hangable = 1
    centreX = 0
    centreY = 0
    angle = 0.0
    distance = 0.0
    speed = 0.0
    tickDelay = 100
    platformIDX=-1   #disable want it to always look like the trampoline
    name = 'platform'
    graphic = 'cellarWheelPlatform'
    dynamic = 1
    def tick(self,delta):
        Platform.tick(self,delta)
    def isSmash(self):
        return 0 

class RotatingPlatformBlue(RotatingPlatform):
    name = 'Blue'
      

class RotatingPlatformRed(RotatingPlatform):
    name = 'Red'
     

class RotatingPlatformGreen(RotatingPlatform):
    name = 'Green'
 
    
class RotatingPlatformWhite(RotatingPlatform):
    name = 'White'
      
    
class RotatingPlatformBlack(RotatingPlatform):
    name = 'Black'

class Stem(WorldObject):
    placeable = 0
    graphic = 'Stem100' #default - never used
    z = 150
    def setUpGraphics(self):
        #overloaded to set up using hte platformIDX
        self.graphic = levelMetaData.platformSet[self.platformIDX]
        self.res = JPG_Resources[self.graphic]
        self.width= PCR.imageWidth( self.res ) 
        self.height = PCR.imageHeight( self.res )

class Stem100(Stem):
    name = 'Stem100'
    platformIDX = levelData.stem100 

class Stem200(Stem):
    name = 'Stem200'
    platformIDX = levelData.stem200 

class Stem400(Stem):
    name = 'Stem400'
    platformIDX = levelData.stem400 
    
class StaticPlatform(Platform):
    validStart = 1
    name = '100plat'
    platformIDX = levelData.platform100 
    
class StaticPlatform200(Platform):
    validStart = 1
    name = '200plat'
    platformIDX = levelData.platform200 

    
class StaticPlatform400(Platform):
    validStart = 1
    name = '400plat'
    platformIDX = levelData.platform400 
    
class JewelPlatform(Platform): 
    validStart = 1
    jewelIDX = -1 #
    flash = 0
    placeable = 0 #tony - surely this is not placeable?
    def render(self):
        Platform.render(self)
        if self.jewelIDX != -1:
            hint = 0 #tony - disabled this becuase we don't hint anymore
            name = levelMetaData.jewelSet[self.jewelIDX]
            frame = JPG_Resources[name]
            width= PCR.imageWidth( frame ) 
            tempx = self.x-cameraX-width/2+self.width/2
            tempy = self.y-1
            PC.drawImage(frame, tempx, tempy)
            if(hint>1):
                PC.drawmodeAdd()
                PC.setColourize(1)
                alpha = self.life%64
                if(alpha>32):
                    alpha = 32-alpha
                alpha *= 8

                PC.setColour( 255, 255, 255, int(alpha) )
                PC.drawImage(frame, tempx, tempy)
                PC.drawmodeNormal()
                PC.setColourize(0)
            
    def stoodOn(self):
        if self.collected == 0:
            self.collected = 1
            jewelX = self.x + (self.width/2)-20
            jewelY = self.y -1
            type = WorldTypes.CollectedJewel
            pointer = addObject(nextID,jewelX,jewelY,type)
            name = levelMetaData.jewelSet[self.jewelIDX]
            pointer.res = JPG_Resources[name] 
            pointer.name = self.name
            pointer.jewelIDX = self.jewelIDX
            pointer.x_speed = -1.25
            self.jewelIDX = -1
            playSimpleSound ('click1')

        
    def tick(self,delta):
        global gridRight
        global gridLeft
        test = (int(self.life+self.y))%2
        if self.collected == 0 and test ==0:
            if gridType == 0:
                self.hint = AddToGrid(self.jewelIDX,self.y,0) 
            else:
                #self.hint = trailGame.test(self.jewelIDX) 
                self.hint = 0
        Platform.tick(self,delta) 
        self.flash += delta*3
        
class RedPlatform(JewelPlatform):
    name = 'Red'
    jewelIDX = levelData.Red
    
class BluePlatform(JewelPlatform):
    name = 'Blue'
    jewelIDX = levelData.Blue
      
class GreenPlatform(JewelPlatform):
    name = 'Green' 
    jewelIDX = levelData.Green    

class WhitePlatform(JewelPlatform):
    name = 'White'
    jewelIDX = levelData.White   
    
class BlackPlatform(JewelPlatform):
    name = 'Blue' 
    jewelIDX = levelData.Black

class OrangePlatform(JewelPlatform):
    name = 'Orange'
    jewelIDX = levelData.Orange

class PurplePlatform(JewelPlatform):
    name = 'Purple'   
    jewelIDX = levelData.Purple
    
class YellowPlatform(JewelPlatform):
    name = 'Yellow' 
    jewelIDX = levelData.Yellow
    
class StripePlatform(JewelPlatform):
    name = 'Stripe' 
    jewelIDX = levelData.Stripe
    
class CollectedJewel(WorldObject):
    placeable = 0
    z = 75
    solid = 0
    name = 'CollectedJewel'
    graphic = 'Fruit01'  #tony - this is never used and should be removed
    jewelIDX = -1
    
    def tick(self,delta):
        if gridType==0:
            if(gridFillRight):
                self.x += delta*self.x_speed
                self.x_speed += 0.25
                if(self.x+self.width>gridLeftTarget+cameraX):
                    AddToGrid(self.jewelIDX,self.y,1) 
                    playSimpleSound ('grid1')               
                    self.x = -500  #move the jewel out of the playing area
            else:
                self.x += delta*self.x_speed
                self.x_speed -= 0.25
                if(self.x<gridRightTarget+cameraX):
                    AddToGrid(self.jewelIDX,self.y,1) 
                    playSimpleSound ('grid1')                          
                    self.x = -500  #move the jewel out of the playing area
        else:
            playSimpleSound ('grid1')  
            trailGame.addIt(self.jewelIDX,self.x,self.y)
            self.x = -500
class DynamicPlatform(Platform):
    name = 'SlowHor'
    platformIDX = levelData.DynamicPlatform 
    leftExtent = 0
    rightExtent = 0
    tickDelay= 200
    dynamic = 1
    x_speed = StaticPlatformXspeed
    max_Xspeed = StaticPlatformXspeed
    target_x_speed = StaticPlatformXspeed
    
    def isSmash(self):  #not smashable
        return 0
        
    def tick(self,delta):
        self.tickDelay -= delta
        if(self.tickDelay>0):
            self.x_speed=0
            return
            
        thisPanning = (self.x-cameraX-400)/100


 
        self.tickDelay = 0 
        if(self.x <=self.leftExtent):
            if self.target_x_speed < 0: 
                playSimpleSound ("bounce1",panning = thisPanning)  
            self.target_x_speed = self.max_Xspeed
        elif(self.x >=self.rightExtent):
            if self.target_x_speed > 0:
                playSimpleSound ("bounce1",panning = thisPanning)  
            self.target_x_speed = - self.max_Xspeed
        if(self.target_x_speed > 0):
            self.x_speed += .2
            if(self.x_speed > self.target_x_speed):
                self.x_speed = self.target_x_speed  
        if(self.target_x_speed < 0):
            self.x_speed -= .2
            if(self.x_speed < self.target_x_speed):
                self.x_speed = self.target_x_speed       
        self.x += (self.x_speed * delta)
        Platform.tick(self,delta)
    #def spawn:
      

class fastDynamicPlatform(DynamicPlatform):
    name = 'fastHor'
    x_speed = StaticPlatformXspeed *1.5
    max_Xspeed = StaticPlatformXspeed *1.5
    target_x_speed = StaticPlatformXspeed *1.5
        
class DynamicVerticalPlatform(Platform):
    name = 'SlowVer'
    platformIDX = levelData.DynamicVerticalPlatform
    TopExtent = 0
    BottomExtent = 0
    tickDelay= 200
    dynamic = 1
    y_speed = StaticPlatformXspeed
    max_Yspeed = StaticPlatformXspeed
    target_y_speed = StaticPlatformXspeed
    
    def isSmash(self):  #not smashable
        return 0
        
    def tick(self,delta):
        self.tickDelay -= delta
        if(self.tickDelay>0):
            return
        self.tickDelay = 0
        thisPanning = (self.x-cameraX-400)/100
        if(self.y <=self.TopExtent):
            if self.target_y_speed < 0:
                playSimpleSound ("bounce2",panning = thisPanning)  
            self.target_y_speed = self.max_Yspeed
        if(self.y >=self.BottomExtent):
            if self.target_y_speed > 0:
                playSimpleSound ("bounce2",panning = thisPanning)   
            self.target_y_speed = - self.max_Yspeed
        if(self.target_y_speed > 0):
            self.y_speed += .2
            if(self.y_speed > self.target_y_speed):
                self.y_speed = self.target_y_speed  
        if(self.target_y_speed < 0):
            self.y_speed -= .2
            if(self.y_speed < self.target_y_speed):
                self.y_speed = self.target_y_speed       
        self.y += (self.y_speed * delta)
        Platform.tick(self,delta)

class fastDynamicVerticalPlatform(DynamicVerticalPlatform):
    name = 'FastVer'
    y_speed = StaticPlatformXspeed * 1.5
    max_Yspeed = StaticPlatformXspeed * 1.5
    target_y_speed = StaticPlatformXspeed * 1.5

class ExitPlatform(Platform):
    global continousWorldXOffset
    validStart = 1
    name = 'Finish'
    platformIDX = levelData.ExitPlatform
    placeable = 0
    
    def isSmash(self):  #not smashable
        return 0
        
    def tick(self,delta):
        Platform.tick(self,delta)

    def stoodOn(self):
        ReachedExit()

class FinishPlatform(Platform):
    global continousWorldXOffset
    validStart = 1
    name = 'Finish'
    platformIDX = levelData.FinishPlatform
    
    def isSmash(self):  #not smashable
        return 0
        
    def tick(self,delta):
        global cameraX
        global finishPlaformRight
        global finishOn
        if(cameraX+gridLeft>self.x+150):
            cameraX = self.x+150-gridLeft
            finishOn = 1
        Platform.tick(self,delta)
        finishPlaformRight = self.x+150
        if(cameraX+gridLeft>self.x):
            scrollManager.disableDash()

    def stoodOn(self):
        ReachedFinish()
        
        
class CoinFinishPlatform(FinishPlatform):
    validStart = 0
    solid = 0  
    alpha = 0
    colourize = 1
    tinta = 0
    forceTint = 1
    
    def render(self):
        if inEditor:
            self.tinta = 255
        else:
            self.tinta = self.alpha
        if self.alpha != 0:
            FinishPlatform.render(self)
    
    def tick(self,delta):
        FinishPlatform.tick(self,delta)
        if(coinsCollected == coinsSpawned):
            if self.solid==0:
                playSimpleSound("PlatformRevealed")
            self.solid = 1
            self.alpha += delta*2
            if self.alpha > 255:
                self.alpha = 255
           
class StagingPlatform(Platform):
    validStart = 1
    name = 'Staging'
    platformIDX = levelData.platform100 
    placeable = 0
    
    def isSmash(self):  #not smashable
        return 0
        
    def tick(self,delta):
        global cameraX
#        print "staging",self.x,self.y
        Platform.tick(self,delta)
        if(self.x<cameraX+400):
            ReachedStaging()
        if(cameraX+gridLeft>self.x):
            scrollManager.disableDash()
    def stoodOn(self):
        ReachedStaging()
        
    def render(self):
        if inEditor:
            self.platformIDX = None
            self.res = JPG_Resources["Staging"]
        Platform.render(self)
            

class Tutorial(WorldObject):
    name = "Tutorial"
    graphic = "Tutorial"
    triggered = 0
    solid = 0
    
    def render(self):
        if inEditor:
            WorldObject.render(self)
            
    def tick(self,delta):
        collided = 0
        if globalPlayer:
            if globalPlayer.x+globalPlayer.width>self.x and self.life>100:
            #    print "tute",globalPlayer.x,globalPlayer.width,self.x
                collided = 1
        if collided and self.triggered == 0:
            self.triggered = 1
            self.doNextTutorial()
        WorldObject.tick(self,delta)
        
    def doNextTutorial(self):      
        if levelMetaData.midInstructions:
            global thisLevelTutioral
            if tutorialsOn and thisLevelTutioral < 2 and arcadeMode == 0:
                thisLevelTutioral += 1
                if levelMetaData.midInstructions == messages.ThirdGemInstructionsB and smashEnabled ==0:
                    return
                if levelMetaData.midInstructions == messages.SecondKeyInstructions2 and (smashEnabled ==0 or dashEnabled ==0):
                    return
                instructionManager.showInstruction(levelMetaData.midInstructions) 

class basicTutorial(WorldObject):
    name = "Tutorial"
    graphic = "Tutorial"
    triggered = 0
    cancelled = 0
    alphaLevel = 0
    instructions = messages.basicInstructions1
    placeable = 0
    alpha = 0
    instructionArrow = "InstructionArrow"
    xOffset = 27
    yOffset = 40
    arrowFlash = 0
    instructionBoxLeft = "instructionBoxLeft"
    instructionBoxRight = "instructionBoxRight" 
    boxWidth = 220
    killed = 0
    fadeOut = 0
    boxXOffset = 0
    z = 10
    arrowDir = 1
    
    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions1

    def render(self):
        if inEditor:
            WorldObject.render(self)
        elif self.alpha>0 and profiles[currentProfile].tutorials:
            PCR.setFontScale(font22,.75)
            longestText = 0
            for text in self.instructions:
                thisLine = PCR.stringWidth(text[0],font22)+ 24
                if thisLine > longestText:
                    longestText = thisLine
            if longestText >self.boxWidth:
                self.boxWidth = longestText
            self.drawArrow()
            self.drawBox()
            x = self.x - cameraX + self.xOffset+10 + self.boxXOffset
            y = self.y + self.yOffset+35

            for text in self.instructions:

                ScreenMessages.RenderMessageDirect(x,y,text,self.alpha)
                y += 35
            PCR.setFontScale(font22,1)     
    def drawArrow(self):
        PC.setColourize(1)
        color = int(128 + math.sin(self.life/10.0)*128)
        PC.setColour(color,color,color,int(self.alpha))
        arrowRes = JPG_Resources[self.instructionArrow]
        x = self.x-cameraX
        y = self.y-cameraY
        if self.arrowDir >0:
            PC.drawImage(arrowRes,x,y)
        else:
            width = PCR.imageWidth( arrowRes )
            height = PCR.imageHeight( arrowRes )
            PC.drawImageScaled(arrowRes,x,y,width*-1,height)
        PC.setColourize(0)
        
    def drawBox(self):
        PC.setColourize(1)
        color = 255
        PC.setColour(color,color,color,int(self.alpha))
        boxRes = JPG_Resources[self.instructionBoxLeft]
        x = self.x-cameraX+self.xOffset
        y = self.y-cameraY+self.yOffset
        PC.drawImage(boxRes,x,y)
        
        boxRes = JPG_Resources[self.instructionBoxRight]
        width = PCR.imageWidth( boxRes )
        x = self.x-cameraX+self.xOffset+self.boxWidth-width
        y = self.y-cameraY+self.yOffset
        PC.drawImage(boxRes,x,y)        
        
        PC.setColourize(0)


  
    def tick(self,delta):
        self.getInstructionPointer()
        self.life += delta
        if self.triggered and self.fadeOut==0:
            if self.alpha <255:
                self.alpha+= delta*5.0
                if self.alpha>255:
                    self.alpha = 255
        if self.fadeOut:
            if self.alpha >0:
                self.alpha-= delta*5.0
                if self.alpha<0:
                    self.alpha = 0  
                    self.x = -500  #remove from scene
       # print "alpha in mesage",self.alpha

class basicTutorial1(basicTutorial):
    name = "BasicTut1"
    instructions = messages.basicInstructions1
    placeable = 1
    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions1

    def tick(self,delta):
        if globalPlayer:
            if globalPlayer.PlatformOn:
                self.triggered = 1
            if self.triggered and globalPlayer.x + 50 > self.x:
                self.fadeOut = 1
                for object in objects:
                    if object.name == "BasicTut2":
                        object.triggered = 1
        basicTutorial.tick(self,delta)
    
class basicTutorial2(basicTutorial):
    name = "BasicTut2"
    instructions = messages.basicInstructions2
    placeable = 1   

    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions2

    def tick(self,delta):
        if globalPlayer:
            if self.triggered and globalPlayer.x + 50 > self.x:
                self.fadeOut = 1
                for object in objects:
                    if object.name == "BasicTut3" or object.name == "BasicTut4":
                        object.triggered = 1
        basicTutorial.tick(self,delta)
    
class basicTutorial3(basicTutorial):
    name = "BasicTut3"
    instructions = messages.basicInstructions3
    placeable = 1  
    xOffset = -320
    yOffset = 45
    instructionBoxLeft = "instructionBoxLeftRed"
    instructionBoxRight = "instructionBoxRightRed"
    instructionArrow = "InstructionArrowRed"
    arrowDir = -1

    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions3
    
    def tick(self,delta):
        if globalPlayer:
            if self.triggered and globalPlayer.x + 50 > self.x and globalPlayer.y < self.y:
                self.fadeOut = 1
                for object in objects:
                    if object.name == "BasicTut4":
                        object.fadeOut = 1
                    if object.name == "Basic5Tut5":
                        object.triggered = 1
        basicTutorial.tick(self,delta)
    
class basicTutorial4(basicTutorial):
    name = "BasicTut4"
    instructions = messages.basicInstructions4
    placeable = 1  
    yOffset = 45
    xOffset = -23

    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions4
    
class basicTutorial5(basicTutorial):
    name = "Basic5Tut5"
    instructions = messages.basicInstructions5
    placeable = 1 
    xOffset = -290  
    yOffset = 45 
    arrowDir = -1    
    
    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions5
    
    def tick(self,delta):
        if globalPlayer:
            if self.triggered and globalPlayer.x < self.x+50 and globalPlayer.y < self.y:
                self.fadeOut = 1
                for object in objects:
                    if object.name == "Basic6Tut":
                        object.triggered = 1
        basicTutorial.tick(self,delta)

class basicTutorial6(basicTutorial):
    name = "Basic6Tut"
    instructions = messages.basicInstructions6
    placeable = 1 
    xOffset = -302
    yOffset = 52 
    arrowDir = -1
    

    def getInstructionPointer(self):
        self.instructions = messages.basicInstructions6

    def tick(self,delta):  
        if globalPlayer:
            #print "ticking",self.name,self.triggered,self.fadeOut
            if self.triggered and globalPlayer.x > self.x and globalPlayer.y < self.y:
                self.fadeOut = 1    
            basicTutorial.tick(self,delta)  

class RandomPlatform100(WorldObject):
    validStart = 1
    name = 'Random100'
    graphic = 'RandomPlatform100'  

class RandomPlatform200(WorldObject):
    validStart = 1
    name = 'Random200'
    graphic = 'RandomPlatform200'   
    
class RandomPlatform400(WorldObject):
    validStart = 1
    name = 'Random400'
    graphic = 'RandomPlatform400'  

class collectable(physicsObject):  
    z = 75
    solid = 0
    name = 'Coin50'
    graphic = 'Coin50'
    collectedSound = 'collected'
    animation = None  
    collected = 0 
    speed = 0
    deltaX=0
    deltaY=0
    mspeed = 0
    inMagnet = 0
    initialY = 0
    static = 0
    def tick(self,delta):  
        if self.x < cameraX+780 and self.x >cameraX+10 and smartBomb.active():
            self.isCollected()
        switchToStaticTrigger = 2.5
        if  self.inMagnet == 0 and self.y_speed > switchToStaticTrigger:
            self.y = self.initialY
            self.y_speed = 0
            self.static = 1
        if(self.collected == 1):
            self.x_speed = self.deltaX * self.speed
            self.y_speed = self.deltaY * self.speed
            self.x += self.x_speed
            self.y += self.y_speed
            self.speed += 1.0
        elif self.inMagnet == 0 and magnetOn and globalPlayer:
              #first check to see if coin is in range of player
              if self.x < cameraX+780 and self.x >cameraX+10:
                  self.inMagnet = 1
        elif self.inMagnet and globalPlayer:
              #if captured then move towards the player
              self.mspeed +=0.25
              playerCentreX = globalPlayer.x+(globalPlayer.width/2*globalPlayer.scale)
              playerCentreY = globalPlayer.y+(globalPlayer.height/2*globalPlayer.scale)
              deltaX= playerCentreX-self.x
              deltaY = playerCentreY-self.y
              distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
              self.deltaX = deltaX/distance
              self.deltaY = deltaY/distance
              self.x_speed = self.deltaX * self.mspeed
              self.y_speed = self.deltaY * self.mspeed
              self.x += self.x_speed
              self.y += self.y_speed
              #self.speed += 1.0  
              WorldObject.tick(self,delta)            
        if self.inMagnet == 0:
            isOnSmashed = 0
            if globalPlayer:
                if globalPlayer.platformSmashed==self.PlatformOn:
                    isOnSmashed = 1
            if self.PlatformOn:
                if isOnSmashed:
                    self.isCollected()
                if self.PlatformOn.dynamic and self.collected==0:
                    self.x = self.PlatformOn.x+(self.PlatformOn.width/2.0)-(self.width/2.0)
                    self.y = self.PlatformOn.y-(self.height)
                WorldObject.tick(self,delta)
            elif self.static:
                WorldObject.tick(self,delta)
            else:
                physicsObject.tick(self,delta)       #tick the parent class  
            if(self.onGround==0 and self.oldPlatformOn != None):
                self.isCollected()  
    def spawn(self):
        self.initialY = self.y
  
    
    def isCollected(self):
        if(self.collected):
            return
        self.speed = 5.0
        deltaX= self.targetX+cameraX-self.x
        deltaY = self.targetY-self.y
        distance = math.sqrt((deltaX*deltaX)+(deltaY*deltaY))
        self.deltaX = deltaX/distance
        self.deltaY = deltaY/distance
        self.collected = 1
        self.frameNumber = 0
        thisPanning = (self.x-cameraX-400)/100
        if smartBomb.active() == 0:
            #print "playSimpleSound (self.collectedSound)",self.collectedSound
            playSimpleSound (self.collectedSound,panning = thisPanning)  
        
class PowerUp(collectable):
    startTimer = 10
    r = 0
    g = 0
    b = 0
    a = 140
    flash = 0
    PowerUpTypePtr = None

    def getInstructionPointer(self):
        return 0

    def isCollected(self):
        self.targetX = scoreX+350.0
        self.targetY = scoreY-100
        collectable.isCollected(self)
        
    def tick(self,delta): 
        global forcePause
        self.flash += delta
        if self.flash>128:
            self.flash = 0
        if self.y < -20:
            self.x = -300
            playSimpleSound("chime")
            self.collectionFinished()
            self.getInstructionPointer()
            if arcadeMode:
                ScreenMessages.setMessageScroll(self.instructions[0],None)
            else:    
                instructionManager.showInstruction(self.instructions) 
        collectable.tick(self,delta) 

    def render(self):
        WorldObject.render(self)
        lightRes = JPG_Resources["starburst100"]
        centreX = self.x+self.width/2
        centreY = self.y+self.height/2
        lightWidth = 60+(self.a)
        lightHeight = 60+(self.a)
        x = centreX- lightWidth/2
        y = centreY - lightHeight/2
        PC.setColourize(1)
        if self.flash <64:
            self.a = self.flash*2
        else:
            self.a = (128 - self.flash)*3
        if self.a<0:
            self.a = 0
        if self.a > 255:
            self.a = 255
        PC.setColour(int(self.r),int(self.g),int(self.b),int(self.a))
        PC.drawImageScaled(lightRes,x-cameraX,y-cameraY,lightWidth,lightHeight)
        PC.setColourize(0)

def arcadePowerUpGot(tokenIndex):
    if tokenIndex == WorldTypes.ArcadePowerUpStunJump:
        return  stunJumpEnabled
        
    if tokenIndex == WorldTypes.ArcadePowerUpHang:
        return hangEnabled
        
    if tokenIndex == WorldTypes.ArcadePowerUpSmash:
        return smashEnabled
        
    if tokenIndex == WorldTypes.ArcadePowerUpDash:
        return dashEnabled

    if tokenIndex == WorldTypes.ArcadePowerUpSpeed:
        if speedEnabled:
            if smartUsed:
                return 0
        return speedEnabled
    
    if tokenIndex == WorldTypes.ArcadePowerUpFairy:
        return  fairyEnabled
        
def updatePowerUpFlags(delta):
  
    global stunJumpEnabled
    global smashEnabled
    global hangEnabled
    global dashEnabled
    global fairyEnabled
    global speedEnabled
    global medalion
  
    stunJumpEnabled = 0
    smashEnabled = 0
    hangEnabled = 0
    dashEnabled = 0
    fairyEnabled = 0
    speedEnabled = 0
    
#comment this back in for cheat    
   # stunJumpEnabled = 1
        
    if cheatCanvas.AllPowerOn:
        stunJumpEnabled = 1
        smashEnabled = 1
        hangEnabled = 1
        dashEnabled = 1
        fairyEnabled = 1
        speedEnabled = 1 

    elif arcadeMode==0:
        hangEnabled = profiles[currentProfile].hangEnabled
        stunJumpEnabled = profiles[currentProfile].stunJumpEnabled
        dashEnabled = profiles[currentProfile].dashEnabled
        smashEnabled = profiles[currentProfile].smashEnabled
        if smartUsed == 0:
            speedEnabled = profiles[currentProfile].speedEnabled
        fairyEnabled = profiles[currentProfile].fairyEnabled                 
    else:
        hangEnabled = profiles[currentProfile].arcadeHangEnabled or profiles[currentProfile].hangEnabled
        stunJumpEnabled = profiles[currentProfile].arcadeStunJumpEnabled or profiles[currentProfile].stunJumpEnabled
        dashEnabled = profiles[currentProfile].arcadeDashEnabled or profiles[currentProfile].dashEnabled
        smashEnabled = profiles[currentProfile].arcadeSmashEnabled or profiles[currentProfile].smashEnabled
        if smartUsed == 0:
            speedEnabled = profiles[currentProfile].arcadeSpeedEnabled or profiles[currentProfile].speedEnabled
        fairyEnabled = profiles[currentProfile].arcadeFairyEnabled or profiles[currentProfile].fairyEnabled                

  
    if medalion != None:
        if cheatCanvas.AllPowerOn:
            medalion.setSegmentStatus(Medalion.Hang,1)
            medalion.setSegmentStatus(Medalion.Stun,1)
            medalion.setSegmentStatus(Medalion.Dash,1)
            medalion.setSegmentStatus(Medalion.Smash,1)
            medalion.setSegmentStatus(Medalion.Fairy,1)
            medalion.setSegmentStatus(Medalion.Speed,1)
        else:
            medalion.setSegmentStatus(Medalion.Hang,hangEnabled)
            medalion.setSegmentStatus(Medalion.Stun,stunJumpEnabled)
            medalion.setSegmentStatus(Medalion.Dash,dashEnabled)
            medalion.setSegmentStatus(Medalion.Smash,smashEnabled)
            medalion.setSegmentStatus(Medalion.Fairy,fairyEnabled)
            medalion.setSegmentStatus(Medalion.Speed,speedEnabled) 
 
class PowerUpHang(PowerUp):
    r = 64
    g = 64
    b = 255
    graphic = "Token01"
    name = "HangToken"
    instructions = messages.HangInstructions

    def getInstructionPointer(self):
        self.instructions = messages.HangInstructions
    
    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):
            profiles[currentProfile].hangEnabled = 1 
            
    def canBePlaced(self):
        if profiles[currentProfile].hangEnabled==1 or arcadeMode:
            return 0
        else:
            return 1
            
class PowerUpstunJump(PowerUp):
    r = 200
    g = 32
    b = 200
    graphic = "Token03"
    name = "DoubleJumpToken"
    instructions = messages.stunJumpInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.stunJumpInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):
            profiles[currentProfile].stunJumpEnabled = 1   
        
    def canBePlaced(self):
        if profiles[currentProfile].stunJumpEnabled==1 or arcadeMode:
            return 0
        else:
            return 1      

class ArcadePowerUp(PowerUp):
    placeable = 0
    centreTrack = 0
    def tick(self,delta):
        tempX = self.x
        PowerUp.tick(self,delta)
        if self.collected==0:
            self.x = tempX-delta/2.5
            self.y = self.centreTrack + math.sin(self.life/60)*160
            
class ArcadePowerUpHang(ArcadePowerUp):
    r = 64
    g = 64
    b = 255
    graphic = "Token01"
    name = "AHangToken"
    instructions = messages.HangInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.HangInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):
        profiles[currentProfile].arcadeHangEnabled = 1  
            
class ArcadePowerUpStunJump(ArcadePowerUp):
    r = 200
    g = 32
    b = 200
    graphic = "Token03"
    name = "AStunJumpToken"
    instructions = messages.stunJumpInstructions

    def getInstructionPointer(self):
        self.instructions = messages.stunJumpInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):
        profiles[currentProfile].arcadeStunJumpEnabled = 1 
            
class ArcadePowerUpDash(ArcadePowerUp):
    r = 10
    g = 0
    b = 200
    graphic = "Token04"
    name = "ADashToken"
    instructions = messages.DashInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.DashInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):     
        profiles[currentProfile].arcadeDashEnabled = 1   #was dash now JUMP!!!!
            
class ArcadePowerUpSmash(ArcadePowerUp):
    r = 64
    g = 255
    b = 32
    graphic = "Token02"
    name = "ASmashToken"
    instructions = messages.SmashInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.SmashInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):  
        profiles[currentProfile].arcadeSmashEnabled = 1
            
class ArcadePowerUpFairy(ArcadePowerUp):
    r = 255
    g = 64
    b = 48
    graphic = "Token06"
    name = "AFairyToken"
    instructions = messages.FairyInstructions

    def getInstructionPointer(self):
        self.instructions = messages.FairyInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self): 
        profiles[currentProfile].arcadeFairyEnabled = 1   
            
class ArcadePowerUpSpeed(ArcadePowerUp):
    r = 255
    g = 0
    b = 0
    graphic = "Token05"
    name = "ASpeedToken"
    instructions = messages.SpeedInstructions

    def getInstructionPointer(self):
        self.instructions = messages.SpeedInstructions
    
    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self): 
        profiles[currentProfile].arcadeSpeedEnabled = 1    
        global smartUsed
        smartUsed = 0
            
class PowerUpDash(PowerUp):
    r = 10
    g = 0
    b = 200
    graphic = "Token04"
    name = "DashToken"
    instructions = messages.DashInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.DashInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):        
        profiles[currentProfile].dashEnabled = 1  
        
    def canBePlaced(self):
        if profiles[currentProfile].dashEnabled==1 or arcadeMode:
            return 0
        else:
            return 1    
  
class PowerUpSmash(PowerUp):
    r = 64
    g = 255
    b = 32
    graphic = "Token02"
    name = "SmashToken"
    instructions = messages.SmashInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.SmashInstructions

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self):   
        profiles[currentProfile].smashEnabled = 1
        
    def canBePlaced(self):
        if profiles[currentProfile].smashEnabled==1 or arcadeMode:
            return 0
        else:
            return 1    
   
class PowerUpFairy(PowerUp):
    r = 255
    g = 64
    b = 48
    graphic = "Token06"
    name = "FairyToken"
    instructions = messages.FairyInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.FairyInstructions   

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self): 
        profiles[currentProfile].fairyEnabled = 1
        
    def canBePlaced(self):
        if profiles[currentProfile].fairyEnabled==1 or arcadeMode:
            return 0
        else:
            return 1 
            
class PowerUpSpeed(PowerUp):
    r = 255
    g = 0
    b = 0
    graphic = "Token05"
    name = "SpeedToken"
    instructions = messages.SpeedInstructions
    
    def getInstructionPointer(self):
        self.instructions = messages.SpeedInstructions   

    def isCollected(self):
        PowerUp.isCollected(self)
        
    def collectionFinished(self): 
        profiles[currentProfile].speedEnabled = 1
        
    def canBePlaced(self):
        if profiles[currentProfile].speedEnabled==1 or arcadeMode:
            return 0
        else:
            return 1   
            
class Coin(collectable):
    solid = 0
    name = 'Coin50'
    graphic = 'coin01'
    collectedSound = 'coinCollected'
    animation = animationSets.coin50_loop   
    value = 50
    
    def isCollected(self):
        self.targetX = scoreX+160.0
        self.targetY = scoreY-100
        collectable.isCollected(self)
    
    def tick(self,delta): 
        global coinsCollected
        global missedCoin
        if(self.y < scoreY and self.collected):
            self.x = cameraX-600 #  move out of world
            self.y = 300
            #print "coin collected",coinsCollected
            incScore(self.value) 
            coinsCollected += 1  
        collectable.tick(self,delta)
        if self.x+self.width<cameraX and missedCoin ==0 and arcadeMode == 0 and self.collected==0 and levelCompleted(finalLevel):
            self.x = -300
            ScreenMessages.setMessageScroll(messages.MissedACoin,None)   
            missedCoin = 1
        
class Coin50(Coin):
    name = 'Coin50'
    graphic = 'coin01'
    collectedSound = 'coinCollected'
    animation = animationSets.coin50_loop   
    value = 50
    
class Coin250(Coin):
    name = 'Coin250'
    graphic = '250Coin01'
    collectedSound = 'coinCollected'
    animation = animationSets.coin250_loop  
    value = 250
    
class Coin1000(Coin):
    name = 'Coin1000'
    graphic = '1000Coin01'
    collectedSound = 'coinCollected'
    animation = animationSets.coin1000_loop  
    value = 1000

class OneUp(collectable):
    solid = 0
    name = 'OneUp'
    graphic = 'OneUp_01' 
    animation = animationSets.oneUp_loop 
    
    def isCollected(self):
        self.targetX = 800-((lives)*44)
        self.targetY = scoreY-30
        collectable.isCollected(self)
    
    def tick(self,delta): 
        if self.x > cameraX+800 and lives>8 and arcadeMode:
            self.x = -300 #remove from the world
        if(self.y < 20 and self.collected):
            self.x = cameraX-600 #  move out of world
            IncrementLife(1) 
        collectable.tick(self,delta)     

class Bomb(collectable):
    solid = 0
    name = 'Bomb01'
    graphic = 'Bomb01' 
    animation = animationSets.bomb_loop
    
    def isCollected(self):
        self.targetX = 700
        self.targetY = 300
        collectable.isCollected(self)
    
    def tick(self,delta): 
        global bombExplosion
        if(self.collected):
            if gridType ==1:
                trailGame.emptytrail(1)
            else:
                bombExplosion = 1
                detonateGrid()
            particleController.addItem(bigExplosion(),self.x,self.y,1)
            self.x = cameraX-600 #  move out of world  
        collectable.tick(self,delta)   
        
class LevelKey(collectable):
    solid = 0
    name = 'LevelKey'
    graphic = 'Key03' 
    animation = animationSets.key_loop
    keyIndex = 0
    instructions = None
    
    def isCollected(self):
        self.targetX = gridRight+(800-gridRight)/2
        self.targetY = 0
        if self.collected == 0:
            playSimpleSound("chime")
            if profiles[currentProfile].keysCollected< self.keyIndex:
                profiles[currentProfile].keysCollected = self.keyIndex 
            instructionManager.showInstruction(self.instructions) 
        collectable.isCollected(self)
    def tick(self,delta):
        if self.keyIndex <= profiles[currentProfile].keysCollected:
            self.x = -300
        collectable.tick(self,delta)
        
class Level1Key(LevelKey):
    name = 'Level1Key'
    keyIndex = 1
    instructions = messages.jungleKeyInstructions
    
class Level2Key(LevelKey):
    name = 'Level2Key' 
    keyIndex = 2  
    instructions = messages.caveKeyInstructions    
    
class Level3Key(LevelKey):
    name = 'Level3Key'  
    keyIndex = 3
    instructions = messages.parkKeyInstructions

class Level4Key(LevelKey):
    name = 'Level4Key'  
    keyIndex = 4
    instructions = messages.cellarKeyInstructions
    
class ClockUp(WorldObject):
    solid = 0
    name = 'ClockUp'
    graphic = 'clockUp' 
    
    def render(self):
        if inEditor:    #only render speed up clock if in editor
            WorldObject.render(self)
    
    def tick(self,delta):
        if self.x < cameraX+400 and scrollManager != None:
            self.x = -300
            scrollManager.incremementScrollDash(delta)


class Clock(collectable):
    solid = 0
    name = 'Clock'
    graphic = 'clock01' 
    animation = animationSets.clock_loop
    
    def isCollected(self):
        self.targetX = gridRight+(800-gridRight)/2
        self.targetY = 300
        collectable.isCollected(self)
        particleController.addItem(clockExplosion(),self.x+100,self.y-100,1)
        self.x = cameraX-600 #  move out of world
        scrollManager.clockCollected()
    
    def tick(self,delta): 
        deltaY = self.y - self.targetY
        collectable.tick(self,delta)
        newDeltaY = self.y - self.targetY
            
class Magnet(collectable):
    solid = 0
    name = 'Magnet'
    graphic = 'Magnet01' 
    animation = animationSets.magnet_loop
    magnetCount = 0
    messageGo = 0
    effectScale = 0
    magnetLife = 0
    seconds = 20
    milliseconds = 100
    
    def isCollected(self):
        global magnetOn
        if self.collected == 0:
            collectable.isCollected(self)
            self.milliseconds = 100
            self.seconds = 20
            self.messageGo = 1   
            magnetOn = 1
            ScreenMessages.setMessageScroll(messages.Blank36,None,str(self.seconds)) 
            playSimpleSound("magnet",1)  
    
    def tick(self,delta): 
        global magnetOn
        if self.collected:
            self.magnetLife += delta
            self.milliseconds -= delta 
            if self.x>0:
                magnetOn = 1
            if(self.milliseconds<=0):
                self.milliseconds = 100
                self.seconds -= 1   
                playSimpleSound("magnet",1)                
                if(self.seconds ==0):
                    self.x = -600 #  move out of world 
                    magnetOn = 0
                ScreenMessages.setMessageScroll(messages.Blank36,None,str(self.seconds)) 
            if self.effectScale < 1:
                self.effectScale += delta/20
        else:
            collectable.tick(self,delta)        


    def render(self):
        if self.collected == 0:
            collectable.render(self)
        if globalPlayer and self.collected:
            playerCentreX = globalPlayer.x+(globalPlayer.width/2.0*globalPlayer.scale)
            playerCentreY = globalPlayer.y+(globalPlayer.height/2.0*globalPlayer.scale)
            self.x = globalPlayer.x
            magnetEffect =  JPG_Resources["gradedCircle100"]
            effectRadius = self.milliseconds*2
            effectX = playerCentreX-effectRadius
            effectY = playerCentreY-effectRadius
            effectDiameter = effectRadius*2
            PC.setColourize(1)
            PC.setColour( 100,100,255,120)
            PC.drawmodeAdd()
            PC.drawImageScaled( magnetEffect, effectX-cameraX, effectY,effectDiameter,effectDiameter)
            PC.drawmodeNormal()
            
            

    

class CSObject(WorldObject):
    placeable = 0
    z = 40
    hitPoints = 1
    solid = 0
    targetX = 0
    targetY = 0
    distanceToTarget = 0
    speed = 0
    maxSpeed = 20
    scale = 1.5
    targetScale = 1.5
    velocityX=0
    velocityY=0
    masterAlpha = 1.0
    
    def tick(self,delta):
        WorldObject.tick(self,delta)
        deltaX = self.targetX-self.x
        deltaY = self.targetY-self.y
        self.distanceToTarget = math.sqrt((deltaX* deltaX)+(deltaY*deltaY))
        if self.distanceToTarget > 1:
            speed = math.sqrt(self.distanceToTarget)/10
            if speed>self.maxSpeed:
               speed = self.maxSpeed
            self.velocityX = (deltaX/self.distanceToTarget)*speed*delta
            self.velocityY = (deltaY/self.distanceToTarget)*speed*delta   
            self.x += self.velocityX
            self.y += self.velocityY
            if self.velocityX <0:
                self.facing = -1
            else:
                self.facing = 1


class CSFairy(CSObject):
    name = 'CSFairy'
    graphic = 'Fairy01'
    animation = animationSets.fairy_move  
    facing = 1
    maxSpeed = 6

    def render(self):
        if self.velocityX<0:
            self.facing = 1
        else:
            self.facing = -1
        WorldObject.render(self)
        particle = fairyRedTrailParticle()
        x = self.x
        y = self.y + 26
        if(self.facing<0):
            x += 120
        else:
            x += 0
        
        particleController.addItem(particle,cameraX+x,y,0.3,0,0)
        makeSparkleParticle(cameraX+x,y,0,0,2)

class CSJake(CSObject):
    name = 'CSPlayer'
    graphic = 'player_walk_01'
    animation = animationSets.player_walk
    maxSpeed = 40
    
    def tick(self,delta):
        if self.velocityX< 0.25:
            self.animation = animationSets.player_idle    
        CSObject.tick(self,delta)
        
class CSAmulet(CSObject):
    name = 'CSAmulet'
    maxSpeed = 40
    graphic = 'BigAmuletUnited01'    
    targetY = 200
    def tick(self,delta): 
        CSObject.tick(self,delta)   
        medalion.tick(delta)

        
    def render(self):
        medalion.render(self.x,self.y,0,1)
        return 0 
        
class CSFireWorks(CSObject):
    name = 'CSFireWork'
    graphic = 'coin01'    
    def tick(self,delta): 
        CSObject.tick(self,delta)  
        #(x,y,deltaX,deltaY,maxSize,h_bias,v_bias)
        if int(self.life)%4 == 0:
            self.launchFireWork(delta)
        
    def render(self):
        return 0
        
    def launchFireWork(self,delta):
        x = random.randint(100,700)
        y = 600
        deltaX = 5 - (random.randint(0,30)/3)
        deltaY = -3
        maxSize = 1.0
        h_bias = 400
        v_bias = 0
        makeFireWorkParticle(x,y,deltaX,deltaY,maxSize,h_bias,v_bias)        
        
    def render(self):
        return 0 
        
class CSLightBeam(CSObject):
    name = 'CSBeam'
    graphic = 'lightBeam2'
#    animation = animationSets.player_walk
    maxSpeed = 0
    
    def tick(self,delta):    
        CSObject.tick(self,delta)
        
    def render(self):
        PC.setColourize(1)
        alpha = self.life*2
            
        if alpha > 255:
            alpha = 900 - (self.life*2)
        alpha = clamp255(alpha)
        PC.setColour( 255,255,255,int(alpha) )
        PC.drawmodeNormal()
        graphicName = JPG_Resources[self.graphic]
        width = PCR.imageWidth( graphicName )*1.5
        height = PCR.imageHeight( graphicName )*1.5
        PC.drawImageScaled( graphicName, self.x, self.y,width,height)
      
    
class CSSpell(CSObject):
    name = 'CSFairy'
    graphic = 'spell01'
    maxSpeed = 5
    count = 0


        
    def tick(self,delta):
        self.count += 1
        if self.count%3==0:
            randomX = random.randint(0,15)
            randomY = random.randint(0,15)
            particleController.addItem(spellParticle(),self.x+randomX,self.y+randomY,1)
        deltaX = self.targetX-self.x
        deltaY = self.targetY-self.y
        self.distanceToTarget = math.sqrt((deltaX* deltaX)+(deltaY*deltaY))
        if self.distanceToTarget > self.maxSpeed*delta:
            speed = self.maxSpeed
            velocityX = (deltaX/self.distanceToTarget)*speed*delta
            velocityY = (deltaY/self.distanceToTarget)*speed*delta   
            self.x += velocityX
            self.y += velocityY

        if self.distanceToTarget!=0 and  self.distanceToTarget < self.maxSpeed*delta and self.x>0:
            particleController.addItem(spellExplosion(),self.targetX,self.targetY,1)
            self.x = -300
            self.targetX = -300
        CSObject.tick(self,delta)


class HUDElement(WorldObject):
    upGraphic = 'Button100Up'
    downGraphic = 'Button100Down'
    GUIElement = 1
    graphic = upGraphic
    placeable = 0   #set to 0 if not placeale
    string = "placeholder"
    def buttonDown(self):
        self.graphic = self.downGraphic
    def buttonUp(self):
        self.graphic = self.upGraphic
    def render(self):
            texture = JPG_Resources[self.graphic]
            PC.drawImage( texture, self.x,self.y)
            PC.setColour( 255,0,0,255)
            PC.setFont( font22 )
            PC.drawString(self.string, self.x+5, self.y+40 )
            
def checkForAlreadythere(x,y,width):
    right = x+width
    bottom = y+60
    for object in objects:
        if object.solid and object.y < bottom  and object.y+60 > y:
            if (object.x < right) and (x < object.x+object.width):
                return 1
    return 0        
            
class PlatormSpawner(WorldObject):
    nextSpawnX = 0
    spawnInterval = 260
    solid = 0
    canSpawn = 1
    spawner = 1
    endSpawnX = 0
    resolution = .0018
    y_scale = 200
    spawnRange = (44/7)/resolution
    y_pitch = 100
    
    def editorTick(self,delta): #ticks exactly the same in game and editor
        self.tick(delta)
      
      
    def tick(self,delta):
        if cameraX+x_max+100 > self.nextSpawnX+self.x:
            if cameraX+x_max+100 < self.x+self.spawnRange:
                self.setUpSpawn(self.nextSpawnX+self.x,self.y)
                self.nextSpawnX += self.spawnInterval
       # print "spawnRange",self.spawnRange
    
    def doSpawn(self,x,y):
        if (y>50 and y <580 and self.canSpawn):
            y = ((int(y/PlatformPitchY))*PlatformPitchY)+4
            if checkForAlreadythere(x,y,self.width)==0:
                type= getRandomPlatform(levelMetaData.RandomTiles) 
                platformIDX=levelData.platform100   #default!
                object = addObject(nextID,x,y,type,platformIDX)
                object.platformIDX=levelData.platform100   #default!
                object.canBeSaved = 0
                object.colourize=1
                object.tinta=80
    
    def render(self):
        if inEditor==1:
            WorldObject.render(self)
          
class SpawnDiamond(PlatormSpawner):
  #not used any more
    name = "SpawnDiamond"
    graphic = "SpawnDiamond"
    toSpawn = 1
    toSpawnMax = 5
    spawnDirection = 1
    spawnInterval=260
    spawnRange = (toSpawnMax-1)*spawnInterval*2
    y_scale = 100
        
    def setUpSpawn(self,x,baseY):
        y = baseY - (((self.toSpawn-1.0)/2.0)*self.y_scale)
        for count in range(self.toSpawn): 
            self.doSpawn(x,y)
            y += self.y_scale
        self.toSpawn += self.spawnDirection
        if(self.toSpawn > self.toSpawnMax):
            self.spawnDirection = -1
            self.toSpawn = self.toSpawnMax-1
        if(self.toSpawn <= 1):
            self.spawnDirection = 1
            self.toSpawn = 2
            
class SpawnFillSine(PlatormSpawner):
    name = "SpawnFillSine"
    graphic = "SpawnFillSine"
    
    def setUpSpawn(self,x,baseY):
        y = baseY + math.sin((x-self.x)*self.resolution)*self.y_scale
        yEnd = baseY - math.sin((x-self.x)*self.resolution)*self.y_scale
        if(y>yEnd):
            temp = y
            y = yEnd
            yEnd = temp
        while y <= yEnd: 
            self.doSpawn(x,y)
            y += self.y_pitch
            
class SpawnSine(PlatormSpawner):
    name = "SpawnSine"
    graphic = "SpawnSine"
    
    def setUpSpawn(self,x,baseY):
        y = baseY - math.sin((x-self.x)*self.resolution)*self.y_scale
        self.doSpawn(x,y)
        
class SpawnInvSine(PlatormSpawner):
    name = "SpawnInvSine"
    graphic = "SpawnInvSine"
    
    def setUpSpawn(self,x,baseY):
        y = baseY + math.sin((x-self.x)*self.resolution)*self.y_scale
        self.doSpawn(x,y)        
 
class SpawnCos(PlatormSpawner):
    name = "SpawnCos"
    graphic = "SpawnCos"
    
    def setUpSpawn(self,x,baseY):
        y = baseY - math.sin((x-self.x)*self.resolution)*self.y_scale
        y = baseY - math.cos((x-self.x)*self.resolution)*self.y_scale
        self.doSpawn(x,y)        

class SpawnBlock(PlatormSpawner):
    name = "SpawnBlock"
    graphic = "SpawnBlock"
    spawnInterval = 300
    spawnRange = 1200
    
    def setUpSpawn(self,x,baseY):
        y = baseY -250
        yEnd = baseY +250

        while y <= yEnd: 
            self.doSpawn(x,y)
            y += self.y_pitch
            
class SpawnLine(PlatormSpawner):
    name = "SpawnLine"
    graphic = "SpawnLine"
    spawnInterval = 300
    spawnRange = 2400
    
    def setUpSpawn(self,x,y):
        self.doSpawn(x,y)

class ExitButton(HUDElement):
    string = "Exit Game"
    def buttonDown(self):
        global doExit

        HUDElement.buttonDown(self)
       #doExit = 1

class scrollManagerClass:
    slowDown = 0
    slowDownSet = 1001
    fastAgain = 0
    initialStorySpeed = 0.45
    initialArcadeSpeed = .45
    scrollSpeed = .3
    messagetimer = 0
    messageGo = 0
    speedIncrement = 0.000001
    ADSpeed = 0
    scrollDashMode = 0
    scrollDashModeTarget = 0
    dashIncrement = 0.5
    adaptiveScrollTarget = 1
    adaptiveScroll = 1
    
    def setScrollSpeed(self):
        if arcadeMode:
            tempLevel = math.sqrt(levelNumber)
            self.scrollSpeed =0.5 + (tempLevel/20.0 + (adaptive.getScroll()/8.0))
        else:
            self.scrollSpeed =levelMetaData.scrollSpeed/5.0   
        if  self.scrollSpeed < 0.3:
            self.scrollSpeed = 0.3
            
    def ressetScroll(self):
        self.setScrollSpeed()
        self.ADSpeed = 0
        self.slowDown = 0
        self.messagetimer = 0
        self.fastAgain = 0
        self.messageGo = 0
        self.scrollDashMode = 0    #set this to make the game scroll really fast
        
    def clearDashMode(self):
        self.scrollDashMode = 0
        self.scrollDashModeTarget = 0
        
    def incremementScrollDash(self,delta):
#        print "incrementing speed",self.dashIncrement
        self.scrollDashModeTarget += self.dashIncrement
        particleController.addItem(clockExplosion(),cameraX+400,cameraY+300,1)        
        ScreenMessages.setMessageScroll(messages.SpeedUp,None,None)        
        incTargetpitch(1)
        
    def clockCollected(self):
        self.slowDown = self.slowDownSet
        self.scrollDashModeTarget = 0
        setTargetpitch(-5)
        setTargetVolume(.3)
        
    def disableDash(self):
        self.scrollDashModeTarget = 0
        setTargetpitch(0)
        if self.scrollDashModeTarget:
            setTargetVolume(1)
        
    def tick(self,delta):
        if self.scrollDashMode < self.scrollDashModeTarget:
            self.scrollDashMode += delta/500
        if self.scrollDashMode >  self.scrollDashModeTarget:
            self.scrollDashMode =  self.scrollDashModeTarget
        if(self.slowDown>0):
            self.slowDown -= delta
            self.messagetimer -= delta
            if(self.slowDown <=0):
                self.slowDown=0
                self.fastAgain = 1
                setTargetpitch(0)
                setTargetVolume(1)
                playSimpleSound("bell",1)
            if(self.messagetimer<=0):
                self.messageGo =1 
                self.messagetimer = self.slowDownSet/10
            
    def render(self):
        if(self.fastAgain):  
            self.fastAgain = 0
        if(self.messageGo):
            if int(self.slowDown/100)%2:
                playSimpleSound("tick",1)
            else:
                playSimpleSound("tock",1)
            ScreenMessages.setMessageScroll(messages.Blank36,None,str(int(self.slowDown/100)+1))  
            self.messageGo = 0
 
    def setADSpeed(self,playerX,delta):
        global levelTimeDelta
        ADOffset = 150
        ADStart = x_max-ADOffset+cameraX
        ADEnd = ADOffset+cameraX
        gameSpeed = self.scrollSpeed
        maxADSpeed = gameSpeed*0.5
        if(playerX> ADStart):
            self.scrollSpeed += delta * (self.scrollSpeed/1000.0)
        levelTimeDelta += self.ADSpeed
       # print "scroll speed",self.scrollSpeed

    def getScrollSpeed(self,delta):
        speed = delta*self.scrollSpeed
        if(self.slowDown):
            speed /=4.0
        if startLevelTimer>0:
            speed = 0
        speed += (self.scrollDashMode*delta/1.666)
#        speed *= (self.adaptiveScroll)
        if gameOver or metaGame != menuItems.game or gamePaused:
            speed = 0
#        print "scroll speed",speed
        return speed

scrollManager = scrollManagerClass()

class TileObject:
    colour = 'none' #only needed till I remove this
    toRemove = 0
    checked = 0
    XOffset = 0
    YOffset = 0
    YSpeed= 0
    XSpeed = 0
    explosiontriggered=0
    hint = 0
    jewelIDX = 0
    
    
AllWorldObjects = [Player(),PlayerSubGame(),DynamicPlatform(),StaticPlatform(),RedPlatform(),GreenPlatform(),BluePlatform(),FinishPlatform(),RandomPlatform100(),Bomb(),KillerOrange(),DynamicVerticalPlatform(),StaticPlatform200(),StaticPlatform400(),Snail(),OneUp(),Coin50(),Spider(),Web(),RotatingPlatformSpawn(),RotatingPlatformRed(),RotatingPlatformGreen(),RotatingPlatformBlue(),RotatingPlatform(),RotatingPlatformWhite(),WhitePlatform(),RotatingPlatformBlack(),BlackPlatform(),ExitButton(),Wasp(),LargeSnail(),LargeSpider(),OrangePlatform(),PurplePlatform(),YellowPlatform(),PlayerGhostUp(),PlayerGhostDown(),Clock(),CollectedJewel(),SmallBall(),StagingPlatform(),PowerUpHang(),PowerUpSmash(),PowerUpstunJump(),PowerUpDash(),PowerUpSpeed(),PowerUpFairy(),Stem100(),Stem200(),Stem400(),ExitPlatform(),BigBall(),Fairy(),BigTrampoline(),SpawnSine(),SpawnBlock(),SpawnDiamond(),SpawnInvSine(),SpawnFillSine(),SpawnCos(),SmallBat(),SwingLong(),SwingMedium(),SwingVeryLong(),Acid(),fastDynamicPlatform(),RandomPlatform400(),RandomPlatform200(),ClockUp(),fastDynamicVerticalPlatform(),MedTrampoline(),SmallTrampoline(),BigBat(),CSFairy(),CSJake(),CSSpell(),CoinWheel(),SmallWheel(),SmallCoinWheel(),CoinFinishPlatform(),Level1Key(),ArcadePowerUpHang(),ArcadePowerUpSmash(),ArcadePowerUpStunJump(),ArcadePowerUpDash(),ArcadePowerUpSpeed(),ArcadePowerUpFairy(),Coin250(),Coin1000(),Magnet(),Level2Key(),Level3Key(),Level4Key(),RWasp(),Balloon(),Conveyor(),ConveyorPlatform(),CellarWheel(),CellarRotatingPlatform(),CoinCellarWheel(),fireBall(),SpawnLine(),StripePlatform(),DoubleCellarWheel(),SmallCellarWheel(),CSLightBeam(),CSAmulet(),CSFireWorks(),Tutorial(),basicTutorial1(),basicTutorial2(),basicTutorial3(),basicTutorial4(),basicTutorial5(),basicTutorial6()]


def ReachedFinish():
    global FinishFlag
    FinishFlag = 1
#    playSimpleSound("IMadeIt1")    
 
def ReachedExit():
    global ExitFlag
    global FinishFlag
    ExitFlag = 1        #mark exit flag set so we know we can't finish
    FinishFlag = 1

def ReachedStaging():
    global StagingFlag
    if(StagingFlag ==1):
        StagingFlag = 0     #Cleared when the player reaches the next staging
  #      ScreenMessages.setMessageScroll(messages.NextLevel,None)
  #      ScreenMessages.setMessageScroll(messages.Blank36,None,levelMetaData.title)
        #doBonus()
    
     
def IncrementLife(increment):
    global lives
    lives += increment
    ScreenMessages.setMessageScroll(messages.OneUP,None)
    
def SaveLevelData(levelName):
    global ObjectStarts
    thisLevelMetaData = LevelMetaDataClass()
#currentLevelFile is set by the level load.  A level must always be loaded before we edit it!
    if editorEnabled == 1:
      
        saveFile = open( "res\\levels\\"+levelMetaData.currentLevelFile+".jld", "w" )
    else:
        try:
            os.mkdir(localAppData+"\\GoOllie\\levels")
        except:
            print("directory found")
        saveFile = open( localAppData+"\\GoOllie\\levels\\"+levelName+".jld", "w" )
    saveFile.write(str(levelMetaData.currentSectionNumber)+"\n") #write section number
    saveFile.write(str(levelMetaData.RandomTiles)+"\n") #write jewel option numbers
    for thisEntry in ObjectStarts:
        for field in thisEntry:
            saveFile.write(str(field)+"\n")
        saveFile.write("RecordEnd\n")
    saveFile.close()
 
class Scenery:
    name = ''
    X = 0
    width = 0
    height = 0
    
def setUpNextLevel():
    global levelNumber
    if arcadeMode:
        levelNumber += 1
        thisLevel = levelData.arcadeCampaign[levelNumber]
        mapName = thisLevel[1]
        if mapName in map_Resources:
            launchArcadeToken()
            if profiles[currentProfile].arcadeProgress < levelNumber:
                profiles[currentProfile].arcadeProgress = levelNumber 
            setUpLevelData()
            scrollManager.ressetScroll()  
        else:
            fadeManager.fadeDown(menuItems.sellUpCanvas)
            global gameOver
            gameOver = 1
 

def setUpNextRandomEnemySpawn():
    distanceToSpawn = random.randint(1000,3000)
    distanceToSpawn -= levelMetaData.randomSpawnEnemy*50
    if distanceToSpawn<600:
        distanceToSpawn = 600
    levelMetaData.nextEnemySpawn = cameraX + distanceToSpawn
#    print "next random spawn",levelMetaData.nextEnemySpawn
    
    
randomEnemyTypes = [ WorldTypes.SmallBat,WorldTypes.KillerOrange,WorldTypes.Wasp,WorldTypes.BigBat,WorldTypes.fireBall]
    
def tickRandomEnemySpawn(delta):
    if levelNumber > levelsInArcde:
        if cameraX > levelMetaData.nextEnemySpawn:
            if arcadeMode:
                numberRange =1+ ((levelNumber-levelsInArcde)/levelsPerArcadeSegment)
                numberToSpawn = random.randint(1,numberRange)
                spawnTypeRange = 1+(levelNumber-levelsInArcde)/4
                if spawnTypeRange>4:
                    spawnTypeRange = 4
                numberToSpawn = random.randint(1,numberRange)
                typeToSpawnIdx = random.randint(0,spawnTypeRange)
                x = cameraX+1000
                for a in range(numberToSpawn):
                    y = random.randint(150,450)
                    object = addObject(nextID,x,y,randomEnemyTypes[typeToSpawnIdx])
                    x += 80
        
            setUpNextRandomEnemySpawn()


def setUpLevelData():
    global ObjectStarts
    global levelMetaData    
    levelMetaData.nextEnemySpawn = 0
    levelMetaData.randomSpawnEnemy = 0
    if(arcadeMode==1):
        thisLevelIdx = levelNumber
        while thisLevelIdx > levelsInArcde:
            thisLevelIdx -= levelsPerArcadeSegment
        thisLevel = levelData.arcadeCampaign[thisLevelIdx]
    else:
        thisLevel = levelData.storyCampaign[levelNumber]
    levelMetaData.currentLevelFile = thisLevel[1]
    levelMetaData.currentSectionNumber = map_Section[levelMetaData.currentLevelFile]
    levelMetaData.currentSection = levelData.sectionList[levelMetaData.currentSectionNumber]
    levelMetaData.currentLevelFile = thisLevel[1]
    levelMetaData.RandomTiles = map_Jewels[levelMetaData.currentLevelFile]
    if arcadeMode: 
        if levelNumber < levelsInArcde+1:
            if levelMetaData.RandomTiles>7:
                levelMetaData.RandomTiles = 7
        else:
            levelMetaData.RandomTiles = 9  
            levelMetaData.randomSpawnEnemy =  (levelNumber-levelsInArcde)   
            setUpNextRandomEnemySpawn()          
#    print "Random Tiles",levelMetaData.RandomTiles,levelNumber
    levelMetaData.RandomSpawn = thisLevel[3]
    levelMetaData.sequence = thisLevel[4]
    levelMetaData.title = thisLevel[5]
    levelMetaData.Instructions = thisLevel[6]
    levelMetaData.midInstructions = thisLevel[9]    
    levelMetaData.levelNumber = thisLevel[10]
    ObjectStarts = map_Resources[levelMetaData.currentLevelFile]
    levelMetaData.scrollSpeed = levelData.levelSpeed[levelMetaData.sequence]+adaptive.getScroll()
    levelMetaData.jewelSet = levelMetaData.currentSection[4] 
    levelMetaData.platformSet = levelMetaData.currentSection[5] 
    levelMetaData.gridDeath = levelMetaData.currentSection[6]
    MusicArray = thisLevel[7]
    if arcadeMode==0:
        if MusicArray:
            levelMetaData.introMusic = MusicArray[0]
            levelMetaData.winMusic =MusicArray[1] 
            levelMetaData.loseMusic = MusicArray[2]
        else:
            levelMetaData.introMusic = None
            levelMetaData.winMusic = None
            levelMetaData.loseMusic = None
    levelMetaData.BackDrop = levelMetaData.currentSection[0]
    backDropManager.checkAndReload(levelMetaData.BackDrop)
    
def LoadLevelData():
    global ObjectStarts
    global levelMetaData
    import PycapRes
    setUpLevelData()
    LowerScenery = levelMetaData.currentSection[1]
    UpperScenery = levelMetaData.currentSection[2]
    ObjectStarts = map_Resources[levelMetaData.currentLevelFile]
    nextX = random.randint(0,200)
    levelMetaData.LowerScenery = []
    levelMetaData.UpperScenery = []
    #set up Grace Layer
    if len(UpperScenery):
        while(nextX < 400):
            nextIndex =  random.randint(0,len(UpperScenery)-1)
            item = Scenery()
            item.name = UpperScenery[nextIndex]
            item.X = nextX
            item.width = PycapRes.imageWidth(JPG_Resources[item.name])
            item.height = PycapRes.imageHeight(JPG_Resources[item.name])
            levelMetaData.UpperScenery.append(item)
            nextX += random.randint(0,300)
    
    nextX = random.randint(0,200)        
    while(nextX < 400):
        nextIndex =  random.randint(0,len(LowerScenery)-1)
        item = Scenery()
        item.name = LowerScenery[nextIndex]
        item.X = nextX
        item.width = PycapRes.imageWidth(JPG_Resources[item.name])
        item.height = PycapRes.imageHeight(JPG_Resources[item.name])
        levelMetaData.LowerScenery.append(item)
        nextX += random.randint(0,300)
  
def clamp255(byte):
    if byte>255:
        return 255
    elif byte < 0:
        return 0
    return byte
    
def clamp0(value,check):
    if value>check:
        return check
    elif value < 0:
        return 0
    return value
    
class ScreenMessage:
    string = None
    tabX = 500
    tabY = 100
    R =  0
    G =  0
    B =  0
    A =  255   
    width = 0
    height = 0
    stringTime = 500
    scroll = 0
    font = None
    mouseDown = 0
    mouseOver = 0
    function = None
    graphic = None
    parameter = None
    forceFade = 0
    fadeUpTime = 0
    mouseOverfunction = None
    collisionX = 0
    collisionWidth = 0
    particleOnStrobe = 0
    scale = 1.0
    life = 0
    flashEnabled = 1
    graphicRes = -1
    
    def RenderMessage(self):
        a = 255
        if PCR == None or PC == None:
            return
        self.collisionX = self.tabX
        self.collisionWidth = self.width
        PC.setColourize(0)
        if self.function and inEditor==0: 
            flash = 18 + math.sin((self.tabY/10+continousTime)/9)*20
        else:
            flash = 0

        
        if(self.string != None and self.string != ""):
            highLightString = None
            right = 0
            workingString = self.string
            HighLight = workingString.find('__H')
           # print workingString,HighLight
            if HighLight != -1:
                HighLightDown = workingString.find('__N')
                right = workingString[:HighLight]
                left = workingString[HighLightDown+3:]
                highLightString = workingString[HighLight+3:HighLightDown]
                workingString = "%s%s%s" % (right,highLightString,left)
 #          self.string = self.string[:-5]
            widthDelta = 0
            font = self.font
            hint = flash
            if (self.mouseOver and inEditor==0):
                hint  = 60
                if font == font22:
                    font = font23
                else:
                    font = font38
            if font == None:
            #    print "error font not loaded"
                return
            if self.string == None:
            #    print "error string not defined"
                return
            if self.graphicRes == -1:
                self.width = PCR.stringWidth(workingString,font)
                self.height = PCR.fontAscent(font)
            if(self.tabX == -1):
                self.tabX = gridRight+((800-gridRight-self.width)/2)
                
            #compensate for selected width
            unselectedwidth = PCR.stringWidth(workingString,self.font)
            #widthDelta = (self.width-unselectedwidth)/2

            a = int(self.A-32)
            alpha = self.A
            if self.fadeUpTime:
                alpha = self.A * (self.fadeTimer/self.fadeUpTime)
                a = int(alpha-32)
            
            PC.setFont(font)
            if(inEditor==0):
                y = self.tabY
            else:
                y = self.tabY+ 20
            if a>=0:
                PC.setColour( 0,0,0,int(a) )
                PC.drawString( workingString,self.tabX+2-widthDelta, y+2 )    
            if(self.mouseDown):
                 PC.setColour( 255, 0, 0, int(alpha) )
            else:        
                PC.setColour( int(clamp255(self.R+hint)), int(clamp255(self.G+hint)), int(clamp255(self.B+hint)),int(clamp255(alpha+hint)) )
            PC.drawString( workingString, self.tabX-widthDelta, y )
            if highLightString:
               # alpha = clamp255(200 + math.sin(self.life/5.0)*50)
                PC.setColour( 255,0,0,int(alpha))
                highLightOffset = PCR.stringWidth(right,font)
                PC.drawString( highLightString, self.tabX-widthDelta+ highLightOffset, y )              
        if(self.graphicRes == -1):
            if self.function and a>0:
                PC.setColourize(1)
                PC.setColour( 255,255,255,int(a) )
                PC.drawmodeNormal()
                graphicName = JPG_Resources["selectableIcon"]
                y = self.tabY - PCR.imageHeight( graphicName )
                x = self.tabX - PCR.imageWidth( graphicName )-5
                width = PCR.imageWidth( graphicName )
                height = PCR.imageHeight( graphicName )
                if self.mouseOver:
                    y += height
                    width *= 1.2
                    height *= 1.2
                    y -= height
                    totalWidth = self.width+PCR.imageWidth( graphicName )
                    x1 = random.randint(0,int(totalWidth)) 
                    y1 = random.randint(int(y),int(y)+PCR.imageHeight( graphicName )) 
                    bias = (totalWidth/2.0 - x1)/-300.0
                    makeSparkleParticle(x1+cameraX+x,y1,bias,0,2) 
                PC.drawImageScaled( graphicName, x, y,width,height)
                self.collisionX -= 40
                self.collisionWidth += 40
        else:
            graphicName = self.graphicRes  
            renderWidth = self.width * self.scale
            renderXOffset = 0
            renderHeight = self.height * self.scale
            renderYOffset = 0
            if inEditor ==0  and self.mouseOver:
                renderWidth *= 1.2
                renderHeight *= 1.2
                renderXOffset = (renderWidth-(self.width*self.scale))/2.0
                renderYOffset = (renderHeight-(self.height*self.scale))/2.0 
            PC.setColourize(1)
            PC.drawmodeNormal()
            if self.mouseOver or self.flashEnabled==0:
                colour = 255
            else:
                colour = clamp255(160+(flash*3))
            color = int(color)
            PC.setColour( colour, colour,colour, 255)
            PC.drawImageScaled( graphicName, self.tabX-renderXOffset, self.tabY-renderYOffset,renderWidth,renderHeight)
            if self.mouseOver:
                PC.drawmodeAdd() 
                if inEditor:
                    PC.setColour( 255, 255,255, 180)
                    PC.drawImage( graphicName, self.tabX, self.tabY)
                else:
                    PC.setColour( 255, 255,255, 55)
                    PC.drawImageScaled( graphicName, self.tabX-renderXOffset, self.tabY-renderYOffset,renderWidth,renderHeight)
                if self.mouseOverFunction:
                    mouseOverMessage.function = self.mouseOverFunction
                    mouseOverMessage.parameter = self.parameter
                else:
                    self.mouseOverMessage = None
                
                x1 = random.randint(0,int(renderWidth)) 
                x1 += self.tabX-renderXOffset
                y1 = random.randint(0,int(renderHeight)) 
                y1 += self.tabY-renderYOffset
                bias = (renderWidth/2.0 - x1)/-300.0
                makeSparkleParticle(x1,y1,bias,0,renderWidth/90.0) 

            if (inEditor and self.string != None and self.string != ""):
                PC.setColour( 255, 0, 0, int(alpha) ) 
                PC.drawString( self.string, self.tabX, y )  
    
    def setMessage(self,message,R,G,B,A,font,tabY,scroll,tabX,function,graphic,parameter,fadeUpTime,mouseOverFunction=None,scale = 1.0,flashEnabled=1):
        self.mouseOverFunction = mouseOverFunction
        self.string = message
        self.tabY = tabY
        self.R = R
        self.G = G
        self.B = B
        self.A = A
        self.tabX = tabX
        self.graphic = graphic
        if graphic:
            self.graphicRes = JPG_Resources[self.graphic]
            self.width = PCR.imageWidth( self.graphicRes )
            self.height = PCR.imageHeight( self.graphicRes ) 
            if(inEditor and (self.width>38 or self.height>38)): 
                if(self.width>self.height):
                    self.height *= 38.0/self.width
                    self.width = 38
                else:
                    self.width *= 38.0/self.height
                    self.height = 38   
        self.function = function
        self.parameter = parameter
        self.scale = scale
        self.flashEnabled = flashEnabled
        if font == 8:
            self.font = font8           
        elif font == 36:
            self.font = font36
        elif font == 22:
            self.font = font22
        else: 
            font = font22
        #    print "error font not know in set message!"
          
        self.scroll = scroll
        self.fadeUpTime = fadeUpTime
        self.fadeTimer = 0

    def tickMessage(self,delta):
        self.life += 1

        if self.fadeUpTime:
            self.fadeTimer += delta
            if self.fadeTimer > self.fadeUpTime:
                self.fadeTimer  = self.fadeUpTime
        if(self.scroll):
            self.tabY -= delta/2.0
            if(self.tabY<70):
                self.A-= delta*3
            if(self.A <=0):
                self.string = None

                
    def setFade(self):
        self.forceFade = 1
        TEMP = 1
            
class ScreenMessagesClass:    
    message = ScreenMessage()
    messages = []
    lastMessageTabY = 0

    def RenderMessages(self):
        for message in self.messages:
            message.RenderMessage()
        PC.drawmodeNormal()
        PC.setColourize(0)
            
    def clearMessages(self):
        self.messages = []
        self.lastMessageTabY = 0 #tony - experiment

    def setMessageScroll(self,message,graphic,string=None,parameter=None,function = None,fadeIn=0,mouseOverFunction = None):
        newMessage = ScreenMessage()
        thisString = message[0]
        tabY = 120
        if(tabY-self.lastMessageTabY<40):
            tabY = self.lastMessageTabY+40
        self.lastMessageTabY = tabY
        if(string != None):
            thisString = thisString+string
        sound = message[1]
        if sound != None:
            playSimpleSound(sound)
        tabX = -1       #we may want to be able to fix this
        scroll = 1
        newMessage.setMessage(thisString,message[2],message[3],message[4],message[5],message[6],tabY,scroll,tabX,function,graphic,parameter,fadeIn,mouseOverFunction)
        self.messages.append(newMessage)

    def setMessageStatic(self,message,graphic,x,y,function,string=None,parameter=None,fadeUp=0,mouseOverFunction = None,scale = 1.0,flashEnabled = 1):
        scroll = 0
        newMessage = ScreenMessage()
        thisString = message[0]
        if(string != None):
            thisString = thisString+string
        playSimpleSound(message[1])
        newMessage.setMessage(thisString,message[2],message[3],message[4],message[5],message[6],y,scroll,x,function,graphic,parameter,fadeUp,mouseOverFunction,scale,flashEnabled)
        self.messages.append(newMessage)

    def tickMessages(self,delta):
        self.lastMessageTabY -= delta/2.0
        for message in self.messages[:]:
            message.tickMessage(delta)
            if message.string == None:
                self.messages.remove(message)
            if message.forceFade:
                message.A -= delta*2
                if message.A <0:
                    message.A = 0
                
    def mouseInput(self,mouseX,mouseY,button):
        for message in self.messages:
#            if message.scroll == 0:
                message.mouseOver = 0
                message.mouseDown= 0
                if(message.graphic != None):
                    localY= message.tabY+message.height
                else:
                    localY= message.tabY
                if(message.function != None and mouseX> message.collisionX and mouseX < message.collisionX+message.collisionWidth):                
                    if(mouseY< localY and mouseY > localY-message.height): 
                        if(button == -1): #mouse has moved
                            message.mouseOver = 1
                        if(button == 1):
                            message.mouseDown = 1
                            if(message.function!= None):
                                playSimpleSound("mouseClick")
                                if(message.parameter != None):
                                    message.function(message.parameter)
                                else:
                                    message.function()
                                    
    def RenderMessageDirect(self,X,Y,string,alpha,extra_string=None):
        thisString = string[0]
        if(extra_string != None):
            thisString = thisString+extra_string
        playSimpleSound(string[1])
        R=string[2]
        G=string[3]
        B=string[4]
        A=string[5]* alpha/255.0
        fontID = string[6]
        if fontID == 8:
            font = font8           
        elif fontID == 36:
            font = font36
        elif fontID == 22:
            font = font22
        else: 
            font = font22
        if(X==-1):
            X = gridRight+((800-gridRight-PCR.stringWidth(thisString,font))/2)
        PC.setColour( 0,0,0,int(128 * alpha/255.0) )
        PC.setFont(font)
        PC.drawString( thisString, X+3, Y+3 )
        PC.setColour( int(R), int(G), int(B), int(A) )
        PC.drawString( thisString, X, Y )
        
    def fadeAndClear(self):
        for message in self.messages:
            message.setFade()
        self.lastMessageTabY = 0 #tony - experiment
        
 
def loadResources(delta):
    global dataIsLoaded
    global whereIsSnakyJake
    global charlieBark
    
    if charlieBark>=0 and logoCount< 300:
            PC.playSound( charlieBark,0.5,0,0)  
            charlieBark = -1
#    if whereIsSnakyJake>=0 and fileIndex>100:
#            PC.playSound( whereIsSnakyJake,0.5,0,0)  
#            whereIsSnakyJake = -1
    if pubLogoCount > 0:
        tickpubLogo(delta)
        return
    if logoCount >0:
        tickLogo(delta)
        return
    unloadLogoGFX()
    tickLoading(delta)
    if(len(allGraphicFiles)==0):
        getFileNames('res/')
    #loadGraphics('res/')
    else:
        loadGraphicsFromList()
        uncrunchMusic()        
        PC.markDirty()
    if(dataIsLoaded):
        loadSounds('res/')
        initialiseGame() 
        unloadLoadingScreen()
        uncrunchMusic()
        

def getFileNames(root):
    import os
    global allGraphicFiles
    global allGraphicFilesNames
#    global allLevelFiles
#    global allLevelFilesNames
 #   global allsoundFiles
 #   global allsoundFilesNames
    files = [] 
    files = os.listdir(PC.getAppResourceFolder() + root)
    #print("checking path ",root)
    for file in files:
        dot = None
        #print "found ",file
        extension = file[-3:]
        name = file[:-4]
        if extension == "JPG" or extension == "jpg":
            if name[-1] != "_":  #don't load include the masks in the list...
                allGraphicFiles.append(root+file)
                allGraphicFilesNames.append(file)
            #print("name",root+file)
        if extension == "jld":
            #print "loading resource ",file
            allGraphicFiles.append(root+file)
            allGraphicFilesNames.append(file)
            #print("name",root+file)
        if extension == "mid" or extension == "MID":
            #print "loading resource ",file
            allGraphicFiles.append(root+file)
            allGraphicFilesNames.append(file)
            #print("name",root+file)
        found= file.find(".")
        if(found == -1):
            getFileNames(root+file+"/")

 ###########################################
# loadMap
###########################################
GSection = 0
GJewels = 0

def loadMap(file):
    #print ("level file",file)
    global GSection 
    global GJewels
    newMapLevel = []
    openFile = open(PC.getAppResourceFolder() + file, "r" )
    newRecord = []
    count = 0
    for line in openFile:
      if(count==0):
          GSection = int(line)
      elif(count==1):
          GJewels = int(line)
      elif(line=="RecordEnd\n"):
          newMapLevel.append(newRecord)            
          newRecord = []
      else:
          newRecord.append(float(line))
      count += 1
    return newMapLevel
    
 ###########################################
# loadGraphics
###########################################
def loadGraphicsFromList():
    import os
    import PycapRes
    global PCR
    global fileIndex
    global dataIsLoaded 
    PCR = PycapRes
    toLoad = len(allGraphicFilesNames)-fileIndex-1
    if(toLoad>5):
        toLoad = 5 #load data 5 files at a time.
    while toLoad>=0:
        dot = None
        file = allGraphicFiles[fileIndex]
        fileName = allGraphicFilesNames[fileIndex]
        fileIndex+=1
        extension = fileName[-3:]
        name = fileName[:-4]
        fileNoExtension = file[:-4]
        if extension == "JPG" or extension == "jpg":
           # print "loadgraphicsfromlist",file,file[:8]
            temp = JPG_Resources[name] = PCR.loadImage( file)
            if file[:8] == "res/pink":
                PCR.imageGreyScale(temp)
        if extension == "jld":
            map_Resources[name] = loadMap(file)
            map_Section[name] = GSection        #horrid hack
            map_Jewels[name] = GJewels
        if extension == "mid" or extension == "MID":
            MIDI_Resources[name] = PCR.loadTune(file)
         #   print"loading midi",file
        toLoad -= 1
    if fileIndex >= len(allGraphicFilesNames)-1:
        dataIsLoaded = 1

###########################################
# loadSounds
###########################################
def loadSounds(root):
    import os
    import PycapRes
    global PCR
    PCR = PycapRes
    files = [] 
    files = os.listdir(PC.getAppResourceFolder() +root)
    #print("checking path ",root)
    for file in files:
        dot = None
        #print "found ",file
        extension = file[-3:]
        name = file[:-4]
        if extension == "WAV" or extension == "wav" or extension == "ogg" or extension == "OGG":
            WAV_Resources[name] = PCR.loadSound( root+file)
        found= file.find(".")
        if(found == -1):
            loadSounds(root+file+"/")
    

def EmptyGrid():
    global grid
    for row in range(len(grid)):
        grid[row] = []
    fillGrid()

###########################################
# Add a tyle to the grid
# GridTick checks to see if tiles need removing
###########################################
def AddToGrid(jewelIDX,row,NotDummy):
    global grid
    global tilesOver
    import copy
    found = 0 
    row = row/GridPitchY
    row = (y_max/GridPitchY)-row
    row = int(row)-1
    if(row<0 or row > 23):
        print(("error row out of range in add to grid",row))
    else:
        tile = TileObject()
        #colour is only needed as an interim step!
        tile.colour = levelData.jewelColour[jewelIDX]
        tile.jewelIDX = jewelIDX
        
        if(NotDummy):
            grid[row].insert(0,tile)
            for tile in grid[row]:
                tile.XOffset = 1
        else:   
            rowCopy = copy.copy(grid[row]) #we need a copy of this row to restore if this is adummy
            grid[row].insert(0,tile)        #we need to chck here so we clean up new patterns 
            found = testRow(row)     
            grid[row]=rowCopy
    return found
  
def getTile(row,collumn):
    if(row<0 or row>len(grid)-1):
        return 'none'
    if(collumn>=len(grid[row]) or collumn < 0 or row >= len(grid) or row < 0):
        return 'none'
    else:
        return grid[row][collumn]



class matchObject:
    row = 0
    collumn = 0
     
def checkMatchVerticalUp(row,collumn,colour):
    global matchedTiles
    tile = getTile(row,collumn)
    if(tile=='none'or tile.colour=='none' or tile.YOffset>0 or tile.XOffset>0):
        return
    if(tile.colour != colour or tile.checked or tile.toRemove!=0):
        return
    newObject = matchObject()
    newObject.row = row
    newObject.collumn = collumn
    matchedTiles.append(newObject)
    grid[row][collumn].checked = 1
    checkMatchVerticalUp(row-1,collumn,colour)
     
def checkMatchVerticalDown(row,collumn,colour):
    global matchedTiles
    tile = getTile(row,collumn)
    if(tile=='none'or tile.colour=='none' or tile.YOffset>0 or tile.XOffset>0):
        return
    if(tile.colour != colour or tile.checked or tile.toRemove!=0):
        return
    newObject = matchObject()
    newObject.row = row
    newObject.collumn = collumn
    matchedTiles.append(newObject)
    grid[row][collumn].checked = 1
    checkMatchVerticalDown(row+1,collumn,colour)
    
def rowMatch(row):
    rowLength = len(grid[row])
    if(rowLength < 3): #can be 3 or 4!
        return 0
    matched = grid[row][0].colour
    if(rowLength>3):
        rowLength =3
    for tileIDX in range(rowLength):
        tile = grid[row][tileIDX]
        if(tile.YOffset>0 or tile.XOffset>0 or (tile.toRemove!=0 and tile.toRemove != RemoveCount) or tile.colour != matched):          
            return 0
    return 1

def matchFound(NotDummy):
    global combo
    global tilesOver
    if(NotDummy):
      combo+= 1
      if(combo==1):
          tilesOver -= 2 
      else:
          tilesOver -= 1 
      if tilesOver<0:
          tilesOver = 0
 
def getTileNew(row,collumn):
    if(row<0 or row>len(grid)-1):
        return 'none'
    tile = grid[row][collumn]
    if(collumn>=len(grid[row]) or collumn < 0 or row >= len(grid) or row < 0  or tile.YOffset>0 or tile.XOffset>0 or (tile.toRemove!=0 and tile.toRemove != RemoveCount)):
        return 'none'
    else:
        return tile.colour
        
###########################
#test row
###########################

#checks this row for any horizontal or vertical lines.  Doesn't work for multiple lines!
def testRow(row):
    if rowMatch(row):
        return 3
    length = len(grid[row])
    if(length<3):
        return 0
    if(length>3):
        length = 3
    for collumn in range(length) :
        matched = 1
        colour = grid[row][collumn].colour
        count = 1
        while colour == getTileNew(row-count,collumn) and count<3:
            matched += 1
            count += 1
        count = 1
        while colour == getTileNew(row+count,collumn) and count < 3:
            matched += 1
            count += 1
        if(matched>=3):
            return(matched)
    return 0

def checkRow(row,NotDummy,orientation):
    global matchedTiles
    global gridRightTarget
    matched = 0
    x = 0
    length = len(grid[row])
    if(length>3):
        length = 3
    if(orientation ==VERTICAL):
        for collumn in range(length):
            x=x+GridPitchY
            matchedTiles = []
            if(grid[row][collumn].checked==0):
                checkMatchVerticalUp(row,collumn,grid[row][collumn].colour)
                checkMatchVerticalDown(row+1,collumn,grid[row][collumn].colour)
            if(len(matchedTiles)>(minimumMatch-1)):
                matched += len(matchedTiles)
                matchFound(NotDummy)
                if(NotDummy):
                    for tile in matchedTiles:
                        grid[tile.row][tile.collumn].toRemove = RemoveCount
            else:
                #set up vertical hint
                for tile in matchedTiles:
                    grid[tile.row][tile.collumn].hint = len(matchedTiles)>1

                  
    else: 
        if length ==3:
            if rowMatch(row):
                matched += 4
                matchFound(NotDummy)
                if(NotDummy):
                    grid[row][0].toRemove = RemoveCount
                    grid[row][1].toRemove = RemoveCount
                    grid[row][2].toRemove = RemoveCount
            #set up horizontal hints
            if grid[row][0].colour == grid[row][1].colour:
                grid[row][0].hint = grid[row][1].hint = 2
            if grid[row][1].colour == grid[row][2].colour:
                grid[row][1].hint = grid[row][2].hint = 2
    return(matched)

def checkForNewPatterns(NotDummy):
    global gridRightTarget
    global gridLeftTarget
    global ghostSpawnX
    global ghostSpawnY
    maxRowLength = 0
    foundV = 0 
    foundH = 0
    if(NotDummy):
        gridRightTarget = 0
        gridLeftTarget = x_max
    clearchecks()
    y = 0
    foundToggle = 1
    for row in range(len(grid)):
        foundV += checkRow(row,NotDummy,VERTICAL)
        foundH += checkRow(row,NotDummy,HORIZONTAL)   
        if((foundV>0 or foundH>0) and foundToggle):
            ghostSpawnY = ((y+1) * GridPitchY)
            if(foundV):
                ghostSpawnY += (1.5* GridPitchY)
            if(gridFillRight):
                ghostSpawnX = x_max - 100
            else:
                ghostSpawnX = 60
            foundToggle = 0
        y +=1
    return foundV+foundH

def clearchecks():
    for row in grid:
        for tile in row:
            tile.checked = 0

def reFillGrid():
    for row in grid:
        for tile in row:
            tile.toRemove = RemoveCount
            tile.toRemove = 0

def detonateGrid():
    global tilesOver
    for row in grid:
        for tile in row:
            tile.toRemove = RemoveCount
    tilesOver = 0
    
# below will add a block in
def addblocks(row):
    #return
    if(levelMetaData.RandomTiles==0):
        return
    while(len(row)<3):
        nexttile = random.randint(0,levelMetaData.RandomTiles-1)
        tried = 0
        tile = TileObject()
        matched = 1
        while matched and tried<5:
            if(nexttile == 0):
                colour = 'Red'
            if(nexttile == 1):
                colour =  'Green'   
            if(nexttile == 2):
                colour = 'Blue' 
            if(nexttile == 3):
                colour = 'Orange'
            if(nexttile == 4):
                colour =  'Purple'   
            if(nexttile == 5):
                colour = 'Yellow'             
            if(nexttile == 6):
                colour = 'White' 
            if(nexttile == 7):
                colour = 'Black'
            if(nexttile == 8):
                colour = 'Stripe'
            tile.colour = colour
            tile.jewelIDX = nexttile 
            row.append(tile)
            #matched = 1    
            clearchecks()
            matched = checkRow(grid.index(row),0,VERTICAL)
            if(matched==0):
                matched = checkRow(grid.index(row),0,HORIZONTAL)            #print("matched",matched)
            if matched:
                nexttile+=1
                tried+= 1
                if tried<5:
                    row.pop()
                if(nexttile>4):
                    nexttile = 0
       # if tried ==5:
       #     print("could not find suitable tile",matched)

                    


def fillGrid():
    for row in grid:
        addblocks(row)
    for row in grid:
        for tile in row:
            tile.YOffset = grid.index(row)+14


def getNextColour(index):
    index += 1
    if(index>levelMetaData.RandomTiles):
        index = 1
    return index

def dropRow(tile,row):
    collumnIDX = row.index(tile)
    rowIDX = grid.index(row)
    #drop all the tiles in the collumn
    for FromRow in grid[rowIDX+1:]:
        if(rowIDX+1>len(grid) or rowIDX<0):
            print(("trying to index of end of grid",rowIDX))
        else:
            ToRow = grid[grid.index(FromRow)-1]
            ToRow[collumnIDX].colour = FromRow[collumnIDX].colour
            ToRow[collumnIDX].checked = FromRow[collumnIDX].checked
            ToRow[collumnIDX].toRemove = FromRow[collumnIDX].toRemove
            ToRow[collumnIDX].YOffset = FromRow[collumnIDX].YOffset+1
            ToRow[collumnIDX].XOffset = FromRow[collumnIDX].XOffset   
            ToRow[collumnIDX].XSpeed = FromRow[collumnIDX].XSpeed  
            ToRow[collumnIDX].YSpeed = FromRow[collumnIDX].YSpeed  
            ToRow[collumnIDX].jewelIDX = FromRow[collumnIDX].jewelIDX
            
    if levelMetaData.RandomTiles==0:
        randomNum = 5
    else:
        randomNum = levelMetaData.RandomTiles
    index = random.randint(1,randomNum)
    grid[len(grid)-1][collumnIDX].jewelIDX = index-1
    grid[len(grid)-1][collumnIDX].colour = levelData.jewelColour[index-1]
    tried = 0
    while testRow(len(grid)-1) and tried < 8:
        index = getNextColour(index)
        grid[len(grid)-1][collumnIDX].jewelIDX = index-1
        grid[len(grid)-1][collumnIDX].colour = levelData.jewelColour[index-1]
        tried += 1
    grid[len(grid)-1][collumnIDX].checked = 0
    grid[len(grid)-1][collumnIDX].toRemove = 0
    grid[len(grid)-1][collumnIDX].YOffset = grid[len(grid)-2][collumnIDX].YOffset+1 
    grid[len(grid)-1][collumnIDX].XOffset = 0 
    grid[len(grid)-1][collumnIDX].YSpeed = 0
    grid[len(grid)-1][collumnIDX].XSpeed = 0 
    grid[len(grid)-1][collumnIDX].explosiontriggered=0  

def bombTick(delta):
    finishedExploding = 1
    global bombExplosion
    for row in grid:
        for tile in row[:3]:     
            if(tile.toRemove > delta):
                finishedExploding = 0
                tile.toRemove -= delta;
            else:
                tile.toRemove = 1
    if(finishedExploding):
        if(delayRefill==0):
            EmptyGrid()
            bombExplosion = 0
        
gridSoundPlaying = 0        
def tickTiles(delta):
    global gridSettled
    global gridSoundPlaying
    if gridLeft>=800:
        return
    removedCount = 0
    elements=0
    count = 0
    gridSoundPlaying-=1
    if gridSoundPlaying<0:
        gridSoundPlaying = 0
    for row in grid:
        for tile in row[:3]: 
            if(tile.YOffset>0):
                gridSettled = 10
                tile.YOffset-= (delta*tile.YSpeed/50.0)
                tile.YSpeed += .2*delta
                if(tile.YOffset<0):      
                    tile.YOffset=0
                    if(tile.YSpeed>6):
                        if gridSoundPlaying==0:
                            playSimpleSound("grid6")
                            gridSoundPlaying = 5
                        tile.YOffset = 0.01
                        tile.YSpeed = tile.YSpeed * -0.25
                    else:
                        tile.YSpeed = 0
                        if gridSoundPlaying==0:
                            playSimpleSound("grid5")
                            gridSoundPlaying = 5

        for tile in row: 
            elements+=1
            if(tile.XOffset>0):
                gridSettled = 10
                tile.XOffset-= (delta*tile.XSpeed/50.0)
                tile.XSpeed += .2 * delta
                if(tile.XOffset<0):  
                    tile.XOffset=0
                    global tilesOver
                    if(tile.XSpeed>3):
                        tile.XOffset = 0.01
                        tile.XSpeed = tile.XSpeed * -0.25
                    else:
                        tile.XSpeed = 0
                     
        for tile in row[:3]: 
            emergencyCount = 20
            while(tile.toRemove>0 and tile.toRemove<=delta and emergencyCount>0):
                dropRow(tile,row)
                emergencyCount -= 1
            removedCount+=3
            if(tile.toRemove>0):
                gridSettled = 10
                tile.toRemove -= delta;
                
        count+=1
#finally check for and remove and objects which     
    for row in grid:
        if(len(row)>3):
            if row[3].XSpeed==0 and row[3].YSpeed==0:
                row.pop()
                if levelMetaData.gridDeath or arcadeMode:
                    tilesOver+=1   #we've added a tile and the grid has settled so incremented hte 
                #decScore(25)
   # print("grid size ",elements)
    return removedCount

def incComboLevel(thisComboLevel):
    type = WorldTypes.PlayerGhostUp
    addObject(nextID,ghostSpawnX+cameraX,600-ghostSpawnY,type)
    levelMultiplier = levelMetaData.sequence
    comboBonus= thisComboLevel * (1+ levelMultiplier/10.0) * 5 * getMutliplier()
    comboBonus = int(comboBonus)
    incScore(comboBonus)

    
def checkCombo(found):
    global combo
    global comboLevel
    global comboTimer
    global gridSettled
    if(found):
        playSimpleSound("gridExplosion")
        tileBonus(found)
        if(combo == 2):
            ScreenMessages.setMessageScroll(messages.Combo,None)
            incComboLevel(2)
            comboTimer = startComboTimer
        elif(combo == 3):
            ScreenMessages.setMessageScroll(messages.SuperCombo,None)
            incComboLevel(3)
            comboTimer = startComboTimer
        elif(combo == 4):
            ScreenMessages.setMessageScroll(messages.MegaCombo,None)
            incComboLevel(4)
            comboTimer = startComboTimer
        elif(combo == 5):
            ScreenMessages.setMessageScroll(messages.UltraCombo,None)
            incComboLevel(5)
            comboTimer = startComboTimer
        elif(combo > 5):
            numberCombo = ' Plus ' + str(combo-5)
            ScreenMessages.setMessageScroll(messages.UltraCombo,None,numberCombo)
            incComboLevel(6)
            comboTimer = startComboTimer 
    else:
        if gridSettled == 0:
            combo = 0
            temp = 0
        else:
            gridSettled -= 1
  
def tickGrid(delta):
    global combo
    global comboLevel
    global gridRight
    global comboTimer
    global gridFillHeight
    global targetGridFillHeight
    global gridLeft
    global tilesOver
    if gridLeftTarget == 800:   #if the grid has been put away then drop the tiles over
        tilesOver = 0
        #if the grid has been put away make sure the grid is empty
        targetGridFillHeight = 0
        GridFillHeight = 0
    comboDecrement = delta*math.sqrt(comboLevel+1)
    comboTimer -=  comboDecrement
    tickGridBackGround(delta)
#    if(comboTimer < 0):
#        comboTimer = startComboTimer
#        if(comboLevel>0):
#            decComboLevel(1)
    if gridFillRight:
        if(gridLeftTarget<gridLeft):
            gridLeft -=delta*1
            if(gridLeftTarget>gridLeft):
                gridLeft=gridLeftTarget
        if(gridLeftTarget>gridLeft):
            gridLeft+=delta*2
            if(gridLeftTarget<gridLeft):
                gridLeft=gridLeftTarget
    else:            
        if(gridRightTarget>gridRight):
            gridRight+=delta*1
            if(gridRightTarget<gridRight):
                gridRight=gridRightTarget
        if(gridRightTarget<gridRight):
            gridRight-=delta*2
            if(gridRightTarget>gridRight):
                gridRight=gridRightTarget
            
    if(bombExplosion):
        bombTick(delta)
        removedTiles = 0
    else:
        removedTiles = tickTiles(delta)
        if(removedTiles and gameOver==0):
            found = checkForNewPatterns(1)  #We also need to check here in case of combos
            checkCombo(found)
        #for row in grid:
        #    addblocks(row)
    return removedTiles
        
def tileBonus(removedTiles):
    tempTiles = removedTiles
    levelMultiplier = levelMetaData.sequence
    if arcadeMode:
        levelMultiplier *= 1.5
    if levelMultiplier<1:
        levelMultiplier = 1
    scoreBonus = (tempTiles*tempTiles*tempTiles)*0.25* levelMultiplier
    increment = int(scoreBonus/10)
    scoreBonus = (increment+1)*10
    incScore(scoreBonus)
    #print ("removed,level,bonus",removedTiles,levelNumber,scoreBonus)
    if(combo<2):
        ScreenMessages.setMessageScroll(messages.ScoreBonus,None,str(scoreBonus))

def getMutliplier():
    multiplier = comboLevel+1
    return multiplier
    
def incScore(scoreIncrement):
    global score
    global nextLifeScoreTarget
    global thisHighScoreIDX
    multiplier = getMutliplier()
    score += scoreIncrement*multiplier
    if arcadeMode:
        adaptive.doingWell(scoreIncrement/8.0)
    if scoreIncrement>10 and  smartBomb.active() == 0:
        if gameOver == 0 and FinishFlag==0:
            playSimpleSound("chime_up")   
    if  score>=nextLifeScoreTarget:
        #print"new life",score,nextLifeScoreTarget
        nextLifeScoreTarget = nextLifeScoreTarget*4
        if FinishFlag==0 and lives>0:
            type = WorldTypes.OneUp
            newObject = addObject(nextID,scoreX+cameraX+150,28,type)

            newObject.isCollected()
        #give an extra life
    if arcadeMode:
        testScore = highScoreCanvas.tryInsert(score,0)
        if testScore!= -1:
            if testScore<thisHighScoreIDX:
                ranking = testScore+1
                if ranking == 1:
                    ScreenMessages.setMessageScroll(messages.TopScore,None,None)
                else:
                    rankingString = str(ranking) 
                    if ranking == 2:
                        rankingString += "nd"
                    elif ranking == 3:
                        rankingString += "rd"
                    else:
                        rankingString += "th"
                    ScreenMessages.setMessageScroll(messages.NewHighScore,None,rankingString)  
                thisHighScoreIDX =  testScore       
        
def decScore(scoreIncrement):
    global score
    score -= scoreIncrement
    if score < 0:
        score = 0
        
###########################################
# Render the grid
###########################################
gridSweep = 0
def RenderGrid():
    import PycapRes
    global gridRight
    global gridSweep
    renderGridBackGround()
    PC.drawmodeNormal()
    PC.setColourize(0)
    y_pos = 1
    max_x = 0
    gridSweep -= .4
    for row in grid:
        x_pos = 1
        for tile in row:
            if(tile.toRemove==0):
                PC.drawmodeNormal()  
                if(tile.colour!='none'):
                    #tileName = tile.colour+'Tile'
                    name = levelMetaData.jewelSet[tile.jewelIDX]
                    graphic = JPG_Resources[name] 
                    #tile.colour = levelData.jewelColour[tile.jewelIDX] #tony hack
                   # if (tile.colour != levelData.jewelColour[tile.jewelIDX]):
                   #     print("error none matchin tile data",tile.colour,levelData.jewelColour[tile.jewelIDX])
                    #graphic = JPG_Resources[tileName]    
                    if(gridFillRight):
                        #print("gridLeft",gridLeft)
                        x = gridLeft+((x_pos-1)*GridPitchX)
                        x-= (tile.XOffset*GridPitchX)
                    else:
                        #print("gridRight",gridRight)
                        x = gridRight - (x_pos*GridPitchX)
                        x+= (tile.XOffset*GridPitchX)
                    y = y_max-(y_pos*GridPitchY)
                    y-= (tile.YOffset*GridPitchY)
                    PC.drawImage( graphic, x, y)
                    if((x_pos+y_pos) == int(gridSweep) %80):
                        PC.drawmodeAdd()
                        PC.setColourize(1)
                        if(tile.hint):
                            PC.setColour( 255, 255, 255, 100)
                        else:
                            PC.setColour( 255, 255, 255, 0 )
                        PC.drawImage( graphic, x, y)
                        PC.drawmodeNormal()
                        PC.setColourize(0)
                    
                    tile.explosiontriggered = 0 
            else:
                if(tile.explosiontriggered==0):
                    scale = 1
                    if(combo>0):
                        scale += combo
                    scale *= 0.25
                    if(gridFillRight):
                        x = gridLeft + ((x_pos-1)*GridPitchX)+(GridPitchX/2)+cameraX
                    else:
                        x = gridRight - (x_pos*GridPitchX)+(GridPitchX/2)+cameraX
                    y = y_max - (y_pos*GridPitchY)+(GridPitchY/2)+cameraY
                    particleController.addItem(tileExplosion(),x,y,scale)
                    tile.explosiontriggered = 1
            x_pos+=1
        y_pos+=1      

firstEdge = 0 #set to false once one object has been rendered at the edge
class trailObject:
    targetSpacing = 32
    atRestSpacing = 0
    jewelIdx = 0
    graphic = None
    name = None
    hint = 0
    width = 0
    height = 0
    x = 0 
    y = 0
    distance = atRestSpacing
    speed = 0
    localScale = 1
    life = 0
    flashSpeed = 0
    unsettledCount = 0
    acceleration = 0.10
    explosionCount  = 0
    backGraphic = None
    gridSoundPlaying = 0
    hintToRemove = 0
    
    def render(self):        
        PC.drawmodeNormal()
        x = self.x - cameraX
        y = self.y - cameraY
        width = self.width * self.localScale
        height = self.height * self.localScale
        x -= width/2
        y -= height/2
        if x+width>0:         
            PC.setColourize(1)  
            PC.drawmodeNormal()   
            alpha = clamp255(removeTrailCount * 5)
            PC.setColour(255,255,255,int(alpha))
            PC.drawImageScaled( self.backGraphic, x-4, y-4,width+8,height+8)        
            PC.drawImageScaled( self.graphic, x, y,width,height)
            if(self.hintToRemove):
                PC.drawmodeAdd()
                flashValue =clamp255(120 + math.sin(self.life/self.flashSpeed)*150)
                PC.setColour( 255, 255, 255, int(flashValue) )
                PC.drawImageScaled( self.graphic, x, y,width,height)
                PC.drawmodeNormal()
                PC.setColourize(0)     
        
    def tick(self,delta,connectedX,connectedY,facing,chainPos,rootDistanceScale,dangerCount):
        if chainPos == 0:
            self.atRestSpacing = self.targetSpacing * rootDistanceScale
        else:
            self.atRestSpacing = self.targetSpacing
        self.gridSoundPlaying -= delta
        if self.gridSoundPlaying<0:
            self.gridSoundPlaying = 0
        deltaX = connectedX-self.x
        deltaY = connectedY-self.y
        deltaX += (0.5 +chainPos/4.0)
        yOffset = math.sin(chainPos/2.0+(levelTime/75.0))*.1*chainPos
        deltaY += yOffset
        distance = math.sqrt((deltaY*deltaY)+(deltaX*deltaX))
        if distance ==0:
            unitX = 0
            unitY = 0
        else:
            unitX = deltaX/distance
            unitY = deltaY/distance
        self.localScale = 0.8/((chainPos/25.0)+1.0)
        dx = (unitX*self.distance*self.localScale*1.5)
        dy = (unitY*self.distance*self.localScale*1.5)
        self.x = connectedX - dx
        self.y = connectedY - dy           
        if self.x < cameraX+15 and levelMetaData.gridDeath:
            global firstEdge
            if firstEdge:
                particlesToDo = range(int((dangerCount+80)/80))
                for count in particlesToDo:
                    self.edgeExplosion(cameraX,2,(dangerCount+120)/120.0)
            firstEdge = 0
        
        self.life += delta
        self.flashSpeed = 6
        if self.flashSpeed < 2:
            self.flashSpeed = 2
        thisRestSpacing = self.atRestSpacing
        if self.distance>thisRestSpacing:
            acceleration = delta * self.acceleration
            self.speed += acceleration
            self.distance -= self.speed *delta
            if self.distance <= thisRestSpacing and self.speed>0:
                self.unsettledCount += delta
                if self.unsettledCount>10:
                    self.distance = thisRestSpacing
                    self.unsettledCount = 0
                    self.speed = 0    
                    if self.gridSoundPlaying==0:
                        playSimpleSound("grid5")
                        self.gridSoundPlaying = 5                    
                if self.speed > 0.1:
                    self.speed *= -0.5
                    self.distance = thisRestSpacing+0.1
                    if self.gridSoundPlaying==0:
                        playSimpleSound("grid6")
                        self.gridSoundPlaying = 10
                else:
                    self.distance = thisRestSpacing
                    self.speed = 0
                    self.unsettledCount = 0
                    if self.gridSoundPlaying==0:
                        playSimpleSound("grid5")
                        self.gridSoundPlaying = 5
                    
        elif self.distance ==thisRestSpacing:
            self.unsettledCount = 0
        else:
            self.distance = thisRestSpacing
    def edgeExplosion(self,thisX,deltaX,scale=1):
        x = thisX   
        y = self.y
        maxSize = 2
        deltaY = 0
        deltaX += 2-(random.randint(0,50)/10.0)
        deltaY -= (random.randint(0,60)/20.0)
        size = .5 + (random.randint(0,10)/50.0)
        size *= maxSize*scale
        particleChosenIndex = random.randint(1,2)
        if particleChosenIndex==1:
            particleChosen = fireParticle1()
        else:
            particleChosen = fireParticle2()
        particleController.addItem(particleChosen,x,y,size,deltaX,deltaY)
    
    def __init__(self,x,y,jewelIdx):
        self.x = x
        self.y = y
        self.jewelIdx = jewelIdx
        self.name = levelMetaData.jewelSet[jewelIdx]
        self.graphic = JPG_Resources[self.name] 
        self.width = PCR.imageWidth(self.graphic)
        self.height = PCR.imageHeight(self.graphic)
        self.backName = 'magneteffect01'
        self.backGraphic = JPG_Resources[self.backName ] 
        #print "jewel name",name,type
        
    def isAtRest(self):
        delta = self.distance - self.atRestSpacing
        if delta <0.2 and delta > -0.2:
            return 1
        else:
            return 0 
            

class trailGameClass:
    YOffset = 20
    XOffset = 20
    trail = []
    trailSettled = 0
    trailSettledOld = 0
    comboRun = 1
    dangerCount = 0
    maxDangerCount = 50
    dangerSoundCount = 0    
    doExplosion  = 0
    trailExplosionDelay = 10
    rootDistanceScale = 0
    newObject = None
    jewelStartX = 0
    addCount = 0
    jewelStartY = 0
    
    def initialise(self):
        self.YOffset = -10
        self.XOffset = -40
        self.trail = []
        self.trailSettled = 0
        self.trailSettledOld = 0
        self.comboRun = 1
        self.dangerCount = 0
        self.maxDangerCount = 200
        self.dangerSoundCount = 0    
        self.doExplosion  = 0
        self.trailExplosionDelay = 20
        self.addCount = 0
      
    def tick(self,delta):
        global removeTrailCount        
        removeTrailCount -= delta
        if removeTrailCount < 0:
            removeTrailCount = 0
            self.trail = []
        self.addCount -= delta
        if self.addCount < 0 or self.comboRun>1:
            self.addCount = 0
        if self.newObject:
            self.rootDistanceScale += delta/20
            self.moveNewJewel(delta)
        if self.rootDistanceScale>1:
            self.rootDistanceScale = 0
            self.trail.insert(0,self.newObject)
            self.newObject = None
        if globalPlayer != None:
            if levelMetaData.gridDeath:
                if self.doExplosion == 0:
                    self.offScreenCheck(delta)
                else:
                    self.checkDetonateLastObject(delta)
            connectedX = globalPlayer.x+(globalPlayer.width * globalPlayer.scale)/2+self.XOffset
            connectedY = globalPlayer.y+(globalPlayer.height+self.YOffset)
            chainPosition  = 0
            global firstEdge
            firstEdge = 1
            for segment in self.trail:
                if self.newObject:
                    segment.x -=4 * delta  #this is to stretch the chain out when a new element is being added
                segment.tick(delta,connectedX,connectedY,globalPlayer.facing,chainPosition,self.rootDistanceScale,self.dangerCount)
                connectedX = segment.x
                connectedY = segment.y 
                chainPosition += 1 
            #attempt to fix last bug where the game would trigger a run after a combo
              
            self.trailSettledOld =  self.trailSettled               
            self.trailSettled = self.testForSettled()   
            if self.trailSettled and self.trailSettledOld:
                self.comboRun = 1
            if self.trailSettled and (self.addCount==0 or self.trailSettledOld==0 or self.doExplosion):
                foundIndex = self.testForThree()  
                if foundIndex != -1:    
                    self.doExplosion  = 0
                    self.dangerCount = 0
                    if self.trailSettledOld == 0:
                        self.comboRun += 1    
                    else:
                        self.comboRun = 1
                    numberFound = self.removeMatch(foundIndex)
                    #self.trailSettled = 1
                    self.checkCombo(numberFound,self.comboRun)
 
                
            else:            
                #if self.trailSettled and self.trailSettledOld:
                #    self.comboRun = 1 
                foundIndex = self.testForThree()  
                if foundIndex != -1: 
                    for segment in self.trail: 
                        if segment.jewelIdx == foundIndex:
                            segment.hintToRemove = 1
            if len(self.trail)==0:
                self.doExplosion  = 0
            if len(self.trail)> 40:
                self.trail = self.trail[:-1]
    def render(self):            
        if self.newObject:
            self.newObject.render()
        for segment in self.trail:
            segment.render()
            if segment.x < cameraX: 
                return 0
        return 0

    def moveNewJewel(self,delta):
        connectedX = globalPlayer.x+(globalPlayer.width * globalPlayer.scale)/2+self.XOffset
        connectedY = globalPlayer.y+(globalPlayer.height+self.YOffset)
        deltaX = connectedX-self.newObject.x
        deltaY = connectedY-self.newObject.y
        distance = math.sqrt( (deltaX*deltaX) + (deltaY * deltaY))
        unitX = deltaX/distance
        unitY = deltaY/distance
        self.newObject.x += unitX*delta*distance/16
        self.newObject.y += unitY*delta*distance/16
        self.newObject.localScale -= delta/150.0
        return

    def addIt(self,jewelIDX,startX,startY):
        global removeTrailCount
        removeTrailCount = removeTrailCountStart
        width = 40  #nasty cludge becuase I can't be bothered to get the dimensions for the jewel
        height = 40
        x = startX + width/2
        y = startY + height/2
        if self.newObject : #New Object already getting added
            self.trail.insert(0,self.newObject)
            self.rootDistanceScale = 0
        self.newObject = trailObject(x,y,jewelIDX)
        self.newObject.flashSpeed = 200
        if len(self.trail)>1:
            if self.trail[0].jewelIdx == jewelIDX:
                self.addCount = 150
            else:
                self.addCount = 0
        else:
            self.addCount = 0
        
    def test(self,jewelIdx):
        if len(self.trail)<2:
            return 0 
        if self.trail[0].jewelIdx  == self.trail[1].jewelIdx  and self.trail[0].jewelIdx == jewelIdx:
            return 3
            
    def testForThree(self):
        trailLength = len(self.trail)
        if trailLength >= 3:
            for index in range(trailLength-2):
                if (self.trail[index].graphic == self.trail[index+1].graphic
                and self.trail[index+1].graphic == self.trail[index+2].graphic):
                    if (self.trail[index].isAtRest() 
                    and self.trail[index+1].isAtRest() 
                    and self.trail[index+2].isAtRest() ):
                        return self.trail[index].jewelIdx
        return -1

    def removeMatch(self,removeIdx):
        lengthTrail = len(self.trail)
        found = 0
        if lengthTrail>1:
            for index in range(lengthTrail-1):
                if self.trail[index].jewelIdx == removeIdx:
                    self.trail[index+1].distance +=  self.trail[index].distance  
                    self.trail[index+1].speed = 0    
                    self.trail[index+1].unsettledCount = 0.5                
        for index in self.trail[:]:
            if index.jewelIdx == removeIdx:
                found += 1
                self.explodeJem(index,self.comboRun-1)
                self.trail.remove(index)

        return found
      
    def testForSettled(self):
        for segment in self.trail:
            if segment.unsettledCount != 0:
                return 0
        return 1
        
    def checkCombo(self,found,combo):
        if(found):
            playSimpleSound("gridExplosion")
            tileBonus(found)
            if(combo == 2):
                ScreenMessages.setMessageScroll(messages.Combo,None)
                incComboLevel(2)
            elif(combo == 3):
                ScreenMessages.setMessageScroll(messages.SuperCombo,None)
                incComboLevel(3)
            elif(combo == 4):
                ScreenMessages.setMessageScroll(messages.MegaCombo,None)
                incComboLevel(4)
            elif(combo == 5):
                ScreenMessages.setMessageScroll(messages.UltraCombo,None)
                incComboLevel(5)
            elif(combo > 5):
                numberCombo = ' Plus ' + str(combo-5)
                ScreenMessages.setMessageScroll(messages.UltraCombo,None,numberCombo)
                incComboLevel(6)       
                
    def explodeJem(self,gemIndex,combo):
        x = gemIndex.x
        y = gemIndex.y
        scale = 1
        if(combo>0):
            scale += combo
        scale *= 0.5
        if x < cameraX-5:
            x = cameraX-5
            scale *= 1.25
        particleController.addItem(tileExplosion(),x,y,scale)
        
    def emptytrail(self,effect=0):
        self.doExplosion = 0 
        for segment in self.trail[:]: 
            if effect:
                x = segment.x
                y = segment.y
                deltaX = 2.0
                deltaY = -10
                deltaX += (0.5-(random.randint(0,10)/10.0))*8.0
                deltaY -= ((random.randint(0,10)/20.0))*4.0
                name = segment.name
                size =  segment.localScale
                particleController.addItem(fruitParticle(name,0),x,y,size,deltaX,deltaY)
            self.trail.remove(segment)
            
    def offScreenCheck(self,delta):  
        lengthTrail = len(self.trail)
        if lengthTrail>0:
            lastItem = self.trail[lengthTrail-1]
            timeIncrement = 20+(self.maxDangerCount-self.dangerCount)/10
            volume = .99
            if lastItem.x < cameraX:
                if self.dangerSoundCount==0 and gameOver == 0 and FinishFlag==0:
                    playSimpleSound("gridAlarm",volume)
                self.dangerCount+=delta
                self.dangerSoundCount+= delta
                if self.dangerSoundCount>timeIncrement:
                    self.dangerSoundCount = 0
            else:
                self.dangerCount = 0
                self.dangerSoundCount = 0
        if self.dangerCount > self.maxDangerCount:
            self.doExplosion = 1            
            
    def checkDetonateLastObject(self,delta):
        lengthTrail = len(self.trail)
        if lengthTrail>0:
            lastItem = self.trail[lengthTrail-1]
            #print "edge explosion",lastItem.x,cameraX
            if lastItem.x > cameraX:
                lastItem.edgeExplosion(lastItem.x,-2)
            if lastItem.explosionCount == 0:
                lastItem.explosionCount = self.trailExplosionDelay
            else:
               # print "trail delta", delta
                lastItem.explosionCount -= delta
                if lastItem.explosionCount < 0:
                    scale = 1.5
                    self.explodeJem(lastItem,scale)
                    self.trail.remove(lastItem)
                    lengthTrail = len(self.trail)
                    volume = 1.0 - lengthTrail/20.0
                    if volume < .12:
                        volume = 0.12

                    playSimpleSound("gridExplosion",volume)
                    if lengthTrail == 0:
                        globalPlayer.painCount = -1
                        globalPlayer.invulnerable = -1
                        global comboLevel
                        #comboLevel = 0
                        #if arcadeMode==1:
                        #    globalPlayer.Death(delta)
                        #else:
                        if comboLevel:
                            removeAllCombo()
                        else:
                            globalPlayer.Death(delta)
                        self.initialise()
        
trailGame = trailGameClass()
###########################################
# loadBase
# Called when resource handler is created.
# Should be used to populate it with basic
# resources required by the game.
#
# Simple games can do all their loading
# here.
###########################################
logoScreen = None
logoText1 = None
logoText2 = None
logoBack = None
pubLogo = None
logoLoaded = 0
loadingScreenLoaded = 0
uncrunchIndex=-30

levelMusic = ['Level1.ogg','Level2.ogg','Level3.ogg','Level4.ogg','Menu.ogg','cutScene.ogg']

def uncrunchMusic():
    global fileIndex
    global uncrunchIndex
    step = 15  #tony - this is set up so that it will uncrunch all the music when all files are loaded
    index = uncrunchIndex//step
    if index >=0 and index < len(levelMusic) and uncrunchIndex%step==0:
        song = levelMusic[index]
        file= 'extraResources/music/'+song
       # print "loading music ",file
        tempMusic =  PCR.loadTune( file )
        PCR.unloadTune(tempMusic) 
    uncrunchIndex += 1


def unloadLogoGFX():
    import PycapRes
    global logoLoaded 
    if logoLoaded:
        PycapRes.unloadImage(logoScreen)
        PycapRes.unloadImage(logoText1)
        PycapRes.unloadImage(logoText2)
        PycapRes.unloadImage(logoBack)
        if pubLogo:
            PycapRes.unloadImage(pubLogo)
        logoLoaded = 0

def unloadLoadingScreen():
    global loadingScreenLoaded
    if loadingScreenLoaded:
        PCR.unloadImage(loadingScreen)
        PCR.unloadImage(loadingBar)
        loadingScreenLoaded = 0
    
def loadBase():
        #print "loadBase called"
        import Pycap
        global PC
        global loadingScreen
        global loadingBar
        global logoScreen
        global logoText1
        global logoText2
        global logoBack
        PC = Pycap
        import PycapRes
        global res
        global pubLogo
        global whereIsSnakyJake
        global charlieBark
        pubLogo = None
        setLocalAppData()             
        if showLogo:
            charlieBark = PycapRes.loadSound( 'res/sounds/charlieBark.ogg')
#            whereIsSnakyJake = PycapRes.loadSound( 'res/sounds/whereIsSnakyJake.ogg')
        if showNonFreeLogos:
                logoScreen = PycapRes.loadImage('extraResources/Logos/Logo.jpg')
                logoText1 = PycapRes.loadImage('extraResources/Logos/LogoText1.jpg') 
                logoText2 = PycapRes.loadImage('extraResources/Logos/LogoText2.jpg') 
                logoBack = PycapRes.loadImage('extraResources/Logos/Bgrnd.jpg') 
                global logoLoaded 
                logoLoaded = 1
                pubLogo= PycapRes.loadImage('extraResources/Logos/tweeler.png') 
        global loadingScreenLoaded
        loadingScreenLoaded = 1
        loadingScreen = PycapRes.loadImage('extraResources/loading/loading.jpg')
        loadingBar = PycapRes.loadImage('extraResources/loading/FairyLoading.jpg')
        #print"loadingScreen"
        global font22
        global font23
        global font36
        global font38
        global font8
        font8= PycapRes.loadFont( "res/font/Arial8.txt" )
        font22 = PycapRes.loadFont( "res/font/KomikaText22.txt" )
        font23 = PycapRes.loadFont( "res/font/KomikaText24.txt" )
        font36 = PycapRes.loadFont( "res/font/KomikaText36.txt" )
        font38 = PycapRes.loadFont( "res/font/KomikaText38.txt" )
        highScoreCanvas.initialiseScores()
 

###########################################
# init
#
# Called when the game board is created,
# after resources have loaded. Set the 
# initial game state here.
#
###########################################
def init():
        #print "init called"
        global totalTimePlayed
        global currentProfile
        # load the pycap module
        #openUrl('http://tycho.usno.navy.mil/cgi-bin/timer.pl')          
        #All the game initialisation is done in here so that it can be redone when the game restarts after a game over
        #initialiseGame()
        regEntry = PC.readReg( "cheats" ) 
        if regEntry:
            cheatCanvas.active = int(regEntry)
        regEntry = PC.readReg( "totalTimePlayed" ) 
        if regEntry:
            totalTimePlayed = int(regEntry)
            totalTimePlayed *= 100
        else:
            #this will happen if the game has never been run before
            PC.setFullscreen(0)
            
        readProfiles()
       # print("user dir",PC.getUserDir("dummy"))

        savedProfile = PC.readReg("CurrentProfile")
        savedVersion = PC.readReg("Version")
        if savedVersion:
           savedVersion = int(savedVersion)
        else:
            savedVersion = -1
        if savedProfile:
            currentProfile = int(savedProfile)
        if savedVersion != currentVersion:
            #print "clearing profile",savedVersion, currentVersion
            currentProfile = 0
            for profile in profiles:
                profile.ressetProfile()
        PC.showMouse(cursorEnabled)
#        regEntry = PC.readReg( "hardware" ) 
        #if regEntry:
         #   if regEntry == "0":
          #      PC.set3DAccelerated(0)
           # else:
            #    PC.set3DAccelerated(1)
        regEntry = PC.readReg( "renderDetail" ) 
        if regEntry:
            global renderDetailLevel
            renderDetailLevel = int(regEntry)
        global messages 
        global levelData
        global cutScenes
        if profiles[currentProfile].currentLanguage == English:
            import messages as messages
            import levelData as levelData
            import cutScenes as cutScenes 
           # print"HangInstructions",messages.HangInstructions  
        else:    
            import messagesES as messages 
            import levelDataES as levelData 
            import cutScenesES as cutScenes            
          #  print"HangInstructions",messages.HangInstructions            
###########################################
# fini
#
# Called when the game board is destroyed.
# Clean up game state here.
#
###########################################
def fini():
        #print ("fini called")
        #print("Wrote time played",str(int(totalTimePlayed/100)))
        highScoreCanvas.writeScores()
        PC.writeReg( "totalTimePlayed",str(int(totalTimePlayed/100)))
        keyMap.saveKeysRegistry()
        writeProfiles()
        PC.writeReg("CurrentProfile",str(currentProfile))
        PC.writeReg("Version",str(currentVersion))
        PC.writeReg("cheats",str(int(cheatCanvas.active)))
        hardwareSupport = PC.getIs3DAccelerated()
        PC.writeReg("hardware",str(int(hardwareSupport)))
        PC.writeReg("renderDetail",str(int(renderDetailLevel)))
###########################################
# PlayMusic
#Wrapper for PC.PlayMusic
def playTune( tuneName):
    tune = MIDI_Resources[tuneName]
    PC.playTune(tune,2)
    setMusicVolume()

currentTunePlaying = None
nextTuneToPlay = None
tuneVolume = 0
killTune = 0
gLooping = 0
gFadeSpeed = 0.03
gFadeTune = 0
gCurrentPitch = 0
gTargetPitch = 0
targetVolume = 0
instance = 1
oldInstance = 1
oldInstanceVolume = 0

def playTuneOgg( tuneName,looping,fadeSpeed = 0.005):
    global nextTuneToPlay
    global gLooping
    global gFadeSpeed
    global gFadeTune
    global currentTunePlaying
    global oldInstance
    global instance
    global oldInstanceVolume
    
    oldInstance = instance
    oldInstanceVolume = tuneVolume
    instance += 1
    if instance > 1:
        instance = 0
    if gFadeTune:
        gFadeTune = 0
        PC.playTune( currentLoadedMusic, 1)
        #PC.playSoundInstance( currentLoadedMusic,0,0, 0,1,instance)
        
    if tuneName:
        nextTuneToPlay = tuneName
        gLooping = looping
        gFadeSpeed = fadeSpeed
        gFadeTune = 0

    else:
        stopTuneOgg()
    
currentLoadedMusic = -1
currentLoadedName = ""

def checkLoadedMusicOgg(tuneName):
    global currentLoadedMusic
    global currentLoadedName

    if currentLoadedName != tuneName:        
        if currentLoadedMusic != -1:
            PCR.unloadTune(currentLoadedMusic)
        currentLoadedMusic = PCR.loadTune( "extraResources/music/"+tuneName)
        currentLoadedName = tuneName
        
def tuneTick(delta):
    global currentTunePlaying
    global nextTuneToPlay
    global tuneVolume
    global killTune
    global gFadeTune
    global gCurrentPitch
    global gTargetPitch
    global targetVolume
    global oldInstanceVolume
    pitch = 0
    pan = 0
    if nextTuneToPlay:
        panning = 1
        checkLoadedMusicOgg(nextTuneToPlay)
        PC.playTune( currentLoadedMusic,gLooping) 
        tuneVolume = 0        
        currentTunePlaying = nextTuneToPlay
        nextTuneToPlay = None
        gFadeTune = 0
        killTune = 0
        gCurrentPitch = 0
        gTargetPitch = 0
        targetVolume = 1

    if (currentTunePlaying and nextTuneToPlay) or (currentTunePlaying and killTune):   
        tuneVolume -= delta * gFadeSpeed
       # print "fading down",tuneVolume
        if tuneVolume < 0:
            tuneVolume = 0
            currentTunePlaying = None
        newTuneVolume = profiles[currentProfile].musicVolume*0.25 * tuneVolume
        PC.setVolume( newTuneVolume ) 
    elif currentTunePlaying:
        if tuneVolume<targetVolume:
            tuneVolume += delta * gFadeSpeed
            if tuneVolume > targetVolume:
                tuneVolume = targetVolume
        if tuneVolume>targetVolume:
            tuneVolume -= delta * gFadeSpeed
            if tuneVolume < targetVolume:
                tuneVolume = targetVolume
        newTuneVolume = profiles[currentProfile].musicVolume*0.25 * tuneVolume
        PC.setVolume( newTuneVolume)   
    if gCurrentPitch<gTargetPitch:
        gCurrentPitch += delta/20.0
        if gCurrentPitch > gTargetPitch:
            gCurrentPitch = gTargetPitch
    if gCurrentPitch>gTargetPitch:
        gCurrentPitch -= delta/20.0
        if gCurrentPitch < gTargetPitch:
            gCurrentPitch = gTargetPitch
            
    if oldInstanceVolume  > 0: 
        oldInstanceVolume -= delta * gFadeSpeed*2.0
        if oldInstanceVolume < 0:
            oldInstanceVolume = 0  
        newTuneVolume = profiles[currentProfile].musicVolume*0.25 * oldInstanceVolume                
        PC.setVolume( newTuneVolume)             
def stopTuneOgg():
    global killTune
    killTune = 1
    
def setTargetpitch(target):
    global gTargetPitch
    gTargetPitch = target
    
def incTargetpitch(inc):
    global gTargetPitch
    gTargetPitch += inc
    
def setTargetVolume(target):
    global targetVolume
    targetVolume = target
    
def forceSoundUpdate():
    global tuneVolume
    if PC == None:
        return
    pan = 0
    if currentTunePlaying:
        playTuneOgg(currentLoadedMusic, gLooping)             
        tuneVolume = 0
        

###########################################
# PlaySound
#Wrapper for PC.PlaySound
def playSound( Sound,volume,panning,pitch):
    PC.playSound( WAV_Resources[Sound],volume,panning-1, pitch)

def stopTune():
    PC.stopTune()
###########################################
# PlaySound
#Wrapper for PC.PlaySound which takes a list of alternate sounds and picks one
def playSimpleSoundList( SoundList,panning=1,volume = 1):
    if(SoundList != None):
        index = random.randint(1,len(SoundList))
        if SoundList[index-1] != None:
            PC.playSound( WAV_Resources[SoundList[index-1]],profiles[currentProfile].soundVolume/4.0*volume,panning,0)

def playSimpleSoundDistance( Sound,soundX):
    if(Sound != None):
        middleScreen =  cameraX+400
        attenuation = soundX- middleScreen
        if attenuation <0:
            attenuation *=-1
        attenuation = 500 - attenuation
        if attenuation>0:
            attenuation /= 800.0
            PC.playSound( WAV_Resources[Sound],attenuation*profiles[currentProfile].soundVolume/4.0,0,0)
                

def playMusicSimple(Sound,tuneVolume = 1):
    if Sound != None:
        MusicVolume = profiles[currentProfile].musicVolume/4.0 * tuneVolume
        PC.playSound( WAV_Resources[Sound],MusicVolume,0,0)

def playSimpleSound( Sound,volume = 1,panning=1):
    if(Sound != None):
        PC.playSound( WAV_Resources[Sound],(profiles[currentProfile].soundVolume/4.0)*volume,panning,0)

soundClock = 0
def testSound():
    global soundClock
    if(soundClock==0):
    #  playSound( 'Ding', 1,((time%500)/500.0), 1)
        playSound( 'Ding', 1,1000, 1)
        soundClock = 20
    else:
        soundClock -= 1
        ###########################################
# MouseWheel
#
# Mouse Wheel handling. Called on wheel turn.
# Parameter is wheel direction.
#
###########################################
def mouseWheel(delta):
    #import copy
    global mouseWheelPos
    global mouseDelta
    global editorScrollBar
    global editorScrolled
    editorScrolled = 1
    editorScrollBar += delta
    if editorScrollBar<0:
      editorScrollBar =0

    mouseDelta = delta
    mouseWheelPos += delta
###########################################
# keydown
#
# Key handling. Called on keypress.
# Parameter is key code.
#
###########################################
def keydown( key ):
        global downKey
        #print "keydown called with", key
        global keyArray
        #print(key)
        if(key>0 and key <512):
            keyArray[key] = 1
        if(key>0 and key <255):
            workingString.addChar(key)
        downKey=key
###########################################
# keyup
#
# Key handling. Called on key release.
# Parameter is key code.
#
###########################################
def keyup( key ):
        global keyArray
      
        if(key>0 and key <512):
            keyArray[key] = 0
            keyRepeatArray[key] = 0
###########################################
# exitGame
#
# Return non-zero if game should terminate 
#
###########################################
def checkKey(key):
    global keyRepeatArray
    if(keyArray[key] == 1):
        keyRepeatArray[key] = 1   
        return 1
    return 0
    
def checkKeyNoRepeat(key):
    global keyRepeatArray
    if(keyArray[key] == 1 and keyRepeatArray[key] == 0):
        keyRepeatArray[key] = 1   
        return 1
    return 0

def checkKeyUp(key):
    if keyArray[key] == 0: 
        return 1
    return 0

def noKeyDown():
    for key in keyArray:
        if key != 0:
            return 0
    return 1

def anyKeyDown():
    found = 0
    for key in keyArray:
        if key != 0:
            keyRepeatArray[key] = 1
            found = 1
    return found

def exitGame(): 
        return doExit;
 
###########################################
oldCameraX=0

def ScrollWorld(delta):
    global cameraX
    global inEditor
    global platformsToSpawn
   # print "in here",cameraX,oldCameraX
    if( inEditor==0):
        if finishOn == 0 and forcePause == 0 and gamePaused==0 and escapeMenu.active==0:
            if globalPlayer:
                deltaX = globalPlayer.x-cameraX
                if arcadeMode:
                    if deltaX>400:
                        adaptive.doingWell(delta/30.0)
                    elif deltaX<150:
                        adaptive.doingBadly(delta/30.0)
        cameraX += scrollManager.getScrollSpeed(delta)
        if(levelMetaData.RandomSpawns >0):
            platformsToSpawn = ((-1 * math.cos(cameraX/400))+1)*levelMetaData.RandomSpawns

def doInstructions(delta):
    global thisLevelTutioral
    if levelMetaData.Instructions:
        if globalPlayer:
            if tutorialsOn and arcadeMode == 0 and thisLevelTutioral==0 and globalPlayer.PlatformOn:
                thisLevelTutioral += 1
                instructionManager.showInstruction(levelMetaData.Instructions)  
                setLevelAttempted(levelNumber)      
# update
#
# Basic tick function. Parameter is a time
# delta.
#
###########################################

def update( delta ):
        # call the draw function
        PC.markDirty()
        global time
        global inEditor
        global lives
        global score
        global tempDelta
        global gamePaused
        global totalTimePlayed
        global displayScore
        global startLevelTimer
        global  levelTime
        global gameOver
        global continousTime
        global oldCameraX
        global double1DownCount
        global double2DownCount
        global smartBombCount
        global globalOldPlatformOn
        global oldCameraX
        global waspSoundDelay
        if gamePaused:
            return
        waspSoundDelay -= delta
        tuneTick(delta)
        if double1DownCount>0:
            double1DownCount -= delta
            if double1DownCount<=0:
                double1DownCount = 0
                globalOldPlatformOn = None
        if double2DownCount>0:
            double2DownCount -= delta
            if double2DownCount<=0:
                double2DownCount = 0
                globalOldPlatformOn = None
#        if smartBombCount<0:
#            smartBombCount = 0
        oldCameraX = cameraX
        tickCursors(delta)
        continousTime += delta
        instructionManager.tick(delta)
        particleController.tick(delta)
       # print "pre fade"
        fadeManager.tick(delta)
       # print "post fade"
        scoreDelta = score - displayScore
        updatePowerUpFlags(delta)    #update all teh power up flags ready for the loop
        if(scoreDelta>0):
            increment = 1+((scoreDelta-1)/50)
            displayScore += increment
        if(displayScore>score):
            displayScore = score


          
        if(dataIsLoaded==0):
            loadResources(delta)
        else:
            if(gamePaused or forcePause or escapeMenu.active):
                delta = 0
                if escapeMenu.active:
                    escapeMenu.tick(delta)
            time += delta
            tempDelta = delta+1
            ScreenMessages.tickMessages(delta)
            medalion.tick(delta)
            PC.showMouse(cursorEnabled)
            inGameMenuManager.tick(delta)
            if(metaGame):
                StartGameTick(delta)
            elif(FinishFlag == 1):
                tickObjects(delta)
                if arcadeMode:
                    finishActionLevelTick(delta)
                else:
                    finishStoryLevelTick(delta)
            else:
                firstTickLevel()

                if(gameOver==0):
                    totalTimePlayed += delta
                ScrollWorld(delta)
                if(gameOver):
                    if gridType == 0:
                        tickGrid(delta)
                    else:
                        if scrollManager.slowDown:
                          #  print "slow down"
                            trailGame.tick(delta/4.0)
                        else:
                             trailGame.tick(delta)                         
                    gameOverMenu.tick(delta)
                elif(checkKey(keyMap.editorKey.keyValue)) or inEditor:  #if we are already in the editor or want to enter it
                    EditorTick(delta)
                    editorTickObjects(delta)
                else:
                    if arcadeMode:
                        scrollManager.setScrollSpeed() 
                    mapName.tick(delta)
                    if startLevelTimer>0:
                        startLevelTimer -= delta
                    if startLevelTimer < 0:
                        startLevelTimer = 0
                    cheatCanvas.mainLoopTick()
                    smartBomb.tick(delta)
                    deltaWarp=timeWarp.tick(delta)
                    tickRandomEnemySpawn(delta)
                    tickObjects(delta*deltaWarp)
                    
                    if gridType==0:
                        tickGrid(delta)
                    else:
                        if scrollManager.slowDown:
                            trailGame.tick(delta/4.0)
                        else:
                            trailGame.tick(delta)  
                    scrollManager.tick(delta*deltaWarp)
                    deleteObjects()
                    spawnObjectOnScroll()
                    doInstructions(delta)
                    levelTime += delta
                    if(playerInWorld==0):
                        object= spawnPlayer()
                        object.restartPlayer()
                    if escapeMenu.active==0:
                        if(checkKeyNoRepeat(keyMap.escapeKey.keyValue) and forcePause == 0):
                            escapeMenu.toggle()
                            test = 1
        oldCameraX = cameraX
        
def insertObject(object):
    if len(objects)== 0:
        objects.append(object)   
    else:
        index = 0
        for nextObject in objects[:]:
            if object.z > nextObject.z:
                objects.insert(index,object)
                return
            index += 1
        #if we get to here then this is object has the greatest Z so goes on teh end of the list
        objects.append(object)

###########################################
# Add Object
#
# Adds an Object to the list of world objects
#
###########################################
def addObject(ID,x,y,type,platformIDX=-1):
        global objects
        global nextID
       # import PycapRes
       # import copy
        global editorToggle
        
#        newObject = StaticPlatform()
        newObject = copy.copy(AllWorldObjects[int(type)])
        newObject.type = type
        newObject.ID = ID
        newObject.y = y
        newObject.x = x
        newObject.topExtent = y
        if type == WorldTypes.DynamicPlatform or type == WorldTypes.fastDynamicPlatform:
            newObject.leftExtent = newObject.x
            newObject.rightExtent = newObject.x + StaticPlatformXRange

        if type == WorldTypes.DynamicVerticalPlatform or type == WorldTypes.fastDynamicVerticalPlatform:
            newObject.TopExtent = newObject.y
            newObject.BottomExtent = newObject.y + StaticPlatformXRange
        if platformIDX != -1:
            newObject.platformIDX=platformIDX        
        newObject.setUpGraphics()
        if(inEditor):
            #If we are in the editor then we always spawn our object
            insertObject(newObject)  
        else:
            if newObject.canBePlaced():
                newObject.spawn()
                insertObject(newObject)         
        nextID += 1 #bump the ID count
        return newObject


def InitialiseAllFixedObjects():   
    global ObjectStarts
    global nextObjectX
    index = 0
    for platform in ObjectStarts:
        ID = platform[0]
        type = platform[1]
        x = platform[2]
        y = platform[3]
        addObject(ID,x,y,type)
        index += 1
        
def getRandomPlatform(range):  
    type = WorldTypes.RedPlatform
    if(range==0):
        type = WorldTypes.StaticPlatform
    elif(range==1):
        type = WorldTypes.RedPlatform
    else:
        tile = random.randint(1,range)
        if(tile==1):
            type = WorldTypes.RedPlatform
        elif(tile==2):
            type = WorldTypes.GreenPlatform
        elif(tile==3):
            type = WorldTypes.BluePlatform 
        elif(tile==4):
            type = WorldTypes.OrangePlatform
        elif(tile==5):
            type = WorldTypes.PurplePlatform
        elif(tile==6):
            type = WorldTypes.YellowPlatform             
        elif(tile==7):
            type = WorldTypes.WhitePlatform    
        elif(tile==8):
            type = WorldTypes.BlackPlatform  
        elif(tile==9):
            type = WorldTypes.StripePlatform  
    return type
    
def getRandomColour(range):
    type = WorldTypes.RedPlatform
    if(range==0):
        type = 'none'
    elif(range==1):
        type = 'red'
    else:
        tile = random.randint(1,range)
        type = getColour(tile)
    return type
    
def getColour(tile):
    type = 'none'
    if(tile==1):
        type = 'Red'
    elif(tile==2):
        type = 'Green'
    elif(tile==3):
        type = 'Blue'
    elif(tile==4):
        type = 'Orange'
    elif(tile==5):
        type = 'Purple'
    elif(tile==6):
        type = 'Yellow'            
    elif(tile==7):
        type = 'White'    
    elif(tile==8):
        type = 'Black'
    elif(tile==9):
        type = 'Stripe'
    return type

def spawnObjectOnScroll():
    global ObjectStarts
    global nextObjectIndex
    global continousWorldXOffset
    global StagingFlag
    if globalFairy == None and fairyEnabled:
        launchFairy()
    if(nextObjectIndex >= len(ObjectStarts)):
        return #no more objects
    while (ObjectStarts[nextObjectIndex][2]+continousWorldXOffset < (cameraX+x_max+200) ):
        platformIDX = -1   #this has to be set to -1 for default
        platform = ObjectStarts[nextObjectIndex]
        ID = platform[0]
        type = platform[1]
        x = platform[2]+continousWorldXOffset
        y = platform[3]
        if type ==WorldTypes.Coin50 or type ==WorldTypes.Coin250 or type ==WorldTypes.Coin1000:
            global coinsSpawned
            coinsSpawned += 1
        if(type == WorldTypes.RandomPlatform100 or type == WorldTypes.RandomPlatform200 or type == WorldTypes.RandomPlatform400):
            if type == WorldTypes.RandomPlatform100:
                platformIDX=levelData.platform100   
            elif type == WorldTypes.RandomPlatform200:
                platformIDX=levelData.platform200   
            else:
                platformIDX=levelData.platform400  
            type= getRandomPlatform(levelMetaData.RandomTiles)
            
            y = ((int(y/PlatformPitchY))*PlatformPitchY)+4            
        if(type== WorldTypes.FinishPlatform):
            if(arcadeMode==1):
                if profiles[currentProfile].arcadeProgress < levelNumber:
                    profiles[currentProfile].arcadeProgress = levelNumber 
                #we've spawned the staging platform so bump the level and start the next set
                if levelNumber%levelsPerArcadeSegment != 0 or levelNumber > levelsInArcde:
                    type = WorldTypes.StagingPlatform
                    continousWorldXOffset = x+100
                    nextObjectIndex=-1 # because it gets incremented later
                    setUpNextLevel()
                    StagingFlag = 1
        addObject(ID,x,y,type,platformIDX)
        randomAdditionSpawns(x)
        nextObjectIndex += 1
        if(nextObjectIndex >= len(ObjectStarts)):
            return #no more objects

#Called from the editor after updating the level
def updateObjectStarts():
    global ObjectStarts
    while len(ObjectStarts)>0:  #clear the array
        ObjectStarts.pop()
    #print("length objectstarts before",len(ObjectStarts))
    for object in objects:
        #while we are here we'll round down the y to the nearest row
        #delta = object.y%40
        #object.y -= delta
        if(object.canBeSaved): #spider webs don't get inserted
            insertIntoStarts(object)

#called by updateObjectStarts by editor
def insertIntoStarts(newObject):
    global ObjectStarts
    count = 0
    temp = [newObject.ID,newObject.type,newObject.x,newObject.y]
    if(len(ObjectStarts)==0):
    #first Object
        ObjectStarts.append(temp)
    else:
        objectInserted = 0
        for platform in ObjectStarts:
            if(platform[2]>newObject.x):
                ObjectStarts.insert(count,temp)
                objectInserted = 1
                break
            count+=1
        if(objectInserted ==0):
            #Goes on end of list
            ObjectStarts.append(temp)
            
def checkSpawnCollision(x,y):
    min_x = x-30
    max_x = x+130
    min_y = y-30
    max_y = y +30
    
    for object in objects:
        if(max_x>object.x-30) and (min_x<(object.x+130)) and(max_y>object.y-30) and (min_y<(object.y+30)):
            return 1
    return 0    

def randomAdditionSpawns(base_x):
  for count in range(platformsToSpawn):
      x = random.randint(int(base_x-150),int(base_x))
      y = random.randint(1,12)
      y *= 40 
      y = y_max - y
      type= getRandomPlatform(levelMetaData.RandomTiles)  
      addObject(nextID,x,y,type)        

###########################################
# RenderObjects
#
# Loops through all the objects in the list rendering them
#
###########################################
def RenderObjects():
    global objects
    #pass 0
    for thisObject in objects:
            thisObject.render()
########################################
# TickObjects
#
# Loops through all the objects in the list ticking them
#
###########################################

def testForSolid(thisObject):
    if thisObject.solid or thisObject == globalPlayer or thisObject == globalFairy:   
        return 1
    else:
        return 0

def tickObjects(delta):
    global objects
    global solidObjects
    numberObjects = 0
    numberSolidObjects = 0
    solidObjects = list(filter(testForSolid,objects))
#    solidObjects = []
#    for thisObject in objects:
#        if thisObject.solid or thisObject == globalPlayer or thisObject == globalFairy:
#            solidObjects.append(thisObject)

    for thisObject in objects[:]:
        if scrollManager.slowDown:
            if thisObject == globalPlayer:
                thisObject.tick(delta)
            else:
                thisObject.tick(delta/4)
        else:
            thisObject.tick(delta)
        numberObjects += 1
#    print "objects active and number solid active",numberObjects,numberSolidObjects
    if globalPlayer and timeWarp.enabled()>0:
        globalPlayer.tick(delta)
        globalPlayer.tick(delta)
        globalPlayer.tick(delta)
        globalPlayer.tick(delta)   
            

def editorTickObjects(delta):  
    global objects
    for thisObject in objects[:]:
        thisObject.editorTick(delta) 

def deleteObjects():
    DeleteIndex = -1
    thisObjectCount = 0
    tempObject = None
    global objects
    for thisObject in objects[:]:
        if((thisObject.x + thisObject.width)- cameraX) < -100 or (thisObject.y>cameraY+800):
              if(thisObject != globalPlayer and thisObject.spawner != 1 and thisObject != globalFairy):  #never delete the player and spawners
                #unusedObjects.append(thisObject)
                objects.remove(thisObject)
                #print "unusedObjects", len(unusedObjects)



def addToMid(scenery,ScenerySource):
        nextIndex =  random.randint(0,len(ScenerySource)-1)
        item = Scenery()
        item.name = ScenerySource[nextIndex]
        item.X = cameraX/2+x_max + random.randint(50,500)
        item.width = PCR.imageWidth(JPG_Resources[item.name])
        item.height = PCR.imageHeight(JPG_Resources[item.name])
        scenery.append(item)
  

def checkRemoveMid(scenery):
    for item in scenery[:]:
        if item.X+item.width < cameraX/2:
            scenery.remove(item)
     
def renderMidbottom():
    PC.setColour(255,255,255,255 )
    lastItemX = 0 
    for item in levelMetaData.LowerScenery:
        width = item.width
        y = y_max - item.height
        graphic = JPG_Resources[item.name]  
        PC.drawImage( graphic, item.X-cameraX/2, y)  
        lastItemX = item.X+width
    checkRemoveMid(levelMetaData.LowerScenery)
    if lastItemX<cameraX/2+x_max+(width/2):  #add on width/2 so we get some overlap
        addToMid(levelMetaData.LowerScenery,levelMetaData.currentSection[1])

def renderMidTop():
    PC.setColour(255,255,255,255 )
    lastItemX = 0
    for item in levelMetaData.UpperScenery:
        width = item.width
        y = 0
        graphic = JPG_Resources[item.name]  
        PC.drawImage( graphic, item.X-cameraX/2, y)
        lastItemX = item.X+width
    checkRemoveMid(levelMetaData.UpperScenery)
    if lastItemX<cameraX/2+x_max+(width/2):
        addToMid(levelMetaData.UpperScenery,levelMetaData.currentSection[2])

def renderGideLines():
    y=0
    while y<y_max:
        PC.setColour(0,255,0,48 )
        PC.fillRect( 0, y, 800, 1 )
        y += GridPitchY
    x = 0
    while x < 800:
        PC.setColour(0,255,0,48 )
        PC.fillRect( x, 0, 1, 600 )
        x += GridPitchY        
 
 
def renderBack():  
    if renderDetailLevel > 0:
        y = 0
        x = (0-cameraX)/4 
        PC.setColour(255,255,255,255 )
        graphic = backDropManager.backDropResource 
        width = PCR.imageWidth( graphic )  
        x = (x%width)-width
        PC.drawImage( graphic, x, 0)
        #if this image doesn't fill the screen then repeat it!
        if(x+width<800):
            PC.drawImage( graphic, x+width, 0) 
    else:
        if backDropManager.backDropLoaded == "Backdrop4":
            PC.setColour(10,50,10,255)
        elif backDropManager.backDropLoaded == "Backdrop2":
            PC.setColour(30,30,30,255)
        elif backDropManager.backDropLoaded == "Backdrop3":
            PC.setColour(00,50,50,255)
        else:
            PC.setColour(40,40,00,255)
        PC.fillRect(0,0, 800,600)      
gridFlash=0
gridFillHeight=0
targetGridFillHeight=0
gridAlarmSoundEnabled = 0

def renderGridBackGround():
    global gridFlash
    global gridFillHeight
    global targetGridFillHeight
    if(gridRight>0 or gridLeft < 800):
        if(gridFillRight==1):
            x1 = gridLeft
            x2= x_max
        else:
            x1 = 0
            x2 = gridRight
        #PC.setColourize(1)
        #PC.setColour(255,255,255,100)
        #graphic = JPG_Resources['gridBackDrop']    
        #PC.drawImage( graphic, x1, 0)
        #PC.setColour(255,0,32,100 )
        PC.setColour(int(155+(100*math.sin(gridFlash))),0,32,200 )
        PC.fillRect(x1,600-gridFillHeight, x2,gridFillHeight)
        PC.setColour(32,0,240,100 )
        PC.fillRect(x1,0, x2,600-gridFillHeight)
        PC.setColourize(1)
        PC.setColour(255,255,255,80)
        graphic = JPG_Resources['gridBackDrop']
        PC.drawImage( graphic, x1, 0)
        
def tickGridBackGround(delta): 
    global gridFlash 
    global targetGridFillHeight
    global gridFillHeight
    global gridAlarmSoundEnabled
    global gridLeftTarget
    global gridRightTarget
    if(gridFillHeight<targetGridFillHeight):
        gridFillHeight+=delta
    if(gridFillHeight>targetGridFillHeight):
        gridFillHeight-=delta
    
    if gameOver:
            gridLeftTarget = x_max
            gridRightTarget = 0  
    
    risk = tilesOver*riskIncrement
    y1 = risk/maximumRisk
    targetGridFillHeight = y1* 600
    if(y1<0.70):
        gridFlash = 11/6
    else:
        speed = (y1-0.60)
        gridFlash+= speed
        if math.sin(gridFlash)>0.9 and gridAlarmSoundEnabled:
            if(gridLeft<800):
                playSimpleSound("gridAlarm",y1*0.5)
            gridAlarmSoundEnabled= 0
        elif  math.sin(gridFlash)< -0.9:
            gridAlarmSoundEnabled= 1
                
            
    
def renderBackGround():
    renderBack()
    if PC.getIs3DAccelerated():
        renderMidbottom()
        renderMidTop()
    if(inEditor ==1):
        renderGideLines()
        
def renderEditorBackground():
    PC.setColour(20,66,0,255)
    PC.fillRect(0,0,editorWidth,600)

###########################################
# draw
#
# Basic draw function. Make all render
# calls from here and here alone.
#
###########################################
def draw():
        global objects
        # draw some stuff
        #import PycapRes
        global time
        global resx
        global resy 
        global fontx
        global fonty
        global rotation
        if(dataIsLoaded==0):
            renderLoadingScreen()
        else:
            renderGame()
        fadeManager.render()

copyRightMessage = ScreenMessage()
doNoDistribute = ScreenMessage()
Demo = ScreenMessage()

startLogoFade = 600
logoCount = startLogoFade-50
pubLogoCount = startLogoFade

def renderpubLogo():
    global pubLogoCount
    x = 0
    y = 0
   # import PycapRes
    if showNonFreeLogos:
        PC.drawImage( pubLogo ,0, 0)
    else:
        PC.setFont( font36 )
        drawStringDropShadow("Tweeler presents....",200,300,255,255,255)         
    fadeAlpha = (150-pubLogoCount)*3
    if pubLogoCount>startLogoFade-300:
        fadeAlpha = (300-(startLogoFade-pubLogoCount))
    if fadeAlpha>255:
        fadeAlpha = 255
    if fadeAlpha>0:
        if fadeAlpha > 255:
            fadeAlpha = 255
        PC.setColourize(1)
        PC.setColour(0,0,0,int(fadeAlpha))
        PC.fillRect( 0,0,800,600)
        PC.setColourize(0)

startLogoFade = 500
logoCount = startLogoFade

def renderLogo():
    x = 100
    y = 50
    #import PycapRes
    if showNonFreeLogos:
        PC.drawImage( logoBack ,0, 0)
        PC.drawImage( logoScreen ,x, y)
        angle = (logoCount+250-startLogoFade)/300.0
        if (int(logoCount)%40)<20:
            logoText = logoText1
        else:
            logoText = logoText2
        PC.drawImageRot( logoText,x, y,angle) 
    else:
        PC.setFont( font36 )
        drawStringDropShadow("A Charlie Dog Games Production",75,300,255,255,255)         
    fadeAlpha = (150-logoCount)*3
    if logoCount>startLogoFade-300:
        fadeAlpha = (300-(startLogoFade-logoCount))
    if fadeAlpha>255:
        fadeAlpha = 255
    if fadeAlpha>0:
        if fadeAlpha > 255:
            fadeAlpha = 255
        PC.setColourize(1)
        PC.setColour(0,0,0,int(fadeAlpha))
        PC.fillRect( 0,0,800,600)
        PC.setColourize(0)
    
def tickLogo(delta):
    global logoCount
    logoCount -= delta
    if showLogo==0:
        logoCount = 0

    
def tickpubLogo(delta):
    global pubLogoCount
    pubLogoCount -= delta
    if showLogo==0:
        pubLogoCount = 0   
        
loadAlpha = 255

def tickLoading(delta):
    global loadAlpha
    loadAlpha -= delta*4
    if loadAlpha < 0:
        loadAlpha = 0

def renderLoadingScreen():
    if pubLogoCount > 0:
        renderpubLogo()
        return
    if logoCount > 0:
        renderLogo()
        return
    message = messages.Loading
    tabY = 450
    copyRightMessage.setMessage(message[0],message[2],message[3],message[4],message[5],message[6],tabY,0,-1,None,None,None,0)
    message = messages.DemoOnly
    tabY = 330
    Demo.setMessage(message[0],message[2],message[3],message[4],message[5],message[6],tabY,0,-1,None,None,None,0)
    message = messages.NotDistribute
    tabY = 370
    doNoDistribute.setMessage(message[0],message[2],message[3],message[4],message[5],message[6],tabY,0,-1,None,None,None,0)
    PC.drawmodeNormal()
    PC.setColour(24,0,80,32 )
    graphic = loadingScreen 
    PC.drawImage( graphic,0, 0)
    #copyRightMessage.RenderMessage()
#    Demo.RenderMessage()
 #   doNoDistribute.RenderMessage()
    LoadingBarX = 100
    fraction = 1
    if(len(allGraphicFilesNames)!=0):
        fraction = (fileIndex*545)/(len(allGraphicFilesNames))
    JakePos = LoadingBarX+ fraction
    PC.drawImage( loadingBar,int(JakePos), 493)
    alpha = loadAlpha
    if alpha>0:
        if alpha > 255:
            alpha = 255
        PC.setColourize(1)
        PC.setColour(0,0,0,int(alpha))
        PC.fillRect( 0,0,800,600)
        PC.setColourize(0)
    
def renderGame():
    if gamePaused:
        return
    if(metaGame):
        StartGameDraw()
    else:
        renderBackGround()
        RenderObjects()
        smartBomb.render()
        if(inEditor==0):
            if gridType==0:
                RenderGrid()
            else:
                trailGame.render()
            if inGameMenuManager.isActive() == 0:
                RenderHUD()
            escapeMenu.render()
        else:
            renderEditorBackground()
        scrollManager.render()
        if(inEditor):
            RenderEditor()
        if(FinishFlag == 1):
            if arcadeMode:
                renderActionLevelFinish()
            else:
                renderStoryLevelFinish()
    instructionManager.render()
    ScreenMessages.RenderMessages()
    particleController.render()
    renderCursors()
    inGameMenuManager.render()
    if mouseOverMessage != None:
        if mouseOverMessage.function!=None:
            mouseOverMessage.function(mouseOverMessage.parameter)
        mouseOverMessage.function=None

def RenderLives():
    ThisX = gridLeft
    PC.setColourize(0)
    if(lives==0):
        return
    if lives>5:
        PC.drawImage( JPG_Resources['Life'], ThisX-130, 5)   
        liveString = " x "+str(lives)
        drawStringDropShadow(liveString,ThisX-90,55,60,200,0)         
    else:
        for life in range(lives):
            ThisX -= 44
            PC.drawImage( JPG_Resources['Life'], ThisX, 5)
            
def missedCoinRender():
    if levelCompleted(finalLevel) and missedCoin ==0:
        PC.drawImage( JPG_Resources['coinMissed'], 500, 5)        
        
def drawStringDropShadow(string,x,y,r,g,b):        
        PC.setColour( 0, 0, 0, 180 ) 
        PC.drawString(string, x+3, y+3) 
        PC.setColour( int(r), int(g), int(b), 255 )
        PC.drawString(string, x, y) 
 
def setglobalDebug1(value):
    global globalDebug1
    globalDebug1 = value
 
def renderGlobalDebug1(): 
    PC.setColour(255,255,255,255 )
    PC.setFont( font22 )
    string = "DB1 "+str(globalDebug1)
    PC.drawString(string, 650,100) 

def RenderHUD():
        global lives
        PC.drawmodeNormal()
        PC.setColour( 255, 255, 255, 255 )
        PC.setFont( font36 )
        PC.setColour( 255, 255, 255, 255 )
        scoreX= gridRight+15
        PC.setFont( font36 )
        scoreString= messages.HUDScoreString
        drawStringDropShadow(scoreString,scoreX,scoreY,254,106,184) 
        length = PCR.stringWidth(scoreString,font36)
        scoreX += length + 10
        multiplierString = "(x" + str(int(getMutliplier()))+")"
        if getMutliplier()>1: 
            PC.setFont( font22 )
            drawStringDropShadow(multiplierString,scoreX,scoreY,254,106,184)
            scoreX += PCR.stringWidth(multiplierString,font22)+10
            
        scoreString = numberToString(displayScore)
        PC.setFont( font36 )
        drawStringDropShadow(scoreString,scoreX,scoreY,254,106,184)        
        RenderLives()
        medalion.render(360,5,1)
        mapName.render()
        if arcadeMode == 0:
            missedCoinRender()
        #renderDebugHud()
      
def renderDebugHud():
    adaptive.renderDebug()
  #  renderGlobalDebug1()
        
          
class classMapName:
    alpha = 0
    x = 10
    y = 590
    oldString = ""
    r=255
    g=255
    b=255
    def render(self):
        PC.setFont( font22 )
        if levelMetaData:
            if self.oldString != levelMetaData.title:
                self.alpha = 255
                self.r = 255
                self.g = 255
                self.b = 255   
                if levelNumber!=1 and levelNumber!=( (levelsPerArcadeSegment*1) +1) and levelNumber!=(( levelsPerArcadeSegment*2) +1) and levelNumber!=( (levelsPerArcadeSegment*3)+1) and arcadeMode==1:
                    playSimpleSound("levelUp")
            self.oldString = levelMetaData.title
            if arcadeMode:
                thisNumber = levelNumber
            else:
                thisNumber = levelMetaData.levelNumber
            global highScoreLevelNumber
            highScoreLevelNumber =  thisNumber   
            string = "Level: "+str(thisNumber)+" "+levelMetaData.title
            PC.setColour( 0, 0, 0, 180 ) 
            PC.drawString(string, self.x+3, self.y+3) 
            PC.setColour(int(self.r), int(self.g), int(self.b), int(self.alpha) )
            PC.drawString(string, self.x, self.y) 
            
    def tick(self,delta):
        if self.alpha>150:
            self.alpha-= delta
        if self.r > 60:
            self.r -= delta
        if self.g > 200:
            self.g -= delta
        if self.b > 0:
            self.b -= delta
            
mapName = classMapName()
        
def renderStoryLevelFinish(): 
      forcePause = 1
      rectAlpha = (EndLength-FinishTimer)*5
      if(rectAlpha>200):
          rectAlpha = 150
      PC.setColour(0,0,0,int(rectAlpha))
      PC.fillRect(0,0,800,600)

def renderActionLevelFinish(): 
      forcePause = 1
      rectAlpha = (EndLength-FinishTimer)*5
      if(rectAlpha>200):
          rectAlpha = 150
      PC.setColour(0,0,0,int(rectAlpha))
      PC.fillRect(0,0,800,600)
     
def StartGameDraw():
    if metaGame >=1:
        menuClasses[metaGame].render()
            
GanyKeyPressed=0

class EscapeMenuClass:
    active = 0
    def tick(self,delta):
        if self.active:
            if checkKeyNoRepeat(keyMap.escapeKey.keyValue):
                returnToStoryEscape()
       
    def render(self):
        if self.active:
            return 0
        
    def toggle(self):
        if self.active:
            self.active = 0
            ScreenMessages.clearMessages()
        else:
            if self.active == 0:
                setTargetVolume(quietMusic)
            ScreenMessages.clearMessages()
            self.active = 1
            setLevelAttempted(levelNumber) 
            x = 250
            y = 200
            ScreenMessages.setMessageStatic(messages.Paused,None,-1,y,None,None) 
            y += 80
            ScreenMessages.setMessageStatic(messages.ResumeLevel,None,x,y,resumeLevel,None) 
            if arcadeMode == 0:
                y += 60
                ScreenMessages.setMessageStatic(messages.RestartLevel,None,x,y,setUpReplayLevel,None) 
            y += 60
            ScreenMessages.setMessageStatic(messages.QuitLevel,None,x,y,returnToStoryEscape,None)   
            
escapeMenu = EscapeMenuClass()


def killPlayer():
    global gameOver
    if gameOver ==0:
        gameOver = 1
        adaptive.doingBadly(250) #lost game so doing really badly!       
        gameOverMenu.startMessages()       

def decrementLives():
    global lives
    lives -= 1
    trailGame.emptytrail(1)
    if lives == 0:
        inGameMenuManager.makeActive(inGameMenuManager.gameOverCanvas)
        setLevelAttempted(levelNumber) 
        stopTuneOgg()
        playMusicSimple(levelMetaData.loseMusic)

class GameOverMenuClass:
    active = 0
    def tick(self,delta):
        return 0
       
    def render(self):
        return 0
        
    def startMessages(self):
        global oldMetaGame  
        if highScoreCanvas.newHighScore(score)!= -1 and arcadeMode ==1:
            fadeManager.fadeDown(menuItems.highScoreCanvas)
            oldMetaGame = 0 
            escapeMenu.active = 0
            return
        y = 260
        x = 220
        ScreenMessages.setMessageStatic(messages.RestartLevel,None,x,y,gameOverRestartLevel,None) 
        y += 60
        if arcadeMode:
            ScreenMessages.setMessageStatic(messages.QuitLevel,None,x,y,returnToStory,None) 
        else:
            ScreenMessages.setMessageStatic(messages.ContinueStory,None,x,y,returnToStory,None)
            
gameOverMenu = GameOverMenuClass()

def doHighScoreMenu():
    global oldMetaGame
    oldMetaGame = 0 
    fadeManager.fadeDown(menuItems.highScoreCanvas)
    #startGame = 1
    escapeMenu.active = 0

def gameOverRestartLevel():
    global gameOver
    global levelNumber
    gameOver = 1  
    escapeMenu.active = 0  
    highScoreCanvas.cameFromLevel = 0
    inGameMenuManager.makeActive(0)
    if arcadeMode and levelNumber>1:
        levelNumber = 1
    setupLevel()
    replayLevel()
    
def resumeLevel():
    escapeMenu.active = 0 
    ScreenMessages.clearMessages()
    setTargetVolume(1)
    
completedMessage = [messages.jungleFinished,messages.caveFinished,messages.parkFinished,messages.cellarFinished]

continueMessage = [messages.jungleStart,messages.caveStart,messages.parkStart,messages.cellarStart]
    
def finishActionLevelTick(delta):  
    global forcePause
    global FinishTimer
    global GanyKeyPressed
    global score
    liveBonusValue = 1000
    totalBonus = 0
    crittersCollectedBonus = 0
    coinsCollectedBonus = 0
    tabX = 150
    totalBonus = crittersCollectedBonus+coinsCollectedBonus
    score += totalBonus
    if  FinishTimer == EndLength:
        GanyKeyPressed= 1
        inGameMenuManager.makeActive(inGameMenuManager.levelCompleteCanvas)
        y = 330
        stopTuneOgg()
        playMusicSimple(levelMetaData.winMusic)
        ScreenMessages.setMessageStatic(completedMessage[(levelNumber-2)/levelsPerArcadeSegment],None,tabX,y,None,None) 
        y += 60
        ScreenMessages.setMessageStatic(messages.CurrentScore,None,tabX,y,None,str(score)) 
        y = 550
        tabX = 200
        ScreenMessages.setMessageStatic(continueMessage[(levelNumber)/levelsPerArcadeSegment],None,tabX,y,continueAction,None) 
        
    FinishTimer -= delta
    if(FinishTimer<0):
        FinishTimer = 0
    if noKeyDown():
        GanyKeyPressed= 0
    if anyKeyDown() and GanyKeyPressed==0:
        returnToStory()  
    
def continueAction():
    global oldMetaGame
    oldMetaGame = 0
    fadeManager.fadeDown(menuItems.arcadeLevel)

def finishStoryLevelTick(delta):
    global forcePause
    global FinishTimer
    global GanyKeyPressed
    liveBonusValue = 1000
    setLevelCompleteStatus()
    coinsCollectedFlag = 0
    crittersCollectedFlag = 0
    crittersCollectedBonus = 0
    tabX = -1
    if lives > 1 and levelNumber > 2:
        livesBonus = (lives-1)*liveBonusValue
    else:
        livesBonus = 0
    if(coinsCollected == coinsSpawned and coinsSpawned):
        coinsCollectedBonus = int((score) *0.50)
        coinsCollectedFlag = 1
    else:
        coinsCollectedBonus = 0
    if(crittersCollected == crittersSpawned and crittersSpawned):
        crittersCollectedBonus = int((score)*0.50)
        crittersCollectedFlag = 1
    else:
        crittersCollectedBonus = 0
    totalBonus = livesBonus+crittersCollectedBonus+coinsCollectedBonus
    totalScore = score + totalBonus
    if  FinishTimer == EndLength:
        if levelNumber >2:
            adaptive.doingWell(500)      
        GanyKeyPressed= 1
        inGameMenuManager.makeActive(inGameMenuManager.levelCompleteCanvas)
        y = 320
        setLevelData(coinsCollectedFlag,totalScore,crittersCollectedFlag)    
        stopTuneOgg()
        playMusicSimple(levelMetaData.winMusic)
        
        if totalBonus:
            ScreenMessages.setMessageStatic(messages.BaseScore,None,tabX,y,None,numberToString(score))
            y += 36
        if(coinsCollected == coinsSpawned and coinsCollected>0):
            playSimpleSound("ImadeItWithCoins")
        else:
            playSimpleSound("IMadeIt1") 
        if(coinsCollected>0):
            if(coinsCollected == coinsSpawned):
                ScreenMessages.setMessageStatic(messages.AllCoinCollected,None,tabX,y,None,numberToString(coinsCollectedBonus))
                y += 36
            else:
                temp = 0
        if(crittersCollected>0):
            if(crittersCollected == crittersSpawned):
                ScreenMessages.setMessageStatic(messages.AllCrittersCollected,None,tabX,y,None,numberToString(crittersCollectedBonus))
                y += 36
            else:
                temp = 0
        if(livesBonus >0 ):
            ScreenMessages.setMessageStatic(messages.UnUsedLives,None,tabX,y,None,str(livesBonus))
            y += 36
        y += 20    
        if (levelNumber>1 or arcadeMode==1):
            ScreenMessages.setMessageStatic(messages.TotalScore,None,tabX,y,None,numberToString(totalScore)) 
        
        y = 550
        tabX = -1
        ScreenMessages.setMessageStatic(messages.ReplayLevel,None,tabX,y,setUpReplayLevel,None) 
        y += 40
        ScreenMessages.setMessageStatic(messages.ContinueStory,None,tabX,y,returnToStory,None) 
        
    FinishTimer -= delta
    if(FinishTimer<0):
        FinishTimer = 0
    if noKeyDown():
        GanyKeyPressed= 0
    if anyKeyDown() and GanyKeyPressed==0:
        returnToStory() 
      
def setUpReplayLevel():
    global oldMetaGame
    oldMetaGame = 0
    fadeManager.fadeDown(menuItems.replayLevel)
#    playTuneOgg (levelMetaData.introMusic,1)

    
def replayLevel():
    ressetScore(0)
    ressetLives()
    launchLevel(levelNumber)
    ScreenMessages.clearMessages()
    fadeManager.fadeUp()



def setLevelCompleteStatus():
    if(ExitFlag==0):  #if we have not exited through the emergency exit and some lives left...
        #If we haven't finished this level before then maybe we need to do something special
        storyCanvas.endDemo = 0
        if levelNumber == 61:
            storyCanvas.cutScene = 2
        elif levelNumber == 62:
            storyCanvas.cutScene = 3
        elif levelNumber == 63:
            if profiles[currentProfile].campaignMaps[levelNumber].done != 2:
                profiles[currentProfile].tutorials = 0  #disable tutorials as we pass this level
            storyCanvas.cutScene = 4
        elif levelNumber == 48:
            if allAmuletGot() == 0:
                storyCanvas.cutScene = 5
            elif testAllCoinsInGame()==0:
                storyCanvas.cutScene = 6

            else:
                storyCanvas.cutScene = 7
        elif levelNumber == 49:
            storyCanvas.cutScene = 8
        profiles[currentProfile].campaignMaps[levelNumber].done=2
    else:
        profiles[currentProfile].campaignMaps[levelNumber].done=1

def returnToStoryEscape():
    global oldMetaGame
    escapeMenu.active = 0
    oldMetaGame = 0
    if arcadeMode: 
        if highScoreCanvas.newHighScore(score)!= -1 and arcadeMode ==1:
            fadeManager.fadeDown(menuItems.highScoreCanvas)
            oldMetaGame = 0 
            escapeMenu.active = 0
        else:
            fadeManager.fadeDown(menuItems.mainScreenCanvas)
    else:
        fadeManager.fadeDown(menuItems.storyCanvas)

def returnToStory():
    global metaGame
    global oldMetaGame
    oldMetaGame = 0 
    if arcadeMode:
        fadeManager.fadeDown(menuItems.mainScreenCanvas)
    else:
        if storyCanvas.endDemo == 1:
            fadeManager.fadeDown(menuItems.sellUpCanvas)
        else:
            fadeManager.fadeDown(menuItems.storyCanvas)
    #startGame = 1
    escapeMenu.active = 0
    
def setLevelData(newCoins,newScore,newCritters):
      if newCoins:
          profiles[currentProfile].campaignMaps[levelNumber].coins=1
      if newScore>profiles[currentProfile].campaignMaps[levelNumber].score:
          profiles[currentProfile].campaignMaps[levelNumber].score=newScore
      if newCritters:
          profiles[currentProfile].campaignMaps[levelNumber].critters=1
          
def launchLevel(newNumber): 
    global levelNumber
    global globalFairy
   # print("changing levels",levelNumber,newNumber)
    levelNumber = newNumber
    objects = []
    globalFairy = None
    scrollManager.clearDashMode()
    initialiseLevel()
    
def StartGameTick(delta):
        global startGame
        global canStart
        if metaGame >=1:
            menuClasses[metaGame].tick(delta)
            cheatCanvas.checkActivation(delta)
            

sectionIcon=[[0,"cellarButton"],[1,"parkButton"],[2,"caveButton"],[3,"jungleButton"]]

def InitialiseObjectIcons():
    global editorScrollBar
    x = 0
    y = 0
    yOffset = 5
    index = editorScrollBar
    displayCount = 0
    displayRange = 48
    ScreenMessages.clearMessages()
#    print "in editor 2",editorScrollBar,(int(editorScrollBar)*iconsWide)
 #   for object in AllWorldObjects[editorScrollBar:]:
    for objectIndex in range(len(AllWorldObjects)):
        index = objectIndex+(int(editorScrollBar)*iconsWide)
        if displayCount<displayRange and index < len(AllWorldObjects):
            object = AllWorldObjects[index]
            height = 46
            if(object.placeable):
                graphicName = object.getGraphic()
                function = selectedMapIcon
                truncatedName = object.name[0:7]
                ScreenMessages.setMessageStatic(messages.Blank8Green, graphicName,x*iconWidth,(y*height)+yOffset,function,parameter=index,string=truncatedName)       
                x+=1
                if(x>=iconsWide):
                    x=0
                    y+= 1
                displayCount += 1
    x = 0
    for icon in sectionIcon:
        graphicName = icon[1]
        index = icon[0]
        width = 35
        height = 47
        yOffset = 20
        ScreenMessages.setMessageStatic(messages.Blank22, graphicName,x*width,570,selectSection,parameter=index)  
        x += 1
    ScreenMessages.setMessageStatic(messages.changeRandom, None,(x*width)+37,595,incrementRandom)
    
def selectSection(section):
    map_Section[levelMetaData.currentLevelFile]= section
    LoadLevelData()
    for thisObject in objects:
        thisObject.setUpGraphics()
    InitialiseObjectIcons()
        
def incrementRandom():
    random = map_Jewels[levelMetaData.currentLevelFile]
    random += 1
    if random>9:
        random = 0
    if random ==1:
        random = 4
    map_Jewels[levelMetaData.currentLevelFile] = random
    LoadLevelData()
    
def selectedMapIcon(index):
   # print "selected",index
    x = cameraX+mousex
    y = mousey
    newObject = addObject(nextID,x-20,y-30,index)
    newObject.x = x-newObject.width/2
    newObject.y = y- newObject.height/2
    newObject.mouseXoffset = -newObject.width/2
    newObject.mouseYoffset = -newObject.height/2
    newObject.Selected = 1
    return 0


def EditorTick(delta):
   # import copy
   # import PycapRes
    global InEditorKeyUP
    global cameraX
    global inEditor
    global CursorY
    global ObjectSelected
    global lives
    global ObjectStarts
    global nextID
    global inEditor
    global objects
    global playerInWorld
    global nextObjectIndex
    global editorMoveSpeed
    global  mouseEnabled
    global editorAddObject
    global mouseDelta
    global newEditorObject
    global inGUI
    global editorScrolled
    if editorScrolled:
        InitialiseObjectIcons()
        editorScrolled = 0
    if(inEditor == 0 and editorEnabled):
        #First time in Editor
        inEditor = 1
        inGUI = 1
     #   print("Entering Editor")
        objects = []
        InitialiseAllFixedObjects()   
        InitialiseObjectIcons()
        playerInWorld= 0
        mouseEnabled = 1
        newEditorObject = WorldTypes.StaticPlatform
        #editorTickOnceObjects(delta)
        
    if(checkKey(keyMap.escapeKey.keyValue) and editorToggle ==0):
        if editorEnabled == 2:
            workingString.clearString()
            workingString.length = 9 
            global enteringLevelName        
            enteringLevelName = 1
        else:
            inEditor = 0
            updateObjectStarts()
            objects = []
            SaveLevelData("")
            nextObjectIndex = 0
            mouseEnabled = 1
            inGUI = 0
            ScreenMessages.clearMessages()
    if checkKey(keyMap.enterKey.keyValue) and enteringLevelName and len(workingString.thisString):    
        #leaving editor
        #print("leaving Editor")
        inEditor = 0
        updateObjectStarts()
        objects = []
        SaveLevelData(workingString.thisString)
        nextObjectIndex = 0
        mouseEnabled = 1
        inGUI = 0
        ScreenMessages.clearMessages()
    if(checkKey(keyMap.reloadKey.keyValue)):
        LoadLevelData()
        objects = []
        InitialiseAllFixedObjects()
        playerInWorld= 0
    ressetLives()
    increment = .03
    if(mousex<50 and mousey>560):
        cameraX -= (50-mousex)/2
    if(mousex>x_max-50 and mousey>560):
        cameraX += (mousex+50-x_max)/2     
    if(checkKey(keyMap.deleteKey.keyValue)):
        for object in objects:
            if object.Selected:
                objects.remove(object)
    for object in objects:
        if(object.Selected):
                    if(checkKey(keyMap.leftKey.keyValue)):
                        object.x -=editorMoveSpeed
                    if(checkKey(keyMap.rightKey.keyValue)):
                        object.x +=editorMoveSpeed
                    if(checkKey(keyMap.upKey.keyValue)):
                        object.y -=editorMoveSpeed
                    if(checkKey(keyMap.downKey.keyValue)):
                        object.y +=editorMoveSpeed                           

def RenderEditor():
    PC.drawmodeNormal()
    PC.drawImageScaled( JPG_Resources['Cursor'], 400-20, CursorY-20, 40, 40)
    PC.setColour( 60,200,0,255)
    PC.setFont( font22 )
    PC.drawString(str(levelMetaData.RandomTiles), 180, 595 )
    if enteringLevelName:
        PC.setColour( 0,0,0, 255 )
        x = 300
        y = 200
        PC.fillRect(x,y,200,50)
        PC.drawmodeNormal() 
        PC.setColour( 255,255,255, 255 )
        PC.setColourize(1)
        PC.setFont( font36 )
        PC.drawString(str(workingString.getDisplayString()), x+40, y+10 )        
    
firstTimeMainScreen =1   

class Score:
    name = ''
    score = 0
    time = 0
    
InitialScores = [
    ['CharlieDog',4000000,0],
    ['Victoria',3000000,0],
    ['Rowan',2000000,0],
    ['Grace',1000000,0],
    ['Joseph',500000,0],
    ['Farbs',250000,0],
    ['Ed',100000,0],
    ['Simon',50000,0],
    ['Peter',25000,0],
    ['Moses',10000,0],
]
   
class canvas:
    life = 0
    animationSwitch =20
    frameNumber = 0
    life = 0
    animation= animationSets.splash_screen1
    backdrop = "Menu"
    frame = None
    title = None
    titleY = -100
    titleRotation = 0.1
    titleTargetY = 10
    titleSpeed = 0
    targetRotation = 0.1
    frame1X = 20
    frame1Y = 330
    frame2X= 780
    frame2Y = 330
    frameScale = 1
    overlay = None
    
    def ressetTitle(self):
        self.titleY = -100
        self.titleRotation = 0.1
        self.titleTargetY = 10
        self.titleSpeed = 0
        self.targetRotation = 0.1
    
 
    def tick(self,delta):
        if metaGame != oldMetaGame:
            fadeManager.fadeUp()
        self.life += delta
        self.animationSwitch -= delta;
        if(self.animationSwitch<= 0):
            self.frameNumber = self.animation[self.frameNumber][1]
            self.animationSwitch = self.animation[self.frameNumber][2]
        
        if(self.title != None):
            self.titleSpeed += 0.7
            self.titleY += self.titleSpeed
            if(self.titleRotation<self.targetRotation):
                self.titleRotation += 0.03
                if(self.titleRotation>self.targetRotation):
                    self.titleRotation=self.targetRotation
            if(self.titleRotation>self.targetRotation):
                self.titleRotation -= 0.03
                if(self.titleRotation<self.targetRotation):
                    self.titleRotation=self.targetRotation            
            if(self.titleY >self.titleTargetY):
                self.targetRotation = self.titleRotation * -0.4
                if(self.titleSpeed>.5):
                    self.titleSpeed *= -0.5
                else:
                    self.titleSpeed = 0
                self.titleY = self.titleTargetY
        
    def render(self):
        PC.setColour(255,255,255,255 )
        if self.backdrop:
            graphic = JPG_Resources[self.backdrop]    #main bac
            PC.drawImage( graphic, 0, 0)
#        if self.overlay != None:
#            PC.setColourize(1)
#            PC.drawmodeAdd()
#            PC.setColour(255,200,180,48 )
#            graphic = self.overlay    #overlay
#            PC.drawImage( graphic, 0, 0)
        PC.setColourize(0)
        PC.drawmodeNormal()
        if(self.title != None):
            width = PCR.imageWidth(self.title)
            if self.titleRotation>0:
                rotation = self.titleRotation
            else:
                rotation = (44/7) + self.titleRotation
            PC.drawImageRot( self.title, (800-width)/2, self.titleY,self.titleRotation) 
        if(self.frame != None):
            width = PCR.imageWidth(self.frame)
            height = PCR.imageHeight(self.frame)
            if(self.frame1X != -1):
                PC.drawImageScaled( self.frame, self.frame1X, self.frame1Y,width*self.frameScale,height*self.frameScale)
            if(self.frame2X != -1):
               PC.drawImageScaled( self.frame, self.frame2X, self.frame2Y,-width,height)

class HighScores(canvas):
    scores = []
    pope = 0
    x=0
    y=0
    cameFromLevel = 0
    def initialiseScores(self):
        self.scores = []
        thisScore = None
        thisScore =  PC.readReg("HighScore")
        if(thisScore):
        #    print("Loading scores from registry")
            while(len(thisScore)>2):
                newScore = Score()
                dividor = thisScore.find('\n')
                newScore.name = thisScore[:dividor]
                thisScore = thisScore[dividor+1:]
                dividor  = thisScore.find('\n')
                newScore.score = int(thisScore[:dividor])
                thisScore = thisScore[dividor+1 :]
                dividor  = thisScore.find('\n')
                newScore.time = int(thisScore[:dividor])
                thisScore = thisScore[dividor+1 :]
                self.scores.append(newScore)
        else:
     #     print("Loading scores from default")
          for score in InitialScores:
              newScore = Score()
              newScore.name = score[0]
              newScore.score = score[1]
              newScore.time=score[2]
              self.scores.append(newScore)
    def writeScores(self):
        concatenatedScore = ""
        for score in self.scores:
            concatenatedScore = concatenatedScore+str(score.name)+'\n'+str(score.score)+'\n'+str(score.time)+'\n'
        if(PC.writeReg( "HighScore", concatenatedScore )):
            temp = 1
            #print("wrote score to registry")
            

    
    def displayScores(self):
        index =0
        x = self.x
        for score in self.scores:

            if(index != scorePos):
                PC.setColour( int(255-(index*10)), int(150+(index*10)),0,255 )
                PC.setFont( font22 )
                PC.drawString(score.name, x, self.y )
            else:
                PC.setColour( 255,0,0,255)
                PC.setFont( font22 )
                PC.drawString(str(workingString.getDisplayString()),x, self.y )
            scoreString = numberToString(score.score)
            PC.drawString(scoreString, x+180, self.y )
            #x += 2
            self.y = self.y + 31
            index += 1
            
    def tryInsert(self,thisscore,doInsert=1):
        index = 0
        for score in self.scores:
            if(thisscore>score.score):
                if doInsert:
                    global scorePos
                    tail = self.scores[index:]
                    head = self.scores[:index]
                    newScore = Score()
                    newScore.score=thisscore
                    newScore.name = ''
                    newScore.time = int(totalTimePlayed/100)
                    head.append(newScore)
                    self.scores = head+tail 
                    self.scores.pop() 
                    scorePos = index                   
                return index
            index+=1
        return -1
    def setName(self):
        if(scorePos>=0 and scorePos < len(self.scores)):
            self.newName = workingString.thisString
            self.scores[scorePos].name = workingString.thisString
    
    def newHighScore(self,thisscore):
        index = 0
        for score in self.scores:
            if(thisscore>score.score):
           #     print "high score",thisscore,score.score
                return index
            index+=1
        return -1
        
    def render(self):
#        self.overlay = JPG_Resources["MenuMask"]
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        self.title = JPG_Resources["HighScore"]
        self.frame1X = -1
        self.frame2Y = 250
        canvas.render(self)
        self.x = 250
        self.y = 215
        PC.setFont( font22 )
        self.displayScores()
        
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        canvas.tick(self,delta)
        self.life += delta
        if(oldMetaGame!= metaGame):
            ScreenMessages.clearMessages()
            workingString.clearString()
            workingString.length = 9
            scorePos=self.tryInsert(score)
            self.newScore = score
            oldMetaGame = metaGame
            y = 500
            x = 260
            if scorePos == -1: 
                if self.cameFromLevel:              
                    ScreenMessages.setMessageStatic(messages.RestartLevel,None,-1,y,gameOverRestartLevel,None) 
                y += 50
                x += 10                
                ScreenMessages.setMessageStatic(messages.returnMenuLrg,None,-1,y,backtoMainScreen)
            else:
                ScreenMessages.setMessageStatic(messages.NewHighScoreMenu,None,-1,540,None) 
                ScreenMessages.setMessageStatic(messages.EnterName,None,-1,590,None) 
            canvas.ressetTitle(self)

        if checkKeyNoRepeat(keyMap.enterKey.keyValue) or checkKeyNoRepeat(keyMap.escapeKey.keyValue):
            if scorePos >= 0:
                self.setName()
                ScreenMessages.clearMessages()
                if self.cameFromLevel:  
                    ScreenMessages.setMessageStatic(messages.RestartLevel,None,-1,screenHeight - 70,gameOverRestartLevel,None)              
                ScreenMessages.setMessageStatic(messages.returnMenu,None,-1,screenHeight - 40,backtoMainScreen)
                ScreenMessages.setMessageStatic(messages.UploadButton,None,-1,screenHeight - 10,self.UploadHighScore)
                scorePos = -1
                ressetScore(0)
            else:
                scorePos = -1
                backtoMainScreen()  

    def UploadHighScore(self):
        score = self.newScore
        name = self.newName
        level = highScoreLevelNumber + 1
        self.sendScore(score,level,name)
        backtoMainScreen()
            
highScoreCanvas = HighScores() 

def ressetScore(newScore=0):
    global score
    global nextLifeScoreTarget
#   newScore = 2499999
    score = newScore
    nextLifeScoreTarget = 5000
    
def ressetLives(newLives=startLives):
    global lives
    lives = newLives

class mainScreen(canvas):
    def render(self):
        PC.setColour( 40, 220, 0, 255 )
        PC.setFont( font36 )
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        self.title = JPG_Resources["Title"]
#        self.overlay = JPG_Resources["MenuMask"]
        self.frame1X = -1
        self.frame2X = 770
        self.frame2Y = 280
        canvas.render(self)
        PC.drawmodeNormal() 
        PC.setFont(font22)
        PC.setColour(210, 190, 255, 255)
        versionString = "Version 1."+str(currentVersion)     
        PC.drawString(  versionString,30,580)      
            
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        canvas.tick(self,delta)
        if(metaGame != oldMetaGame):
            fairyPointer.enabled = 1
            #playTune("MainScreen")
            if currentTunePlaying != levelData.menuSong:
                playTuneOgg(levelData.menuSong,1)
            inGUI = 1
            oldMetaGame = metaGame
            ScreenMessages.clearMessages()
            startX = 110
            XStep =  29
            StartY = 260
            YStep = 50
            curve = 2
            ScreenMessages.setMessageStatic(messages.WelcomeBack,None,startX,StartY,None,profiles[currentProfile].playerName)
            startX += XStep+60
            StartY += YStep+1
            ScreenMessages.setMessageStatic(messages.Story,None,startX,StartY,selectStory)
            startX += XStep
            XStep += curve
            StartY += YStep
            ScreenMessages.setMessageStatic(messages.Arcade,None,startX,StartY,selectArcade) 
            startX += XStep
            XStep += curve
            StartY += YStep
            ScreenMessages.setMessageStatic(messages.ChangeProfile,None,startX,StartY,changeProfile)
            startX += XStep
            XStep += curve
            StartY += YStep
            ScreenMessages.setMessageStatic(messages.HighScore,None,startX,StartY,selectHighScore)
            startX += XStep
            XStep += curve
            StartY += YStep            
            ScreenMessages.setMessageStatic(messages.Options,None,startX,StartY,selectOptions)
            startX += XStep
            XStep += curve
            StartY += YStep
            ScreenMessages.setMessageStatic(messages.Quit,None,startX,StartY,exitGameOption) 
            startX += XStep
            XStep += curve
            StartY += YStep
            #ScreenMessages.setMessageStatic(messages.CharlieWeb,None,-1,595,launchCharlie) 
            if cheatCanvas.active:
                ScreenMessages.setMessageStatic(messages.Cheats,None,700,595,selectCheats)            
            mouseEnabled = 1
           # versionString = "Version 1."+str(currentVersion)  
            canvas.ressetTitle(self)  


mainScreenCanvas = mainScreen()
  
class WelcomeScreen(canvas):
    def render(self):
        self.frame1X = -1
        self.frame2X = 790
        self.frame2Y = 320
        PC.setColour( 40, 220, 0, 255 )
        PC.setFont( font36 )
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        self.title = JPG_Resources["Title"]
        canvas.render(self)
            
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        canvas.tick(self,delta)
        if(metaGame != oldMetaGame):
            inGUI = 1
            oldMetaGame = metaGame
            ScreenMessages.clearMessages()
            x = -1
            ScreenMessages.setMessageStatic(messages.Welcome,None,x,240,None,profiles[currentProfile].playerName+"!")
            x = -1
            ScreenMessages.setMessageStatic(messages.WelcomeInstructions1,None,x,290,None) 
            ScreenMessages.setMessageStatic(messages.WelcomeInstructions2,None,x,330,None) 
            ScreenMessages.setMessageStatic(messages.WelcomeInstructions3,None,x,370,None) 
            ScreenMessages.setMessageStatic(messages.WelcomeStory,None,270,480,selectStory) 
            ScreenMessages.setMessageStatic(messages.WelcomeMainMenu,None,270,530,backtoMainScreen)        
            mouseEnabled = 1
            canvas.ressetTitle(self)


welcomeCanvas = WelcomeScreen()
copywrite2 = "all game code is copywrite Charlie Dog Games August 2006"  
class CheatScreen(canvas):
    AllLevelOn = 0
    AllPowerOn = 0
    ScaleUpOn = 0
    active = 0
    def render(self):
        PC.setColour( 40, 220, 0, 255 )
        PC.setFont( font36 )
        self.title = JPG_Resources["Title"]
        canvas.render(self)
            
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        canvas.tick(self,delta)
        if(metaGame != oldMetaGame):
            inGUI = 1
            oldMetaGame = metaGame
            ScreenMessages.clearMessages()
            ScreenMessages.setMessageStatic(messages.CheatTitle,None,-1,230,None) 
            y = 280
            if self.AllLevelOn:
                ScreenMessages.setMessageStatic(messages.AllLevelOn,None,-1,y,self.AllLevelCheat) 
            else:
                ScreenMessages.setMessageStatic(messages.AllLevelOff,None,-1,y,self.AllLevelCheat)
            y+= 35
            
            if self.AllPowerOn:
                ScreenMessages.setMessageStatic(messages.AllPowerOn,None,-1,y,self.AllPowerCheat) 
            else:
                ScreenMessages.setMessageStatic(messages.AllPowerOff,None,-1,y,self.AllPowerCheat)
            y+= 35
            
            if self.ScaleUpOn:
                ScreenMessages.setMessageStatic(messages.ScaleCheatOn,None,-1,y,self.scaleCheat) 
            else:
                ScreenMessages.setMessageStatic(messages.ScaleCheatOff,None,-1,y,self.scaleCheat)
            
            y+= 35  


            ScreenMessages.setMessageStatic(messages.AllLevelComplete,None,-1,y,allLevelComplete) 
            
            y+= 35
            string = "Game Mode: "+str(adaptive.gameMode) +"   Compensator: " +str(int(profiles[currentProfile].compensator))        
            ScreenMessages.setMessageStatic(messages.Blank22,None,-1,y,None,string) 
            
            y+= 35
            
            ScreenMessages.setMessageStatic(messages.WelcomeMainMenu,None,-1,580,backtoMainScreen)        
            mouseEnabled = 1
            canvas.ressetTitle(self)
            
    def checkActivation(self,delta):
        global oldMetaGame
        if ((checkKey(keyMap.leftControlKey.keyValue) or checkKey(keyMap.rightControlKey.keyValue) ) and showLogo == 0):
            if checkKeyNoRepeat(keyMap.cheatKey.keyValue):
                oldMetaGame = -1
                if self.active == 0:
                    self.active = 1
                else: 
                    self.active = 0
            
    def AllLevelCheat(self):
        global oldMetaGame
        oldMetaGame= -1
        if self.AllLevelOn == 0:
            self.AllLevelOn = 1
        else:
            self.AllLevelOn = 0
            
    def scaleCheat(self):
        global oldMetaGame
        oldMetaGame= -1
        if self.ScaleUpOn == 0:
            self.ScaleUpOn = 1
        else:
            self.ScaleUpOn = 0
            
    def AllPowerCheat(self):
        global oldMetaGame
        oldMetaGame= -1
        if self.AllPowerOn == 0:
            self.AllPowerOn = 1
        else:
            self.AllPowerOn = 0
            
    def mainLoopTick(self):
        global comboLevel
        if self.ScaleUpOn:
            comboLevel = 5
        
            
cheatCanvas = CheatScreen()

  

class gameOverScreen(canvas):
    enteringName = 0
    active = 0
    backdrop = None
    animation = animationSets.sad_jake
    frameYOffset = 0
    time = 0
  
    def render(self):
        self.overlay = None
        self.frame2X = -1
        self.frame1X = 270
        self.frameYFinish = 330
        self.titleTargetY = 20
        yOffset = (self.time*10) - 300
        if yOffset < self.frameYFinish:
            self.frame1Y = yOffset
        else:
            self.frame1Y =  self.frameYFinish + math.sin(self.time/7.5)*5
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        self.title = JPG_Resources["GameOver"]
        canvas.render(self) 
        
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        canvas.tick(self,delta)
        self.time += delta

    def makeActive(self):
        canvas.ressetTitle(self)
        self.active = 1
        self.time = 0
            
gameOverCanvas = gameOverScreen()    

class levelCompleteScreen(canvas):
    enteringName = 0
    active = 0
    backdrop = None
    animation = animationSets.splash_screen1
    frameYOffset = 0
    time = 0
  
    def render(self):
        self.overlay = None
        self.frame1X = -1
        self.frame2XFinish = 800
        self.frameYFinish = 280
        self.frame2Y = 330
        self.frame2X = 1000
        xOffset = 1000 - (self.time)
        if xOffset > self.frame2XFinish:
            self.frame2X = xOffset
            self.frame2Y = self.frameYFinish
        else:
            self.frame2X = self.frame2XFinish
            self.frame2Y =  self.frameYFinish + math.sin(self.time/7.5)*5
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        self.title = JPG_Resources["LevelComplete"]
        canvas.render(self) 
        
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        canvas.tick(self,delta)
        self.time += delta

    def makeActive(self):
        canvas.ressetTitle(self)
        self.active = 1
        self.time = 0
            
levelCompleteCanvas = levelCompleteScreen()   

class inGameMenuManagerClass :
    screens = [None,gameOverCanvas,levelCompleteCanvas]
    active = 0
    inactive,gameOverCanvas,levelCompleteCanvas = range(3)
    
    def tick(self,delta):
        if self.active:
            self.screens[self.active].tick(delta)

    def render(self):
        if self.active:
            self.screens[self.active].render()
            
    def makeActive(self,screen):
        self.active = screen
        if screen:
            self.screens[self.active].makeActive()
            
    def isActive(self):
        return self.active
            
inGameMenuManager = inGameMenuManagerClass()

class nameScreen(canvas):
    enteringName = 0
  
    def render(self):
#        self.overlay = JPG_Resources["MenuMask"]
        self.frame1X = -1
        self.frame2X = 770
        self.frame2Y = 300
        if(profiles[currentProfile].playerName != "Empty"):
            return
        PC.setColour( 210,40,20, 255 )
        PC.setFont( font36 )
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        self.title = JPG_Resources["Title"]
        canvas.render(self) 
        if(self.enteringName):
            PC.drawmodeNormal() 
            PC.setColour( 210,40,20, 255 )
            PC.setColourize(1)
            PC.setFont( font36 )
            PC.drawString(str(workingString.getDisplayString()), 300, 380 )
        #canvas.render(self) 
        
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        canvas.tick(self,delta)
        if(metaGame != oldMetaGame):
            playTuneOgg(levelData.menuSong,1)
            inGUI = 1
            fairyPointer.enabled = 0
            workingString.clearString()
            workingString.length = 9
            oldMetaGame = metaGame
            ScreenMessages.clearMessages()
            if(profiles[currentProfile].playerName == "Empty"):
              #  ScreenMessages.setMessageStatic(messages.Welcome,None,-1,250,None)
                ScreenMessages.setMessageStatic(messages.EnterName,None,-1,250,None)
                ScreenMessages.setMessageStatic(messages.PressEnter,None,-1,300,None)
                self.enteringName = 1
            else:
                self.enteringName = 0
                exitNameSelection(0)    
            mouseEnabled = 1
            canvas.ressetTitle(self)
        if checkKey(keyMap.enterKey.keyValue):
            profiles[currentProfile].playerName = workingString.thisString
            self.enteringName = 0
            exitNameSelection(1)
            fairyPointer.enabled = 1
            
nameCanvas = nameScreen()    

def changeProfile():
    global metaGame
    fadeManager.fadeDown(menuItems.profileCanvas)
    nextAvailableProfile=0

class profileScreen(canvas):
    enteringName = 0
    y = 0
    stringEnterY=0
    deletingName = 0   
  
    def render(self):
        self.frame1X = -1
        PC.setColour( 40, 220, 0, 255 )
        PC.setFont( font36 )
        name = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[name]
        canvas.render(self)
        if(self.enteringName):
            PC.setFont( font22)
            PC.setColour( 210,40,20, 255 )
            PC.drawString(str(workingString.getDisplayString()), 490, self.stringEnterY )
       
    def tick(self,delta):
        global startGame
        global canStart
        global metaGame
        global oldMetaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver
        global currentProfile
        canvas.tick(self,delta)
        if(metaGame != oldMetaGame):
            inGUI = 1
            workingString.clearString()
            workingString.length = 9
            oldMetaGame = metaGame
            ScreenMessages.clearMessages()
            ScreenMessages.setMessageStatic(messages.ProfileTile,None,-1,100,None)
            index = 0
            self.nextAvailableProfile = -1
            self.y = 160
            profileIdx = 0
            baseX = 190
            selectedName = None
           # print "showing profiles"
            activeProfiles = 0
            for profile in profiles:
                if(profile.playerName != "Empty"):
                    x = baseX
                    activeProfiles += 1
                    if(index==currentProfile):
                        ScreenMessages.setMessageStatic(messages.ProfileS,None,x,self.y,selectProfile,profile.playerName,index)
                        selectedName = profile.playerName +" ?"
                    else:
                        ScreenMessages.setMessageStatic(messages.ProfileNS,None,x,self.y,selectProfile,profile.playerName,index) 
                    x += 180
                    self.showStoryPercentage(x,self.y,index)    
                    x += 75
                    self.showStoryScore(x,self.y,index)
                    self.y +=50
                else:
                    self.nextAvailableProfile = index
                index += 1
            if self.nextAvailableProfile != -1:
                if(self.enteringName):
                    ScreenMessages.setMessageStatic(messages.enterNameProfile,None,baseX,self.y,None)
                    self.stringEnterY = self.y
                else:  
                    ScreenMessages.setMessageStatic(messages.createProfile,None,baseX,self.y,newProfile,parameter=index)
            if self.enteringName==0:
                if self.deletingName == 0:
                    if activeProfiles > 1:
                        ScreenMessages.setMessageStatic(messages.deleteProfile,None,baseX,490,self.checkDelete,parameter=index) 
                    ScreenMessages.setMessageStatic(messages.returnMenu,None,baseX,530,self.exitNameSelectionProfile) 
                else:
                    ScreenMessages.setMessageStatic(messages.confirmDeleteMessage,None,40,490,None,selectedName)
                    ScreenMessages.setMessageStatic(messages.confirmDelete,None,baseX,540,self.deleteProfile,parameter=index)
                    ScreenMessages.setMessageStatic(messages.cancelDelete,None,baseX,580,self.cancelDelete,parameter=index)                    
            mouseEnabled = 1
            canvas.ressetTitle(self)



        if self.enteringName:
            if checkKey(keyMap.enterKey.keyValue):
                if self.nextAvailableProfile != -1:
                    currentProfile = self.nextAvailableProfile
                    profiles[currentProfile].ressetProfile()
                    profiles[currentProfile].playerName = str(workingString.thisString)
                    self.enteringName = 0
                    oldMetaGame = 0 #force refresh
    def exitNameSelectionProfile(self):
        global metaGame
        if(self.enteringName==0):
            exitProfile()  

    def deleteProfile(self,index):
        global oldMetaGame
        global currentProfile
        occupied = 0
        index = 0
        #need to make sure there is at least two slots occupied so we can delete one
        for profile in profiles:
            if profile.playerName != "Empty":
                occupied += 1
        if(occupied >1):
            #resset the selected profile
            profiles[currentProfile].ressetProfile()
            #now find the first occupied profile so we can reset the current profile
            index = 0
            for profile in profiles:
                if profile.playerName != "Empty":
                    currentProfile = index
                    break
                index += 1
            oldMetaGame = 0 
            self.deletingName = 0
            
    def checkDelete(self,index):
        global oldMetaGame     
        oldMetaGame = 0   
        self.deletingName = 1
        
    def cancelDelete(self,index):
        global oldMetaGame     
        oldMetaGame = 0   
        self.deletingName = 0
    
    def showStoryScore(self,x,y,profileIdx):
        index = 1
        score = 0
        for point in levelData.storyCampaign[1:]:
            score += getLevelScore(index,profileIdx) 
            index += 1           
        ScreenMessages.setMessageStatic(messages.Blank22Green,None,x,y,None,str(score))   

    def showStoryPercentage(self,x,y,profileIdx):
        index = 1
        complete = 0
        for point in levelData.storyCampaign[1:]:
            complete += levelCompleted(index,profileIdx) 
            index += 1  
        percentage = int(complete/63.0*100.0)
        ScreenMessages.setMessageStatic(messages.Blank22Green,None,x,y,None,str(percentage)+"%") 

profileCanvas = profileScreen()

def newProfile(index):
    global oldMetaGame
    profileCanvas.enteringName = 1
    oldMetaGame = 0 #force refres
    
 
def selectProfile(index):
    global currentProfile
    global oldMetaGame
    #("index",index)
    currentProfile = index
    oldMetaGame = 0

def exitNameSelection(first):
    global metaGame
    writeProfiles()
    PC.writeReg("CurrentProfile",str(currentProfile))
    if first:
        fadeManager.fadeDown(menuItems.welcomeCanvas)
    else:
        fadeManager.fadeDown(menuItems.mainScreenCanvas)
        
def exitProfile():
    global metaGame
    writeProfiles()
    PC.writeReg("CurrentProfile",str(currentProfile))
    fadeManager.fadeDown(menuItems.mainScreenCanvas)

def doCredits():
    fadeManager.fadeDown(menuItems.creditCanvas)
    
def doInstructionScreen():
    fadeManager.fadeDown(menuItems.instructionListCanvas)
    
def exitGameOption():
      global doExit
      fadeManager.fadeDown(menuItems.sellUpExitCanvas)
#      else:
#      doExit = 1
    
def selectHighScore():
    global metaGame
    #print ("high score selected")
    highScoreCanvas.cameFromLevel = 0
    fadeManager.fadeDown(menuItems.highScoreCanvas)
def selectCheats():
    global metaGame
    fadeManager.fadeDown(menuItems.cheatCanvas)  
    
def selectOptions():
    global metaGame
    fadeManager.fadeDown(menuItems.optionsCanvas)

def selectSellUp():
    fadeManager.fadeDown(menuItems.sellUpCanvas)

def selectStory():
    global metaGame
    if profiles[currentProfile].storyBegun==0: 
        storyCanvas.cutScene = 1 #if this is the first time in the story then open the start C
        profiles[currentProfile].storyBegun = 1 #tony - put this back in
    if testCutScene >= 0:
        storyCanvas.cutScene = testCutScene
    fadeManager.fadeDown(menuItems.storyCanvas)

def selectArcade():
    global startGame
    global metaGame
    global score
    global lives
    global newGame
    global mouseEnabled
    global inGUI
    global firstTimeMainScreen
    global gameOver 
    global arcadeMode   
    global levelNumber
    lastArcadeSection = getArcadeSectionCompleted()  
  #  print "lastArcadeSection",lastArcadeSection
    ressetScore(0)
    ressetLives()
    if lastArcadeSection ==0:
        levelNumber = 1
        fadeManager.fadeDown(menuItems.arcadeLevel)
    else:
        fadeManager.fadeDown(menuItems.arcadeChoiceCanvas)

leveleStarts = [config.levelStart1,config.levelStart2,config.levelStart3,config.levelStart4]

def getArcadeSectionCompleted():
    arcadeProgress = profiles[currentProfile].arcadeProgress+1
    if arcadeProgress < leveleStarts[1]:
        return 0
    elif arcadeProgress < leveleStarts[2]:
        return 1
    elif arcadeProgress < leveleStarts[3]:
        return 2
    else:
        return 3
    return 0

def startArcadeGame(startingSection):
    global startGame
    global metaGame
    global score
    global lives
    global newGame
    global mouseEnabled
    global inGUI
    global firstTimeMainScreen
    global gameOver 
    global arcadeMode   
    global levelNumber
    startGame = 0
    fadeManager.fadeDown(menuItems.game)
    mouseEnabled = 1
    inGUI = 0  
   # ScreenMessages.clearMessages()
    arcadeMode = 1
    levelNumber = leveleStarts[startingSection]
    initialiseLevel()
    trailGame.emptytrail()
    EmptyGrid()
#    ressetScore(0)
#    ressetLives()
    newGame = 0
    gameOver = 0  
    metaGame = 0
    fadeManager.fadeUp()
 #   print("arcade selected",arcadeMode)

def getKeyName(key):
    keyName = chr(key.keyValue)
    for namedKey in keyMap.namedKeys:
        if namedKey[0] == key.keyValue:
            keyName = namedKey[1]  
    return keyName

renderOptions = [messages.Low[0],messages.Med[0],messages.High[0]]

class optionsScreen(canvas):
    selectedOption = -1
    oldDownKey=0
    selectionReady = -1
    oldDownKey = -1

    def render(self):
        character = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[ character]
        self.title = JPG_Resources[ 'Options']

        canvas.render(self)
        
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global inGUI
        canvas.tick(self,delta)
        maxOption = len(keyMap.configurableKeys)
        if(oldMetaGame!= metaGame):
            canvas.ressetTitle(self)
            inGUI = 1
            mouseEnabled = 1
            ScreenMessages.clearMessages()
            self.frame1X = -1
            self.frame2X = 770
            self.frame2Y = 280
            x = 270
            y = 220
            sound = getWordFromNumber(int(profiles[currentProfile].soundVolume)) 
            music = getWordFromNumber(int(profiles[currentProfile].musicVolume))
            ScreenMessages.setMessageStatic(messages.SoundVolume,None,x,y,changeSoundVolume,sound)
            y += 45           
            ScreenMessages.setMessageStatic(messages.MusicVolume,None,x,y,changeMusicVolume,music)
            y += 45 
            global fullScreenMode
            if(PC.getFullscreen()):
                fullScreenMode = 1
                string  = "Full" 
            else:
                fullScreenMode = 0
                string = "Window"
            ScreenMessages.setMessageStatic(messages.WindowMode,None,x,y,ToggleWindowed,string)
            y += 45
            if profiles[currentProfile].tutorials:
                string = messages.TutorialEnabled[0]
            else:
                string = messages.TutorialDisabled[0]   
            ScreenMessages.setMessageStatic(messages.Tutorials,None,x,y,ToggleTutorials,string)   
            y += 45
            if PC.getIs3DAccelerated():
                string = messages.Enabled[0]
            else:
                string = messages.Disabled[0]
            ScreenMessages.setMessageStatic(messages.Acceleration,None,x,y,ToggleAcceleration,string)  
            y += 45
            string = renderOptions[renderDetailLevel]
            ScreenMessages.setMessageStatic(messages.DetailLevel,None,x,y,ToggleDetailLevel,string)
            y += 45            
            selectedLanguage = availableLanguageNames[profiles[currentProfile].currentLanguage]
            
            ScreenMessages.setMessageStatic(messages.changeLanguage,None,x,y,self.doChangeLanguage,selectedLanguage) 
            y += 45            
            ScreenMessages.setMessageStatic(messages.ShowCredit,None,x,y,doCredits) 
            y += 45
            ScreenMessages.setMessageStatic(messages.returnMenu,None,x,y,backtoMainScreen)            
            oldMetaGame = metaGame
            checkKey(keyMap.escapeKey.keyValue) #make sure the no repeat flag is set
        if(checkKeyNoRepeat(keyMap.escapeKey.keyValue)):
            backtoMainScreen()
        if(self.selectedOption >= 0): 
            if(downKey != self.oldDownKey):
                keyMap.configurableKeys[self.selectedOption].keyValue = downKey
                self.selectedOption = -1
        self.oldDownKey=downKey

    def doChangeLanguage(self):
        global oldMetaGame
        oldMetaGame = -1
        profiles[currentProfile].currentLanguage += 1
        if profiles[currentProfile].currentLanguage >= len(availableLanguageNames):
            profiles[currentProfile].currentLanguage = 0 
        global messages    
        global levelData
        global cutScenes
        if profiles[currentProfile].currentLanguage == English:
            import messages as messages
            import levelData as levelData
            import cutScenes as cutScenes 
           # print"HangInstructions",messages.HangInstructions  
        else:    
            import messagesES as messages 
            import levelDataES as levelData 
            import cutScenesES as cutScenes                

    def chooseSelection(self):
        self.selectedOption = ((mousey-210)/40)+1

arcadeIcons = [["arcadeJungleIcon",150,120,0],["arcadeCaveIcon",462,120,1],["arcadeParkIcon",150,340,2],["arcadeCellarIcon",462,340,3]]

arcadeIconsDim = ["arcadeJungleIcon","arcadeCaveIconDim","arcadeParkIconDim","arcadeCellarIconDim"]

def ToggleAcceleration():
    global oldMetaGame
    oldMetaGame = -1
    if PC.getIs3DAccelerated():
        PC.set3DAccelerated(0)
    else:
        PC.set3DAccelerated(1)
        
        
def ToggleDetailLevel():
    global oldMetaGame
    oldMetaGame = -1
    global renderDetailLevel
    renderDetailLevel += 1
    if renderDetailLevel > 2:
        renderDetailLevel = 0

def ToggleTutorials():
    global oldMetaGame
    oldMetaGame = -1
    if profiles[currentProfile].tutorials: 
        profiles[currentProfile].tutorials = 0
    else:
        profiles[currentProfile].tutorials = 1

class arcadeChoiceScreen(canvas):
        
    def render(self):
        character = self.animation[self.frameNumber][0]
        self.frame = None
        #self.title = JPG_Resources[ 'Options']

        canvas.render(self)
        PC.setFont( font22 )  
        for icon in arcadeIcons:
            index = icon[3]
            #if index > getArcadeSectionCompleted():   
            graphicName = icon[0]
            x = icon[1]
            y = icon[2]
            height = PCR.imageHeight(JPG_Resources[graphicName])
            width = PCR.imageWidth(JPG_Resources[graphicName])
            PC.setColour( 0, 00, 00, 60)
            PC.fillRect( x, y, width, height )    
            x -= 5
            y -= 5
            height +=10
            width += 10
            PC.fillRect( x, y, width, height )  
            x -= 5
            y -= 5
            height +=10
            width += 10
            PC.fillRect( x, y, width, height )  
            x -= 5
            y -= 5
            height +=10
            width += 10
            PC.fillRect( x, y, width, height )  
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global inGUI
        canvas.tick(self,delta)
        if(oldMetaGame!= metaGame):
            ScreenMessages.clearMessages()
            lastArcadeSection = getArcadeSectionCompleted() 
            for icon in arcadeIcons:
                index = icon[3]
                if index <=lastArcadeSection:
                    graphicName = icon[0]
                    function = self.mouseDownFunction
                else:
                    graphicName = None
                    function = None
                x = icon[1]
                y = icon[2]
                if graphicName:
                    ScreenMessages.setMessageStatic(messages.Blank22, graphicName,x,y,function,parameter=index,mouseOverFunction = self.mouseOverFunction) 
            canvas.ressetTitle(self)
            inGUI = 1
            mouseEnabled = 1
            ScreenMessages.setMessageStatic(messages.arcadeMessage1,None,-1,80,None )
            ScreenMessages.setMessageStatic(messages.returnMenu,None,-1,580,backtoMainScreen) 
            x = 265
            y = 210
                 
            oldMetaGame = metaGame
            
    def mouseOverFunction(self,index):
        return 0
        
    def mouseDownFunction(self,index):
        global levelNumber
        levelNumber = index * levelsPerArcadeSegment
        fadeManager.fadeDown(menuItems.arcadeLevel)

arcadeChoiceCanvas = arcadeChoiceScreen()

#screenShots = [["sample1",20,20,0],["sample2",420,20,1],["sample3",20,320,2],["sample4",420,320,3]]

class creditScreen(canvas):
    exitFlag = 0    
    def render(self):
        character = self.animation[self.frameNumber][0]
        self.frame = None

        canvas.render(self)
        PC.setFont( font22 )  
        
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global inGUI
        canvas.tick(self,delta)
        if(oldMetaGame!= metaGame):
            ScreenMessages.clearMessages()
            canvas.ressetTitle(self)
            inGUI = 1
            mouseEnabled = 1
            y_delta = 40
            y = 100
            ScreenMessages.setMessageStatic(messages.credit1,None,-1,y,None )
            y += 70
            ScreenMessages.setMessageStatic(messages.credit2,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.credit3,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.credit4,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.credit10,None,-1,y,None )
#            ScreenMessages.setMessageStatic(messages.TweelerWeb2,None,-1,y,tweelerWebsite )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.credit5,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.credit6,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.credit11,None,-1,y,None )
            y += y_delta+20
            ScreenMessages.setMessageStatic(messages.credit8,None,-1,y,None )
            y += 30
            ScreenMessages.setMessageStatic(messages.credit9,None,-1,y,None )
            
            if self.exitFlag:
                ScreenMessages.setMessageStatic(messages.Quit,None,-1,570,self.exit) 
            else:
                ScreenMessages.setMessageStatic(messages.WelcomeMainMenu,None,-1,590,self.exit) 
            x = 265
            y = 210
                 
            oldMetaGame = metaGame
            
    def buyGame(self):
        backtoMainScreen()
        
    def exit(self):
        backtoMainScreen()

creditCanvas = creditScreen()


class instructionListCanvas(canvas):
    exitFlag = 0    
    InstructionIndex = 0
    def render(self):
        character = self.animation[self.frameNumber][0]
        self.frame = None

        canvas.render(self)
        PC.setFont( font22 )  
        
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global inGUI
        canvas.tick(self,delta)
        if(oldMetaGame!= metaGame):
            ScreenMessages.clearMessages()
            canvas.ressetTitle(self)
            inGUI = 1
            mouseEnabled = 1
            y_delta = 40
            y = 100
            ScreenMessages.setMessageStatic(messages.Instructions,None,-1,y,None )
            y += y_delta+20
            index = 0
            for instruction in messages.completeInstructions:  
                
                ScreenMessages.setMessageStatic(instruction[0],None,300,y,doInstruction,parameter=index,string ="...")
                y += y_delta
                index+= 1
            
            ScreenMessages.setMessageStatic(messages.backToOptions,None,-1,590,self.exit) 
            x = 265
            y = 210
                 
            oldMetaGame = metaGame
        
    def exit(self):
        fadeManager.fadeDown(menuItems.optionsCanvas)

instructionListCanvas = instructionListCanvas()

def doInstruction(index):
    instructionListCanvas.InstructionIndex = index
    fadeManager.fadeDown(menuItems.instructionCanvas)
    return

class instructionCanvas(canvas):
    exitFlag = 0    
    def render(self):
        character = self.animation[self.frameNumber][0]
        self.frame = None

        canvas.render(self)
        PC.setFont( font22 )  
        
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global inGUI
        canvas.tick(self,delta)
        if(oldMetaGame!= metaGame):
            ScreenMessages.clearMessages()
            canvas.ressetTitle(self)
            inGUI = 1
            mouseEnabled = 1
            y_delta = 50
            y = 150
            index = 0
            for instruction in messages.completeInstructions[ instructionListCanvas.InstructionIndex]:
                if index ==0:
                    ScreenMessages.setMessageStatic(messages.Blank36,None,-1,y,None,string = instruction[0])
                else:
                    ScreenMessages.setMessageStatic(instruction,None,-1,y,None)
                y += y_delta
                index += 1

            ScreenMessages.setMessageStatic(messages.MoreInstructions,None,-1,590,self.exit) 
            x = 265
            y = 210
                 
            oldMetaGame = metaGame
        
    def exit(self):
        fadeManager.fadeDown(menuItems.instructionListCanvas)

instructionCanvas = instructionCanvas()


class sellUpScreenExit(creditScreen):
    exitFlag = 1
    def exit(self):
        exitGameOption()



numberString = ["Off","Low","Med","High","Max"]

def getWordFromNumber(number):
    return numberString[number]
      

def changeSoundVolume():
    global oldMetaGame
    oldMetaGame = -1
    profiles[currentProfile].soundVolume += 1.0
    if(profiles[currentProfile].soundVolume>4):
        profiles[currentProfile].soundVolume = 0.0
    playSimpleSound( 'Ding')
    
def changeInputDevice():
    global oldMetaGame
    oldMetaGame = 0
    if(profiles[currentProfile].mouseControl):
        profiles[currentProfile].mouseControl = 0
    else:
        profiles[currentProfile].mouseControl = 1
    
def changeMusicVolume():
    global oldMetaGame
    oldMetaGame = -1
    profiles[currentProfile].musicVolume += 1
#    internalVolume = -1
    if(profiles[currentProfile].musicVolume>4):
        profiles[currentProfile].musicVolume =0
    setMusicVolume()

def setMusicVolume():
    internalVolume = -1.0
    musicVolume = profiles[currentProfile].musicVolume
    if musicVolume == 0:
        internalVolume = 0.0
    elif musicVolume == 1:
        internalVolume = 0.25 
    elif musicVolume == 2:
        internalVolume = 0.5       
    elif musicVolume == 3:
        internalVolume = 0.75     
    elif musicVolume == 4:
        internalVolume = 1.0   
    if internalVolume != -1.0:
        PC.setVolume( internalVolume )      

def ToggleWindowed():
    global fullScreenMode
    if(fullScreenMode):
        fullScreenMode = 0
        PC.setFullscreen(0)
    else:
        fullScreenMode = 1
        PC.setFullscreen(1)


def backtoMainScreen():
    global metaGame
    highScoreCanvas.cameFromLevel = 0
    fadeManager.fadeDown(menuItems.mainScreenCanvas)
        
optionsCanvas = optionsScreen()

campaignXOffset = 50
campaignYOffset = 200

def allAmuletGot():
    if profiles[currentProfile].hangEnabled:
        if profiles[currentProfile].smashEnabled: 
            if profiles[currentProfile].stunJumpEnabled: 
                if profiles[currentProfile].dashEnabled:  
                    if profiles[currentProfile].speedEnabled:
                        if profiles[currentProfile].fairyEnabled:
                            return 1
    return 0
    
    
    
def setUpLevelItemData():
    levelItems = []
    for thisLevel in levelData.storyCampaign[1:]:
        itemFound = None 
        mapName = thisLevel[1]
        if mapName in map_Resources:
            mapData = map_Resources[mapName]
        for item in mapData:
            itemID = int(item[1])
            if itemID == WorldTypes.Level1Key and profiles[currentProfile].keysCollected < 1: 
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.Level2Key and profiles[currentProfile].keysCollected < 2:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.Level3Key and profiles[currentProfile].keysCollected < 3:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.Level4Key and profiles[currentProfile].keysCollected < 4: 
                itemFound = AllWorldObjects[itemID].graphic
                
            if itemID == WorldTypes.PowerUpHang and profiles[currentProfile].hangEnabled==0:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.PowerUpSmash and profiles[currentProfile].smashEnabled==0:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.PowerUpstunJump and profiles[currentProfile].stunJumpEnabled==0:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.PowerUpDash and profiles[currentProfile].dashEnabled==0:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.PowerUpSpeed and profiles[currentProfile].speedEnabled==0:
                itemFound = AllWorldObjects[itemID].graphic
            if itemID == WorldTypes.PowerUpFairy and profiles[currentProfile].fairyEnabled==0:
                itemFound = AllWorldObjects[itemID].graphic
        levelItems.append(itemFound)
    return levelItems
    
def getLevelItem(index,levelItems):
#    if testLevelAttempted(index):
    if levelreachable(index):
        return levelItems[index-1]
    else:
        return None

class storyScreen(canvas):
    selectedOption = -1
    oldDownKey=0
    selectionReady = -1
    oldDownKey = -1
    LaunchLevelFlag = 0
    ressetScore(0)
    cutScene = 0
    endDemo = 0

    def tintPannel(self,thisPannel,x,width):
        tinted = 1
        index = 0
        for point in levelData.storyCampaign:
            section = point[0]
            pannel = section[7]
            if levelCompleted(index) and pannel == thisPannel: 
                tinted = 0
            index += 1
        if(tinted):
            PC.setColour( 30, 10, 10, 200)
            PC.fillRect( x, campaignYOffset+8, width, PCR.imageHeight(JPG_Resources['campaignMapScaled'])-17 )    


    def render(self):
        self.frame = None
       # canvas.render(self)

        PC.setFont( font22 )          
        graphic = JPG_Resources['campaignMapScaled']    #main bac
        self.title = JPG_Resources["OlliesTale"]
        character = self.animation[self.frameNumber][0]
        self.frame = JPG_Resources[ character]
        self.frame2X = -1
        self.frame1X = 0
        self.frame1Y = 0
        self.frameScale = 0.75
        canvas.render(self)
        PC.drawImage( graphic,campaignXOffset,campaignYOffset)
        medalion.render(655,20,0)
        self.tintPannel(2,229,165)
        self.tintPannel(3,403,171)
        self.tintPannel(4,583,156)         

    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global startGame
        global metaGame
        global score
        global lives
        global newGame
        global mouseEnabled
        global inGUI
        global firstTimeMainScreen
        global gameOver  
        global arcadeMode 
        if self.cutScene != 0:
            metaGame = 6
            cutScene.cutSceneNumber = self.cutScene
            self.cutScene = 0
            return
        canvas.tick(self,delta)
        maxOption = len(keyMap.configurableKeys)
        if(oldMetaGame!= metaGame):
            if currentTunePlaying != levelData.storyScreenSong:
                playTuneOgg(levelData.storyScreenSong,1)
            global cameraX
            cameraX = 0
            levelItemData = setUpLevelItemData()
            arcadeMode = 0 
            canvas.ressetTitle(self)
            mouseEnabled = 1
            inGUI = 1
            ScreenMessages.clearMessages()
            ScreenMessages.setMessageStatic(messages.returnMenu,None,-1,590,backtoMainScreen)         
            index = 1
            self.score = 0
            writeProfiles()           
            
            for point in levelData.storyCampaign[1:]:
                tickXOffset = 12
                self.score += getLevelScore(index)
                y_size = 10
                function = playLevel
                #function = testCampaign #Comment this back in to test campaign
                section = point[0]
                graphicName = section[3]
                tickType = getTickType(index)
                if levelreachable(index) or index==startingLevelCampaign:
                    graphicName += ""
                else:
                    if graphicName[-5:]!="Arrow":
                        graphicName = "Campaign1UA"   
                    else:
                        graphicName = None
                    function = None
                coord = point[4] 
                if index == startingLevelCampaign:
                    tickXOffset = 25
                    graphicName = "StoryStart"  
                if index == finishLevelCampaign:
                    if levelreachable(index):
                        graphicName = "StoryFinish" 
                    else:
                        graphicName = "StoryFinishUA" 
                lock = leveLocked(index)
                if lock and levelreachable(index):
                    graphicName = lock
                    function = levelLocked
                x= campaignXOffset + 15 + levelData.campaignTrial[coord][0]*7/8
                y= campaignYOffset + 18 + levelData.campaignTrial[coord][1]*7/8
                if checkOpenLock(index):
                    size = 1.0
                    deltaX = 0
                    deltaY = -3
                    playSimpleSound ('unLock')
                    particleController.addItem(lockParticle(),x+20,y,size,deltaX,deltaY)
                self.levelY = y + 30
                if x<700:
                    self.levelX = x-20
                else:
                    self.levelX = 700
                thisFlashEnabled = 0
                if (levelreachable(index) or index == 1) and levelCompleted(index)==0:
                      thisFlashEnabled = 1
                ScreenMessages.setMessageStatic(messages.Blank22, graphicName,x,y,function,parameter=index,mouseOverFunction = self.mouseOverFunction,flashEnabled = thisFlashEnabled) 
                if levelCompleted(index):
                    ScreenMessages.setMessageStatic(messages.Blank22, tickType,x+tickXOffset,y+15,None)               
                itemGraphic = getLevelItem(index,levelItemData) 
                if itemGraphic:
                    function = self.dummy
                else:
                    function = None
                ScreenMessages.setMessageStatic(messages.Blank22, itemGraphic,x+2,y+5,function,scale = 0.5)                 
                index += 1 
            profiles[currentProfile].oldKeysCollected = profiles[currentProfile].keysCollected
            scoreString = numberToString(self.score)
            ScreenMessages.setMessageStatic(messages.TaleScore,None,-1,160,None,string=scoreString
) 
            if testLevelAttempted(1):
                startInstructionString = messages.ClickOnLevel
            else:    
                startInstructionString = messages.ClickOnStart
            ScreenMessages.setMessageStatic(startInstructionString,None,-1,190,None,None)
        oldMetaGame= metaGame 
        if(self.LaunchLevelFlag==1):
            buyUp = setupLevel()         
            self.LaunchLevelFlag=0
            if buyUp == 0:
                launchLevel(levelNumber)
#                global oldMetaGame
            #oldMetaGame = 0
    def dummy(self):
        return 0 
            
    def mouseOverFunction(self,index):
        point = levelData.storyCampaign[index]
        section = point[0]
        string1 = point[5]
        if leveLocked(index):
            string1 = messages.stringLocked
            string2 = messages.stringFindKey
#            playSimpleSound ('locked')
        elif testLevelAttempted(index):
            if testLevelAttempted(index)==1:
                string2 = messages.stringNotCompleted
            else:
                scoreString = numberToString(getLevelScore(index))
                string2 = messages.stringScore+ scoreString
        else:
            string2 = messages.stringNotAttempted
            if index ==1:
                string1 = None 
        if string1 != None:
            coord = point[4] 
            alpha = 255
            font = font22
            PCR.setFontScale(font,.75)
            PC.setColour( 40,230,40,int(alpha))
            PC.setFont( font )
            if string1 == "":
                string1 = point[1]
            coord = point[4]    
            x= (campaignXOffset + 15 + levelData.campaignTrial[coord][0]*7/8) + 15
            y= (campaignYOffset + 18 + levelData.campaignTrial[coord][1]*7/8) + 68
            length = PCR.stringWidth(string1,font)
            x1 = x - (length * 0.5)
            if x1 < 0:
                x1 = 0
            if x1 + length > 800:
                x1 = 800 - length
            PC.drawString( string1, x1, y) 
            length = PCR.stringWidth(string2,font)
            x1 = x - (length * 0.5)
            if x1 < 0:
                x1 = 0
            if x1 + length > 800:
                x1 = 800 - length
            PC.drawString( string2, x1, y+22) 
            PCR.setFontScale(font,1)
def levelLocked(index):
    playSimpleSound ('locked')
    return 0
            
def setupLevel():
    global arcadeMode
    global startGame
    global mouseEnabled
    global inGUI
    global score
    global lives
    global newGame 
    global gameOver
    global metaGame
    thisLevel = levelData.storyCampaign[levelNumber]
    mapName = thisLevel[1]
    
    if mapName in map_Resources:
#        print "level",levelNumber,mapName
        #arcadeMode = 0 
        startGame = 0
    #    metaGame = 0
        fadeManager.fadeDown(0)
    #    print ("setting up level")
        mouseEnabled = 1
        inGUI = 0  
        #ScreenMessages.clearMessages()
        ressetScore(0)
        ressetLives()
        newGame = 0
        gameOver = 0 
        return 0
    else:
        fadeManager.fadeDown(menuItems.sellUpCanvas)
        return 1
  
  
            
storyCanvas = storyScreen()

def levelCompleted(index,profile = -1):
    if profile == -1:
        profile = currentProfile
    if(profiles[profile].campaignMaps[index].done==2):
        return 1
    else:
        return 0
        
def testLevelAttempted(index):
        return profiles[currentProfile].campaignMaps[index].done
       
        
def getLevelScore(index,profile=-1):
    if profile == -1:
        profile = currentProfile
    return profiles[profile].campaignMaps[index].score


def checkIfTutorialsEnabled():
    index = 62 # after the second half turn off tutorials
    if profiles[currentProfile].tutorials:
        return 1
    else:
        return 0

def getTickType(index):
    if levelreachable(index)==0 and index != 1:
        return ""
    if levelCompleted(index)==0:
        return ""
    if profiles[currentProfile].campaignMaps[index].coins:
        return "Gold"
    return "Green"
    
def testAllCoinsInGame():
    index = 2
    for point in levelData.storyCampaign[2:]:
        if profiles[currentProfile].campaignMaps[index].coins == 0:
            return 0
        index += 1  
    return 1
    
def allLevelComplete():  
    index = 1
    for point in levelData.storyCampaign[1:]:
        profiles[currentProfile].campaignMaps[index].coins = 1
        profiles[currentProfile].campaignMaps[index].done = 2
        index += 1  

def leveLocked(index):
    thisLevel = levelData.storyCampaign[index]
    lockLevel = thisLevel[8]
    if lockLevel>profiles[currentProfile].keysCollected:
        return "Padlock"
    return None
    
def checkOpenLock(index):
    if profiles[currentProfile].keysCollected != profiles[currentProfile].oldKeysCollected:
        #The lock level has changed!
        thisLevel = levelData.storyCampaign[index]
        lockLevel = thisLevel[8]
        if lockLevel != 0 and lockLevel == profiles[currentProfile].keysCollected:
            return 1
    return 0

def levelreachable(index):
    reachable = 0
    if cheatCanvas.AllLevelOn:
        reachable = 1
    for link in levelData.campaignLinks[index]:
        if levelCompleted(link):
            reachable = 1
    return reachable

def playLevel(newLevelNumber):
    global levelNumber
    storyCanvas.LaunchLevelFlag=1
    levelNumber = newLevelNumber
    return 0
    
def testCampaign(newLevelNumber):
    global oldMetaGame
    profiles[currentProfile].campaignMaps[newLevelNumber].done = 2
    oldMetaGame = 0
    
def setLevelAttempted(levelnumber):
    if arcadeMode:
        return
    if profiles[currentProfile].campaignMaps[levelNumber].done==0:
        profiles[currentProfile].campaignMaps[levelNumber].done = 1
    
class particle:
    x=0
    y=0
    rotation = 0
    y_speed = 0 
    x_speed = 0
    angularVelocity =  0
    scale=1      #scale value for size
    r=255           #scale values for colour
    g=255
    b=255
    a=255
    width=1
    height=1
    frameNumber=-1      #start at minus one because first time through we'll increment this
    animation=None
    life=0
    name = ''
    frame = 0
    alphaDelta = 0
    scaleDelta = 0
    delete = 0
    frame = -1
    gravity = 0
    maximumYSpeed = 1000
    graphic=''
    overRideFrame = None # if this is set to true then we use this instead of the grahic in the particle data
    additive = 1
    
    def render(self):
        if(self.animation!=None):
            screenWidth = self.width*self.scale
            screenHeight = self.height*self.scale
            screenX = self.x-cameraX-(screenWidth/2)
            screenY = self.y-cameraY-(screenHeight/2)

            PC.setColour(int(self.r),int(self.g),int(self.b),int(self.a))
            if(self.frame >=0):
                frame = self.frame
                if self.additive:
                    PC.drawmodeAdd()
                if(self.animation[self.frameNumber][6]):
                    #rotating so can't scale
                    if(self.overRideFrame):
                        PC.drawmodeNormal() 
                        PC.drawImageRot(frame, screenX, screenY, self.rotation) 
                    else:
                        PC.drawImageRot(frame, screenX, screenY, self.rotation) 
                else:
                    if(self.overRideFrame):
                        PC.drawmodeNormal() 
                    else:
                        if self.additive:
                            PC.drawmodeAdd()
                    PC.drawImageScaled(frame, screenX, screenY,screenWidth,screenHeight)
                PC.drawmodeNormal()  
            
    def tick(self,delta):
        self.life-= delta
        self.y_speed += self.gravity
        if self.y_speed >self.maximumYSpeed:
            self.y_speed = self.maximumYSpeed
        self.y += self.y_speed*delta 
        self.x += self.x_speed*delta
        particle.stepAnimation(self,delta)
        #if(self.animation):
         #   self.angularVelocity = self.animation[self.frameNumber][6] 
        if(self.angularVelocity>0):
            self.rotation += self.angularVelocity*delta
        elif(self.angularVelocity<0):
            self.rotation += self.angularVelocity*delta   
            if(self.rotation<0):
                self.rotation += 2.0 * 22.0/7.0
        
    def stepAnimation(self,delta):
      
        if(self.life<=0):
            if(self.frameNumber==-1):
                self.frameNumber =0
            else:
                self.frameNumber = self.animation[self.frameNumber][1]
            self.graphic = self.animation[self.frameNumber][0]
            if(self.graphic=='end'):
            #We've reached the last frame
                self.animation = None
                self.delete = 1
            else:
                if self.overRideFrame:
                    self.frame = JPG_Resources[ self.overRideFrame]
                else:
                    self.frame = JPG_Resources[self.graphic]
                self.width= PCR.imageWidth( self.frame )
                self.height= PCR.imageHeight( self.frame )
                self.life = self.animation[self.frameNumber][2]  
                SFX = self.animation[self.frameNumber][3]
                if SFX != None:
                        playSimpleSound(SFX)  
                self.scaleDelta = self.animation[self.frameNumber][4]/1.333
                self.alphaDelta = self.animation[self.frameNumber][5]/1.333 

        else:
            self.life -= delta
            self.scale+=self.scaleDelta*delta
            self.a +=self.alphaDelta*delta
            if self.a > 255:
                self.a = 255
            if(self.a<0 or self.y > 800):
                self.a=0
                self.delete = 1 #delete particle if it's alpha is zero or it's off the screen


            
class tileExplosion(particle):
    name="tileExplosion"
    animation = particleEffects.tile_explosion
    
class spellParticle(particle):
    name="spellParticle"    
    animation = particleEffects.spell
    
class fairyTrailParticle(particle):
    name="fairyTrailParticle"    
    animation = particleEffects.fairyTrail
    
class fairySparleParticle1(particle):
    name="fairySparkleParticle1"    
    animation = particleEffects.fairySparkle1 
    gravity = 0.05
    maximumYSpeed = 7.0
    
class acidParticle(particle):
    name="acid"    
    animation = particleEffects.acid 
    gravity = 0.1
    maximumYSpeed = 9.0
    additive = 0
    
class fairySparleParticle2(particle):
    name="fairySparkleParticle2"    
    animation = particleEffects.fairySparkle2 
    gravity = 0.07
    maximumYSpeed = 8.0  

class ghostParticle(particle):
    name="ghostParticle"    
    animation = particleEffects.ghostParticle
    gravity = 0.00
    maximumYSpeed = 7.0
    #additive = 0
 
class fairyAttackParticle1(particle):
    name="fairyAttack1"   
    animation = particleEffects.fairyAttack1 
    gravity = 0.2
    maximumYSpeed = 14.0
    
class fairyAttackParticle2(particle):
    name="fairyAttack2"    
    animation = particleEffects.fairyAttack2
    gravity = 0.12
    maximumYSpeed = 14.0   
     
class fireParticle1(particle):
    name="fire1"    
    animation = particleEffects.fire1 
    gravity = 0.05
    maximumYSpeed = 7.0
    
class fireParticle2(particle):
    name="fire2"    
    animation = particleEffects.fire2 
    gravity = 0.07
    maximumYSpeed = 8.0    
    
class fireWorkParticle1(particle):
    name="fireWork1"    
    animation = particleEffects.fireWork1 
    gravity = 0.05
    maximumYSpeed = 8.0    
    
class fireWorkParticle2(particle):
    name="fireWork1"    
    animation = particleEffects.fireWork2 
    gravity = 0.05
    maximumYSpeed = 8.0  
    
class fireWorkParticle3(particle):
    name="fireWork1"    
    animation = particleEffects.fireWork3 
    gravity = 0.05
    maximumYSpeed = 8.0     
    
class fairyRedTrailParticle(particle):
    name="fairyRedTrailParticle"    
    animation = particleEffects.fairyRedTrail  

class dustParticle(particle):
    name="DustParticle"    
    animation = particleEffects.dustPuff
    gravity = 0.05
    maximumYSpeed = 7.0
    
class hitEffectParticle(particle):
    name="hitEffectParticle"    
    animation = particleEffects.hitEffect
    gravity = 0.05
    maximumYSpeed = 7.0   
    
class spellExplosion(particle):
    name="spellExplosion"    
    animation = particleEffects.spell_explosion
    
class clockExplosion(particle):
    name="clockExplosion"
    animation = particleEffects.clock_explosion

class bigExplosion(particle):
    name="bigExplosion"
    animation = particleEffects.big_explosion

class vBigExplosion(particle):
    name="vBigExplosion"
    animation = particleEffects.big_explosion
    
particleGravity = .1

class gravityParticle(particle):
    def tick(self,delta):
        self.y_speed += particleGravity*delta
        particle.tick(self,delta)
    
class debris(gravityParticle):
    name = "debris"
    animation = particleEffects.debris
    def __init__(self,graphic=None,rotation=0):
        if(graphic):
            self.overRideFrame = graphic
        if(rotation):
            self.angularVelocity = rotation

class fruitParticle(particle):
    name = "fruit"
    animation = particleEffects.fruit
    gravity = 0.4
    maximumYSpeed = 10
    def __init__(self,graphic=None,rotation=0):
        if(graphic):
            self.overRideFrame = graphic
         #   print"over ride set on fruit",graphic
        if(rotation):
            self.angularVelocity = rotation

class lockParticle(particle):
    name = "lock"
    animation = particleEffects.lock
    gravity = 0.2
    maximumYSpeed = 4
    additive = 0
            
class particleControllerClass:
    effectsList = []
   
    def addItem(self,effect,x,y,scale,xSpeed = 0,ySpeed = 0):
        effect.x = x
        effect.y = y
        effect.x_speed = xSpeed
        effect.y_speed = ySpeed
        effect.scale=scale
        self.effectsList.append(effect)
        
    def render(self):
        PC.setColourize(1)
        for item in self.effectsList:
            item.render()
            
    def tick(self,delta):
        for item in self.effectsList[:]:
            item.tick(delta)
            if(item.delete):
                self.effectsList.remove(item)
                
    def clearEffects(self):
        self.effectsList = []
                
particleController = particleControllerClass()

#particleController.addItem(tileExplosion(),x,y)

class mapData:
    index = 0
    done = 0
    coins = 0
    critters = 0
    score = 0
    def __init__(self,index):
        self.index = index
    
    def writeRegistry(self,key):
        key += 'map'+str(self.index)+"/"
        writeReg(key+"d",str(self.done))
        writeReg(key+"c",str(self.coins))
        writeReg(key+"t",str(self.critters))
        writeReg(key+"s",str(self.score))
        #print("write map done",key,self.done)
        
    def readRegistry(self,key):
        key += 'map'+str(self.index)+"/"
        d = readReg(key+"d")
        c = readReg(key+"c")
        t = readReg(key+"t")
        s = readReg(key+"s")
        if(d and c and t and s):
            self.done = int(d)
            #print("read map done",key,self.done)
            self.coins = int(c)
            self.critters = int(t)
            self.score = int(s)

profileSaveFile = None

def openProfileDataForRead():
    global profileSaveFile
    try:
        path = localAppData+"/GoOllie/profiles.int"
        profileSaveFile = open( path, "r" )
    except IOError:
      #  print "file error not found"
        profileSaveFile = None
        

def openProfileDataForWrite():
    global profileSaveFile
    try:
        os.mkdir(localAppData+"/GoOllie")
    except:
        #print "directory exists"
        temp = 1
    path = localAppData+"/GoOllie/profiles.int"
    profileSaveFile = open( path, "w" )
 
def closeProfileData():
      global profileSaveFile
      profileSaveFile.close()
      profileSaveFile = 0

def writeReg(key,value):
    profileSaveFile.write(key+"\n")
    profileSaveFile.write(value+"\n")   
    
def readReg(key):   
    if key in Profile_Data:  
        value = Profile_Data[key]
    else:
        value = 0
    return value

def writeProfiles():
    openProfileDataForWrite()
    for profile in profiles:
        profile.writeRegistry()
    closeProfileData()
    
Profile_Data = {}    
    
def readProfiles():  
    global Profile_Data
    Profile_Data = {} 
    openProfileDataForRead()  
    key = 1
    if profileSaveFile != None:
        for line in profileSaveFile:
            if key:
                thisKey = line[:-1]
                key = 0
            else:
                value = line[:-1]
                Profile_Data[thisKey] = value
                key = 1
    for profile in profiles:
        profile.readRegistry()
    closeProfileData()

class profile:
    playerName = "Empty"
    index = 0
    compensator = 0
    stunJumpEnabled = 0
    smashEnabled = 0
    hangEnabled = 0
    dashEnabled = 0
    fairyEnabled = 0
    speedEnabled = 0
    arcadeStunJumpEnabled = 0
    arcadeSmashEnabled = 0
    arcadeHangEnabled = 0
    arcadeDashEnabled = 0
    FairyEnabled = 0
    arcadeSpeedEnabled = 0
    mouseControl = 1           #need to store to registry
    soundVolume = 2
    musicVolume = 2
    storyBegun = 0
    version = 1
    keysCollected = 0
    oldKeysCollected = 0
    campaignMaps = []
    arcadeProgress = 0
    tutorials = 1
    currentLanguage = 0
    
    def __init__(self,index):
        self.index = index
        self.ressetProfile()
            
    def getKey(self):
        return"profile"+str(self.index)+"/"

    def writeRegistry(self):
        writeReg(self.getKey()+"playerName",self.playerName)
        writeReg(self.getKey()+"DJ",str(self.stunJumpEnabled))
        writeReg(self.getKey()+"Smash",str(self.smashEnabled))
        writeReg(self.getKey()+"Hang",str(self.hangEnabled))
        writeReg(self.getKey()+"Dash",str(self.dashEnabled))
        writeReg(self.getKey()+"Fairy",str(self.fairyEnabled))
        writeReg(self.getKey()+"Speed",str(self.speedEnabled))
        
        writeReg(self.getKey()+"ADJ",str(self.arcadeStunJumpEnabled))
        writeReg(self.getKey()+"ASmash",str(self.arcadeSmashEnabled))
        writeReg(self.getKey()+"AHang",str(self.arcadeHangEnabled))
        writeReg(self.getKey()+"ADash",str(self.arcadeDashEnabled))
        writeReg(self.getKey()+"AFairy",str(self.arcadeFairyEnabled))
        writeReg(self.getKey()+"ASpeed",str(self.arcadeSpeedEnabled))        
        
        writeReg(self.getKey()+"Mouse",str(self.mouseControl))
        writeReg(self.getKey()+"Sound",str(int(self.soundVolume)))
        writeReg(self.getKey()+"Music",str(int(self.musicVolume)))
        writeReg(self.getKey()+"keysCollected",str(int(self.keysCollected)))
        writeReg(self.getKey()+"StoryBegun",str(self.storyBegun))
        writeReg(self.getKey()+"Version",str(self.version))
        writeReg(self.getKey()+"ArcadeProgress",str(self.arcadeProgress))
        writeReg(self.getKey()+"tutorials",str(self.tutorials))
        writeReg(self.getKey()+"adaptive",str(int(self.compensator)))
        writeReg(self.getKey()+"currentLanguage",str(int(self.currentLanguage)))        

        for map in self.campaignMaps:
            map.writeRegistry(self.getKey())
        
    def readRegistry(self):  
        playerName = readReg(self.getKey()+"playerName")
        if playerName:
            self.playerName = playerName
            
            stunJumpEnabled = readReg(self.getKey()+"DJ")
            if stunJumpEnabled:
                self.stunJumpEnabled = int(stunJumpEnabled)           
            
            smashEnabled = readReg(self.getKey()+"Smash")
            if smashEnabled:
                self.smashEnabled = int(smashEnabled)  

            hangEnabled = readReg(self.getKey()+"Hang")
            if hangEnabled:
                self.hangEnabled = int(hangEnabled)  

            dashEnabled = readReg(self.getKey()+"Dash")
            if dashEnabled:
                self.dashEnabled = int(dashEnabled)           
            
            fairyEnabled = readReg(self.getKey()+"Fairy")
            if fairyEnabled:
                self.fairyEnabled = int(fairyEnabled)  

            speedEnabled = readReg(self.getKey()+"Speed")
            if speedEnabled:
                self.speedEnabled = int(speedEnabled)  
 
 
            stunJumpEnabled = readReg(self.getKey()+"ADJ")
            if stunJumpEnabled:
                self.arcadeStunJumpEnabled = int(stunJumpEnabled)           
            
            smashEnabled = readReg(self.getKey()+"ASmash")
            if smashEnabled:
                self.arcadeSmashEnabled = int(smashEnabled)  

            hangEnabled = readReg(self.getKey()+"AHang")
            if hangEnabled:
                self.arcadeHangEnabled = int(hangEnabled)  

            dashEnabled = readReg(self.getKey()+"ADash")
            if dashEnabled:
                self.arcadeDashEnabled = int(dashEnabled)           
            
            fairyEnabled = readReg(self.getKey()+"AFairy")
            if fairyEnabled:
                self.arcadeFairyEnabled = int(fairyEnabled)  

            speedEnabled = readReg(self.getKey()+"ASpeed")
            if speedEnabled:
                self.arcadeSpeedEnabled = int(speedEnabled)  


            mouseControl = readReg(self.getKey()+"Mouse")
            if mouseControl:
                self.mouseControl = int(mouseControl) 
            
            soundVolume = readReg(self.getKey()+"Sound")
            if soundVolume:
                self.soundVolume = int(soundVolume)    

            musicVolume = readReg(self.getKey()+"Music")
            if musicVolume:
                self.musicVolume = int(musicVolume)
                
            keysCollected = readReg(self.getKey()+"keysCollected")
            if keysCollected:
                self.keysCollected = int(keysCollected)
                self.oldKeysCollected = self.keysCollected
                
            storyBegun = readReg(self.getKey()+"StoryBegun")
            if storyBegun:
                self.storyBegun = int(storyBegun) 
                
            arcadeProgress = readReg(self.getKey()+"arcadeProgress")
            if arcadeProgress:
                self.arcadeProgress= int(arcadeProgress) 

            tutorials = readReg(self.getKey()+"tutorials")
            if tutorials:
                self.tutorials= int(tutorials) 
                
            adaptive = readReg(self.getKey()+"adaptive")
            if adaptive:
                self.compensator= int(adaptive)                 
              
            currentLanguage = readReg(self.getKey()+"currentLanguage")
            if currentLanguage:
                self.currentLanguage= int(currentLanguage)    

            for map in self.campaignMaps:
                map.readRegistry(self.getKey())
              

            
    def ressetProfile(self):
        self.playerName = "Empty"
        self.stunJumpEnabled = 0
        self.smashEnabled = 0
        self.hangEnabled = 0
        self.dashEnabled = 0
        self.fairyEnabled = 0
        self.speedEnabled = 0
        
        self.arcadeStunJumpEnabled = 0
        self.arcadeSmashEnabled = 0
        self.arcadeHangEnabled = 0
        self.arcadeDashEnabled = 0
        self.arcadeFairyEnabled = 0
        self.arcadeSpeedEnabled = 0
        
        self.arcadeProgress = 0
        
        self.mouseControl = 1
        self.storyBegun = 0
        self.soundVolume = 2
        self.musicVolume = 2
        self.keysCollected = 0
        self.compensator = 0
        self.campaignMaps = []
        self.tutorials = 1
        self.currentLanguage = 0
        index = 0
        for map in range(len(levelData.storyCampaign)):
            newMapData = mapData(index)
            self.campaignMaps.append(newMapData)
            index += 1
      
profiles = [profile(0),profile(1),profile(2),profile(3),profile(4),profile(5)]

    
class AdaptiveDifficultyManager:
    terrible,poor,average,good,great= list(range(5))
    streak = 0
    gameMode = average
    max = 900  #must be less than maximum compensator threshold
    min = -900 #must be greater than minimum compensator threshold
    thresholds = [[-1000,-680],[-700,-280],[-300,300],[280,700],[680,1000]]
    def doingWell(self,increment):
        profiles[currentProfile].compensator += increment
        self.streak += increment/50.0
        #limit compensator to maximum
        if(profiles[currentProfile].compensator > self.max):
            profiles[currentProfile].compensator = self.max

    def doingBadly(self,increment):
        profiles[currentProfile].compensator -= increment
        #limit compensator to minimum
        if(profiles[currentProfile].compensator < self.min):
            profiles[currentProfile].compensator = self.min

    def setGameMode(self):
        index = 0
        for threshold in self.thresholds:
            if profiles[currentProfile].compensator>=threshold[0] and profiles[currentProfile].compensator<threshold[1]:
                self.gameMode = index
            index += 1
 
    def checkGameMode(self):
        if profiles[currentProfile].compensator <self.thresholds[self.gameMode][0]:
            self.gameMode -= 1
        if profiles[currentProfile].compensator > self.thresholds[self.gameMode][1]:
            self.gameMode += 1  
            #just in case clamp them
        if self.gameMode < self.terrible:
            self.gameMode = self.terrible
        if self.gameMode > self.great:
            self.gameMode = self.great
        #print("adaptive difficulty",profiles[currentProfile].compensator,self.gameMode)
            
    def getGameMode(self):
        self.checkGameMode()
        return self.gameMode
        
    def renderDebug(self):
        self.checkGameMode()
        PC.setColour( 255, 255, 255, 255 )
        tabX= 300
        PC.setFont( font22 )
        scoreString= "Mode"+str(self.gameMode)+" comp "+str(int(profiles[currentProfile].compensator))
        drawStringDropShadow(scoreString,tabX,60,60,200,0) 
        
    def getScroll(self):  
        self.checkGameMode()
        scrollCompensation = (self.gameMode-self.average)/2.0
        return scrollCompensation
            
adaptive = AdaptiveDifficultyManager()    



class InstructionManagerClass:
    anyKeyPressed = 1
    instructionsUp = 0
    backAlpha = 0
    targetBackAlpha = 0
    fairyFrameNumber = 0
    animationSwitch=10
    animation = animationSets.fairy_move
    frame = None
    fairyX = 0
    fairyY = 0
    fairyTargetX = 770
    fairyTargetY = 10
    fairyScale = 1
    rectX = 100
    rectY = 50
    rectWidth = 600
    rectHeight = 200
    fairAlpha = 0
    def showInstruction(self,instructions):
        global forcePause
        global instructionWait
        instructionWait = 1
        forcePause = 1
        self.fairyX = 830
        self.fairyY = -10
        self.fairyTargetX = 770
        self.fairyTargetY = 30
        self.targetBackAlpha = 255
        self.instructionsUp = 1
        self.anyKeyPressed = 1 #set this true initially 
        maxWidth = 0 
        self.rectHeight = 80
        ScreenMessages.lastMessageTabY  = 120

        for message in instructions:
            ScreenMessages.setMessageScroll(message,None)
            ScreenMessages.lastMessageTabY -= 2
            if message[6] == 22:
                font = font23
            else:
                font = font38
            if font == None:
                return
            workingString = message[0]
            HighLight = workingString.find('__H')
            if HighLight != -1:
                HighLightDown = workingString.find('__N')
                right = workingString[:HighLight]
                left = workingString[HighLightDown+3:]
                highLightString = workingString[HighLight+3:HighLightDown]
                workingString = right + highLightString +  left
            width = PCR.stringWidth(workingString,font)
            self.rectHeight += 40
            if width > maxWidth:
                maxWidth = width
        self.rectY = ScreenMessages.lastMessageTabY - self.rectHeight+ 80
        self.rectWidth = maxWidth
        self.fairyX = 335 + maxWidth/2
        self.fairyY = 25
        self.rectX = (800 - self.rectWidth)/2
#        ScreenMessages.setMessageScroll(messages.Blank22,None)  
        ScreenMessages.setMessageScroll(messages.ClickHere,None,function = self.continueGame)  
    
    def continueGame(self):
        global forcePause
        forcePause = 0
        self.targetBackAlpha = 0
        self.instructionsUp = 0
        self.fairyAlpha = 0
        if ScreenMessages and metaGame==0:
            ScreenMessages.fadeAndClear()   
        setTargetVolume(1)
        
    def tick(self,delta):        
        if self.fairyScale  < 1.5:
            self.fairyScale += delta/200.0             
        self.animationSwitch -= delta;
        if(self.animationSwitch<= 0):
            self.fairyFrameNumber = self.animation[self.fairyFrameNumber][1]
            self.animationSwitch = self.animation[self.fairyFrameNumber][2]        
        if noKeyDown():
            self.anyKeyPressed = 0
        if metaGame:
            self.targetBackAlpha = 0
            
        if self.targetBackAlpha:    
            setTargetVolume(quietMusic)

        if anyKeyDown() and self.anyKeyPressed==0 and forcePause==1:
            self.continueGame()
        if(self.backAlpha<self.targetBackAlpha):
            self.backAlpha += delta*4
            if(self.backAlpha>self.targetBackAlpha):
                self.backAlpha = self.targetBackAlpha
        if(self.backAlpha>self.targetBackAlpha):
            self.backAlpha -= delta*4
            if(self.backAlpha<self.targetBackAlpha):
                self.backAlpha = self.targetBackAlpha
    def render(self):
        if  self.backAlpha: 
            PC.setColourize(1)          
            PC.setColour( 255, 255, 255, int(self.backAlpha))
            res = JPG_Resources['helpBack'] 
            PC.drawmodeNormal()
            PC.drawImageScaled( res, self.rectX,self.rectY,self.rectWidth,self.rectHeight)
            self.renderFairy(self.fairyX,self.fairyY,self.fairyScale)
            
    def renderFairy(self,x,y,scale):
        name = self.animation[self.fairyFrameNumber][0]
        self.frame = JPG_Resources[name]
        if(self.frame != None):
            PC.setColourize(1)          
            PC.setColour( 255, 255, 255, int(self.backAlpha))
            width = PCR.imageWidth(self.frame)
            height = PCR.imageHeight(self.frame)
            PC.drawImageScaled( self.frame, x, y,width*scale,height*scale)
    


instructionManager = InstructionManagerClass()

class cutSceneClass(canvas):
    nextEvent = 0
    running = 0
    backDrop = None
    stepTimer = 0
    openingScene = 0
    anyKeyPressed = 1
    cutSceneNumber = 1
    cutScenePtr = None
    cutSceneTitle = None
    commands = None
    nextCommand = 0
    tabY = 0
    ForeGroundAlpha = 255
    fadeSpeed = 0
    higherScenery = []
    lowerScenery = []
    
    def startNew(self):
        global objects
        global cameraX
        global cameraY

        self.stepTimer=0
        self.nextEvent = 0
        self.nextCommand = 0
        self.ForeGroundAlpha = 255
        self.tabY = 60
        ScreenMessages.clearMessages()
        self.running = 1
        self.stepTimer = 10
        self.cutScenePtr = cutScenes.cutsceneList[self.cutSceneNumber]
        #print "setting up cutscene"
        self.backDrop = self.cutScenePtr[0]
        self.stepTimer = self.cutScenePtr[1]
        self.commands = self.cutScenePtr[2]
        self.music = self.cutScenePtr[3]
        self.lowerScenery = self.cutScenePtr[4]
        self.higherScenery = self.cutScenePtr[5]
        if self.music != "":
            (self.music,1)
            playTuneOgg (self.music,1)
        else:
            stopTuneOgg()
        #ScreenMessages.setMessageStatic(messages.Blank36,None,-1,self.tabY,None,self.cutSceneTitle)
        objects = []
        cameraX = 0
        cameraY = 0
        fairyPointer.stop()
        particleController.clearEffects()

    def setAnimation(self,ID,animation):
        for object in objects:
            if object.ID == ID:
                object.animation = animation
                object.frameNumber = 0
      
    def addStartButton(self):
        self.tabY += 20
        ScreenMessages.setMessageStatic(messages.Continue,None,-1,self.tabY,self.exit)
        
    def addEndButton(self):
        self.tabY += 20
        ScreenMessages.setMessageStatic(messages.TheEnd,None,-1,self.tabY,self.exit)
    def render(self):
      
        self.renderBackDrop()
        self.renderScenery()
        self.renderObjects()

        
    def createObject(self,type,x,y,ID):
        global objects
      #  import copy
        newObject = copy.copy(AllWorldObjects[int(type)])
        newObject.setUpGraphics()
        newObject.x = x
        newObject.y = y
        newObject.targetX = x
        newObject.targetY = y
        newObject.ID= ID
        objects.append(newObject)
        
    def moveObject(self,ID,x,y):
        for object in objects:
            if object.ID == ID:
                object.x = x
                object.y = y
                
    def setTarget(self,ID,x,y):
        for object in objects:
            if object.ID == ID:
                object.targetX = x
                object.targetY = y
                
    def tickObjects(self,delta):
        for object in objects:
            object.tick(delta)
            
    def renderObjects(self):
        for object in objects:
            object.render()
            
    def startFadeOutForeground(self,fadeSpeed):
        self.fadeSpeed = fadeSpeed
        
    def fadeForGround(self,delta):
        self.ForeGroundAlpha += self.fadeSpeed*delta
        if self.ForeGroundAlpha<0:
            self.ForeGroundAlpha = 0
            self.fadeSpeed = 0
        if self.ForeGroundAlpha>255:
            self.ForeGroundAlpha = 255
            self.fadeSpeed = 0              
      
    def tick(self,delta):
        global oldMetaGame
        global cameraX
        global cameraY
        canvas.tick(self,delta)
        cameraX = 0
        cameraY = 0
        if(oldMetaGame!= metaGame):
            self.startNew()
            oldMetaGame = metaGame
        else:
            self.tickObjects(delta)
            if self.nextCommand < len(self.commands):
                self.stepTimer -= delta
                if self.stepTimer <=0:
                    commandPtr = self.commands[self.nextCommand]
                    self.stepTimer = commandPtr[0] #set up the timer
                    if commandPtr[1] == cutScenes.StringCommmand:
                        self.printString(commandPtr)
                    if commandPtr[1] == cutScenes.VerticalTab:
                        self.tabY +=  int(commandPtr[2])   
                    if commandPtr[1] == cutScenes.SpawnObject:
                        self.createObject(commandPtr[2],commandPtr[3],commandPtr[4],commandPtr[5])
                    if commandPtr[1] == cutScenes.MoveObject:
                        self.moveObject(commandPtr[2],commandPtr[3],commandPtr[4])
                    if commandPtr[1] == cutScenes.setTarget:
                        self.setTarget(commandPtr[2],commandPtr[3],commandPtr[4])   
                    if commandPtr[1] == cutScenes.fadeOutForeground:
                        self.startFadeOutForeground(commandPtr[2])
                    if commandPtr[1] == cutScenes.setAnimation:
                        self.setAnimation(commandPtr[2],commandPtr[3])  
                    if commandPtr[1] == cutScenes.addStartButton:
                        self.addStartButton()
                    if commandPtr[1] == cutScenes.addEndButton:
                        self.addEndButton()
                    self.nextCommand+=1
                if noKeyDown():
                    self.anyKeyPressed = 0
                if (anyKeyDown() and self.anyKeyPressed==0) :
                    self.exit()
            else:
                fairyPointer.enabled  = 1
            self.fadeForGround(delta)
                
    def printString(self,commandPtr):
        string = commandPtr[2]
        sound = commandPtr[3]
        fadeUpTime = 100.0
        if commandPtr[8] == 22:
            message = messages.Blank22Light
        else:
            message = messages.Blank36Light
        ScreenMessages.setMessageStatic(message,None,-1,self.tabY,None,string,fadeUp = fadeUpTime)
        self.tabY += 30
        
    def renderBackDrop(self):
        PC.drawmodeNormal()
        if self.backDrop:
            backDropManager.checkAndReload(self.backDrop)
            backDropRes = backDropManager.backDropResource
            PC.drawImage( backDropRes, 0,0)

    def renderScenery(self):
        x = 100
        for item in self.lowerScenery:
            res = JPG_Resources[item]
            width = PCR.imageWidth(res)
            height = PCR.imageHeight(res)
            y = 600 - height
            PC.drawImage( res, x, y)  
            x += width + 50
        x = 100
         
        for item in self.higherScenery:
            res = JPG_Resources[item]
            width = PCR.imageWidth(res)
            height = PCR.imageHeight(res)
            y = 0
            PC.drawImage( res, x, y)  
            x += 300           
        PC.setColour(0,0,0,int(self.ForeGroundAlpha))
        PC.fillRect( 0,0,800,600)

            
    def exit(self):
        global metaGame
        self.running = 0
        metaGame = 3
        fairyPointer.enabled  = 1 #has to be done here too in case of escape key
        
cutScene = cutSceneClass()

class FadeManagerClass:
    alpha = 0
    speed = 0
    direction = 0
    nextMetaGameMenu = 0
    def tick(self,delta):   
        global metaGame
        global startGame
        if self.direction <0:
            if self.alpha > 0:
                self.alpha -= self.speed*delta
            if self.alpha <= 0:
                self.alpha =0
                self.direction = 0
        if self.direction >0:
            if self.alpha < 256:
                self.alpha += self.speed*delta
            if self.alpha >= 255:
                self.alpha = 255
                self.direction = 0
                inGameMenuManager.makeActive(0)
                if self.nextMetaGameMenu != -1:
                    if self.nextMetaGameMenu == menuItems.replayLevel:
                        replayLevel()
                    elif self.nextMetaGameMenu == menuItems.arcadeLevel:
                        #print "starting arcade",levelNumber
                        startArcadeGame(levelNumber/levelsPerArcadeSegment)
                    else:
                        metaGame = self.nextMetaGameMenu
                        startGame = 1
              
    def render(self):
        if self.alpha >0:
            PC.setColourize(1)
            PC.setColour(0,0,0,int(self.alpha))
            PC.fillRect( 0,0,800,600)
            PC.setColourize(0)
            
    def fadeDown(self,nextMetaGame=-1,speed = 5):
        self.nextMetaGameMenu = nextMetaGame
        self.direction = 1
        self.speed = speed
        
    def fadeUp(self,speed = 5):
        self.direction = -1
        self.speed = 10
      
    def fadeUpIfReady(self):
        if self.direction == 0:
            self.direction = -1
        
    def finished(self):
        return self.direction == 0

fadeManager = FadeManagerClass()

def startGridExplosion():
    playSimpleSound ("explosion2") 
    particleController.addItem(vBigExplosion(),cameraX+750,000,1)
    particleController.addItem(vBigExplosion(),cameraX+750,300,1)   
    particleController.addItem(vBigExplosion(),cameraX+750,600,1)

class notUsed:
    def tick():
        return 0
    def render():
        return 0
        
class sellUpScreen(canvas):
    exitFlag = 0    
    def render(self):
        character = self.animation[self.frameNumber][0]
        self.frame = None
        #self.title = JPG_Resources[ 'Options']

        canvas.render(self)
 
        x = 0
        y = 300
        image = JPG_Resources["AW1"]
        PC.drawImage(image,x,y)
        
        image = JPG_Resources["AW2"]
        PC.drawImage(image,400,y)
                
    def backToStory(self):
        fadeManager.fadeDown(menuItems.storyCanvas)
        
    def tick(self,delta):    
        global metaGame
        global oldMetaGame
        global scorePos
        global score
        global inGUI
        canvas.tick(self,delta)
        if(oldMetaGame!= metaGame):
            playTuneOgg("Level3.ogg",1)
            ScreenMessages.clearMessages()
            canvas.ressetTitle(self)
            inGUI = 1
            mouseEnabled = 1
            y_delta = 35
            y = 50
            ScreenMessages.setMessageStatic(messages.buyUp6,None,-1,y,None )
            y += 35
            ScreenMessages.setMessageStatic(messages.buyUp7,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.buyUp8,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.buyUp9,None,-1,y,None )
            y += y_delta
            ScreenMessages.setMessageStatic(messages.buyUp10,None,-1,y,None )
            y += y_delta +10 
#            ScreenMessages.setMessageStatic(messages.CharlieWeb,None,-1,y,charlieWebsite)  
#            y += y_delta + 10           
            ScreenMessages.setMessageStatic(messages.TweelerWeb,None,-1,y,tweelerWebsite)  
            y += y_delta + 20           
            ScreenMessages.setMessageStatic(messages.Quit,None,-1,y,self.exit1) 

                 
            oldMetaGame = metaGame
            
    def buyGame(self):
        if superior:
            openWebPage("https://secure.bmtmicro.com/servlets/Orders.ShoppingCart?PRODUCTID=28610000&CID=4&AID=709763")  
        else:
            openWebPage("https://secure.bmtmicro.com/servlets/Orders.ShoppingCart?CID=2861&PRODUCTID=28610000")
        global doExit
        doExit = 1        

    def snakeWebsite(self):
        openWebPage("http://www.charliedoggames.com/?page_id=3")
        
    def exit1(self):
        global doExit
        doExit = 1

def charlieWebsite():
        openWebPage("http://www.charliedoggames.com")        

def tweelerWebsite():
        openWebPage("http://www.tweeler.com")

sellUpCanvas = sellUpScreen()


class sellUpScreenExit(sellUpScreen):
    exitFlag = 1
    def exit(self):
        exitGameOption()

sellUpExitCanvas = sellUpScreenExit()        
        

class menuItems: 
    game,highScoreCanvas,optionsCanvas,storyCanvas,nameCanvas,profileCanvas,cutScene,mainScreenCanvas,replayLevel,welcomeCanvas,cheatCanvas,arcadeChoiceCanvas,creditCanvas,sellUpExitCanvas,arcadeLevel,instructionListCanvas,instructionCanvas,sellUpCanvas = list(range(18))
    
menuClasses = [notUsed,highScoreCanvas,optionsCanvas,storyCanvas,nameCanvas,profileCanvas,cutScene,mainScreenCanvas,notUsed,welcomeCanvas,cheatCanvas,arcadeChoiceCanvas,creditCanvas,sellUpExitCanvas,notUsed,instructionListCanvas,instructionCanvas,sellUpCanvas]    

def numberToString(number):
#takes a number and returns it as an integer string with commas seperating the thousands
    output = ""
    newNumber = int(number)
    while newNumber>999:
        numberString = str(newNumber)[-3:]
        output = ","+numberString+output
        newNumber /= 1000
    output = str(newNumber)+output 
    return output
    
def setLocalAppData():
    global localAppData
    localAppData = PC.getAppDataFolder()
    try:
        os.mkdir(localAppData+"/GoOllie")
        path = localAppData+"/GoOllie/profiles.int"
        profileSaveFile = open( path, "w" )
        profileSaveFile.close()
    except:
        temp = 1
        #print "directory already exists",localAppData+"/GoOllie"
    #print "user path",localAppData
    
    
    
