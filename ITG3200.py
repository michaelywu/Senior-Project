#ITG-3200 Python library for Raspberry Pi B+
#Written by Michael Wu

import smbus

bus = smbus.SMBus(1)# the value '1' is for raspberry pi b+ 
                    #TODO, change to different numbers
#i2c buss address
I2C_ADDRESS = 0x68

#ITG-3200 Registers (Found on datasheet)
WHO_AM_I = 0x00
SMPLRT_DIV= 0x15
DLPF_FS = 0x16
INT_CFG = 0x17
INT_STATUS = 0x1A
TEMP_OUT_H = 0x1B
TEMP_OUT_L = 0x1C
GYRO_XOUT_H = 0x1D
GYRO_XOUT_L = 0x1E
GYRO_YOUT_H = 0x1F
GYRO_YOUT_L = 0x20
GYRO_ZOUT_H = 0x21
GYRO_ZOUT_L = 0x22
PWR_MGM = 0x3E

#ITG-3200 Constants
INITIAL_RATE = 9 
INITIAL_DLPF = 0x1A
class ITG3200:
    address = None
    
    def __init__(self,address = 0x68):
        self.address = address
        self.setSampleRate(INITIAL_RATE) #1 Khz/10 = 100Hz sampling
        self.DLPF(INITIAL_DLPF) #sets 98 Hz LPF and enables gyro 2000 degress per second range
        
    def setSampleRate(self, rate): # F sample = 1kHz /(rate + 1)
        bus.write_byte_data(self.address,SMPLRT_DIV, rate)
        
    def DLPF(self, value):
        bus.write_byte_data(self.address,DLPF_FS, value)
        
    def getRawData(self): # prints out the raw data already 2's complemented
        X_DATA = self.getXData()
        Y_DATA = self.getYData()
        Z_DATA = self.getZData()
        
        print "x: ",X_DATA
        print "y: ",Y_DATA
        print "z: ",Z_DATA
    
    def getAngularVelocity(self): # prints out the angular velocity
        X_DATA = self.getXData() * (1/14.375)
        Y_DATA = self.getYData() * (1/14.375)
        Z_DATA = self.getZData() * (1/14.375) #sensitivity 
        
        print "x: ",X_DATA
        print "y: ",Y_DATA
        print "z: ",Z_DATA
        
    def getAngularX(self): #returns angular velocity of X
        return self.getXData() * (1/14.375)
    
    def getAngularY(self): #return angular velocity of Y
        return self.getYData() * (1/14.375)

    def getAngularZ(self): #return angular velocity of Z
        return self.getZData() * (1/14.375)
    
    def getXData(self): # data is returned in 16 bit 2's complement
        X_VALUE_H = bus.read_byte_data(self.address, GYRO_XOUT_H)
        X_VALUE_L = bus.read_byte_data(self.address,GYRO_XOUT_L)
        combinedData = (X_VALUE_H <<8) | X_VALUE_L
        
        if(combinedData & (1<< (16 -1))) != 0: #if sign bit is '1'
                combinedData = combinedData - (1<<16) #determine neg value
                
        return combinedData
        
    def getYData(self):
        Y_VALUE_H = bus.read_byte_data(self.address, GYRO_YOUT_H)
        Y_VALUE_L = bus.read_byte_data(self.address,GYRO_YOUT_L)
        combinedData = (Y_VALUE_H <<8) | Y_VALUE_L
        
        if(combinedData & (1<< (16 -1))) != 0: #if sign bit is '1'
                combinedData = combinedData - (1<<16) #determine neg value
                
        return combinedData

    def getZData(self):
        Z_VALUE_H = bus.read_byte_data(self.address, GYRO_ZOUT_H)
        Z_VALUE_L = bus.read_byte_data(self.address,GYRO_ZOUT_L)
        combinedData = (Z_VALUE_H <<8) | Z_VALUE_L
        
        if(combinedData & (1<< (16 -1))) != 0: #if sign bit is '1'
                combinedData = combinedData - (1<<16) #determine neg value
                
        return combinedData

        
