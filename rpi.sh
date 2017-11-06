#!/bin/bash
cwd=$(pwd)

tar zxvf open.tar.gz

apt-get install -y build-essential
#libbgpdump
apt-get install -y libbz2-dev zlib1g-dev
tar zxvf libbgpdump-1.4.99.15.tgz
cd libbgpdump-1.4.99.15/
./configure
make
make install
cd ../

#scamper
tar zxvf scamper-cvs-20141211e.tar.gz
cd scamper-cvs-20141211e/
./configure
make
make install
cd ../

cd $cwd

#tornado
apt-get install -y python-pip
easy_install tornado
