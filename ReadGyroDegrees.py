import ITG3200
import time
itg3200 = ITG3200.ITG3200()
xyzAngle = [0,0,0]
DELAY = 0.20
while True:
    start = time.time()
    xyzData = itg3200.getData()
    xyzAngle[0] = xyzAngle[0] + (xyzData[0] * DELAY) #converts degrees/sec to degrees
    xyzAngle[1] = xyzAngle[1]+(xyzData[1] * DELAY)
    #xyzAngle[2] = xyzAngle[2] +(xyzData[2] * DELAY)

    print "X: ",xyzAngle[0]
    print "Y: ",xyzAngle[1]
    #print "Z: ",xyzAngle[2]
    while(time.time() - start < DELAY): #busy waiting for delay
        pass#Do nothing
   
"""
start = time.time()
time.sleep(.020)
end = time.time()
print end - start
"""
"""start = time.time()
while(time.time() - start <0.02):
    print("Hey")"""
