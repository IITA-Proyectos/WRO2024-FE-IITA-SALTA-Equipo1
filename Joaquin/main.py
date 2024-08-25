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
            return self.sensor_derecho.medir_distancia()
        #elif self.control_direccion ==-1:
        else:
            return self.sensor_izquierda.medir_distancia()
        
    def ultrasonico_frontal(self):
        return self.sensor_frontal.medir_distancia()
        
    def direccion_centrar(self): #Centra la direccion 
        self.servo.angle=90 
        
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
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
kit = ServoKit(channels=16)
kp = 10
yaw_offset = sensor.euler[0]

inicializar_esc()

def sensor_elegido(sentido):
    if sentido == 180: #izquierda
        return distance_izq
    elif sentido == 0: #derecha
        return distance_der
    
def get_yaw():
    yaw = sensor.euler[0]
    if yaw is not None:
        return yaw - yaw_offset
    return 0

def estabilizar_auto(target_yaw):
    while True:
        current_yaw = get_yaw()
        error = target_yaw - current_yaw
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360
        control_signal = kp * error
        
        control_signal = max(min(control_signal, 90), -90)
        servo_angle = 90 - control_signal
        kit.servo[servo_channel].angle = servo_angle
        


#-----------------INICIO-------------------------
robot = Robot()

robot.servo.angle = 0
time.sleep(1)
robot.direccion_centrar()

sentido = 0
neutro()
#time.sleep(2)
inicializar_esc()
#neutro()
time.sleep(5)

"""while True:
    front = Ultrasonico(25,22)
    sensor_izquierdo = Ultrasonico(10,7)
    sensor_derecho = Ultrasonico(8,27)
    
    distance = front.medir_distancia()
    distance_der = sensor_derecho.medir_distancia()
    distance_izq = sensor_izquierdo.medir_distancia()
    print(distance)
    if distance >40:
        #robot.adelante(145)
        if distance < 40:
            robot.detener()
            if distance_izq > distance_der:
                robot.detener()
                sentido = 180
                break
            else:
                sentido = 0
                break
    break

sensor_elegido(sentido)"""
"""

while True:
    front = Ultrasonico(25,22)
    sensor_izquierdo = Ultrasonico(10,7)
    sensor_derecho = Ultrasonico(8,27)
    robot.adelante(150)
        #sensor_elegido()
    if sensor_izquierdo.medir_distancia() > 45:
        giro = 270
        estabilizar_auto(giro)
    else:
        giro = 90
        estabilizar_auro(giro)
"""
direccion = 0
while True:
    front = Ultrasonico(25,22)
    sensor_izquierdo = Ultrasonico(10,7)
    sensor_derecho = Ultrasonico(8,27)
    robot.adelante(150)
    distancia_frontal = front.medir_distancia()
    distancia_izquierda = sensor_izquierdo.medir_distancia
    
    if distancia_frontal<40:
        direccion -= 90
        direccion = direccion%360
        
    else:
        direccion += 90
        direccion = direccion%360
        
    while int(distancia_izquierda) < 45:
        estabilizar_auto(direccion)
    

        """if distance_izq > 45:
            robot.servo.angle = 180
            print("pared")
    
        else:
            robot.servo.angle = 90
            print("adelante")"""
            
        """if distance_der > 45:
            robot.servo.angle = 180
            print("pared der")"""        
        
        """else:
            robot.servo.angle=90
            print("adelante")"""
        #robot.adelante(160)
            
            
            
            
        
        
        
        
        
        
    """while True:
        #front = Ultrasonico(25,22)
        #sensor_derecho = Ultrasonico(8,27)
        robot.adelante(160)
        sensor_izquierdo = Ultrasonico(10,7)
        
        direccion = 0
        
        #distance = front.medir_distancia()
        distance_izq = sensor_izquierdo.medir_distancia()
        #distance_der = sensor_derecho.medir_distancia()
        while distance > 45:
            robot.adelante(150)
            if distance <= 45:
                robot.detener()
                if distance_izq > distance_der:
                    direccion = 1
                    break
                else:
                    direccion = 0
                    break
        if direccion == 1
            if distance_izq > 45:
                robot.servo.angle = 180
            
            else:
                robot.servo.angle = 90
        
        print(distance_izq)
        #print(distance, " cm")"""
        
        
        
"""except KeyboardInterrupt:
     GPIO.cleanup()"""

#-----------------DEFINIR DIRECCION-----------------
"""
print("Definir direccion")
while True:
    while robot.sensor_frontal.medir_distancia()<45:
        robot.direccion_controlar(direccion, 1, 145)
        print("recto 1")
        break 
    if robot.sensor_izquierdo.medir_distancia() <90:
        robot.control_direccion = -1
        robot.direccion_controlar(270, 1, 145)
        robot.detener()
        robot.direccion_centrar()
    print("evaluando direccion ...")
    if robot.sensor_izquierdo.medir_distancia() <90:
        robot.control_direccion = -1
        robot.direccion_controlar(90, 1, 145)
        time.sleep(2)
        robot.detener()
        robot.direccion_centrar()
        break
    
else:
    robot.control_direccion = 1
    robot.direccion_controlar(90, 1, 145)
    time.sleep(2)
    robot.detener()
print("Direccion definida")
#-----------HACER LAS VUELTAS-------------------------
print("Inicio vueltas")
while True:
    if robot.control_direccion == -1:
        direccion -= 90
        direccion = direccion%360
    else:
        direccion += 90
        direccion = direccion%360
    while robot.ultrasonico_elegido()<90 and robot.ultrasonico_frontal()>45:
        robot.direccion_controlar(direccion, 1, 145)
    if lados >= 12:
        break
print("Fin vueltas")
        
robot.detener()
GPIO.cleanup()  
"""