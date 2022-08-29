import sys
import psutil
import os

os.system('rm benchmark.txt')
os.system('rm network.txt')
os.system('rm portAvail.txt')

ethernetDevice = input("input the name of your networking device")
vmCount = input("Maximum VMs that will run on server?")
portRange = input("Range of ports in 'xxxx-yyyy' format").split("-")
portSkip = input("Enter reserved ports to skip over separated with commas").split(",")

with open('network.txt', 'w') as bench:
    bench.write(ethernetDevice+"\n")
    bench.write(vmCount+"\n")
    bench.write(portRange[0]+" "+portRange[1]+"\n")
    bench.write(''.join(str(x) for x in portSkip)+"\n")
    
with open('benchmark.txt', 'w') as bench:
    bench.write(str(psutil.cpu_count(logical=False))+"\n")
    bench.write(str(psutil.virtual_memory().total)+"\n")
    bench.write(str(psutil.disk_usage('/').total)+"\n")


#portskip not implemented yet
