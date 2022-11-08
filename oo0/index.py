import time
import random
import sys

personajes = [
  {
      "nombre" : "Alfonse",
      "salud" : 5,
      "puntos" : 0,
      "ataque" : 2,
      "defensa" : False,
      "combo" : False
  },
  {
      "nombre" : "Shrek",
      "salud" : 12,
      "puntos" : 0,
      "ataque" : 1,
      "defensa" : False,
      "combo" : False
  }
]

con = True;

def desc(char):
  print("\n*** Descripcion de ",char["nombre"],"***");
  for inf in char:
    print(inf," : ",char[inf]);
  print("*** ********************* ***\n");

def compM(char):
  if (char["salud"] < 1):
    print(char["nombre"],"ha sido derrotado!💔");
    print("+++++ EL COMBATE A ACABADO +++++");
    return True;
  else:
    return False;

def atacar(char1,char2):
  print("\n *** "+char1["nombre"],"ataca!")
  
  if(char2["defensa"]):
    print("\nataque inefectivo!❌");
    print(char2["nombre"]," se ha perdido su defensa💥");
    char2["defensa"] = False;
  else:
    print("\nataque efectivo!💥")
    print("♥️ -",(char1["ataque"])," de salud para ",char2["nombre"]);
    char2["salud"]-=char1["ataque"];

    con = compM(char2);

    if not con:
      print("+1 puntos para ",char1["nombre"]);
      char1["puntos"]+=1;
      if char1["puntos"] >= 3: 
        char1["combo"] = True;
      else: 
        char1["combo"] = False;
    
def defender(char):
  char["defensa"] = True;
  print("\n",char["nombre"], " se defiende!🛡️");

def combo(char1,char2):
  if (char1["combo"]):
    print("\n~~~❇️COMBO❕❇️~~~");
    #time.sleep(2);
    atacar(char1,char2);
    #time.sleep(1);
    atacar(char1,char2);
    defender(char1);
    char1["puntos"] -= 3;
    if char1["puntos"] >= 3: 
      char1["combo"] = True;
    else: 
      char1["combo"] = False;
    return True;
  else:
    print("\n--❌ ",char1["nombre"]," intenta hacer y combo, pero necesita almenos 3 puntosy resbala!❌--");
    return False;

def autoAct(char1,char2):
    if char1["salud"] > 0:
        if char1["combo"]: opc = ["1","1","2","3"];
        else: opc = ["1","1","2"];
    sel = random.randint(0,len(opc)-1);
    sel = opc[sel];
    if sel == "1":
        atacar(char1,char2);
    elif sel == "2":
        defender(char1);
    elif sel == "3":
        combo(char1,char2);

def select(chars):
  
  i=0;
  for char in chars: i+=1;print(i,". ",char["nombre"]);

select(personajes);

def jugar(char1,char2):
  print("++++ INICIA EL COMBATE ++++");
  print("+++ ",pj["char1"]," ⚔️ ",en["char2"]," +++\n");

  turno = 0;
  while(not compM(char1) and not compM(char2)):
    turno+=1;
    #time.sleep(2);
    print("\nturno",turno,": ( "+char1["nombre"],char1["salud"]," hp) ⚔️ (",char2["nombre"],char2["salud"]," hp)")
    consulta = "0";
    while True:
      if pj["combo"]: cmb = "✅"; 
      else: cmb = "❌";
      consulta = input(
          "\nAcciones: \n"
          " 1. descripcion mia🆔\n"
          " 2. descripcion del enemigo🆔\n"
          " 3. atacar🗡️\n"
          " 4. defender🛡️\n"
          " 5. combo ("+(cmb)+")💫\n"
          " Seleciones una de las opciones: "
          );
      if consulta == "1":
        desc(pj);
      elif consulta == "2": 
        desc(en);
      elif consulta == "3":
        atacar(pj,en);
        break;
      elif consulta == "4":
        defender(pj);
        break
      elif consulta == "5":
        combo(pj,en);
        break
    
    #time.sleep(2);
    autoAct(en,pj);

  print("+++++++++++GAME OVER++++++++++++");