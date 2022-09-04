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
parser.add_argument("-p","--ports", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-n","--name", default="", help="Number of Virtual CPUs in machine")
parser.add_argument("-ps","--password", default="pass", help="Number of Virtual CPUs in machine")


args = parser.parse_args()

    
#line1 = file.readline()
line1 = args.name
print(line1)
os.system('microstack.openstack flavor create '+'--vcpu '+args.virtualcpus+' --disk '+args.storage+' --ram '+args.ram+' --property "pci_passthrough:alias"="'+args.gputype+':'+args.gpucount+'" '+line1)

os.system('microstack.openstack flavor set '+line1+' --property "pci_passthrough:alias"="'+args.gputype+'Audio:'+args.gpucount+'"')
#os.system('microstack launch '+args.operatingsys+' --flavor '+line1+' --name '+line1)
with open(line1+'.txt', 'w') as bench:
    bench.write("#cloud-config \n")
    bench.write("user: tensordock \n")
    bench.write("password: "+args.password+" \n")
    bench.write("chpasswd: {expire: False} \n")
    bench.write("ssh_pwauth: True \n")

os.system('microstack.openstack server create --flavor '+line1+' --image '+args.operatingsys+' --network external --user-data '+line1+'.txt '+line1)
   # os.system('sudo sysctl -w net.ipv4.ip_forward=1')



os.system('microstack.openstack server list --name '+line1+' > outIP.temp')
count = 0
with open("outIP.temp") as f:
    for i in f:
        if count==3:
            j = str(i).split(' | ')
            if '10' in j[3]:
                ipstr=i.split(', ')[1]
                ip=ipstr.split(' |')[0]
                with open('network.txt') as f:
                    eth = f.readline()
                    ports=str(args.ports).split(',')
                    for port in ports:
                        portOutIn = port.split(':')
                        os.system('sudo iptables -t nat -A PREROUTING -i '+eth+' -p tcp --dport '+portOutIn[0]+' -j  DNAT --to-destination '+ip+':'+portOutIn[1])
os.remove('outIP.temp')
