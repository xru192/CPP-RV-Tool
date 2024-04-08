#!/bin/bash
cmop -v -d . /home/xyc/CLionProjects/examples/C/MF/MF.mop
rv-monitor -c -p MF.rvm
clang++  -O3  -fPIC -c  *.cc
clang -r -o libaspect.a *.o
echo "The aspect library  have been generated."
