#!/bin/bash

staticDir=static/data

today=`date +"%Y%m%d"`
mkdir -p $staticDir/$today/lunch9
mkdir -p $staticDir/$today/lunch22
mkdir -p $staticDir/$today/dinner9
mkdir -p $staticDir/$today/dinner22

root="/Volumes/NO NAME/DCIM"
folder=`ls -t "$root"|head -n1`
find "$root/$folder" -mtime 1 -exec cp {} $staticDir/$today/lunch9/ \;
#find "$root/$folder" -mtime 1 -exec cp {} /tmp/test/ \;
