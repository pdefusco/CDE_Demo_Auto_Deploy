FROM docker-private.infra.cloudera.com/cloudera/dex/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15
USER root
RUN yum install ${YUM_OPTIONS} gcc openssl-devel libffi-devel bzip2-devel wget python39 python39-devel && yum clean all && rm -rf /var/cache/yum
RUN update-alternatives --remove-all python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.9 /usr/bin/python3
RUN yum install python39-pip
RUN /usr/bin/python3.9 -m pip install numpy==1.22.0 pandas==1.2.5 pickleshare==0.7.5 py4j==0.10.9 pyarrow==4.0.1 python-dateutil==2.8.1 six==1.15.0 pyparsing==2.4.7 jmespath
RUN /usr/bin/python3.9 -m pip install dbldatagen
USER ${DEX_UID}
