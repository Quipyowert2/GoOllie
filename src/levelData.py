#level data
import game
messages = game.messages

levelMusic1 = ["Level1","level1Win","level1Lose"]
levelMusic2 = ["Level2","level2Win","level2Lose"]
levelMusic3 = ["Level3","level3Win","level3Lose"]
levelMusic4 = ["Level4","level4Win","level4Lose"]
menuSong = "Menu"
storyScreenSong = "cutScene"

Red,Green,Blue,Orange,Purple,Yellow,White,Black,Stripe = list(range(9))
#tony below is only needed as interim step
jewelColour = ['Red','Green','Blue','Orange','Purple','Yellow','White','Black','Truck'] 
jewel1 = ['Ball','Bear','Car','Block','Hoop','Top','Drum','Panda','Truck']
jewel2 = ['Amethyst','Citrine','Fanta','Ruby','Sapphire','Topaz','Emerald','White','Truck']
jewel3 = ['Flower01','Flower02','Flower03','Flower04','Flower05','Flower06','Flower07','Flower08','Truck']
jewel4 = ['Fruit01','Fruit02','Fruit03','Fruit04','Fruit05','Fruit06','Fruit07','White','Truck']
DynamicPlatform,DynamicVerticalPlatform,FinishPlatform,platform100,platform200,platform400,StagingPlatform,stem100,stem200,stem400,ExitPlatform=list(range(11))

DynamicPlatformWood = ['DynamicPlatformWood']
DynamicPlatformVerticalWood=['DynamicPlatformVerticalWood']
FinishPlatformWood=['FinishPlatformWood']
ExitPlatformWood=['ExitPlatformWood']
StagingPlatformWood=['StagingPlatformWood']
platform100Wood=['platform100Wood','platform100WoodF1','platform100WoodF2']
platform200Wood=['platform200Wood','platform200WoodF1','platform200WoodF2']
platform400Wood=['platform400Wood','platform400WoodF1','platform400WoodF2']
swingWood = ['SwingPlatform','ChainShort','ChainMed','ChainLong','SwingPlatformShort','SwingPlatformMed']
platforms1 =[DynamicPlatformWood,DynamicPlatformVerticalWood,FinishPlatformWood,platform100Wood,platform200Wood,platform400Wood,StagingPlatformWood,'Stem100','Stem200','Stem400',ExitPlatformWood,swingWood]


DynamicPlatformSquareRock=['DynamicPlatformSquareRock']
DynamicVerticalPlatformSquareRock=['DynamicVerticalPlatformSquareRock']

DynamicPlatformRock = ['DynamicPlatformRock']
DynamicPlatformVerticalRock=['DynamicPlatformVerticalRock']
FinishPlatformRock=['FinishPlatformRock']
StagingPlatformRock=['StagingPlatformRock']
platform100Rock=['platform100Rock','platform100RockF1','platform100RockF2']
platform200Rock=['platform200Rock','platform100RockF1','platform100RockF2']
platform400Rock=['platform400Rock','platform100RockF1','platform100RockF2']
swingWood = ['SwingPlatform','ChainShort','ChainMed','ChainLong','SwingPlatformShort','SwingPlatformMed']
platforms2 =[DynamicPlatformSquareRock,DynamicVerticalPlatformSquareRock,FinishPlatformRock,platform100Rock,platform200Rock,platform400Rock,StagingPlatformRock,'Stem100','Stem200','Stem400',ExitPlatformWood,swingWood]

DynamicPlatformHedge = ['PlatformDynamicHedge']
DynamicPlatformVerticalHedge=['PlatformDynamicVerticalHedge']
FinishPlatformHedge=['FinishPlatformHedge']
StagingPlatformHedge=['StagingPlatformRock']
platform100Hedge=['Platform100Hedge','Platform100Hedge','Platform100Hedge']
platform200Hedge=['Platform200Hedge','Platform200Hedge','Platform200Hedge']
platform400Hedge=['Platform400Hedge','Platform400Hedge','Platform400Hedge']
swingWood = ['SwingPlatform','ChainShort','ChainMed','ChainLong','SwingPlatformShort','SwingPlatformMed']
platforms3 =[DynamicPlatformHedge,DynamicPlatformVerticalHedge,FinishPlatformHedge,platform100Hedge,platform200Hedge,platform400Hedge,StagingPlatformHedge,'Stem100','Stem200','Stem400',ExitPlatformWood,swingWood]

