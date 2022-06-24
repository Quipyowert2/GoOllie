# Copyright (C) 2009 Charlie Dog Games

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

import WorldTypes
import animationSets

StringCommmand,LinearCommmand,VerticalTab,SpawnObject,MoveObject,setTarget,fadeOutForeground,addStartButton,setAnimation,addEndButton = list(range(10))
JakeID,FairyID,SpellID,Jake2ID,LightID,amuletID,fireWorksID = list(range(7))

#command is structured: time delay till next command, command type, body
CS1Commands = [
              [170,StringCommmand,"Ollie visita la jungla",None,200,20,20,180,36],
              [0,VerticalTab,30],
              [170,StringCommmand,"Ollie el Oligoqueto",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSJake,-100,120,JakeID],
              [0,setTarget,JakeID,50,130],
              [170,StringCommmand,"Anda siempre muy coqueto",None,60,200,0,180,22],
              [170,StringCommmand,"Y quiere conocer una se\xF1orita",None,60,200,0,180,22],
              [170,StringCommmand,"Con un coraz\xF3n que de amor palpita",None,60,200,0,180,22],
              [170,StringCommmand,"\"\xA1Ay, desear\xEDa poder conocerla!\"",None,60,200,0,180,22],
              [75,VerticalTab,15],
              [0,SpawnObject,WorldTypes.CSFairy,900,170,FairyID],
              [0,setTarget,FairyID,620,220],
              [170,StringCommmand,"Un hada escucha los pedidos del gusano",None,60,200,0,180,22],
              [170,StringCommmand,"Y espera que su coraz\xF3n pueda ser liberado",None,60,200,0,180,22],
              [170,StringCommmand,"Con su varita le cumple el deseo",None,60,200,0,180,22],
              [170,StringCommmand,"R\xE1pidamente, en un parpadeo.",None,60,200,0,180,22],
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSSpell,630,240,SpellID],
              [100,setTarget,SpellID,90,170],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [170,StringCommmand,"\"Quiz\xE1s en la jungla encuentres a tu ser amado\"",None,60,200,0,180,22],

              [100,setTarget,FairyID,860,400],
              [0,addStartButton],
              ]
              
CS2Commands = [
              [170,StringCommmand,"Yendo bajo tierra",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,300,JakeID],
              [0,setTarget,JakeID,150,450],
              [170,StringCommmand,"Mientras se balancea por los \xE1rboles se le ocurre al gusano",None,60,200,0,180,22],
              [170,StringCommmand,"Que la jungla no es un lugar al que est\xE9 acostumbrado",None,60,200,0,180,22],
              [170,StringCommmand,"Y no es el sitio ideal para un invertebrado",None,60,200,0,180,22],
              [170,StringCommmand,"Que est\xE1 solo y busca diversi\xF3n",None,60,200,0,180,22],              [75,VerticalTab,15],
              [170,StringCommmand,"\"Me gustar\xEDa ir a otro lugar en esta ocasi\xF3n",None,60,200,0,180,22],        
              [170,StringCommmand,"Algo variado y con m\xE1s acci\xF3n\"",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,550,420],              
              [170,StringCommmand,"De pronto aparece el hada y Ollie est\xE1 preocupado",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSSpell,560,440,SpellID],
              [75,setTarget,SpellID,190,470],  
              [0,MoveObject,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [125,setTarget,JakeID,-200,0],              
              [170,StringCommmand,"\xA1Porque ahora en una cueva se encuentra varado!",None,60,200,0,180,22],
              [50,VerticalTab,15],
              [50,setTarget,FairyID,860,400],
              [0,addStartButton],
              ]
              
CS3Commands = [
              [170,StringCommmand,"El patio",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,450,JakeID],
              [0,setTarget,JakeID,150,450],
              
              [200,StringCommmand,"La cueva fue divertida como breve interludio",None,60,200,0,180,22],
              [200,StringCommmand,"Pero ahora el p\xE1nico se apodera de su joven alma",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSLightBeam,120,-5,LightID],             
              [170,StringCommmand,"Ve una salida",None,60,200,0,180,22],
              [200,StringCommmand,"Y la toma en seguida",None,60,200,0,180,22],   
              [0,setTarget,JakeID,1000,-600],              
              [170,StringCommmand,"Y sale del agujero ya con m\xE1s calma",None,60,200,0,180,22],
              
              [150,VerticalTab,10], 
              [0,SpawnObject,WorldTypes.CSJake,-300,530,Jake2ID],
              [0,setTarget,Jake2ID,80,535],
              [0,fadeOutForeground,-1],
              [170,StringCommmand,"Cuando por fin del pozo logra salir,",None,60,200,0,180,22],
              [170,StringCommmand,"Un bello paisaje puede distinguir,",None,60,200,0,180,22],
              [170,StringCommmand,"Un parque con trampolines llama su atenci\xF3n,",None,60,200,0,180,22],
              [170,StringCommmand,"Tambi\xE9n hay hamacas para gran diversi\xF3n,",None,60,200,0,180,22],
              [170,StringCommmand,"Nada mejor podr\xEDa pedir",None,60,200,0,180,22],

              [75,VerticalTab,10], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,640,500],   
              [170,StringCommmand,"Entonces en el parque aparece el hada,",None,60,200,0,180,22],
              [170,StringCommmand,"Y le informa a Ollie que las apariencias enga\xF1an",None,60,200,0,180,22],
              [170,StringCommmand,"Hay pelotas para golpearlo",None,60,200,0,180,22],
              [170,StringCommmand,"E insectos para picarlo",None,60,200,0,180,22],
              [170,StringCommmand,"Y una nueva piedra deber\xE1 ser hallada",None,60,200,0,180,22],
              [50,VerticalTab,10],
              [50,setTarget,FairyID,860,400],
              [50,addStartButton],
              [50,setTarget,Jake2ID,-300,500],
              ]

