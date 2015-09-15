#!/bin/bash
if [[ $# < 1 || ($1 != "lunch" && $1 != "dinner") ]]
then
    echo 'Usage: [lunch, dinner]'
    exit
fi

staticDir=static/data

today=`date +"%Y%m%d"`
mkdir -p $staticDir/$today/lunch9
mkdir -p $staticDir/$today/lunch22
mkdir -p $staticDir/$today/dinner9
mkdir -p $staticDir/$today/dinner22

root="/Volumes/NO NAME/DCIM"
folder=`ls -t "$root"|head -n1`
find "$root/$folder" -cmin -90 -exec cp -v {} $staticDir/$today/${1}9/ \;
#find "$root/$folder" -mtime 1 -exec cp {} /tmp/test/ \;
#git test
