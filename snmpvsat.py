#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, multiprocessing, collections, argparse, traceback, json, time, datetime
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pprint import pprint
from pymemcache.client import base


parser = argparse.ArgumentParser(description='Simple Nagios plugin VSAT')
parser.add_argument('--assignedip', action='store', default='10.52.38.77',  help="IP Address from VSAT")

args = parser.parse_args()

address= args.assignedip


cmd = 'timeout 5 ping -c 3 ' + address
data = os.popen(cmd).read()
if 'time=' in data and 'ms' in data:
     ms = data.split('rtt min/avg/max/mdev = ')[1].split('.')[0]
else:
     printderesultado = 'CRITICAL | in=; VolIn=; countIn=; out=; VolOut=; countOut=; cno=; snr=; esno=; time=;\n'
     sys.stdout.write(printderesultado) ; sys.stdout.flush()
     os._exit(2)


Scientist = collections.namedtuple('Scientist',[
    'name',
    'oid',
    'noble',
])

scientists = (
    Scientist(name='in', oid='1.3.6.1.4.1.7352.3.5.11.6.16.1.0', noble=False),
    Scientist(name='out', oid='1.3.6.1.4.1.7352.3.5.11.6.16.2.0', noble=True),
    Scientist(name='cno', oid='1.3.6.1.4.1.7352.3.5.10.16.9.0', noble=True),
    Scientist(name='snr', oid='1.3.6.1.4.1.7352.3.5.10.16.8.0', noble=True),
    Scientist(name='esno', oid='1.3.6.1.4.1.7352.3.5.10.16.25.0', noble=True),
)

def transform(x):
    oid = str(x.oid)
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
       cmdgen.CommunityData('public'),
       cmdgen.UdpTransportTarget((address, 161), timeout=8.0, retries=3),
       oid
         )
    resultadosnmp = str(varBinds[0][1])
    nombresnmp = x.name
    result = {'name': nombresnmp, 'oid': resultadosnmp}
    if len(resultadosnmp) == 0:
       printderesultado = 'UNKNOWN | Fallo SNMP consulta\n'
       sys.stdout.write(printderesultado) ; sys.stdout.flush()
       os._exit(3)
    else:
       return result

pool = multiprocessing.Pool(processes=5, maxtasksperchild=1)
result = pool.map(transform, scientists)


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Formato desconocido")

today = datetime.datetime.now()
hoy = today.strftime('%d-%m-%Y %H:%M:%S')
createarray = [{'name':(str(result[0]['name'])), 'data':(int(result[0]['oid'])) }, {'name':(str(result[1]['name'])), 'data':(int(result[1]['oid']))}, {'name':'date', 'data':(str(hoy))}]

client = base.Client(('localhost', 11211), serializer=json_serializer, deserializer=json_deserializer)
resultmemcache = client.get(address)
rx = (int(result[0]['oid']))
tx = (int(result[1]['oid']))

if str(resultmemcache) == "None": # Si mencache contiene NONE crearemos la key en memcache para luego obtener datos de ella
    client.set(address, createarray, expire=900)
    salidadata = 'OK | Renovando la Cache de datos\n'
    sys.stdout.write(salidadata) ; sys.stdout.flush()
    os._exit(0)
elif int(resultmemcache[0]['data']) <= rx and int(resultmemcache[1]['data']) <= tx:
    fecha1 = datetime.datetime(*time.strptime((resultmemcache[2]['data']), '%d-%m-%Y %H:%M:%S')[:6])
    fecha2 = datetime.datetime(*time.strptime(hoy, '%d-%m-%Y %H:%M:%S')[:6])
    resta = fecha2-fecha1
    segundos = resta.seconds
    resulKbpsRx = round((((rx - int(resultmemcache[0]['data'])) / segundos) * 8 / 1000),2)
    resulKbpsTx = round((((tx - int(resultmemcache[1]['data'])) / segundos) * 8 / 1000),2)
    printderesultado = 'OK time=' + str(ms) + 'ms; status=up; | in=' + str(resulKbpsRx) + 'Kbps; VolIn=' +  str(round(rx - int(resultmemcache[0]['data']),3))  + '; countIn=' + (str(result[0]['oid']))  + '; out=' + str(resulKbpsTx)  + 'Kbps; VolOut=' + str(round(tx - int(resultmemcache[1]['data']),3))  + '; countOut=' + (str(result[1]['oid']))  + '; cno=' + str(int(result[2]['oid']) / 10)  + 'dB; snr=' + str(int(result[3]['oid']) / 100)  + 'dB; esno=' + str(int(result[4]['oid']) / 10)  + 'dB; time=' + str(ms) + 'ms;\n'
    sys.stdout.write(printderesultado) ; sys.stdout.flush()
    client.set(address, createarray, expire=900)
    os._exit(0)
else:
    client.set(address, createarray, expire=900)
    salidadata = 'OK | Renovando la Cache de datos\n'
    sys.stdout.write(salidadata) ; sys.stdout.flush()
    os._exit(0)
