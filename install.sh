# First, we will install MicroStack
sudo snap install microstack --beta --devmode
sudo microstack init --auto --control

# Now, we will blacklist all unnecessary drivers
cat << EOF >> /etc/modprobe.d/blacklist.conf
blacklist snd_hda_intel
blacklist amd76x_edac
blacklist vga16fb
blacklist nouveau
blacklist rivafb
blacklist nvidiafb
blacklist rivatv
EOF

# Now the fun part: we will grab the PCI device IDs
lspci | grep VGA | grep -v NVIDIA
if [ $? -ne 0 ]; then
	echo "This computer doesn't have a integrated VGA"
	echo "It's not possible configure GPU passthrough"
	echo "exiting"
	exit 1
fi

IDS=`lspci -nnk -d 10de: | grep NVIDIA | grep -v Subsystem | awk -F '10de:' {'print $2'} | awk -F ']' {'print "10de:"$1'} `
IDS=`echo $IDS | tr ' ' ','`

# Now, let us put those IDs into the grub and enable the IOMMU
sed -i "s/GRUB_CMDLINE_LINUX_DEFAULT=\"\"/GRUB_CMDLINE_LINUX_DEFAULT=\"intel_iommu=on amd_iommu=on vfio_iommu_type1.allow_unsafe_interrupts=1 vfio-pci.ids=${IDS}\"/" /etc/default/grub

# Now, we will put those IDs into the vfio conf file
echo "options vfio-pci ids=${IDS} disable_vga=1" > /etc/modprobe.d/vfio.conf

# Now, let's add the vfio-pci module to the kernel
cat <<EOF >> /etc/modules
vfio-pci
EOF

# Allow unsafe interrupts (just like in the grub file but again)
echo "options vfio_iommu_type1 allow_unsafe_interrupts=1" > /etc/modprobe.d/iommu_unsafe_interrupts.conf

# Ignore messages, just as specified in the grub
echo "options kvm ignore_msrs=1" > /etc/modprobe.d/kvm.conf

# Finally, let's enable the GPUs in OpenStack (please adjust to your GPU PCI ID)

# Enable IP port forwarding
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

sudo apt install python3-pip
pip3 install psutil
python3 benchmark.py
python3 gpuConfig.py
wget http://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
wget https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img
microstack.openstack image create --container-format bare --disk-format qcow2 --file bionic-server-cloudimg-amd64.img ubuntu18
microstack.openstack image create --container-format bare --disk-format qcow2 --file focal-server-cloudimg-amd64.img ubuntu20

update-grub
update-initramfs -u

reboot
