import enum
import os
import subprocess

os.system('lspci -nn | grep VGA |grep NVIDIA > out.temp')
os.system('lspci -nn | grep Audio |grep NVIDIA > outAudio.temp')
id=[]
idAudio=[]
with open("out.temp") as f:
    for line in f:
        j = str(line).split(' ')
        for h in j:
            if "10de" in h:
                id.append(h[6:int(len(h))-1])


with open("outAudio.temp") as f:
    for line in f:
        j = str(line).split(' ')

        for h in j:
            if "10de" in h:
                idAudio.append(h[6:int(len(h))-1])
           # print(h)


#todo delete repeats

os.system('sudo echo \'\n[pci]\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in id:
    os.system('sudo echo \'\npassthrough_whitelist = {"vendor_id": "10de", "product_id": "'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in idAudio:
    os.system('sudo echo \'\npassthrough_whitelist = {"vendor_id": "10de", "product_id": "'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in id:
    os.system('sudo echo \'\nalias = {"vendor_id":"10de","product_id":"'+i+'"," device_type":"type-PCI","name":"'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for idx, x in enumerate(idAudio):
    os.system('sudo echo \'\nalias = {"vendor_id":"10de","product_id":"'+x+'"," device_type":"type-PCI","name":"'+id[idx]+'Audio"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

os.remove('out.temp')
os.remove('outAudio.temp')
