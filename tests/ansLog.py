#!/usr/bin/python

#############################################################
# Helper functions to log ansible command output to a file
#############################################################

import os

def clearlog( logfilename ):
    "This function logs a buffer to a file"
    
    if os.path.isfile(logfilename):
        os.remove(logfilename)

def logbuffer( logfilename, output ):
    "This function logs a buffer to a file"

    with open(logfilename, "a") as fileptr:
        fileptr.write(output)    
    
    return

