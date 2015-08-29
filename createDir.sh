#!/bin/bash

staticDir=~/tmp/

prefix=`python -c 'import time; import datetime; ts=time.time(); prefix=datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d"); print prefix'`
mkdir -p $staticDir/$prefix/lunch9
mkdir -p $staticDir/$prefix/lunch22
mkdir -p $staticDir/$prefix/dinner9
mkdir -p $staticDir/$prefix/dinner22
