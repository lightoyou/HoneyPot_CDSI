#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Pymodbus Synchronous Server Example
--------------------------------------------------------------------------

The synchronous server is implemented in pure python without any third
party libraries (unless you need to use the serial protocols which require
pyserial). This is helpful in constrained or old environments where using
twisted just is not feasable. What follows is an examle of its use:
'''
#---------------------------------------------------------------------------# 
# import the various server implementations
#---------------------------------------------------------------------------# 
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer
#---------------------------------------------------------------------------# 
# configure the service logging
#---------------------------------------------------------------------------# 
import logging
import logstash 
import time
import sys
time.sleep(40)
#logging.basicConfig(format='%(asctime)s machinedetest  %(name)s %(levelname)s %(message)s', filename='/var/log/modbus/modbus.log')
log = logging.getLogger('python-logstash-logger')
log.setLevel(logging.DEBUG)
# test_logger.addHandler(logstash.LogstashHandler('127.0.0.1', 5959, version=1))
log.addHandler(logstash.TCPLogstashHandler('logstash', 5959, version=1))
#logging.FileHandler('log_ser.log')
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)


def demandeobligatoire(question,typedem="text"):
    """
        Fonction de demande d'input obligatoire
        Oblige l'utilisater à entrer une réponse différende de '' et qui correspond au type demandé
        Elle prend en argument le texte pour le input (question)
        le type de la var à renvoyer 
        Types : (typedem)
            text -> string
            int ->  Entier
        + Gestion des erreur

        Renvoie la variable demandée (tempon)
    """
    if typedem == "int":
        while 1:
            try:
                tempon = int(input(question))
                if tempon != '': break
            except:
                print("Veuillez entrer un nombre : ")
    else:
        while 1:
            tempon = input(question)
            if tempon != '': break
    return tempon

def affichagesignature(dico):
    for i in range(len(dico)): 
        print ("Signature          = " + i)
        print ("VendorName         = " + dico[i]['VendorName'])
        print ("ProductCode        = " + dico[i]['ProductCode'])
        print ("VendorUrl          = " + dico[i]['VendorUrl'])
        print ("ProductName        =" + dico[i]['ProductName'])
        print ("ModelName          =" + dico[i]['ModelName'])
        print ("MajorMinorRevision = " + dico[i]['MajorMinorRevision'])
        print ("\n")

#---------------------------------------------------------------------------# 
# initialize your data store
#---------------------------------------------------------------------------# 
# The datastores only respond to the addresses that they are initialized to.
# Therefore, if you initialize a DataBlock to addresses of 0x00 to 0xFF, a
# request to 0x100 will respond with an invalid address exception. This is
# because many devices exhibit this kind of behavior (but not all)::
#
#     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
#
# Continuing, you can choose to use a sequential or a sparse DataBlock in
# your data context.  The difference is that the sequential has no gaps in
# the data while the sparse can. Once again, there are devices that exhibit
# both forms of behavior::
#
#     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
#     block = ModbusSequentialDataBlock(0x00, [0]*5)
#
# Alternately, you can use the factory methods to initialize the DataBlocks
# or simply do not pass them to have them initialized to 0x00 on the full
# address range::
#
#     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
#     store = ModbusSlaveContext()
#
# Finally, you are allowed to use the same DataBlock reference for every
# table or you you may use a seperate DataBlock for each table. This depends
# if you would like functions to be able to access and modify the same data
# or not::
#
#     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
#     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
#
# The server then makes use of a server context that allows the server to
# respond with different slave contexts for different unit ids. By default
# it will return the same context for every unit id supplied (broadcast
# mode). However, this can be overloaded by setting the single flag to False
# and then supplying a dictionary of unit id to context mapping::
#
#     slaves  = {
#         0x01: ModbusSlaveContext(...),
#         0x02: ModbusSlaveContext(...),
#         0x03: ModbusSlaveContext(...),
#     }
#     context = ModbusServerContext(slaves=slaves, single=False)
#
# The slave context can also be initialized in zero_mode which means that a
# request to address(0-7) will map to the address (0-7). The default is
# False which is based on section 4.4 of the specification, so address(0-7)
# will map to (1-8)::
#
#     store = ModbusSlaveContext(..., zero_mode=True)
#---------------------------------------------------------------------------# 
store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0, [17]*100),
    co = ModbusSequentialDataBlock(0, [17]*100),
    hr = ModbusSequentialDataBlock(0, [17]*100),
    ir = ModbusSequentialDataBlock(0, [17]*100))
context = ModbusServerContext(slaves=store, single=True)

#---------------------------------------------------------------------------# 
# initialize the server information
#---------------------------------------------------------------------------# 
# If you don't set this or any fields, they are defaulted to empty strings.
#---------------------------------------------------------------------------# 

dico = { 
    '0': 
        {'VendorName':"Schneider Electric", 
         'ProductCode':"A9MEM3255", 
         'VendorUrl':"", 
         'ProductName':"", 
         'ModelName':"Model", 
         'MajorMinorRevision':"1.0"
        },

    '1': 
        {'VendorName':"Schneider Electric", 
         'ProductCode':"BMXNOE01005", 
         'VendorUrl':"", 
         'ProductName':"", 
         'ModelName':"Model", 
         'MajorMinorRevision':"1.0"
        },

    '2': 
        {'VendorName':"Schneider Electric", 
         'ProductCode':"TM221CE40T", 
         'VendorUrl':"", 
         'ProductName':"", 
         'ModelName':"Model", 
         'MajorMinorRevision':"1.0"
        },

    '3': 
        {'VendorName':"Schneider Electric", 
         'ProductCode':"SAS TSXETY4103", 
         'VendorUrl':"", 
         'ProductName':"", 
         'ModelName':"Model", 
         'MajorMinorRevision':"1.0"
        },
}

#print("Liste des signature : ")
#-affichagesignature(dico)
#i = demandeobligatoire("Quelle signature voulez vous utiliser ?","int")

identity = ModbusDeviceIdentification()
identity.VendorName  = dico[sys.argv[1]]['VendorName']
identity.ProductCode = dico[sys.argv[1]]['ProductCode']
identity.VendorUrl   = dico[sys.argv[1]]['VendorUrl']
identity.ProductName = dico[sys.argv[1]]['ProductName']
identity.ModelName   = dico[sys.argv[1]]['ModelName']
identity.MajorMinorRevision = dico[sys.argv[1]]['MajorMinorRevision']

#---------------------------------------------------------------------------#
# run the server you want
#---------------------------------------------------------------------------# 
# Tcp:
print("=== [START] ====")
log.info("Server start")
StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))

# Udp:
#StartUdpServer(context, identity=identity, address=("localhost", 502))

# Ascii:
#StartSerialServer(context, identity=identity, port='/dev/pts/3', timeout=1)

# RTU:
# StartSerialServer(context, framer=ModbusRtuFramer, identity=identity, port='/dev/ptyp0', timeout=.005, baudrate=9600)

