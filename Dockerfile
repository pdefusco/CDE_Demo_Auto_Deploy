FROM registry.fedoraproject.org/fedora:37

RUN dnf update -y && dnf clean all

RUN useradd --create-home cdeuser
USER cdeuser
WORKDIR /home/cdeuser
RUN mkdir /home/cdeuser/.cde
RUN chmod 777 /home/cdeuser/.cde
RUN chmod 777 /home/cdeuser/
