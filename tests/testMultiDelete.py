#!/usr/bin/python

import os
import sys
import ansVol  as ansVol
import ansPool as ansPool
import ansLog  as ansLog

failedReturn=2
successReturn=0

ansLog.clearlog( "ansibleOut.txt")

print "Delete Volumes and pools"
ansVol.removeallvolumes()
ansPool.removeallpools()

print "Creating Pools"
ansPool.createpool("testa", "raid0", "2")
ansPool.createpool("testb", "raid0", "2")

print "Creating volumes"
ansVol.createvolume("temp1", "testa")    
ansVol.createvolume("temp2", "testa")    
ansVol.createvolume("temp3", "testb")    
ansVol.createvolume("temp4", "testb")    

print "Current volumes"
ansPool.showpools()
ansVol.showvolumes()

if ansPool.checkpools("testa;testb") == -1:
    print "TEST FAILED - Pools don't exist\n"
    sys.exit(failedReturn)
    
if ansVol.checkvolumes("temp1;temp2;temp3;temp4") == -1:
    print "TEST FAILED - Volumes don't exist\n"
    sys.exit(failedReturn)

print "Delete Volumes"
ansVol.removeallvolumes()

print "Delete Pools"
ansPool.removeallpools()

print "Volumes after delete:"
ansPool.showpools()
ansVol.showvolumes()

if ansPool.checkpools("") == -1:
    print "TEST FAILED - Pools exist\n"
    sys.exit(failedReturn)
    
if ansVol.checkvolumes("") == -1:
    print "TEST FAILED - Volumes exist\n"
    sys.exit(failedReturn)

print "TEST PASSED\n"
sys.exit(successReturn)


