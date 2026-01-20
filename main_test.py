from pycomm3 import LogixDriver

with LogixDriver('172.17.31.86') as plc:
    print(plc.read('AR[5]'))