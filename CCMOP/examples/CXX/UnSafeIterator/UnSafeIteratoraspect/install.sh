#!/bin/bash
cmop -v -d . /root/CCMOP/examples/CXX/UnSafeIterator/UnSafeIterator.mop
rv-monitor -c -p UnSafeIterator.rvm
clang++  -O3  -fPIC -c  *.cc
clang -r -o libaspect.a *.o
echo "The aspect library  have been generated."
