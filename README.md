Eseries Solution ToolKit (ESTK)

========

This repository contains ansible playbooks that assist in configuring NetApp Eseries and attached hosts

#### Table of Contents

  1. [Disclaimer](#disclaimer)
  2. [Overview](#overview)
  3. [Requirements](#requirements)
  4. [To Docker or Not to Docker](#todockerornottodocker)
  5. [Getting Started](#gettingstarted)

## Disclaimer

These Ansible playbooks are written as best effort and provide no warranties or SLAs, expressed or implied. 
##TODO Recommended/tested control server distro?
##TODO Recommended/tested hosts?
##TODO tested/supported santricity versions?
##TODO Support statement


## Overview

These Ansible playbooks are modular in nature and depending on what is defined in your hosts file, a small 
portion of the overall playbooks will be used.

## Requirements

It is recommended to have SSH keys setup prior to installation. 
Package installers (apt,yum etc...) need to be configured.  
##TODO package requirements. ansbile handle it?

## To docker or not to docker?
To docker workflow:
## TODO Commands to download and run docker image
 
Not to Docker Workflow:
1. git clone ansible in correct directory
2. Git clone TODO http git package
3. ##TODO control server package requirements?
4. 

## Getting Started 

1. Set your ip addresses for your roles in the hosts file. Each role is a set of specific tasks and one host can be a part of several roles.
2. For Eseries arrays, just use the ip address for the first controller.  
3. For Eseries arrays, set your user/pass for Eseries (api_username, api_password) in ./group_vars/all file.  BETTER WAY FOR THIS?

