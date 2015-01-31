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
#g range setting
2_G = 0
4_G = 1
8_G = 2
16_G = 3

#Scale Factor
4_MG_LSB = 4 * (1/1000)

MEASURE_VAL = 0x08
class ADXL345:

    address = None
    tempXData = None
    tempYData = None
    tempZData = None
    def __init__(self, address = 0x53)
        self.address = address
        self.dataFormat(4_G)# sets to full res with 4g range
        self.beginMeasure()

    def dataFormat(self, rangeSetting) # sets to full res with 4 g range
        dataFormatByte = FULL_RES | 4_G #will maintain 4mg/LSB

        bus.write_byte_data(self.address, DATA_FORMAT, dataFormatByte)

    def beginMeasure(self)
        bus.write_byte_data(self.address, POWER_CTL, MEASURE_VAL)#being measure
    def printRawData(self) #prints the raw data with 2's complement
        X_DATA = self.getXData()
        Y_DATA = self.getYData()
        Z_DATA = self.getZData()
        
        print"Raw ADXL345 Data: "
        print "x: ",X_DATA
        print "y: ",Y_DATA
        print "z: ",Z_DATA
    def printData(self) # prints out the converted data
        X_DATA = self.getXData() * 4_MG_LSB
        Y_DATA = self.getYData() * 4_MG_LSB
        Z_DATA = self.getZData() * 4_MG_LSB #sensitivity

        print "ADXL345 Data (g)"
        print "x: ",X_DATA
        print "y: ",Y_DATA
        print "z: ",Z_DATA
    def getData(self) # gets raw data and converts and returns it in list format
        data = []
        data.append(self.getXData() * 4_MG_LSB)#x axis data
        data.append(self.getYData() * 4_MG_LSB)#x axis data
        data.append(self.getZData() * 4_MG_LSB)#x axis data

        return data
    def getXData(self)
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
    def getYData(self)
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
    def getZData(self)
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
