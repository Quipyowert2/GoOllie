
import WorldTypes
import animationSets

StringCommmand,LinearCommmand,VerticalTab,SpawnObject,MoveObject,setTarget,fadeOutForeground,addStartButton,setAnimation,addEndButton = list(range(10))
JakeID,FairyID,SpellID,Jake2ID,LightID,amuletID,fireWorksID = list(range(7))

#command is structured: time delay till next command, command type, body
CS1Commands = [
              [170,StringCommmand,"Ollie Visits the jungle",None,200,20,20,180,36],
              [0,VerticalTab,30],
              [170,StringCommmand,"Ollie the Oligocheata",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSJake,-100,120,JakeID],
              [0,setTarget,JakeID,50,130],
              [170,StringCommmand,"Wants to meet a sweet senorita",None,60,200,0,180,22],
              [170,StringCommmand,"With eyes of blue",None,60,200,0,180,22], 
              [170,StringCommmand,"And a heart that's true",None,60,200,0,180,22],                
              [170,StringCommmand,"\"Oh I wish that I could meet her!\"",None,60,200,0,180,22],
              [75,VerticalTab,15],
              [0,SpawnObject,WorldTypes.CSFairy,900,170,FairyID],
              [0,setTarget,FairyID,620,220],
              [170,StringCommmand,"A fairy hears the worms plea",None,60,200,0,180,22],
              [170,StringCommmand,"And hopes the worms heart she can free",None,60,200,0,180,22],
              [170,StringCommmand,"She grants his wish",None,60,200,0,180,22],               
              [170,StringCommmand,"Her wand goes swish!",None,60,200,0,180,22],
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSSpell,630,240,SpellID],
              [100,setTarget,SpellID,90,170],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [170,StringCommmand,"\"In the jungle a lady you might see\"",None,60,200,0,180,22],

              [100,setTarget,FairyID,860,400],
              [0,addStartButton],
              ]
              
CS2Commands = [
              [170,StringCommmand,"Going Underground",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,300,JakeID],
              [0,setTarget,JakeID,150,450],
              [170,StringCommmand,"As he swings through the trees it occurs to the worm",None,60,200,0,180,22],
              [170,StringCommmand,"That the jungle's a great place for some",None,60,200,0,180,22],
              [170,StringCommmand,"But it's really not great for invertibrates",None,60,200,0,180,22],   
              [170,StringCommmand,"Who are lonely and looking for fun",None,60,200,0,180,22],              [75,VerticalTab,15],
              [170,StringCommmand,"\"I wish I could try another scene for a while",None,60,200,0,180,22],        
              [170,StringCommmand,"varieties something I crave\"",None,60,200,0,180,22], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,550,420],              
              [170,StringCommmand,"Then in whisks the fairy and Olli is wary",None,60,200,0,180,22],   
              [0,SpawnObject,WorldTypes.CSSpell,560,440,SpellID],
              [75,setTarget,SpellID,190,470],  
              [0,MoveObject,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [125,setTarget,JakeID,-200,0],              
              [170,StringCommmand,"Because now he's lost deep in a cave!",None,60,200,0,180,22],               
              [50,VerticalTab,15],
              [50,setTarget,FairyID,860,400],
              [0,addStartButton],
              ]
              
