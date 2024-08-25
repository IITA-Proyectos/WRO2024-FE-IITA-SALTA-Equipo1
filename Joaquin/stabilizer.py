"""
Estabilizacion del servo de latrax traxxas en 0 grados usando IMU BNO055 y PCA9685 para control
"""
import time
import board
import busio
import adafruit_bno055 
from adafruit_servokit import ServoKit

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
kit = ServoKit(channels=16)

servo_channel = 0
kit.servo[servo_channel].set_pulse_width_range(1000,2000)
kit.servo[servo_channel].actuation_range = 180

kp = 10
yaw_offset = sensor.euler[0]

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
        
       # if abs(error) < 5:
        #    break
        
       
       
    
estabilizar_auto(270)

"""
try:
    while True:
        control_servo(target_yaw)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Terminado")  
"""
"""
def estabilizar_auto():
    yaw=sensor.euler[0]
    if yaw is not None:
        servo_angle = yaw
        angulo_actual = yaw
        servo_angle = max(0, min (180, servo_angle))
        if angulo_actual > 180 and angulo_actual < 360:
            angulo_actual = angulo_actual - 360
        kit.servo[servo_channel].angle = servo_angle
        
        print(f"yaw:{yaw:.2f}, Angule del servo:{servo_angle:.2f}")
    else:
        print("no se pudo leer el yaw")
        
    time.sleep(0.1)
    
while True:
    try:
        #avanzar(145)
        estabilizar_auto()
    except KeyboardInterrupt:
        print("estabilizacion detenida")
"""















