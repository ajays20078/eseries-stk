#!/bin/sh
# bail if any io-mnt exists
disk_mount_flags="nobarrier,_netdev,discard"
mnts=`ls /mnt/`
fs_type=xfs

for mnt in $mnts; do
    if [[ $mnt == *"netapp-mnt"* ]]; then
        # bail if netapp-mnt exists
        exit 0
    fi
done

# Write IOMNT Section Footer
echo "#IOMNT START#" >> /etc/fstab

# find device mapper disks
disks=`/sbin/multipath -l | egrep "NETAPP.*INF" | egrep "dm-[0-9]+" | awk '{print "/dev/mapper/"$1}'`

# create mount points
for disk in $disks; do
    echo 'y' | mkfs.$fs_type -f -q $disk > /dev/null 2>&1
    tmp=`echo "$disk" | sed 's#\(/dev/\)*\(mapper/\)*##'`
    mkdir /mnt/netapp-mnt-$tmp &> /dev/null
    echo -e "$disk\t/mnt/netapp-mnt-$tmp\t\t$fs_type\t$disk_mount_flags\t0 0" >> /etc/fstab
done

# Write IOMNT Section Footer
echo "#IOMNT END#" >> /etc/fstab

# Mount all targets
mount -a &> /dev/null
