Update the path in "runDocker.bat" before using it.  It should be whatever directory the docker file goes.

Make sure sharing is turned on for the C: drive.

Two directories are created:
	/root/ansiblelink is the shared drive between the docker image and the windows host
	/root/netapp_ansible_modules is the symbolic link to the ansible modules.