CS4Commands = [
              [170,StringCommmand,"La feria de atracciones embrujada",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,530,JakeID],
              [0,setTarget,JakeID,50,530],

              [170,StringCommmand,"Fue divertido en el trampol\xEDn saltar",None,60,200,0,180,22],
              [170,StringCommmand,"Y muy bello bajo el sol poder estar",None,60,200,0,180,22],
              [170,StringCommmand,"Pero las pelotas y las avispas",None,60,200,0,180,22],
              [170,StringCommmand,"Hacen que Ollie ya no resista",None,60,200,0,180,22],
              [170,StringCommmand,"Y ahora se quiere ir a su hogar",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,680,500], 
              [50,VerticalTab,10],    
              [170,StringCommmand,"\"Pero casi completas mi aventura\"",None,60,200,0,180,22],
              [170,StringCommmand,"Dice el hada sin demasiada premura.",None,60,200,0,180,22],
              [170,StringCommmand,"\"Queda solo una piedra por hallar",None,60,200,0,180,22],
              [170,StringCommmand,"Para mi amuleto completar",None,60,200,0,180,22],
              [170,StringCommmand,"Y luego mi ayuda tendr\xE1s por segura.\"",None,60,200,0,180,22],
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSSpell,690,520,SpellID],
              [100,setTarget,SpellID,70,560],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [50,VerticalTab,10],
              [170,StringCommmand,"Ollie aparece en una feria de atracciones embrujada",None,60,200,0,180,22],
              [170,StringCommmand,"En donde los juegos y los globos no lo quieren nada",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSJake,-300,530,Jake2ID],
              [0,setTarget,Jake2ID,80,535],
              [0,SpawnObject,WorldTypes.fireBall,900,400,Jake2ID],
              [0,SpawnObject,WorldTypes.fireBall,400,-100,Jake2ID],
              [170,StringCommmand,"Luces raras y extra\xF1os ruidos",None,60,200,0,180,22],
              [170,StringCommmand,"Hacen que Ollie de agudos aullidos",None,60,200,0,180,22],
              [170,StringCommmand,"Pero va hacia donde ning\xFAn gusano antes se animaba.",None,60,200,0,180,22],
              [50,VerticalTab,10],  
              [50,setTarget,FairyID,860,400],
              [0,setTarget,Jake2ID,900,500],
              [0,addStartButton],
              ]

