FROM python:2.7

WORKDIR /home/

RUN apt-get update && apt-get install -y \
    sshpass \
 && rm -rf /var/lib/apt/lists/*

ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN pip install ansible

#Assuming that this file exists, it will mark our local ansible hosts file
# as the default for any ansible-playbook invocations
RUN mkdir -p /etc/ansible && ln -s /home/hosts /etc/ansible/hosts

ENTRYPOINT ["/bin/bash"]