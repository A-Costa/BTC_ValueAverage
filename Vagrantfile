# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "private_network", ip: "192.168.10.100"
  config.vm.provision "shell", inline: <<-SHELL
    apt update
    apt upgrade -y
    apt install -y python3 python3-distutils
    cd /tmp
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    pip install flask
   SHELL
end