CS5Commands = [
              [170,StringCommmand,"\xBFFinal de la historia?",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,70,JakeID],
              [0,setTarget,JakeID,50,140], 
              [0,SpawnObject,WorldTypes.CSFairy,900,350,FairyID],
              [0,setTarget,FairyID,680,280], 
              [170,StringCommmand,"\"\xA1Finalmente lo lograste! Estoy orgullosa\",",None,60,200,0,180,22],
              [170,StringCommmand,"Dice el hada con una sonrisa cari\xF1osa.",None,60,200,0,180,22],
              [170,StringCommmand,"\"Lo hiciste mucho mejor",None,60,200,0,180,22],
              [170,StringCommmand,"De lo que cre\xEDas posible",None,60,200,0,180,22],
              [170,StringCommmand,"Y lo hiciste todo con una actitud hermosa.",None,60,200,0,180,22],
              [50,VerticalTab,10],  
              [170,StringCommmand,"\"Pero mi amuleto no est\xE1 completo",None,60,200,0,180,22],
              [170,StringCommmand,"Necesito que todas las partes encuentres",None,60,200,0,180,22],
              [170,StringCommmand,"Cuando las tengas vuelve conmigo",None,60,200,0,180,22],
              [170,StringCommmand,"Y muy contenta cumplir\xE9",None,60,200,0,180,22],
              [170,StringCommmand,"Tu deseo r\xE1pidamente\"",None,60,200,0,180,22],
              [50,setTarget,FairyID,860,400],
              [0,setTarget,JakeID,900,500],
              [0,fadeOutForeground,-1],
              [0,addStartButton],
              ]
              
CS6Commands = [
              [170,StringCommmand,"\xBFFinal de la historia?",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,100,JakeID],
              [0,setTarget,JakeID,50,150], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,680,230], 
              [170,StringCommmand,"\"\xA1Finalmente lo lograste! Debes estar aliviado\",",None,60,200,0,180,22],
              [170,StringCommmand,"Le dice el hada contenta al gusano",None,60,200,0,180,22],
              [170,StringCommmand,"\"Lo hiciste mucho mejor",None,60,200,0,180,22],
              [170,StringCommmand,"De lo que cre\xEDas posible",None,60,200,0,180,22],
              [170,StringCommmand,"Y esta oportunidad de sobresalir has aprovechado",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSAmulet,-200,250,amuletID],              
              [0,setTarget,amuletID,20,260],
              [50,VerticalTab,10], 
              [170,StringCommmand,"\"Has descubierto todo el poder de mi amuleto",None,60,200,0,180,22],
              [170,StringCommmand,"Y te lo ofrezco como gentil regalo",None,60,200,0,180,22],
              [170,StringCommmand,"Cuando descansado ya est\xE9s",None,60,200,0,180,22],
              [170,StringCommmand,"Algo te pedir\xE9",None,60,200,0,180,22],
              [170,StringCommmand,"Que solo un gusano h\xE1bil llevar\xEDa a cabo.\"",None,60,200,0,180,22],

              [50,VerticalTab,10],  
              [170,StringCommmand,"\"En los lugares por donde estuviste varias monedas de oro tu viste",None,60,200,0,180,22],
              [170,StringCommmand,"Mientras corr\xEDs con prisa por cada nivel.",None,60,200,0,180,22],
              [170,StringCommmand,"Junta todas las monedas",None,60,200,0,180,22],
              [170,StringCommmand,"Y ya no tendr\xE1s problemas",None,60,200,0,180,22],
              [170,StringCommmand,"Con tus amigos te har\xE9 volver\"",None,60,200,0,180,22],
              [50,setTarget,FairyID,860,400],
              [0,setTarget,JakeID,900,500],
              [0,addStartButton],
              ]   

