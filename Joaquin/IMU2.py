"""
Lectura de datos en angulos de euler con el sensor Adafruit BNO055
Ejemplo con el eje z-yaw
"""

import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    print("giroscopio: {}".format(sensor.euler))
    time.sleep(1)