DynamicPlatformBamboo = ['PlatformDynamicBamboo']
DynamicPlatformVerticalBamboo=['PlatformDynamicVerticalBamboo']
FinishPlatformBamboo=['FinishPlatformBamboo']
StagingPlatformBamboo=['StagingPlatformBamboo']
platform100Bamboo=['Platform100Bamboo','Platform100BambooF1','Platform100BambooF2']
platform200Bamboo=['Platform200Bamboo','Platform200BambooF1','Platform200BambooF2']
platform400Bamboo=['Platform400Bamboo','Platform400BambooF1','Platform400BambooF2']
swingVine = ['JVineBase','JVineMed','JVineLong','JVineVLong','JVineBase','JVineBase']
platforms4 =[DynamicPlatformBamboo,DynamicPlatformVerticalBamboo,FinishPlatformBamboo,platform100Bamboo,platform200Bamboo,platform400Bamboo,StagingPlatformBamboo,'Stem100','Stem200','Stem400',ExitPlatformWood,swingVine]

gridDeath = 1
noGridDeath = 0
#defines data used in each section
lower1 = ['JunkPile01','JunkPile02']
upper1 = ['OverheadLight01','OverheadLight02']
lower2 = ['FB1','FB2','Stalagmite01']
upper2 = ['FB3','FB4','Stalactite01']
lower3 = ['Shrub01','Shrub02','Shrub03']
upper3 = ['Cloud01','Cloud02']
lower4 = ['JungleScenery01','JungleScenery02']
upper4 = ['Vine01','Vine02']
section1 = ['Backdrop1',lower1,upper1,'Campaign1',jewel1,platforms1,gridDeath,1,"enterLevel"]
section1A = ['Backdrop1',lower1,upper1,'CampaignArrow',jewel1,platforms1,gridDeath,2,"enterLevel"]
section2 = ['Backdrop03',lower3,upper3,'Campaign1',jewel3,platforms3,gridDeath,2,"enterLevel"]
section2A = ['Backdrop03',lower3,upper3,'CampaignArrow',jewel3,platforms3,gridDeath,3,"enterLevel"]
section3 = ['Backdrop2',lower2,upper2,'Campaign1',jewel2,platforms2,gridDeath,3,"enterLevel"]
section3A = ['Backdrop2',lower2,upper2,'CampaignArrow',jewel2,platforms2,gridDeath,4,"enterLevel"]
section4 = ['Backdrop4',lower4,upper4,'Campaign1',jewel4,platforms4,gridDeath,4,"enterLevel"]
section4A = ['Backdrop4',lower4,upper4,'CampaignEnd',jewel4,platforms4,gridDeath,4,"enterLevel"]
sectionList = [section1,section2,section3,section4]
#defines dat used in each level 
#section number,name,random tiles, randomly generated tiles,metaGameData,Name,?,midi
dummy = [section1,0,'',0,0,00]

level05=  [section1,'level003',0,0,1,"The snake's tale",messages.BasicMouseInstructions1,levelMusic3,0,0,1]
level10 =  [section1,'level005',0,0,2,"Collect the coins",messages.coinInstructions1,levelMusic3,0,messages.coinInstructions2,2]
level20 =  [section1,'level010',0,1,3,"Scrolling along",messages.ScrollInstructions1,levelMusic3,0,messages.ScrollInstructions2,3]
level40 =  [section1,'level020',4,0,4,"Jake's a swinger",messages.MoversInstructions,levelMusic2,0,0,6]
level60 =  [section1,'level030',4,0,5,"Fruit salad!",messages.BlocksInstructions1,levelMusic2,0,messages.BlocksInstructions2,5]
level30 =  [section1,'level015',0,1,6,"Creepy crawlies",messages.EnemyInstructions1,levelMusic2,0,messages.EnemyInstructions2,4]
level70 =  [section1,'level035',4,0,7,"Quest",messages.FirstGemInstructions,levelMusic1,0,messages.SnakePowerInstructions,7]
level80 =  [section1,'level040',4,0,8,"Getting tricky",0,levelMusic1,0,0,8]
level90 =  [section1,'level045',5,0,9,"Busy work",0,levelMusic2,0,0,9]
level100 = [section1,'level050',5,0,10,"Tarzan",0,levelMusic2,0,0,10]
level110 = [section1,'level055',5,0,11,"Static",0,levelMusic1,0,0,11]
level120 = [section1,'level060',5,0,12,"Speedy",0,levelMusic1,0,0,12]
level130 = [section1,'level065',5,0,13,"Hanging out",messages.SecondGemInstructions1,levelMusic1,0,0,13]
level140 = [section1,'level070',5,0,14,"Sting in the tail",0,levelMusic3,0,0,14]
level150 = [section1,'level075',5,0,15,"Almost out",messages.FirstKeyInstructions1,levelMusic1,0,0,15]