CS3Commands = [
              [170,StringCommmand,"The Play Ground",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,450,JakeID],
              [0,setTarget,JakeID,150,450],
              
              [200,StringCommmand,"The cave was quite fun as a brief interlude",None,60,200,0,180,22],
              [200,StringCommmand,"But panic grips Ollies young soul",None,60,200,0,180,22],              
              [0,SpawnObject,WorldTypes.CSLightBeam,120,-5,LightID],             
              [170,StringCommmand,"He spies a high exit",None,60,200,0,180,22],  
              [200,StringCommmand,"And imediately takes it",None,60,200,0,180,22],   
              [0,setTarget,JakeID,1000,-600],              
              [170,StringCommmand,"And legs it straight out of a hole",None,60,200,0,180,22],
              
              [150,VerticalTab,10], 
              [0,SpawnObject,WorldTypes.CSJake,-300,530,Jake2ID],
              [0,setTarget,Jake2ID,80,535],
              [0,fadeOutForeground,-1],
              [170,StringCommmand,"As he ventures out into the light,",None,60,200,0,180,22],
              [170,StringCommmand,"A beautiful view is in sight,",None,60,200,0,180,22],   
              [170,StringCommmand,"A park with trampolines,",None,60,200,0,180,22],              
              [170,StringCommmand,"Swings and other play things,",None,60,200,0,180,22],  
              [170,StringCommmand,"Ollie thinks it might work out alright",None,60,200,0,180,22],

              [75,VerticalTab,10], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,640,500],   
              [170,StringCommmand,"Then the fairy comes into the park,",None,60,200,0,180,22],
              [170,StringCommmand,"And warns Ollie its not such a lark",None,60,200,0,180,22],   
              [170,StringCommmand,"There are bouncers to bump him",None,60,200,0,180,22],              
              [170,StringCommmand,"And stingers to pierce him",None,60,200,0,180,22],  
              [170,StringCommmand,"And a new stone to find before dark ",None,60,200,0,180,22],
              [50,VerticalTab,10],
              [50,setTarget,FairyID,860,400],
              [50,addStartButton],
              [50,setTarget,Jake2ID,-300,500],
              ]

CS4Commands = [
              [170,StringCommmand,"The Haunted Fun Fair",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,530,JakeID],
              [0,setTarget,JakeID,50,530],

              [170,StringCommmand,"Trampoling was really great fun",None,60,200,0,180,22],
              [170,StringCommmand,"And it was nice spending time in the sun",None,60,200,0,180,22],
              [170,StringCommmand,"But the balls and the wasps",None,60,200,0,180,22],
              [170,StringCommmand,"Made Ollie quite cross",None,60,200,0,180,22],
              [170,StringCommmand,"And now he just wants to go home",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,680,500], 
              [50,VerticalTab,10],    
              [170,StringCommmand,"\"But you have almost completed my quest\"",None,60,200,0,180,22],
              [170,StringCommmand,"Says the fairy whilst they take a rest.",None,60,200,0,180,22],
              [170,StringCommmand,"\"There is just one more stone",None,60,200,0,180,22],
              [170,StringCommmand,"Till my amulet's done",None,60,200,0,180,22],
              [170,StringCommmand,"Then my personal help I'll invest\"",None,60,200,0,180,22],
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSSpell,690,520,SpellID],
              [100,setTarget,SpellID,70,560],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [50,VerticalTab,10],
              [170,StringCommmand,"Ollie appears in a haunted fun fair",None,60,200,0,180,22],
              [170,StringCommmand,"Where old rides and balloons don't play fair",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSJake,-300,530,Jake2ID],
              [0,setTarget,Jake2ID,80,535],
              [0,SpawnObject,WorldTypes.fireBall,900,400,Jake2ID],
              [0,SpawnObject,WorldTypes.fireBall,400,-100,Jake2ID],
              [170,StringCommmand,"Strange lights and odd sounds",None,60,200,0,180,22],
              [170,StringCommmand,"Make Ollie's little heart pound ",None,60,200,0,180,22],
              [170,StringCommmand,"But he goes where no other worm dares.",None,60,200,0,180,22],
              [50,VerticalTab,10],  
              [50,setTarget,FairyID,860,400],
              [0,setTarget,Jake2ID,900,500],
              [0,addStartButton],
              ]

