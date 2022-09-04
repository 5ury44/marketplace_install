import argparse
import os

parser = argparse.ArgumentParser()
args = parser.parse_args()


parser.add_argument("-n","--name", default="", help="Number of Virtual CPUs in machine")

os.system('microstack.openstack server delete '+args.name)
os.system('microstack.openstack flavor delete '+args.name)
os.system('rm '+args.name+'.txt')
#remove txt and flavor