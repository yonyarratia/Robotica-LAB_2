import time
import serial
import globales


# Conexión serial con ESP32
esp = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)
esp.write(b"START\n")

pizarra = [0, 0, 0, 0]  # [tiempo, distancia, RPM_der, RPM_izq]


def s1():
    if globales.start_time == 0:
        pizarra[0] = 0
    pizarra[0] = time.time() - globales.start_time

def s2_s3_s4():
    if esp.in_waiting:
        linea = esp.readline().decode('utf-8').strip()
        if "D:" in linea and "A:" in linea and "B:" in linea:
            try:
                partes = linea.split()
                distancia = int(partes[0].split(":")[1])
                rpma = int(partes[1].split(":")[1])
                rpmb = int(partes[2].split(":")[1])

                # Guardar en pizarra
                pizarra[1] = distancia
                pizarra[2] = rpma
                pizarra[3] = rpmb

                print(f"📡 Recibido -> Distancia: {distancia} | RPMA: {rpma} | RPMB: {rpmb}")

            except Exception as e:
                print("Error al interpretar datos:", e)
        else:
            print("Línea serial no válida:", linea)


def getPizarraSen(x):
    return pizarra[x - 1]

def pizarrasensorre():
    s1()
    s2_s3_s4()
