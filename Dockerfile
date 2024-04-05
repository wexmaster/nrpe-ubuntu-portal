FROM ubuntu:20.04
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -y
# Install Required build tools
RUN apt-get install -y \
        nagios-nrpe-server \
        nagios-plugins \
        python3-pip \
        memcached \
        libmemcached-tools \
        mtr \
        vim \
        tzdata

RUN python3 -m pip install pysnmp==4.4.12 \
    && python3 -m pip install pymemcache==3.0.0 \
    && python3 -m pip install regex==2020.1.8 \
    && python3 -m pip install requests==2.9.1 \
    && python3 -m pip install urllib3==1.13.1

# Copy need files
ADD nrpe_local.cfg /etc/nagios/nrpe_local.cfg
ADD nrpe.cfg /etc/nagios/nrpe.cfg

RUN mkdir -p /var/run/memcached
RUN chmod 0757 /var/run/memcached

RUN mkdir -p /usr/lib/nagios/plugins/portal
ADD ./snmpvsat.py /usr/lib/nagios/plugins/portal/snmpvsat.py
RUN chmod 755 /usr/lib/nagios/plugins/portal/snmpvsat.py

# check_hosts_alive
run mkdir -p /var/log/centreon/centplugins/
run mkdir -p /usr/lib/nagios/plugins/scripts/
ADD ./scripts/check_hosts_alive.sh /usr/lib/nagios/plugins/scripts/check_hosts_alive.sh
RUN chmod 755 /usr/lib/nagios/plugins/scripts/check_hosts_alive.sh

ADD ./run.sh entrypoint.sh
RUN chmod 755 /*.sh
ENTRYPOINT ["/entrypoint.sh"]
