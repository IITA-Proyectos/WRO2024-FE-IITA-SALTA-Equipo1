

# Documentacion del MPU6050

Mediante el giroscopio y el acelerometro buscamos realizar un movimiento preciso con el robot 

# MPU6050
 El MPU6050 es un módulo de sensor que combina un acelerómetro de 3 ejes y un giroscopio de 3 ejes en un solo chip. Es ampliamente utilizado en aplicaciones de control de movimiento y detección de posición debido a su precisión y facilidad de integración con microcontroladores como Arduino y Raspberry Pi.
 
## Características 
- **Acelerómetro de 3 ejes**: Mide la aceleración en las direcciones X, Y y Z. 
-  **Giroscopio de 3 ejes**: Mide la velocidad angular en las direcciones X, Y y Z


# Uso de Librerías

### `smbus`

La librería `smbus` se utiliza para la comunicación I2C con el MPU6050. Permite leer y escribir datos en el sensor.

### `time`

La librería `time` se utiliza para manejar retrasos y cronometrajes en el código. En este ejemplo, se utiliza `time.sleep(1)` para crear un retraso de un segundo entre las lecturas de los datos del sensor.

### `math`

La librería `math` se utiliza para realizar cálculos matemáticos complejos. Aunque no se usa explícitamente en el ejemplo básico, puede ser útil para calcular ángulos, magnitudes y otras operaciones matemáticas relacionadas con los datos del acelerómetro y giroscopio..

#Repositorios en los que basamos el codigo:


[m-rtijn](https://github.com/m-rtijn/mpu6050/blob/master/README.rst)
[adafruit_CircuitPython_MPU6050](https://github.com/adafruit/Adafruit_CircuitPython_MPU6050)
[ [MPU6050-MotionTracking](https://github.com/Edubgr/MPU6050-MotionTracking)](https://github.com/Edubgr/MPU6050-MotionTracking)
