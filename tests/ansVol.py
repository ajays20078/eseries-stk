#!/usr/bin/python

import subprocess
import os
import re
import sys
import ansLog as ansLog

#############################################################
# Helper functions create, delete, and show E-Series storage
# volumes via Ansible.  This depends two simple playbooks to 
# control Ansible via it's netapp_e_facts and netapp_e_volume
# modules.
# 
# Other tests may add support for bypassing Ansible, but this
# is meant for testing the Ansible functionality.
#############################################################

debugPrints=0

def getvolumes( ):
    "Fetches the volumes and returns them in an string separated by a semi-colon"

    # buffer up Ansible input from reading the facts
    ansibleInput="Getting volumes from Ansible:\n"
    p = subprocess.Popen('ansible-playbook testbooks/netapp_facts.yml', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        ansibleInput+=line
    retval = p.wait()
    
    # Log ansible output to logfile
    ansLog.logbuffer("ansibleOut.txt", ansibleInput)
    
    # Parse output for volume lines
    foundVolumes = 0
    volumeList = ""
    ansibleList = ansibleInput.split(os.linesep)
    for i in ansibleList:
        if i.find('Volume name is') != -1:
            if foundVolumes != 0:
                volumeList+=";;;"
            volumeList+=i
            foundVolumes+=1
            
    # Convert grepped output into array
    if debugPrints == 1:
        print "volumeList: %s\n" % volumeList
    volumeList = volumeList.split(';;;') 
    volumes = ""
    foundVolumes = 0

    # now convert to just raw names
    for i in volumeList:
        volume = re.sub(r'\s*"msg": "Volume name is ', '', i)
        volume = re.sub(r'"', '', volume)
        if debugPrints == 1:
            print "volume is %s" % volume
        if foundVolumes != 0:
            volumes+=";"
        volumes += volume
        foundVolumes+=1
            
    return volumes

def removevolume( volumeName, poolName ):
    "Uses ansible to remove a volume from the array:  1 if success, 0 if failed"

    # buffer up Ansible input from reading the facts
    ansibleInput="Removing volume via ansible:\n"
    cmdLine = "ansible-playbook testbooks/netapp_volume.yml -e \""
    cmdLine += "volume_name="
    cmdLine += volumeName
    cmdLine += " pool_name="
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
    
def createvolume( volumeName, poolName ):
    "Uses ansible to remove a volume from the array:  1 if success, 0 if failed"

    # buffer up Ansible input from reading the facts
    ansibleInput="Creating Volume Via Ansible:\n"
    cmdLine = "ansible-playbook testbooks/netapp_volume.yml -e \""
    cmdLine += "volume_name="
    cmdLine += volumeName
    cmdLine += " pool_name="
    cmdLine += poolName
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
    
def showvolumes ( ):
    "Debug function to show volumes on the array"

    tempBuffer=getvolumes( )
    print "Volumes are: "
    for i in tempBuffer.split(";"):
        print "  %s" % i


def checkvolumes ( volumeList ):
    "Verifies pools on the array"

    tempBuffer=getvolumes( )
    if debugPrints == 1:
        print "Volumes are: <%s>\n" % tempBuffer        
    if tempBuffer == volumeList:
        return 1
    else:
        return -1
        
def removeallvolumes( ):
    "Uses ansible to remove a volume from the array:  1 if success, 0 if failed"

    tempvolumes=getvolumes( )
    volumeList = tempvolumes.split(";")
    
    for i in volumeList:
        print "Removing %s" % i
        removevolume(i, "dummy")