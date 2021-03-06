#!/bin/bash

DIR=$(dirname "$(readlink -f "$0")")

cd $DIR

! [ -d "bin/" ] && mkdir bin/
gcc -DSUPERMODE -O3 src/expdecay.c -lm -o bin/expdecay_super
gcc             -O3 src/expdecay.c -lm -o bin/expdecay

scalac -d src src/ExpDecay.scala

bin/expdecay_super
bin/expdecay
scala -classpath src ExpDecay
python2 expdecay.py
python3 expdecay.py

cd $OLDPWD
