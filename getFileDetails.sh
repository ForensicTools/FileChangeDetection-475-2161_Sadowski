#!/bin/bash
#Jackson Sadowski

#SET VARIABLES HERE
DIRECT='/root/check/'

#sha256 hash files in directory
for file in `find $DIRECT -iname "*"`; do stat $file 2> /dev/null 1; done
