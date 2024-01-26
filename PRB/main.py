import random
import math

class item: # items que un personaje puede usar
    # el item por defecto es un té
    def __init__(self,nombre="té🍵", cantidad=3, dialogo=("\n --- té refrescante que cura 35hp🍵"), efectos=["hp"], valores=[35]):
        self.id = " "
        self.usuario = " "
        self.nombre = nombre
        self.cantidad = cantidad
        self.dialogo = dialogo
        self.efectos = efectos
        self.valores = valores
    def usar(self):
        print("     *** %s uso %s!"%(self.usuario,self.nombre))
        for efect in self.efectos:
            textE = ("        %s: "%efect)
            if self.valores[self.efectos.index(efect)] >= 0: textE += " +"
            textE+= str(self.valores[self.efectos.index(efect)])
            print(textE)
        self.cantidad-=1
        return [self.efectos,self.valores]
            

            

class personaje: # clase para la construccion de los personajes

    def __init__(self, nombre, salud, ataque, defensa, velocidad, bolsa=["cancelar",item()]):
        self.id = " "
        self.nombre = nombre
        self.saludMax = salud #maxima salud posible
        self.salud = salud #salud actual
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.bolsa = bolsa
        self.bebida = 3
        self.proteccion = False # escudo
        self.puntos = 0 # energia, una mecanica de intercambio

    def atacar(self, oponente):
        print("\n *** %s ataca!" % (self.nombre))

        if (oponente.proteccion): # el ataqque es efectivo si el enemigo no se proteje
            print("\nataque inefectivo!❌")
            print("%s se ha protegido💥" % (oponente.nombre))
            oponente.proteccion = False
        else:
            multip = random.randint(85,115)/100
            dagno = math.ceil(multip*(20*(self.ataque/oponente.defensa)))
            print("\nataque efectivo!💥")
            print("♥️ -%s de salud para %s (atk: %s||multip: %s)" % (dagno, oponente.nombre,self.ataque,multip))
            oponente.salud -= dagno

            con = compM(oponente)

            if not con and random.randint(0,10) >= 3:
                print("➕1️ puntos para %s" % (self.nombre))
                self.puntos += 1

    def desc(self): # para obtener la info de un personaje
        desc = """
hp: %s
Ataque: %s 
Defensa: %s
Velocidad: %s
Proteccion: %s
Puntos: %s
Bolsa: 
"""% (self.salud, self.ataque, self.defensa, self.velocidad, self.proteccion, self.puntos)
        for item in self.bolsa:
            if item != "cancelar": desc+="  -- %s. %s x%s \n"%(self.bolsa.index(item),item.nombre,item.cantidad)
        print("\n*** Descripcion de %s ***" % (self.nombre))    
        print(desc)
        print("*** ********************* ***\n")

    def protect(self): 
        self.proteccion = True
        print("\n *** %s se proteje!🛡️" % (self.nombre))

    def boost(self): # aumenta el poder del personaje
        if (self.puntos >= 1):
            print("\n *** %s medita... la meditacion aumenta su poder!⬆️" %
                  (self.nombre))
            print(
                """
                Ataque: +%s 
                Defensa: +%s
                Velocidad: +%s
                """ % (math.ceil(3/self.ataque), math.ceil(3/self.defensa), math.ceil(18/self.velocidad))
            )
            # El aumento es inversamente proporcional al valor actual de la estadistica
            # Se redondea hacia arriba
            self.ataque += math.ceil(3/self.ataque)
            self.defensa += math.ceil(3/self.defensa)
            self.velocidad += math.ceil(18/self.velocidad)
            self.puntos -= 1
        else:
            print(
                "\n *** ❌ %s no tiene energia suficiente para potenciarse ❌ ***\n" % (self.nombre))

    def uBolsa(self,rand=False):
        if len(self.bolsa) > 1:
            continuar = True
            print("\n *** bolsa de %s 🎒"%self.nombre)
            # mostrar items en la mochila
            for item in self.bolsa: 
                if item!="cancelar":print("%s. %s x%s"%(self.bolsa.index(item),item.nombre,item.cantidad))
                else: print("%s. %s "%(self.bolsa.index(item),item))
            if not rand: # seleccion no aleatoria, manual.
                valid = False
                while not valid:
                    sel = input("seleccion: "); 
                    for item in self.bolsa:
                        if str(self.bolsa.index(item)) == sel: 
                            sel = item; valid = True; break
                if sel == "cancelar": continuar = False
            else: # seleccion aleatoria, pude ser cualquer cosa menos cancelar.
                sel = "cancelar"
                while sel == "cancelar": sel = random.choice(self.bolsa)
            if continuar:
                sel.usuario = self.nombre
                uso = sel.usar()
                for efect in uso[0]:
                    if efect == "hp":
                        self.salud += uso[1][uso[0].index(efect)]
                        if self.salud > self.saludMax: self.salud = self.saludMax # si su salud actual es mayor al maximo, que se iguales 
                    elif efect == "atk":
                        self.ataque += uso[1][uso[0].index(efect)]
                    elif efect == "def":
                        self.defensa += uso[1][uso[0].index(efect)]
                    elif efect == "vel":
                        self.velocidad += uso[1][uso[0].index(efect)]
                    elif efect == "pnt":
                        self.puntos += uso[1][uso[0].index(efect)]

                if sel.cantidad <= 0: self.bolsa.remove(sel)
                return True
            else: return False
        else: 
            print("\n *** ❌ %s no tiene objetos! ❌ ***" % (self.nombre))
            return False

    def hCombo(self, oponente):
        if (self.puntos >= 3):
            print("\n~~~❇️COMBO❕❇️~~~")
            self.atacar(oponente)
            self.atacar(oponente)
            self.protect()
            self.puntos -= 3
            return True
        else:
            print(
                "\n *** ❌ %s intenta hacer un combo, pero no tiene energia suficiente!❌ ***" % (self.nombre))
            if (random.randint(0, 10) >= 7): # si un combo no se hace bien, es posible que el usuario se haga daño
                print(" *** %s se hirio a si mismo! -10hp💥" % (self.nombre))
                self.salud -= 10
            return False

    def autoAct(self, oponente):
        # este condicional define las probabilidades de hacer una u otra accion, e imposibilita algunos en determinados casos 
        # cuantas mas veces se repita un valor, mas probable es que caiga
        opc=["1"]
        if self.salud > 0:
            if self.puntos >= 3:
                opc = ["1", "1", "1", "1", "2", "3", "4", "4"]
            elif self.puntos >= 1:
                opc = ["1", "1", "1", "1","2", "2", "3", "4"]
            else:
                opc = ["1", "1", "2"]
            if self.salud<=self.saludMax*3/4: # si tiene menos de 3 cuartos de su salud maxima, podra intentar curarse
                opc.append("5")
            sel = random.choice(opc)  # la accion es aleatoria
            if sel == "1": self.atacar(oponente)
            elif sel == "2": self.protect()
            elif sel == "3": self.hCombo(oponente)
            elif sel == "4": self.boost()
            elif sel == "5": self.uBolsa(True)

    def act(self, oponente):
        if self.salud > 0:
            if self.puntos >= 3:
                cmb = "✅"
                pUp = "✅"
            elif self.puntos >= 1:
                cmb = "❌"
                pUp = "✅"
            else:
                cmb = "❌"
                pUp = "❌"
                
            sel = input(
"""
\nAcciones: 
    1. stats (%s)🆔
    2. stats del oponente (%s)🆔
    3. atacar🗡️
    4. protect🛡️
    5. combo (%s)💫
    6. meditar (%s)🧘
    7. mochila 🎒
    Selecione una de las opciones: """%(self.nombre,oponente.nombre,cmb,pUp)
            ) # Las acciones que devuelven True consumen 1 turno
            if sel == "1": self.desc(); return False
            elif sel == "2": oponente.desc(); return False
            elif sel == "3":self.atacar(oponente) ;return True
            elif sel == "4": self.protect() ;return True
            elif sel == "5": self.hCombo(oponente) ;return True
            elif sel == "6": self.boost() ;return True
            elif sel == "7": return self.uBolsa(False)
            else: return False
        else: return False

