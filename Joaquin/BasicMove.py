"""
Manejo del ESC-Electronic Speed Controller del Latrax Traxxas con placa PCA9685

Pasos:
1. Encender ESC Latrax Traxxas. Boton Azul
2. El LED del ESC titilara en verde esperando a recibir señal
3. La funcion inicializar_ESC manda un rango de anchos de pulso para que el ESC empiece a recibir señal pwm de la PCA9685
4. El ESC ya puede recibir señales PWM de la placa

reversa : 0-100 grados
neutro: 120 grados
adelante: 140-180 grados

"""

import time
from adafruit_servokit import ServoKit

MIN_RANGO = 1000
MAX_RANGO = 2000

avance_minimo = 0

kit = ServoKit(channels=16)
kit.frequency = 50

esc = kit.servo[2]
servo = kit.servo[0]
                        
#kit.servo[2].set_pulse_width_range(0, 4096)
servo.set_pulse_width_range(1000, 2000)
esc.set_pulse_width_range(MIN_RANGO, MAX_RANGO)

def avanzar(velocidad):
    
        esc.angle = velocidad
        
        
def retroceder(tiempo, velocidad):
    if velocidad < 0 or velocidad > 170:
        print("Error: La variable no esta comprendida entre 0 y 99")
    else:
        esc.angle = velocidad
        time.sleep(tiempo)
        
def neutro():
    esc.angle = 120
    
    
def inicializar_esc():
    for i in range(0,120):
        esc.angle = i
        time.sleep(0.2)
        if i == 120:
            neutro()

"""
inicializar_esc() 
while True:
    esc.angle = int(input("angle: "))
      
   """     





