#!/bin/bash

DIR=$(dirname "$(readlink -f "$0")")

cd $DIR
gcc src/expdecay.c -lm -o bin/expdecay

bin/expdecay
python2 expdecay.py
python3 expdecay.py

cd $OLDPWD
