FROM python:2.7

WORKDIR /home/

RUN apt-get update && apt-get install -y \
    sshpass \
 && rm -rf /var/lib/apt/lists/*

ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN pip install ansible

ENTRYPOINT ["/bin/bash"]