level160 = [section2,'level105',5,3,16,"Jack knife",messages.SecondKeyInstructions1,levelMusic4,0,messages.SecondKeyInstructions2,29]
level170 = [section2,'level110',5,3,17,"Bat cave",0,levelMusic2,2,0,30]
level180 = [section2,'level115',5,0,18,"Duplicity",0,levelMusic4,0,0,31]
level190 = [section2,'level120',5,3,19,"Torment",messages.ThirdGemInstructionsA,levelMusic1,0,messages.ThirdGemInstructionsB,26]
level200 = [section2,'level125',5,3,20,"Quick slither",0,levelMusic1,2,0,27]
level210 = [section2,'level130',5,0,21,"Complex",0,levelMusic3,2,0,28]
level220 = [section2,'level135',5,0,22,"Charisma",0,levelMusic2,0,0,23]
level230 = [section2,'level140',5,0,23,"Rotation",0,levelMusic3,0,0,24]
level240 = [section2,'level145',5,0,24,"Purity",0,levelMusic4,0,0,25]
level250 = [section2,'level150',6,0,25,"Charmed",0,levelMusic3,0,0,22]
level260 = [section2,'level155',6,0,26,"Arachn0phobia",0,levelMusic2,0,0,21]
level270 = [section2,'level160',6,0,27,"You need wheels",0,levelMusic2,0,0,20]
level280 = [section2,'level165',6,0,28,"Hidden agenda",messages.HiddenInstructions,levelMusic4,0,0,17]
level290 = [section2,'level170',6,0,29,"Bigger is better",messages.SecondGemInstructions2,levelMusic4,0,0,18]
level300 = [section2,'level175',6,0,30,"Precious stones",messages.CaveGems,levelMusic2,0,messages.CaveGems2,19]

level310 = [section3,'level205',5,0,31,"Walk in the park",0,levelMusic2,0,0,33]
level320 = [section3,'level210',6,0,32,"Bouncy bouncy",messages.TrampInstructions,levelMusic2,0,0,34]
level330 = [section3,'level215',6,0,33,"Flower power",0,levelMusic1,0,0,35]
level340 = [section3,'level220',6,0,34,"Inversion",0,levelMusic2,0,0,40]
level350 = [section3,'level225',6,0,35,"Signs",0,levelMusic4,0,0,39]
level360 = [section3,'level230',6,0,36,"Stingers",0,levelMusic2,0,0,36]
level370 = [section3,'level235',6,0,37,"Sprint",0,levelMusic1,0,0,41]
level380 = [section3,'level240',6,0,38,"Puzzling",0,levelMusic3,0,0,38]
level390 = [section3,'level245',6,0,39,"Ball games",0,levelMusic4,0,0,37]
level400 = [section3,'level250',6,0,40,"Park life",0,levelMusic1,0,0,42]
level410 = [section3,'level255',6,0,41,"Popping python",0,levelMusic2,0,0,43]
level420 = [section3,'level260',6,0,42,"Tick tock!",0,levelMusic3,3,0,44]
level430 = [section3,'level265',6,0,43,"On the rebound",0,levelMusic3,0,0,45]
level440 = [section3,'level270',6,0,44,"Links",0,levelMusic2,3,0,46]
level450 = [section3,'level275',6,0,45,"Chastity",0,levelMusic4,0,0,47]

level460 = [section4,'level305',6,0,46,"Home straight",0,levelMusic3,0,0,61]
level470 = [section4,'level310',6,0,47,"Cave cruisader",0,levelMusic4,0,0,62]
level480 = [section4A,'level315',6,0,48,"Jungle finale",0,levelMusic1,0,0,63]
level490 = [section4,'level320',6,0,49,"Frantic",0,levelMusic1,0,0,58]
level500 = [section4,'level325',6,0,50,"Transient",0,levelMusic2,0,0,59]
level510 = [section4,'level330',6,0,51,"Reunion",0,levelMusic4,0,0,60]
level520 = [section4,'level335',6,0,52,"Syncopation",0,levelMusic4,4,0,55]
level530 = [section4,'level340',6,0,53,"Up, up & away",0,levelMusic1,4,0,56]
level540 = [section4,'level345',6,0,54,"Toy trail",0,levelMusic2,4,0,57]
level550 = [section4,'level350',6,0,55,"Trinity",0,levelMusic3,0,0,52]
level560 = [section4,'level355',6,0,56,"Virtue",0,levelMusic4,0,0,53]
level570 = [section4,'level360',6,0,57,"Haunted",0,levelMusic1,0,0,54]
level580 = [section4,'level365',6,0,58,"Derelict rides",0,levelMusic3,0,0,49]
level590 = [section4,'level370',6,0,59,"Ghosts'n toys",0,levelMusic3,0,0,50]
level600 = [section4,'level375',6,0,60,"GR4C3 R4C3",0,levelMusic4,0,0,51]

