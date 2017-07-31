#!/bin/bash

### bail if any iface exists with netapp name
if [[ $(iscsiadm -m iface | grep netapp) ]]; then
    exit 0
fi

### parse inputs from command line
while getopts ":p:i:" cmdln; do
   case "$cmdln" in
      p)
           ports=$OPTARG
           ;;
      i)
           ip=$OPTARG
           ;;
   esac
done

initiator_name=`cat /etc/iscsi/initiatorname.iscsi | grep -v "#" | cut -d "=" -f 2`

for port in $(echo $ports | sed "s/,/ /g"); do
    host_ip = `ip addr show p5p1 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1`]
    host_mac = `ip addr show p5p1 | grep "link/ether" | awk '{print $2}'`

    iscsiadm -m iface -I netapp_iface_$port -o new
    iscsiadm -m iface -I netapp_iface_$port -o update -n iface.hwaddress -v $host_mac
    iscsiadm -m iface -I netapp_iface_$port -o update -n iface.ipaddress -v $host_ip
    iscsiadm -m iface -I netapp_iface_$port -o update -n iface.initiatorname -v $initiator_name
    iscsiadm -m discovery -t st -p  -I netapp_iface_$port

done



#iscsiadm -m node -L all
#sed -i 's/node.session.timeo.replacement_timeout = 120/node.session.timeo.replacement_timeout = 20/' /etc/iscsi/iscsid.conf
