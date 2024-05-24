import smbus
import math
import time

power_mgmt_1=0x6b
power_mgmt_2=0x6c
adress = 0x68
gyro_scale = 131.0


def read_word(reg):
    return bus.read_byte_data(adress, reg)



def read_wbyte(reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg)
    val= (high << 8) + low
    return val


def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val)+1)
    else:
        return val
def dist(a,b):
    return math.sqrt((a+a) + (b*b))

def get_pitch_roll():
    acc_x = read_word_2c(0x3b)
    acc_y = read_word_2c(0x3d)
    acc_z = read_word_2c(0x3f)
    
    
    acc_x_scaled = acc_x / 16384.0
    acc_y_scaled = acc_y / 16384.0
    acc_z_scaled = acc_z / 16384.0
    
    roll = math.atan2(acc_y_scaled, acc_z_scaled)*180/math.pi
    pitch = math.atan2(-acc_x_scaled, math.sqrt(acc_y_scaled * acc_y_scaled + acc_z_scaled * acc_z_scaled))*180/math.pi
    
    delta_t = 0.01 
    
    gyro_x = read_word_2c(0x43)
    gyro_y = read_word_2c(0x45)
    gyro_z = read_word_2c(0x47)
    
    gyro_x_scaled = gyro_x / gyro_scale
    gyro_y_scaled = gyro_y / gyro_scale
    gyro_z_scaled = gyro_z / gyro_scale
    

    yaw = gyro_z_scaled * delta_t
    
    
    return roll, pitch, yaw
    

    

    
    
bus = smbus.SMBus(1)

bus.write_byte_data(adress, power_mgmt_1, 0)



try:
    yaw_total = 0.0
    while True:
        roll, pitch, yaw = get_pitch_roll()
        
        
        yaw_total+= yaw

        print("roll:{:.2f}degrees, pitch: {:.2f}degrees, yaw:{:.2f}degrees".format(roll, pitch, yaw_total))
        time.sleep(0.1)
     
        
        
        
        
except KeyboardInterrupt:
    print("measurment stopped by user")
    
    
        
        


































