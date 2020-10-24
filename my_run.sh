#!/bin/bash
echo "install torch 1.1.0 torchvision 0.3.0"
pip install torch==1.1.0 torchvision==0.3.0

echo "install gcc 5"
sudo apt install gcc-5 g++-5
sudo ln -s /usr/bin/gcc-5 /usr/local/cuda/bin/gcc 
sudo ln -s /usr/bin/g++-5 /usr/local/cuda/bin/g++

gcc --version

echo "install cython"
pip install cython

echo "install mmcv 0.4.3"
pip install mmcv==0.4.3

echo "install pillow < 7"
pip install "pillow<7"

echo ">>>>>>>>>>>>>>>>>>build the project >>>>>>>>>>>>>>"
cd ../AerialDetection

chmod 775 ./compile.sh
./compile.sh

pip install -r requirements.txt
python setup.py develop

sudo apt-get install swig
cd DOTA_devkit
swig -c++ -python polyiou.i
python setup.py build_ext --inplace

echo "the curral path :"
pwd

/opt/bin/nvidia-smi


echo ">>>>>>>>>>>>>>>>>>>>>>>successfully!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

