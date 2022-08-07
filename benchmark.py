import sys
import psutil
import os

vmCount = input("Maximum VMs that will run on server?")
portRange = input("Range of ports in 'xxxx-yyyy' format").split("-")
portSkip = input("Enter reserved ports to skip over separated with commas").split(",")

if int(portRange[1]) - int(portRange[0]) + 1 - len(portSkip) != int(vmCount):
    print("Range of ports does not match maximum VMs running")
    os.system('rm benchmark.txt')
    os.system('rm network.txt')
    os.system('rm portAvail.txt')
    sys.exit

with open('network.txt', 'w') as bench:
    bench.write(vmCount+"\n")
    bench.write(portRange[0]+" "+portRange[1]+"\n")
    bench.write(''.join(str(x) for x in portSkip)+"\n")

with open('portAvail.txt', 'w') as bench:
    isFinished = False
    curr = int(portRange[0])
    while isFinished==False:
        bench.write(str(curr)+"\n")
        if curr == int(portRange[1]):
            isFinished=True
        curr += 1

with open('benchmark.txt', 'w') as bench:
    bench.write(str(psutil.cpu_count(logical=False))+"\n")
    bench.write(str(psutil.virtual_memory().total)+"\n")
    bench.write(str(psutil.disk_usage('/').total)+"\n")

#portskip not implemented yet
