FROM ubuntu:14.04

# Add my username / password
RUN useradd ansible -p ansible3B
RUN echo "ansible:ansible3B" | chpasswd
RUN mkdir /home/ansible
RUN chown ansible /home/ansible
run chgrp ansible /home/ansible

# fix root password 
RUN echo "root:root4l1fe" | chpasswd

# Install packages that allow us to add ansible repositories
RUN apt-get update
RUN apt-get -y install openssh-server
RUN apt-get install -y software-properties-common

# Install misc tools
RUN apt-get -y install vim
RUN apt-get -y install nano
RUN apt-get -y install git

# Install Ansible
RUN apt-add-repository ppa:ansible/ansible
RUN apt-get update
RUN apt-get install -y ansible

# Install SSH dependencies
RUN apt-get -y install python-software-properties software-properties-common
RUN apt-get -y install gcc make build-essential libssl-dev libffi-dev python-dev
RUN easy_install pip
RUN pip install pyOpenSSL ndg-httpsclient pyasn1

# Setup an easy to find link to the netapp ansible modules in the root directory
RUN ln -s /usr/lib/python2.7/dist-packages/ansible/modules/storage/netapp /root/netapp_ansible_modules

# Setup the SSH server
RUN cp /etc/ssh/sshd_config /etc/ssh/sshd_config.factory-defaults
RUN chmod a-w /etc/ssh/sshd_config.factory-defaults
RUN echo "AllowUsers ansible" >> /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN mkdir /var/run/sshd

EXPOSE 22

CMD /usr/sbin/sshd && /bin/bash

