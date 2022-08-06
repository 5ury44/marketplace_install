import argparse
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument("-v","--virtualcpus", default="1", help="Number of Virtual CPUs in machine")
parser.add_argument("-s","--storage", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-r","--ram", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-os","--operatingsys", default="ubuntu", help="Number of Virtual CPUs in machine")
parser.add_argument("-g","--gputype", default="", help="Number of Virtual CPUs in machine")
parser.add_argument("-c","--gpucount", default="0", help="Number of Virtual CPUs in machine")
parser.add_argument("-e","--useremail", default="", help="Number of Virtual CPUs in machine")

args = parser.parse_args()


result = subprocess.run(['microstack.openstack flavor create', '--vcpu'+args.virtualcpus,'--disk'+args.storage,'--ram'+args.ram,], stdout=subprocess.PIPE, shell=True)

#check if existing flavor like this, if not make one
