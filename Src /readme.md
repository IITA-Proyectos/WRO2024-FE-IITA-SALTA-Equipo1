En este archivo se pueden ver tres codigos:

# CÓDIGO 1

BasicMove.py

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

# CODIGO 2

main.py

import board
import busio
import RPi.GPIO as GPIO
import time
from BasicMove import avanzar, retroceder, neutro, inicializar_esc
from adafruit_servokit import ServoKit
from ultrasonic import Ultrasonico
import adafruit_bno055

class Robot():
    def __init__(self):
        #Inicializar IMU BNO055
        i2c = busio.I2C(board.SCL, board.SDA)
        self.imu = adafruit_bno055.BNO055_I2C(i2c)
        
        #Inicializar sensores de distancia
        self.sensor_frontal = Ultrasonico(25,22)
        self.sensor_izquierdo = Ultrasonico(10,7)
        self.sensor_derecho = Ultrasonico(8,27)
        
        #Inicializar servo 
        self.kit = ServoKit(channels=16)
        self.servo = self.kit.servo[0]
        self.servo.set_pulse_width_range(1000, 2000)
        
        self.control_direccion = None #Variable para seleccionar el sensor ultrasonico interno

    def get_heading(self):
        return self.imu.euler[0] if self.imu.euler else None #Devuelve el angulo del Yaw del imu
    
    def ultrasonico_elegido(self):#Retorna la distancia medida por el sensor ultrasonico seleccionado, 1=derecho
        if self.control_direccion == 1:
            return int(self.sensor_derecho.medir_distancia())
        #elif self.control_direccion ==-1:
        else:
            return int(self.sensor_izquierdo.medir_distancia())
        
    def ultrasonico_frontal(self):
        return int(self.sensor_frontal.medir_distancia())
        
    def direccion_centrar(self): #Centra la direccion 
        self.servo.angle=90
        time.sleep(1)
        
    def direccion_controlar(self, angulo_deseado, kp, velocidad): #Controla la direccion del robot ajustando el angulo del servo basado en el yaw actual y el deseado
        angulo_actual =float(self.get_heading())
        if angulo_actual > 180 and angulo_actual < 360:
            angulo_actual = angulo_actual - 360
        if angulo_actual is None:
            return
        error = angulo_deseado - angulo_actual
        correccion = int(error * kp) * -1
        
        nuevo_angulo = 90 + correccion
        nuevo_angulo = max(0, min(180, nuevo_angulo))
        self.servo.angle = nuevo_angulo
        self.adelante(velocidad)
        print("correccion: ",correccion ,"angulo actual: ", angulo_actual, nuevo_angulo)
        
        
    def adelante(self, velocidad):
        avanzar(velocidad)
    def detener(self):
        neutro()
#-----------------INICIO-------------------------

robot = Robot()
robot.direccion_centrar()
direccion = 0
lados = 0
robot.control_direccion = 0
time.sleep(5)

#-----------------DEFINIR DIRECCION-----------------
while robot.ultrasonico_frontal()>=45:
    robot.direccion_controlar(direccion, 1, 145)
    if robot.ultrasonico_frontal() <=45:
        robot.detener()
        break

if robot.sensor_izquierdo.medir_distancia() <90:
    robot.control_direccion = -1
    direccion_controlar(270, 1, 145)
    time.sleep(2)
    robot.detener()
else:
    robot.control_direccion = 1
    direccion_controlar(90, 1, 145)
    time.sleep(2)
    robot.detener()
    
#-----------HACER LAS VUELTAS-------------------------
while True:
    if robot.control_direccion == -1:
        direccion -= 90
        direccion = direccion%360
    else:
        direccion +=90
        direccion = direccion%360
    while robot.ultrasonico_elegido()<90 and robot.ultrasonico_frontal()>45:
        robot.direccion_controlar(direccion, 1, 145)
    lados = lados + 1
    
    if lados >= 12:
        break
    
        
robot.detener()
GPIO.cleanup()    

# CÓDIGO 3
 
 ultrasonic.py

 import RPi.GPIO as GPIO
import time

"""
frente:
izq = Ultrasonico(10,7)
der = Ultrasonico(8,27)
front = Ultrasonico(25,22)
"""

class Ultrasonico:

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    def __init__(self, trigger_pin, echo_pin):
        
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.1)
        
    def medir_distancia(self):
        
        GPIO.output(self.trigger_pin, True)
        
        time.sleep(0.000001)
        GPIO.output(self.trigger_pin, False)
        
        start_time = time.time()
        stop_time = time.time()
        
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
            
        while GPIO.input(self.echo_pin)==1:
            stop_time = time.time()
            
        elapsed_time = stop_time - start_time
        distancia = (elapsed_time * 34600)/2
        return distancia
"""  
try:
    while True:
        izq = Ultrasonico(10,7)
        der = Ultrasonico(8,27)
        front = Ultrasonico(25,22)
        distance = front.medir_distancia()
        print(distance, " cm")
        time.sleep(.5)
        
except KeyboardInterrupt:
     GPIO.cleanup()
     """

