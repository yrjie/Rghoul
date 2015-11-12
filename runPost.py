import os, sys
import requests

if len(sys.argv)<2:
    print 'Usage: jsonFile'
    exit(1)

infile = sys.argv[1]

url1 = 'http://genome.ddns.comp.nus.edu.sg:8080/thisisupdateSp/'
jsonStr = open(infile).readlines()[0].replace('\\', '')
ret = requests.post(url1, data=jsonStr)
print ret.text

