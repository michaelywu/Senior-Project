import ADXL345
import time
import math
adxl345 = ADXL345.ADXL345()
xyzAngle = [0,0,0]
DELAY = 0.01
while True:
    time.sleep(DELAY)# 10 milliseconds sleep
    xyzData = adxl345.getData()
    xyzAngle[0] = math.degrees((math.atan2(xyzData[1],xyzData[2])+math.pi)) - 180
    xyzAngle[1] = math.degrees((math.atan2(xyzData[0],xyzData[2])+math.pi)) - 180

    print "X: ",xyzAngle[0]
    print "Y: ",xyzAngle[1]
