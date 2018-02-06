#!/usr/bin/env python
'''
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
'''
#---------------------------------------------------------------------------# 
# import the various server implementations
#---------------------------------------------------------------------------# 
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

client = ModbusClient('127.0.0.1', port=502)
#client = ModbusClient('honeycdsi_pymodbus', port=502)
#client = ModbusClient(method='ascii', port='/dev/pts/2', timeout=1)
# client = ModbusClient(method='rtu', port='/dev/ttyp0', timeout=1)
client.connect()

#time.sleep(5)
#log.debug("Reading Coils")
#rr = client.read_coils(1, 1, unit=0x01)

#time.sleep(3)
log.debug("Ecrire True sur la bobine 0")
rq = client.write_coil(0, True, unit=1)
rr = client.read_coils(0, 1, unit=1)
assert(rq.function_code < 0x80)     # test that we are not an error
print("Reponse :" + str(rr.bits[0]))
assert(rr.bits[0] == True)          # test the expected value

time.sleep(3)
log.debug("Ecrire plusieurs bobines")
rq = client.write_coils(1, [True]*8, unit=1)
assert(rq.function_code < 0x80)     # test that we are not an error
rr = client.read_coils(1, 21, unit=1)
assert(rr.function_code < 0x80)     # test that we are not an error
resp = [True]*21
print("rep : " + str(rr))
# If the returned output quantity is not a multiple of eight,
# the remaining bits in the final data byte will be padded with zeros
# (toward the high order end of the byte).

resp.extend([False]*3)
assert(rr.bits == resp)         # test the expected value
#time.sleep(3)
#log.debug("Write to multiple coils and read back - test 2")
#rq = client.write_coils(1, [False]*8, unit=1)
#rr = client.read_coils(1, 8, unit=1)
#assert(rq.function_code < 0x80)     # test that we are not an error
#assert(rr.bits == [False]*8)         # test the expected value

time.sleep(3)
log.debug("lire les registre discrets")
rr = client.read_discrete_inputs(0, 8, unit=1)
assert(rq.function_code < 0x80)     # test that we are not an error

log.debug("ecrire dans les regitres")
rq = client.write_register(1, 10, unit=1)
rr = client.read_holding_registers(1, 1, unit=1)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rr.registers[0] == 10)       # test the expected value

#log.debug("Write to multiple holding registers and read back")
#rq = client.write_registers(1, [10]*8, unit=1)
#rr = client.read_holding_registers(1, 8, unit=1)
#assert(rq.function_code < 0x80)     # test that we are not an error
#assert(rr.registers == [10]*8)      # test the expected value

log.debug("Read input registers")
rr = client.read_input_registers(1, 8, unit=1)
assert(rq.function_code < 0x80)     # test that we are not an error

arguments = {
    'read_address':    1,
    'read_count':      8,
    'write_address':   1,
    'write_registers': [20]*8,
}

log.debug("Read write registeres simulataneously")
rq = client.readwrite_registers(unit=1, **arguments)
rr = client.read_holding_registers(1, 8, unit=1)
assert(rq.function_code < 0x80)     # test that we are not an error
assert(rq.registers == [20]*8)      # test the expected value
assert(rr.registers == [20]*8)      # test the expected value

#---------------------------------------------------------------------------# 
# close the client
#---------------------------------------------------------------------------# 
client.close()
