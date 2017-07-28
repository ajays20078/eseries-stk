#!/usr/bin/python

import os
import sys
import ansVol  as ansVol
import ansPool as ansPool
import ansLog  as ansLog

failedReturn=2
successReturn=0

raidLevels = ["raid0", "raid1", "raid5", "raid6"] 
driveCount = [    "4",     "4",     "5",     "5"]
i=0
ansLog.clearlog( "ansibleOut.txt")

print "Delete Volumes and pools"
ansVol.removeallvolumes()
ansPool.removeallpools()

for currTest in raidLevels:
    print "******TEST START : %s*******\n" % currTest
    ansPool.showpools()
    ansVol.showvolumes()
    if ansPool.checkpools("") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)
    if ansVol.checkvolumes("") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)

    print "******POOLS CREATED******\n"
    ansPool.createpool("testa", currTest, driveCount[i])
    ansPool.showpools()
    ansVol.showvolumes()
    if ansVol.checkvolumes("") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)
    if ansPool.checkpools("testa") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)

    print "******VOLUMES CREATED******\n"
    ansVol.createvolume("tempb", "testa")    
    ansPool.showpools()
    ansVol.showvolumes()
    if ansPool.checkpools("testa") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)
    if ansVol.checkvolumes("tempb") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)

    print "******VOLUMES REMOVED******\n"
    ansVol.removevolume( "tempb" , "testa")
    ansPool.showpools()
    ansVol.showvolumes()
    if ansVol.checkvolumes("") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)
    if ansPool.checkpools("testa") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)

    print "******POOLS DELETED******\n"
    ansPool.removepool("testa")    
    ansPool.showpools()
    ansVol.showvolumes()
    i+=1
    if ansPool.checkpools("") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)
    if ansVol.checkvolumes("") == -1:
        print "TEST FAILED\n"
        sys.exit(failedReturn)

print "TEST PASSED\n"
sys.exit(successReturn)

