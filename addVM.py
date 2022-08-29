import argparse
import subprocess
import random
import os

#from pyparsing import line

parser = argparse.ArgumentParser()

parser.add_argument("-v","--virtualcpus", default="1", help="Number of Virtual CPUs in machine")
parser.add_argument("-s","--storage", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-r","--ram", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-os","--operatingsys", default="ubuntu", help="Number of Virtual CPUs in machine")
parser.add_argument("-g","--gputype", default="", help="Number of Virtual CPUs in machine")
parser.add_argument("-c","--gpucount", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-d","--device", default="eth0", help="Number of Virtual CPUs in machine")
parser.add_argument("-p","--port", default="0", help="Number of Virtual CPUs in machine")

args = parser.parse_args()

with open('portAvail.txt') as file:
    #line1 = file.readline()
    line1 = args.port
    print(line1)
    os.system('microstack.openstack flavor create '+'--vcpu '+args.virtualcpus+' --disk '+args.storage+' --ram '+args.ram+' --property "pci_passthrough:alias"="'+args.gputype+':'+args.gpucount+'" '+line1)
    os.system('microstack.openstack flavor set '+line1+' --property "pci_passthrough:alias"="'+args.gputype+'Audio:'+args.gpucount+'"')
    os.system('microstack launch '+args.operatingsys+' --flavor '+line1+' --name '+line1)
   # os.system('sudo sysctl -w net.ipv4.ip_forward=1')

    os.system('microstack.openstack server list --name '+line1+' > outIP.temp')
    with open("outIP.temp") as f:
        for i in f:
            if i!=0:
                j = str(i).split(' | ')
                if '10' in j[3]:
                    ip=i.split(', ')[1]
                    os.system('sudo iptables -t nat -A PREROUTING -i '+args.device+' -p tcp --dport '+line1+' -j  DNAT --to-destination '+ip+':22')
    os.remove('outIP.temp')
