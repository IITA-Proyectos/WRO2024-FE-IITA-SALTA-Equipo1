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
    