CS5Commands = [
              [170,StringCommmand,"The end of the tail?",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,70,JakeID],
              [0,setTarget,JakeID,50,140], 
              [0,SpawnObject,WorldTypes.CSFairy,900,350,FairyID],
              [0,setTarget,FairyID,680,280], 
              [170,StringCommmand,"\"You finally made it! I am really quite proud\",",None,60,200,0,180,22],
              [170,StringCommmand,"Says the fairy with a nod and a smile.",None,60,200,0,180,22],
              [170,StringCommmand,"\"You bettered the best",None,60,200,0,180,22],
              [170,StringCommmand,"That you thought you could do",None,60,200,0,180,22],              
              [170,StringCommmand,"And you managed it all in good style",None,60,200,0,180,22],                
              [50,VerticalTab,10],  
              [170,StringCommmand,"\"But my amulet's not yet completely unlocked",None,60,200,0,180,22],
              [170,StringCommmand,"I need you to find all the parts",None,60,200,0,180,22],
              [170,StringCommmand,"When you've found them return",None,60,200,0,180,22],
              [170,StringCommmand,"And I'll gladly fulfill",None,60,200,0,180,22],
              [170,StringCommmand,"The desire which is deep in your heart\"",None,60,200,0,180,22],
              [50,setTarget,FairyID,860,400],
              [0,setTarget,JakeID,900,500],
              [0,fadeOutForeground,-1],
              [0,addStartButton],
              ]
              
CS6Commands = [
              [170,StringCommmand,"The end of the tail?",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,100,JakeID],
              [0,setTarget,JakeID,50,150], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,680,230], 
              [170,StringCommmand,"\"You finally made it! You must be relieved\",",None,60,200,0,180,22],
              [170,StringCommmand,"Says the fairy who looks really pleased",None,60,200,0,180,22],
              [170,StringCommmand,"\"You bettered the best",None,60,200,0,180,22],
              [170,StringCommmand,"That you thought you could do",None,60,200,0,180,22],              
              [170,StringCommmand,"And this chance to excel you have siezed",None,60,200,0,180,22],  
              [0,SpawnObject,WorldTypes.CSAmulet,-200,250,amuletID],              
              [0,setTarget,amuletID,20,260],
              [50,VerticalTab,10], 
              [170,StringCommmand,"\"My amulet's power you completely unlocked",None,60,200,0,180,22],
              [170,StringCommmand,"And I make it a present to you",None,60,200,0,180,22],
              [170,StringCommmand,"Once you've had a quick rest",None,60,200,0,180,22],
              [170,StringCommmand,"I have one more quest",None,60,200,0,180,22],
              [170,StringCommmand,"That only a skilled worm can do.\"",None,60,200,0,180,22],        

              [50,VerticalTab,10],  
              [170,StringCommmand,"\"Gold coins you have seen in the places you've been",None,60,200,0,180,22],
              [170,StringCommmand,"As you've raced in great haste through each stage",None,60,200,0,180,22],
              [170,StringCommmand,"Collect every gold coin",None,60,200,0,180,22],
              [170,StringCommmand,"And your friends you'll rejoin",None,60,200,0,180,22],
              [170,StringCommmand,"For I'll whisk you straight back to your cage\"",None,60,200,0,180,22],  
              [50,setTarget,FairyID,860,400],
              [0,setTarget,JakeID,900,500],
              [0,addStartButton],
              ]   

CS7Commands = [
              [170,StringCommmand,"The end of the tail",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,100,JakeID],
              [0,setTarget,JakeID,50,150], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,680,240], 
              [170,StringCommmand,"\"You finally made it! I am ever so proud\",",None,60,200,0,180,22],
              [170,StringCommmand,"Says the fairy in a tone of respect.",None,60,200,0,180,22],
              [170,StringCommmand,"\"You bettered the best",None,60,200,0,180,22],
              [170,StringCommmand,"That you thought you could do",None,60,200,0,180,22],              
              [170,StringCommmand,"And passed all of my difficult tests",None,60,200,0,180,22],                
              [50,VerticalTab,10],  
              [0,SpawnObject,WorldTypes.CSAmulet,-200,250,amuletID],
              [0,setTarget,amuletID,20,260],
              [170,StringCommmand,"\"My amulet's power you completely unlocked",None,60,200,0,180,22],
              [170,StringCommmand,"And I make it a present to you",None,60,200,0,180,22],
              [170,StringCommmand,"Please look after it always",None,60,200,0,180,22],
              [170,StringCommmand,"For you never can know",None,60,200,0,180,22],
              [170,StringCommmand,"When you might have a new quest to do\"",None,60,200,0,180,22],
              [50,VerticalTab,10],  
              [170,StringCommmand,"\"You found all the gold that the fairies had lost",None,60,200,0,180,22],
              [120,StringCommmand,"And returned it to us in fine style.",None,60,200,0,180,22],
              [120,StringCommmand,"Now I am so happy,",None,60,200,0,180,22],
              [120,StringCommmand,"And you can go home,",None,60,200,0,180,22],
              [120,StringCommmand,"To spend time with your friends... for a while!\"",None,60,200,0,180,22],     
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSFireWorks,300,600,fireWorksID],
              [0,SpawnObject,WorldTypes.CSSpell,690,260,SpellID],
              [100,setTarget,SpellID,70,170],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],              
              [50,VerticalTab,10],  
              [0,addEndButton],
              ]
              
