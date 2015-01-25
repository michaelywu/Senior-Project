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

    def __init__(self, address = 0x53)
        self.address = address
        self.dataFormat(4_G)# sets to full res with 4g range
        self.beginMeasure()

    def dataFormat(self, rangeSetting) # sets to full res with 4 g range
        dataFormatByte = FULL_RES | 4_G #will maintain 4mg/LSB

        bus.write_byte_data(self.address, DATA_FORMAT, dataFormatByte)

   def beginMeasure(self)
       bus.write_byte_data(self.address, POWER_CTL, MEASURE_VAL)#being measure
