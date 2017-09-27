
ARG PYTHON_VERSION=2.7
FROM python:${PYTHON_VERSION}

ARG ANSIBLE_BRANCH=origin/devel
ARG ANSIBLE_REPO=https://github.com/ansible/ansible
ARG ESERIES_STK_REPO=https://github.com/NetApp/eseries-stk
ARG ESERIES_STK_BRANCH=master


WORKDIR /home

RUN apt-get update && apt-get install -y \
    sshpass vim nano \
 && rm -rf /var/lib/apt/lists/*

ENV ANSIBLE_HOST_KEY_CHECKING=False

#RUN pip install ansible
RUN git clone ${ANSIBLE_REPO} --recursive /opt/ansible
RUN cd /opt/ansible && git checkout ${ANSIBLE_BRANCH}
RUN pip install --upgrade -r /opt/ansible/requirements.txt
RUN cd /opt/ansible && python /opt/ansible/setup.py install
# Assuming that this file exists, it will mark our local ansible hosts file
# as the default for any ansible-playbook invocations
RUN mkdir -p /etc/ansible && ln -s /home/eseries-stk/hosts /etc/ansible/hosts
RUN cd /home && git clone ${ESERIES_STK_REPO}
WORKDIR "/home/eseries-stk/"
ENTRYPOINT ["/bin/bash"]