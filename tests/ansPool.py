#!/usr/bin/python

#############################################################
# Helper functions create, delete, and show E-Series storage
# pools via Ansible.  This depends two simple playbooks to 
# control Ansible via it's netapp_e_facts and 
# netapp_e_storagepool modules.
# 
# Other tests may add support for bypassing Ansible, but this
# is meant for testing the Ansible functionality.
#############################################################

import subprocess
import os
import re
import sys
import ansLog as ansLog

debugPrints=0

def removepool( poolName ):
    "Uses ansible to remove a pool from the array:  1 if success, 0 if failed"

    # buffer up Ansible input from reading the facts
    ansibleInput="Removing pool via ansible:\n"
    cmdLine = "ansible-playbook testbooks/netapp_pools.yml -e \""
    cmdLine += "pool_name="
    cmdLine += poolName
    cmdLine += " state=absent\""
    ansibleInput += "Using command: %s" % cmdLine
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        ansibleInput+=line
    retval = p.wait()
    
    # Log ansible output to logfile
    ansLog.logbuffer("ansibleOut.txt", ansibleInput)
    
    # Look for success, return 1 if found
    ansibleList = ansibleInput.split(os.linesep)
    for i in ansibleList:
        if i.find('changed=1') != -1:
            return 1
    
    # Didn't find it.  Return -1
    return -1
    
def createpool( poolName, raidLevel, driveCnt):
    "Uses ansible to remove a pool from the array:  1 if success, 0 if failed"

    # buffer up Ansible input from reading the facts
    ansibleInput="Creating pool Via Ansible:\n"
    cmdLine = "ansible-playbook testbooks/netapp_pools.yml -e \""
    cmdLine += "pool_name="
    cmdLine += poolName
    cmdLine += " raid_level="
    cmdLine += raidLevel
    cmdLine += " drive_count="
    cmdLine += driveCnt
    cmdLine += " state=present\""
    ansibleInput += "Using command: %s" % cmdLine
    p = subprocess.Popen(cmdLine, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        ansibleInput+=line
    retval = p.wait()
    
    # Log ansible output to logfile
    ansLog.logbuffer("ansibleOut.txt", ansibleInput)
    
    # Look for success, return 1 if found
    ansibleList = ansibleInput.split(os.linesep)
    for i in ansibleList:
        if i.find('changed=1') != -1:
            return 1
    
    # Didn't find it.  Return -1
    return -1
    
def showpools ( ):
    "Debug function to show pools on the array"

    tempBuffer=getpools( )
    print "Pools are: "
    for i in tempBuffer.split(";"):
        print "  %s" % i

def getpools( ):
    "Fetches the pools and returns them in an array"

    # buffer up Ansible input from reading the facts
    ansibleInput="Getting pools from Ansible:\n"
    p = subprocess.Popen('ansible-playbook testbooks/netapp_facts.yml', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        ansibleInput+=line
    retval = p.wait()
    
    # Log ansible output to logfile
    ansLog.logbuffer("ansibleOut.txt", ansibleInput)
    
    # Parse output for pool lines
    foundpools = 0
    poolList = ""
    ansibleList = ansibleInput.split(os.linesep)
    for i in ansibleList:
        if i.find('Pool name is') != -1:
            if foundpools != 0:
                poolList+=";;;"
            poolList+=i
            foundpools+=1
            
    # Convert grepped output into array
    if debugPrints == 1:
        print "poolList: %s\n" % poolList
    poolList = poolList.split(';;;') 
    pools = ""
    foundpools = 0

    # now convert to just raw names
    for i in poolList:
        pool = re.sub(r'\s*"msg": "Pool name is ', '', i)
        pool = re.sub(r'"', '', pool)
        if debugPrints == 1:
            print "pool is %s" % pool
        if foundpools != 0:
            pools+=";"
        pools += pool
        foundpools+=1
            
    return pools

def checkpools ( poolList ):
    "Verifies pools on the array"

    tempBuffer=getpools( )
    if debugPrints == 1:
        print "Pools are: %s\n" % tempBuffer        

    if tempBuffer == poolList:
        return 1
    else:
        return -1
        

def removeallpools( ):
    "Uses ansible to remove a pool from the array:  1 if success, 0 if failed"

    temppools=getpools( )
    poolList = temppools.split(";")
    
    for i in poolList:
        print "Removing %s" % i
        removepool(i)