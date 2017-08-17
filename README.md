Eseries Solution ToolKit (ESTK)

========

This repository contains ansible playbooks that assist in configuring NetApp Eseries and attached hosts

#### Table of Contents

  1. [Disclaimer](#disclaimer)
  2. [Overview](#overview)
  3. [Requirements](#requirements)
  4. [To Docker or Not to Docker](#todockerornottodocker)
  5. [TODOs and Future plans](#TODOsandFutureplans)

## Disclaimer

These Ansible playbooks are written as best effort and provide no warranties or SLAs, expressed or implied.

Tested control server distros

  1.  Windows 10 with Docker
  2.  Centos 7.3

Tested host distributions

  1.  Centos 7.3
  
Future planned control and host distributions

  1.  SLES
  2.  Ubuntu 16
  3.  RHEL
  
Tested Santricity versions

  1.  98.40.00.08  
  
## Overview

These Ansible playbooks are modular in nature and depending on what is defined in your hosts file, a small 
portion of the overall playbooks will be used.

## Requirements

It is recommended to have SSH keys setup prior to installation. 
Package installers (apt,yum etc...) need to be configured.  

## To docker or not to docker?
To use the docker workflow:

  1. Download docker/ansibleDev/dockerfile 

  2. Run the docker file with the following commands:
    * docker build -t dev
    * docker run --rm -it -v ${PWD}:/home dev

  3. From inside the docker image, clone the git repository:
    * cd /home
    * git clone https://github.com/NetApp/easy-button

  4. Fill out /home/easy-button directory/hosts.  The containing directory also appears outside of the docker image of the directory it was started in.
    * splunk_eseries:  Any array that should be provisioned for splunk.
	* fc_hosts:  Host servers that are connected to the array via the host channels
	* splunk_indexers:  Index servers that splunk is being deployed on.  These may be the same as other roles, or different.

 
  5. Fill out /home/easy-button/group_vars/all.
    *  For Eseries arrays, just use the ip address for the first controller.
    *  For Eseries arrays, set your user/pass for Eseries (api_username, api_password) in ./group_vars/all file.
	
  6. Run the Ansible playbook with the following command:
    * cd /home/easy-button/
	* cp -r roles /home
	* cp -r hosts /home
    * ansible-playbook splunk.yml --vvv

If you don't won't to use the docker workflow, and have a Unix host, you can do the following:
 
 1.  Verify that you have the following packages installed:
    *  Python 2.7.6
	*  Ansible 2.3.2.0
	*  Git
    *  The following packages may also be required
	   *  software-properties-common
	   *  python-software-properties
	   *  software-properties-common
       *  gcc
	   *  build-essential   
	   *  libssl-dev   
	   *  libffi-dev python-dev
       *  make  
	
 2.  Clone the git repository:
    * git clone https://github.com/NetApp/easy-button
  
 3.  Update ansible.cfg with the path to the roles/eseries/library directory
 
 4. Fill out /home/easy-button directory/hosts.  The containing directory also appears outside of the docker image of the directory it was started in.
    * splunk_eseries:  Any array that should be provisioned for splunk.
	* fc_hosts:  Host servers that are connected to the array via the host channels
	* splunk_indexers:  Index servers that splunk is being deployed on.  These may be the same as other roles, or different.
  
 5. Fill out /home/easy-button/group_vars/all.
    *  For Eseries arrays, just use the ip address for the first controller.
    *  For Eseries arrays, set your user/pass for Eseries (api_username, api_password) in ./group_vars/all file.

 6. Run the Ansible playbook with the following command:
    * ansible-playbook splunk.yml --vvv

## TODOs and Future plans

1.  Find a better way to pass in array IP addreses and passwords other than group_vars/all
2.  Having Ansible handling the packaging requirements.
3.  Expand host and control server types to Ubuntu, Redhat, and SLES