import PID


# === Variables de posición ===
x = 0.0
y = 0.0
theta = 0.0  # Orientación en radianes
#=================CONFIGURACION DEL PID===============
pid_izq = PID(1.2, 0.01, 0.05)
pid_der = PID(1.2, 0.01, 0.05)
dt = 0.1  # Intervalo de muestreo en segundos

     