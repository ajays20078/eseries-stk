
easy-button

========

This repository contains ansible playbooks that assist in configuring NetApp Eseries and attached hsots

#### Table of Contents

  1. [Disclaimer](#disclaimer)
  2. [Overview](#overview)
  3. [Getting Started](#gettingstarted)

## Disclaimer

These Ansible playbooks are written as best effort and provide no warranties or SLAs, expressed or implied. 
# TODO Support statement




## Overview

These Ansible playbooks are modular in nature and depending on what is defined in your hsots file, a small 
portion of the overall code will be used.


## Getting Started 

Host and ESeries targets are currently supported.  Hosts are defined in the host file.  It is recommended 
to have SSH keys setup prior to installatoin.  Due to ESeries arrays not having an SSH shell, Eseries 
arrays are defined in the group_vars/eseries file.  "host" file should have [eseries] defined with 
127.0.0.1 defined as IP.



