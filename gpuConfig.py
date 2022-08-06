import enum
import os
import subprocess

os.system('lspci -nn | grep VGA |grep NVIDIA > out.temp')
os.system('lspci -nn | grep Audio |grep NVIDIA > outAudio.temp')
id=[]
idAudio=[]
fp = open("out.temp")
for i, line in enumerate(fp):
    j = i.split(' ')
    for h in j:
        if j.contains("10de"):
            id.append(j.substring(6,j.length()-1))
    
fp.close()
fp = open("outAudio.temp")
for i, line in enumerate(fp):
    j = i.split(' ')
    for h in j:
        if j.contains("10de"):
            id.append(j.substring(6,j.length()-1))
    
fp.close()

#todo delete repeats

os.system('echo \'[pci]\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in id:
    os.system('echo \'passthrough_whitelist = {"vendor_id": "10de", "product_id": "'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in idAudio:
    os.system('echo \'passthrough_whitelist = {"vendor_id": "10de", "product_id": "'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in id:
    os.system('echo \'alias = {"vendor_id":"10de","product_id":"'+i+'"," device_type":"type-PCI","name":"'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for idx, x in enumerate(idAudio):
    os.system('echo \'alias = {"vendor_id":"10de","product_id":"'+x+'"," device_type":"type-PCI","name":"'+id[idx]+'Audio"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

os.remove('out.temp')
os.remove('outAudio.temp')