import sys
import psutil

vmCount = input("Maximum VMs that will run on server?")
portRange = input("Range of ports in 'xxxx-yyyy' format").split("-")
portSkip = input("Enter reserved ports to skip over separated with commas").split(",")

if int(portRange[1]) - int(-portRange[0]) + 1 -portSkip.length() != int(vmCount):
    print("Range of ports does not match maximum VMs running")
    sys.exit

with open('network.txt', 'w') as bench:
    bench.write(vmCount+"\n")
    bench.write(portRange[0]+" "+portRange[1]+"\n")
    bench.write(portSkip+"\n")

with open('portAvail.txt', 'w') as bench:
    isFinished = False
    curr = int(portRange[0])
    while isFinished==False:
        bench.write(curr+"\n")
        if curr == int(portRange[1]):
            isFinished=True
        curr += 1

with open('benchmark.txt', 'w') as bench:
    bench.write(psutil.cpu_count(logical=False))
    bench.write((psutil.virtual_memory().total))
    bench.write((psutil.disk_usage('/').total))