personajes = [
    personaje("Alfonse🤖", 80, 2, 5, 10,[
        "cancelar",
        item(cantidad=4),
        item(nombre="piedra filosofal💎",cantidad=1,efectos=["hp","vel","atk","def"],valores=[25,5,5,5])
        ]),
    personaje("Shrek👹", 120, 1, 4, 9,[
        "cancelar",
        item(),
        item(nombre="cebolla🧅", cantidad=2,efectos=["hp","def"],valores=[30,7]),
        item(nombre="caramelo🍬",cantidad=2,efectos=["vel","atk","hp"],valores=[2,1,-5])
        ]),
    personaje("Pablo🐧",50,1,2,5,[
        "cancelar",
        item(),
        item("imaginacion🌈",1,efectos=["hp","atk","def","vel"],valores=[50,50,50,50]),
    ])
]
con = True

def compM(self):
    if (self.salud < 1):
        print(self.nombre, "ha sido derrotado!💔")
        print("+++++ EL COMBATE A ACABADO +++++")
        return True
    else:
        return False

def select(chars:list):
    print("\n*** Selecciona un personaje ***")
    for char in chars: print(chars.index(char), ". ", char.nombre)
    print("*** *********************** ***\n")
    sel = input("seleccion : ")


def luchar(jugador: personaje, oponente: personaje):
    print("\n++++ INICIA EL COMBATE ++++")
    print("++++ %s ⚔️  %s  ++++\n" % (jugador.nombre, oponente.nombre))
    
    turno = 0
    while jugador.salud > 0 and oponente.salud > 0: #bucle principal
        turno += 1
        print(
            "\n▶️  turno %s : (%s %s hp) ⚔️ ( %s %s hp) ▶️"
            % (turno, jugador.nombre,jugador.salud,oponente.nombre, oponente.salud)
            )
        # cambia jugador.act por jugador.autoAct para una batalla automatica
        if jugador.velocidad >= oponente.velocidad:
            #while not jugador.act(oponente): False 
            jugador.autoAct(oponente)
            oponente.autoAct(jugador)
        else:
            oponente.autoAct(jugador)
            jugador.autoAct(oponente)
            #while not jugador.act(oponente): False
        
            
    

#select(personajes)
luchar(personajes[1], personajes[0])
