# nrpe-ubuntu-portal
Dockerfile y Kubernetes Imagen necesaria para servicio NRPE server con Pyton y Memcached

Descargar y compliar
```
git clone https://github.com/wexmaster/nrpe-ubuntu-portal.git
cd nrpe-ubuntu-portal
git pull
docker build -t nrpe-ubuntu-portal .
docker run  -d -p 5666:5666 --name nrpe-centreon  nrpe-ubuntu-portal
```

Ver LOG ( veremos mas datos pero ver al inicio del log que esten arrancados los servicios
```
docker logs nrpe-centreon
Starting memcached: memcached.
 * Starting nagios-nrpe nagios-nrpe
   ...done.
.........
```

Prueba desde otro Servidor el cual tenga check_nrpe

```
$ /opt/nagios/plugins/check_nrpe -H 10.52.38.200 
NRPE v4.0.0
$ /opt/nagios/plugins/check_nrpe -H 10.52.38.200 -t 90 -c check_total_procs
PROCS OK: 7 processes | procs=7;150;200;0;
$ /opt/nagios/plugins/check_nrpe -H 10.52.38.200 -t 90 -c check_load
OK - load average: 0.00, 0.00, 0.00|load1=0.001;0.150;0.300;0; load5=0.003;0.100;0.250;0; load15=0.001;0.050;0.200;0; 
$ /opt/nagios/plugins/check_nrpe -H 10.52.38.200 -t 90 -c check_users
USERS OK - 0 users currently logged in |users=0;5;10;0
$ /opt/nagios/plugins/check_nrpe -H 10.52.38.200 -t 90 -c check_zombie_procs
PROCS OK: 0 processes with STATE = Z | procs=0;5;10;0;
