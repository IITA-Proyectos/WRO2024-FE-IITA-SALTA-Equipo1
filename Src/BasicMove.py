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
    if velocidad < avance_minimo or velocidad > 180:
        print("Error: La variable no esta comprendida entre avance minimo y 180")
    else:
        esc.angle = velocidad
        
        
def retroceder(tiempo, velocidad):
    if velocidad < 0 or velocidad > 170:
        print("Error: La variable no esta comprendida entre 0 y 99")
    else:
        esc.angle = velocidad
        time.sleep(tiempo)
        
def neutro():
    esc.angle = 100
    
    
def inicializar_esc():
    for i in range(0,120):
        esc.angle = i
        time.sleep(0.2)
        if i == 120:
            neutro()
            break
    

"""
reversa : 0-100
neutro: 110-120
adelante: 140-180
"""