CS8Commands = [
              [170,StringCommmand,"The Journey Home",None,60,200,0,180,36],
              [0,VerticalTab,30],
              [170,StringCommmand,"At the end of the cellar of dread,",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSJake,-100,120,JakeID],
              [0,setTarget,JakeID,50,130],
              [170,StringCommmand,"With relief and frustrution he weeps.",None,60,200,0,180,22],
              [170,StringCommmand,"\"I wish I could go straight home to my bed,",None,60,200,0,180,22],
              [170,StringCommmand,"I'm tired and in need of some sleep\"",None,60,200,0,180,22],
              [75,VerticalTab,15],
              [0,SpawnObject,WorldTypes.CSFairy,900,170,FairyID],
              [0,setTarget,FairyID,660,220],
              [170,StringCommmand,"The fairy appears and takes pity on Ollie,",None,60,200,0,180,22],
              [170,StringCommmand,"He has learnt the error of his ways.",None,60,200,0,180,22],
              [170,StringCommmand,"Life may be quite boring but it is a mistake,",None,60,200,0,180,22],              
              [170,StringCommmand,"To want great excitement each day.",None,60,200,0,180,22],
              [75,VerticalTab,15],
              [120,StringCommmand,"She agrees once again to grant him his wish,",None,60,200,0,180,22],         
              [170,StringCommmand,"And send him back home to his cage.",None,60,200,0,180,22],
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSSpell,660,240,SpellID],
              [100,setTarget,SpellID,90,170],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [170,StringCommmand,"But first he will have to work back through the worlds,",None,60,200,0,180,22],
              [170,StringCommmand,"That first led him here to this place.",None,60,200,0,180,22],
              [100,setTarget,FairyID,860,400],
              [0,addStartButton],
              ]
              
lower1 = ['JunkPile01','JunkPile02','JunkPile01']
upper1 = ['OverheadLight01','OverheadLight02','OverheadLight02']
lower2 = ['FB1','FB2','Stalagmite01']
upper2 = ['FB3','FB4','Stalactite01']
lower3 = ['Shrub02','Trampoline113','Shrub01','Shrub01']
upper3 = ['Cloud01','Cloud02','Cloud01','Cloud02']
lower4 = ['JungleScenery01','JungleScenery02','JungleScenery01','JungleScenery02']
upper4 = ['Vine01','Vine02','Vine01','Vine02']

#data for cut scene.  Made up of:Name of Backdrop,title, pointer to scene instructions
cutScene1 = ["Backdrop4",50,CS1Commands,"cutScene",lower4,upper4]

cutScene2 = ["Backdrop2",50,CS2Commands,"cutScene",lower2,upper2]

cutScene3 = ["Backdrop03",50,CS3Commands,"cutScene",lower3,upper3]

cutScene4 = ["Backdrop1",50,CS4Commands,"cutScene",lower1,upper1]
cutScene5 = ["Backdrop1",50,CS5Commands,"cutScene",lower1,upper1]
cutScene6 = ["Backdrop1",50,CS6Commands,"cutScene",lower1,upper1]
cutScene7 = ["Backdrop1",50,CS7Commands,"cutScene",lower1,upper1]
cutScene8 = ["Backdrop03",50,CS8Commands,"cutScene",lower3,upper3]

#list of all cutscenes
cutsceneList = [None,cutScene1,cutScene2,cutScene3,cutScene4,cutScene5,cutScene6,cutScene7,cutScene8]

print("cutsceneList English")