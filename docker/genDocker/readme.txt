It's better to run the batch files from the commandline.  They will attempt to create an ansiblelink 
directory in the current location to assit in moving files in and out of the docker container.

When starting the docker container, they will also attempt to create a full path to the ansiblelink
directory, and this may not work well if being run from the icon.

Make sure sharing is turned on for the C: drive.  If another windows program is browsing the 
ansiblelink folder, or editing a file in it, docker may not be able to read the file.  It tends to
show up as an unreadable directory from unix.

The following directories are created:
	/root/ansiblelink is the shared drive between the docker image and the windows host
	/root/netapp_ansible_modules is the symbolic link to the ansible modules.
	/home/ansible is the home directory for the user ansible
	
Two users are created:
    root:root4l1fe
    ansible:ansible3B
    
Only the user ansible can SSH in to the server.

