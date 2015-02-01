#This library is to interace with the ADXL345 for Raspberry Pi B+
#Written By: Michael Wu

import smbus

bus = smbus.SMBus(1) # the value '1' is for raspberry pi B/B+
                        # other versions may need to change the value
                        
#I2C Address for ADXL345
I2C_ADDRESS = 0x53

#ADXL345 Registers
DATAX0 = 0x32#register locations of the x, y, z data
DATAX1 = 0x33
DATAY0 = 0x34
DATAY1 = 0x35
DATAZ0 = 0x36
DATAZ1 = 0x37

DATA_FORMAT = 0x31 #controls presentation of data
FULL_RES = 0x08
POWER_CTL = 0x2D #R/W register
BW_RATE = 0x2C
#g range setting
G_2 = 0
G_4 = 1
G_8 = 2
G_16 = 3

#Scale Factor
LSB_4_MG = (4 * 0.001) # taken from data sheet

#Bandwidth Rate
HZ_3200 = 0x0F
HZ_1600 = 0x0E
HZ_800 = 0x0D
HZ_400 = 0x0C
HZ_200 = 0x0B
HZ_100 = 0x0A #taken from datasheet
HZ_50 = 0x09
HZ_25 = 0x08
HZ_12_5 = 0x07
HZ_6_25 = 0x06

#Measure Value
MEASURE_VAL = 0x08
class ADXL345:

    address = None
    tempXData = None
    tempYData = None
    tempZData = None
    def __init__(self, address = 0x53):
        self.address = address
        self.dataFormat(G_4)# sets to full res with 4g range
        self.setBandwidth(HZ_100)
        self.beginMeasure()

    def dataFormat(self, rangeSetting): # sets to full res with 4 g range
        dataFormatByte = FULL_RES | G_4 #will maintain 4mg/LSB

        bus.write_byte_data(self.address, DATA_FORMAT, dataFormatByte)
    def setBandwidth(self, bandwidth):
        bus.write_byte_data(self.address, BW_RATE, bandwidth)
    def beginMeasure(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE_VAL)#being measure
    def printRawData(self): #prints the raw data with 2's complement
        X_DATA = self.getXData()
        Y_DATA = self.getYData()
        Z_DATA = self.getZData()
        
        print"Raw ADXL345 Data: "
        print "x: ",X_DATA
        print "y: ",Y_DATA
        print "z: ",Z_DATA
        print LSB_4_MG
    def printData(self): # prints out the converted data
        X_DATA = self.getXData() * LSB_4_MG
        Y_DATA = self.getYData() * LSB_4_MG
        Z_DATA = self.getZData() * LSB_4_MG #sensitivity

        print "ADXL345 Data (g)"
        print "x: ",X_DATA
        print "y: ",Y_DATA
        print "z: ",Z_DATA
    def getData(self): # gets raw data and converts and returns it in list format
        data = []
        data.append(self.getXData() * LSB_4_MG)#x axis data
        data.append(self.getYData() * LSB_4_MG)#x axis data
        data.append(self.getZData() * LSB_4_MG)#x axis data

        return data
    def getXData(self):
        try:
            X_VALUE_L = bus.read_byte_data(self.address,DATAX0)
            X_VALUE_H = bus.read_byte_data(self.address,DATAX1)
            combinedData = (X_VALUE_H <<8) | X_VALUE_L
            tempXData = combinedData
        except:
            combinedData = tempXData
            
        if(combinedData & (1<< (16 -1))) != 0: #if sign bit is '1'
                combinedData = combinedData - (1<<16) #determine neg value

        return combinedData
    def getYData(self):
        try:
            Y_VALUE_L = bus.read_byte_data(self.address,DATAY0)
            Y_VALUE_H = bus.read_byte_data(self.address,DATAY1)
            combinedData = (Y_VALUE_H <<8) | Y_VALUE_L
            tempYData = combinedData
        except:
            combinedData = tempYData
            
        if(combinedData & (1<< (16 -1))) != 0: #if sign bit is '1'
                combinedData = combinedData - (1<<16) #determine neg value

        return combinedData
    def getZData(self):
        try:
            Z_VALUE_L = bus.read_byte_data(self.address,DATAZ0)
            Z_VALUE_H = bus.read_byte_data(self.address,DATAZ1)
            combinedData = (Z_VALUE_H <<8) | Z_VALUE_L
            tempZData = combinedData
        except:
            combinedData = tempZData
            
        if(combinedData & (1<< (16 -1))) != 0: #if sign bit is '1'
                combinedData = combinedData - (1<<16) #determine neg value

        return combinedData
#acc = ADXL345()
#print acc.getData()
