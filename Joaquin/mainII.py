import board
import busio
import RPi.GPIO as GPIO
import time
from BasicMove import avanzar, retroceder, neutro, inicializar_esc, girar
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
    def Angle(self,angulo):
        girar(angulo)
#-----------------INICIO-------------------------

robot = Robot()
neutro()
time.sleep(5)
robot.direccion_centrar()
direccion = 0
lados = 0
robot.control_direccion = 0
time.sleep(1)

"""#-----------------DEFINIR DIRECCION-----------------
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
"""    
x=0
while True:
    if robot.ultrasonico_frontal()<=40:
        robot.Angle(90)
        
    else:
        robot.adelante(145)    
    
        
        
            
  
  
  
  
  
  
  
  

robot.detener()
GPIO.cleanup()            