CS7Commands = [
              [170,StringCommmand,"\xBFFinal de la historia?",None,60,200,0,180,36],
              [0,SpawnObject,WorldTypes.CSJake,-300,100,JakeID],
              [0,setTarget,JakeID,50,150], 
              [0,SpawnObject,WorldTypes.CSFairy,900,300,FairyID],
              [0,setTarget,FairyID,680,240], 
              [170,StringCommmand,"\"\xA1Finalmente lo lograste! Estoy orgullosa\",",None,60,200,0,180,22],
              [170,StringCommmand,"Dice el hada con tono respetuoso.",None,60,200,0,180,22],
              [170,StringCommmand,"\"Lo hiciste mucho mejor",None,60,200,0,180,22],
              [170,StringCommmand,"De lo que cre\xEDas posible",None,60,200,0,180,22],
              [170,StringCommmand,"Y de mis dif\xEDciles pruebas saliste airoso",None,60,200,0,180,22],
              [50,VerticalTab,10],  
              [0,SpawnObject,WorldTypes.CSAmulet,-200,250,amuletID],
              [0,setTarget,amuletID,20,260],
              [170,StringCommmand,"\"Has descubierto todo el poder de mi amuleto",None,60,200,0,180,22],
              [170,StringCommmand,"Y te lo ofrezco como gentil regalo",None,60,200,0,180,22],
              [170,StringCommmand,"Por favor, cu\xEDdalo siempre",None,60,200,0,180,22],
              [170,StringCommmand,"Porque qui\E9n sabe",None,60,200,0,180,22],
              [170,StringCommmand,"Si en otra aventura te ver\xE1s enredado\"",None,60,200,0,180,22],
              [50,VerticalTab,10],  
              [170,StringCommmand,"\"Has hallado todas las monedas que las hadas perdimos",None,60,200,0,180,22],
              [120,StringCommmand,"Y nos las devolviste con gran encanto.",None,60,200,0,180,22],
              [120,StringCommmand,"Ahora estoy contenta,",None,60,200,0,180,22],
              [120,StringCommmand,"Y puedes volver a casa,",None,60,200,0,180,22],
              [120,StringCommmand,"Para pasar tiempo con amigos... \xA1pero eso no durar\xE1 tanto!\"",None,60,200,0,180,22],
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
              [170,StringCommmand,"El viaje a casa",None,60,200,0,180,36],
              [0,VerticalTab,30],
              [170,StringCommmand,"Al final del s\xF3tano temible,",None,60,200,0,180,22],
              [0,SpawnObject,WorldTypes.CSJake,-100,120,JakeID],
              [0,setTarget,JakeID,50,130],
              [170,StringCommmand,"Con alivio y frustraci\xF3n Ollie llora.",None,60,200,0,180,22],
              [170,StringCommmand,"\"Desear\xED estar en mi cama apacible,",None,60,200,0,180,22],
              [170,StringCommmand,"De dormir tranquilo no veo la hora\"",None,60,200,0,180,22],
              [75,VerticalTab,15],
              [0,SpawnObject,WorldTypes.CSFairy,900,170,FairyID],
              [0,setTarget,FairyID,660,220],
              [170,StringCommmand,"El hada aparece y se apiada de Ollie,",None,60,200,0,180,22],
              [170,StringCommmand,"Ya se ha dado cuenta del error cometido.",None,60,200,0,180,22],
              [170,StringCommmand,"Por m\xE1s que por la vida se ande aburrido,",None,60,200,0,180,22],
              [170,StringCommmand,"Querer aventuras todo el tiempo no tiene sentido.",None,60,200,0,180,22],
              [75,VerticalTab,15],
              [120,StringCommmand,"Nuevamente accede a cumplirle el deseo,",None,60,200,0,180,22],
              [170,StringCommmand,"Y al hogar de su jaula lo vuelve a env\xEDar.",None,60,200,0,180,22],
              [30,setAnimation,FairyID,animationSets.fairy_spell],
              [0,setAnimation,FairyID,animationSets.fairy_move],
              [0,SpawnObject,WorldTypes.CSSpell,660,240,SpellID],
              [100,setTarget,SpellID,90,170],
              [0,MoveObject,JakeID,-200,0],
              [100,setTarget,JakeID,-200,0],
              [0,fadeOutForeground,-1],
              [170,StringCommmand,"Pero primero tendr\xE1 que pasar por todos los mundos,",None,60,200,0,180,22],
              [170,StringCommmand,"que lo trajeron hasta aqu\xED en primer lugar.",None,60,200,0,180,22],
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
cutScene1 = ["Backdrop4",50,CS1Commands,"cutScene.ogg",lower4,upper4]

cutScene2 = ["Backdrop2",50,CS2Commands,"cutScene.ogg",lower2,upper2]

cutScene3 = ["Backdrop03",50,CS3Commands,"cutScene.ogg",lower3,upper3]

cutScene4 = ["Backdrop1",50,CS4Commands,"cutScene.ogg",lower1,upper1]
cutScene5 = ["Backdrop1",50,CS5Commands,"cutScene.ogg",lower1,upper1]
cutScene6 = ["Backdrop1",50,CS6Commands,"cutScene.ogg",lower1,upper1]
cutScene7 = ["Backdrop1",50,CS7Commands,"cutScene.ogg",lower1,upper1]
cutScene8 = ["Backdrop03",50,CS8Commands,"cutScene.ogg",lower3,upper3]

#list of all cutscenes
cutsceneList = [None,cutScene1,cutScene2,cutScene3,cutScene4,cutScene5,cutScene6,cutScene7,cutScene8]
