import Sensores
import math
import time
import PID

import serial


# Conexión serial con ESP32
esp = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)   
esp.write(b"START\n")

pizarra = [0, 0, 0, 0]  # [tiempo, distancia, RPM_der, RPM_izq]

# === Variables de posición ===
x = 0.0
y = 0.0
theta = 0.0  # Orientación en radianes
#=================CONFIGURACION DEL PID===============
pid_izq = PID.PID(1.2, 0.01, 0.05)
pid_der = PID.PID(1.2, 0.01, 0.05)
dt = 0.1  # Intervalo de muestreo en segundos

#----------------DIMENSIONES DEL CARRO----------------
h=114 #Distancia de las ruedas mm
R=9.5 #Radio de la llanta mm  

def run(VT):
  global x, y, theta
  W=0 #Velocidad angular del robot,rad/s
  VR = VT+(W*h/2) #velocidad lineal del motor derecho mm/s
  VL = VT-(W*h/2) #velocidad lineal del motor izquierdo mm/s
  RPM_izq = Sensores.getPizarraSen(4)
  RPM_der = Sensores.getPizarraSen(3)

  VR_encoder=RPM_der * (2 * math.pi * R) / 60
  VL_encoder=RPM_izq * (2 * math.pi * R) / 60

  salida_pid_izq = pid_izq.compute(VL, VR_encoder, dt)
  salida_pid_der = pid_der.compute(VR, VR_encoder, dt)
  pwm_out_izq = max(0, min(255, int(salida_pid_izq))) #Lo escalanos para el PWM del esp y lo eviamos
  pwm_out_der = max(0, min(255, int(salida_pid_der)))
  
  VT_encoder = (VR_encoder + VL_encoder) / 2
  omega_encoder = (VR_encoder - VL_encoder) / h
    # Actualizar posición y orientación
  x = x + VT_encoder * math.cos(theta) * dt
  y = y + VT_encoder * math.sin(theta) * dt
  theta = theta + omega_encoder * dt
  time.sleep(dt)
  print(f"[POS] x={x:.3f} m, y={y:.3f} m, θ={math.degrees(theta):.2f}°")


def run_angle(VT, W):
  global x, y, theta
  VR = VT+(W*h/2) #velocidad lineal del motor derecho mm/s
  VL = VT-(W*h/2) #velocidad lineal del motor izquierdo mm/s
  RPM_izq = Sensores.getPizarraSen(4)
  RPM_der = Sensores.getPizarraSen(3)

  VR_encoder=RPM_der * (2 * math.pi * R) / 60
  VL_encoder=RPM_izq * (2 * math.pi * R) / 60

  salida_pid_izq = pid_izq.compute(VL, VR_encoder, dt)
  salida_pid_der = pid_der.compute(VR, VR_encoder, dt)
  pwm_out_izq = max(0, min(255, int(salida_pid_izq))) #Lo escalanos para el PWM del esp y lo eviamos
  pwm_out_der = max(0, min(255, int(salida_pid_der)))
  VT_encoder = (VR_encoder + VL_encoder) / 2
  omega_encoder = (VR_encoder - VL_encoder) / h
    # Actualizar posición y orientación
  x = x + VT_encoder * math.cos(theta) * dt
  y = y + VT_encoder * math.sin(theta) * dt
  theta = theta + omega_encoder * dt
  time.sleep(dt)
  print(f"[POS] x={x:.3f} m, y={y:.3f} m, θ={math.degrees(theta):.2f}°")
def motores(VT, W):
    VR_MAX=50
    VL_MAX=50
    VR = VT+(W*h/2) #velocidad lineal del motor derecho mm/s
    VL = VT-(W*h/2) #velocidad lineal del motor izquierdo mm/s
    PWM_R=VR*255/VR_MAX
    PWM_L=VL*255/VL_MAX
    #ENVIAR PWM
    # Enviar por serial
    comando = f"{PWM_L},{PWM_R}\n"
    esp.write(comando.encode())
    

def compor1():
    print("PARAR")
    #run(0)
    motores(0,0)

def compor2():
    print("AVANZAR")
    #run(15)
    motores(20,0)

def compor3():
    print("GIRAR")
    #run_angle(15, 6)
    motores(8,5)

def pizarraComportamiento(tarea):
    if tarea == 1:
        compor1()
    elif tarea == 2:
        compor2()
    elif tarea == 3:
        compor3()