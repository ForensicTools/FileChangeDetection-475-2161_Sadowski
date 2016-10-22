#!/bin/bash
#Jackson Sadowski

#SET VARIABLES HERE
DIRECT='/root/check/'
HASHFILE='/root/hashes.txt'

#sha256 hash files in directory
for file in `find $DIRECT -iname "*"`; do sha256sum $file 2> /dev/null 1; done
