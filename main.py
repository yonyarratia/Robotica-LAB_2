import time
import Sensores
import Acciones
import posicion
import globales
#-------------RUN TIME--------------------
#eL carro se va mover en un tiempo determinado, pero este puede evadir obstaculos,
#además vamos a sacar la posición actual del robot mediante los encoders
tareaT = False
tiempo = 10
dt=0.1

tareaT = False

if globales.start_time == 0:
    globales.start_time = time.time()

tiempo = 20

while not tareaT:
    Sensores.pizarrasensorre()
    posicion.pos(Sensores.getPizarraSen(3),Sensores.getPizarraSen(4))
    if Sensores.getPizarraSen(1) >= tiempo:
        Acciones.pizarraComportamiento(1)
        tareaT = True
    elif Sensores.getPizarraSen(2) != 0:
        Acciones.pizarraComportamiento(3)   
    else:
        Acciones.pizarraComportamiento(2)
    time.sleep(dt)


print("FIN")          