level610 = [section1A,'level710',6,0,61,"The exit",0,levelMusic1,1,0,16]
level620 = [section2A,'level720',6,0,62,"Long jump",0,levelMusic1,0,0,32]
level630 = [section3A,'level730',6,0,63,"Park gate",0,levelMusic1,0,0,48]

arcadeCampaign = [dummy, #currenty not used.

level30,
level60,
level80,
level90,
level100,
level130,
level140,
level120,

level300,
level260,
level250,
level240,
level220,
level190,
level180,
level200,

level330,
level340,
level350,
level390,
level400,
level410,
level450,
level370,

level570,
level560,
level540,
level510,
level500,
level490,
level520,
level600,
]

#defines data used in campaign
storyCampaign =  [ dummy,             #currenty not used.
              level05,
              level10,
              level20,
              level40,
              level60,
              level30,
              level70,
              level80,
              level90,
              level100,
              level110,
              level120,
              level130,
              level140,
              level150,
              level160,
              level170,
              level180,
              level190,            
              level200,              
              level210,
              level220,
              level230,
              level240,
              level250,
              level260,
              level270,
              level280,
              level290,            
              level300,              
              level310,
              level320,
              level330,
              level340,
              level350,
              level360,
              level370,
              level380,
              level390,            
              level400,
              level410,
              level420,
              level430,
              level440,
              level450,
              level460,
              level470,
              level480,
              level490,            
              level500,
              level510,
              level520,
              level530,
              level540,
              level550,
              level560,
              level570,
              level580,
              level590,            
              level600,
              level610,
              level620,            
              level630,
              ]

campaignTrial = [[0,0],
[-18,-28],[60,0],[120,0],
[0,75],[60,75],[120,75],
[0,150],[60,150],[120,150],
[0,225],[60,225],[120,225],
[0,300],[60,300],[120,300],

[190,0],[255,0],[320,0],
[190,75],[255,75],[320,75],
[190,150],[255,150],[320,150],
[190,225],[255,225],[320,225],
[210,300],[265,300],[320,300],

[415,0],[470,0],[520,0],
[400,75],[455,75],[520,75],
[400,150],[460,150],[520,150],
[400,225],[460,225],[520,225],
[400,300],[460,300],[520,300],

[590,0],[640,0],[690,-28],
[600,75],[660,75],[720,75],
[600,150],[660,150],[720,150],
[600,225],[660,225],[720,225],
[600,300],[660,300],[720,300],

[166,300],[371,0],[566,300],
]

campaignLinks = [ [0],
[0],[1,3],[2,6],
[5,7],[4,6],[3,5],
[4,10,8],[7,9,11],[8,12],
[7,11,13],[10,8,12,14],[9,11,15],
[10,14],[13,11,15],[14,12,61],

[19,17],[16,18,20],[17,21,62],
[20,22,16],[19,17,21,23],[18,20,24],
[19,25,23],[22,20,24,26],[21,23,27],
[26,22],[25,23,27],[24,26,30],
[61,29],[28,30],[29,27],
#[29],[28,30],[29,27],

[62,32],[31,33],[32,36],
[35,37],[34,38],[33,39],
[34,40,38],[35,37,39,41],[36,38,42],
[37,41,43],[40,38,42,44],[39,41,45],
[40,44],[41,43,45],[42,44,63],

[47,49],[46,48],[47],
[46,50,52],[49,51,47,53],[50,48,54],
[49,55,53],[52,50,56,54],[53,51,57],
[52,58,56],[53,55,57,59],[56,54,60],
[63,59,55],[58,56,60],[59,57],

[15,28],[18,31],[45,58],

]




levelSpeed = [0,
2.0,2.0,2.2,
2.4,1.4,2.3,
2.6,2.8,3.0,
2.8,3.0,3.2,
3.0,3.2,3.3,

3.5,3.5,3.5,
3.5,3.5,3.5,
3.4,3.4,3.4,
3.4,3.4,3.4,
3.3,3.3,3.3,

3.5,3.5,3.5,
3.6,3.6,3.6,
3.7,3.7,3.7,
3.7,3.7,3.7,
3.8,3.8,3.8,

4.2,4.2,4.3,
4.1,4.1,4.0,
4.0,4.0,4.0,
3.9,3.9,3.9,
3.8,3.8,3.8,

3.3,3.5,3.8,
]
