import time
import random
import math


class personaje: # clase para la construccion de los personajes
    def __init__(self, nombre, salud, ataque, defensa, velocidad):
        self.nombre = nombre
        self.saludMax = salud #maxima salud posible
        self.salud = salud #salud actual
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.bebida = 3
        self.proteccion = False # escudo
        self.puntos = 0 # energia, una mecanicade intercambio

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
                print("+1 puntos para %s" % (self.nombre))
                self.puntos += 1

    def desc(self): # para obtener la info de un personaje
        print("\n*** Descripcion de %s ***" % (self.nombre))
        print(
            """
        hp: %s
        Ataque: %s 
        Defensa: %s
        Velocidad: %s
        Proteccion: %s
        Puntos: %s
        """
            % (self.salud, self.ataque, self.defensa, self.velocidad, self.proteccion, self.puntos)
        )
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

    def curar(self):
        if (self.bebida > 0):
            print("\n *** %s se bebe un té... refrescante! +35hp🍵" % (self.nombre))
            self.salud += 35
            self.bebida -= 1
            if self.salud > self.saludMax: self.salud = self.saludMax # si su salud actual es mayor al maximo, que se iguales 
        else:
            print("\n *** ❌ %s no tiene bebidas! ❌ ***" % (self.nombre))

    def hCombo(self, oponente):
        if (self.puntos >= 3):
            print("\n~~~❇️COMBO❕❇️~~~")
            # time.sleep(2);
            self.atacar(oponente)
            # time.sleep(1);
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
        if sel == "1":
            self.atacar(oponente)
        elif sel == "2":
            self.protect()
        elif sel == "3":
            self.hCombo(oponente)
        elif sel == "4":
            self.boost()
        elif sel == "5":
            self.curar()


personajes = [
    personaje("Alfonse", 80, 2, 5, 10),
    personaje("Shrek", 120, 1, 4, 9)
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


select(personajes)


def luchar(jugador: personaje, oponente: personaje):
    print("++++ INICIA EL COMBATE ++++")
    print("++++ %s ⚔️  %s  ++++\n" % (jugador.nombre, oponente.nombre))
    turno = 0
    jugador.desc()
    oponente.desc()

    while jugador.salud > 0 and oponente.salud > 0:
        turno += 1
        print(
            "\n▶️  turno %s : ( %s %s hp) ⚔️ (  %s %s hp) ▶️"
            % (turno, jugador.nombre,jugador.salud,oponente.nombre, oponente.salud)
            )
        if jugador.velocidad >= oponente.velocidad:
            jugador.autoAct(oponente)
            oponente.autoAct(jugador)
        else:
            oponente.autoAct(jugador)
            jugador.autoAct(oponente)
            
    jugador.desc()
    oponente.desc()

    """
    turno = 0
    while (not compM(jugador) and not compM(oponente)):
        turno += 1
        # time.sleep(2);
        print(
              "\nturno %s : ( %s %s hp) ⚔️ (  %s %s hp)"
              % (turno, jugador.nombre,jugador.salud,oponente.nombre, oponente.salud)
              )
        consulta = "0"
        while True:
            if jugador.combo:
                cmb = "✅"
            else:
                cmb = "❌"
            consulta = input(
                "\nAcciones: \n"
                " 1. descripcion mia🆔\n"
                " 2. descripcion del enemigo🆔\n"
                " 3. atacar🗡️\n"
                " 4. protect🛡️\n"
                " 5. combo ("+(cmb)+")💫\n"
                " Seleciones una de las opciones: "
            )
            if consulta == "1":
                desc(jugador)
            elif consulta == "2":
                desc(en)
            elif consulta == "3":
                atacar(jugador, en)
                break
            elif consulta == "4":
                protect(jugador)
                break
            elif consulta == "5":
                combo(jugador, en)
                break

        # time.sleep(2);
        autoAct(en, jugador)

    print("+++++++++++GAME OVER++++++++++++")
    """

luchar(personajes[0], personajes[1])
