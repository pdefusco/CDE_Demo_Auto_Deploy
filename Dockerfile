FROM registry.fedoraproject.org/fedora:37

RUN dnf update -y && dnf clean all

RUN useradd --create-home cdeuser
USER cdeuser
WORKDIR /home/cdeuser

RUN mkdir /home/cdeuser/.cde
RUN chmod 777 /home/cdeuser/.cde
RUN chmod 777 /home/cdeuser/

ADD CDE_Demo /home/cdeuser/CDE_Demo
ADD CDE_Resources /home/cdeuser/CDE_Resources
ADD deploy.sh /home/cdeuser/deploy.sh
ADD teardown.sh /home/cdeuser/teardown.sh
ADD config.yaml /home/cdeuser/.cde/config.yaml
ADD cde /usr/bin/cde
