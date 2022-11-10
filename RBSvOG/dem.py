import os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

columna = []; fila = [];

cols = 7; rows = 7;

x = -1; y = -1;

fx = 4; fy = 4;

fs = 0;

for i in range(cols):
  fila = [];
  for o in range(rows):
    fila.append("🟦");
  columna.append(fila)

dir = 5;
columna[fy][fx] = "🍒";

while(dir!="0"):
  columna[y][x] = "🟡";
  for i in range(cols):
    print(" ");
    for o in range(rows):
      print(columna[i-1][o-1],end="");
  
  print("\n \n"+
    "w. arriba\n"+
    "s. abajo\n"+
    "a. izquierda\n"+
    "d. derecha\n"+
    "0.salir"
  );
  if(x==fx and y ==fy):
    fs+=1; print("comiste");
    break;
  dir = input("\ndireccion: ");
  columna[y][x] = "🟦"
  if dir == "w":
    y-=1;
  elif dir == "s":
    y+=1;
  elif dir == "a":
    x-=1;
  elif dir == "d":
    x+=1;
  clear()
  

if fs == 0:
  print("\n\n*** no conseguiste ninguna fruta 😥 ***")
else:
  print("\n\n*** ¡ FELICIDADES! 🥳 ***")