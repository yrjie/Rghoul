import sys, os
import requests
import getpass

if len(sys.argv)<2:
    print 'Usage: auto script'
    exit(1)

pw=getpass.getpass()

url0='https://adfs.mail.rakuten.com/adfs/ls/auth/integrated/'
url1='https://login.microsoftonline.com/common/login'
# url2='https://jira.rakuten-it.com/jira/browse/AUDIT-2243'
url2='https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_9F/TodaysMenu.aspx'
url3='https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/Forms/DispForm.aspx'
# issues.append(url2)
payload={'login': 'ruijie.yang@rakuten.com', 'passwd': pw, 'ctx':'', 'flowToken':''}

name=''
pri=''
with requests.session() as s:
    s.auth=('ruijie.yang', pw)
    ret0 = s.get(url0, verify=False)
    print ret0.text.split('\n')
    # lines = ret0.text.split('\n')
    # for line in lines:
    #     if 'name="ctx"' in line:
    #         payload['ctx'] = line.split('value="')[1].split('"')[0]
    #     if 'name="flowToken"' in line:
    #         payload['flowToken'] = line.split('value="')[1].split('"')[0]
    # print payload['ctx']
    # print payload['flowToken']
    # ret=s.post(url1, data=payload, verify=False)
    # print ret.text.split('\n')
    info = s.get(url3)
    print info.text.decode('UTF-8').split('\n')
    # for url2 in issues:
    #     info = s.get(url2, verify=False)
    #     # print info.text
    #     page = info.text.split('\n')
    #     # print len(page)
    #     print >>sys.stderr, url2
    #     try:
    #         for i, line in enumerate(page):
    #             if 'issue-header-content' in line:
    #                 # print line
    #                 # print line.split('\"summary-val\">')[1]
    #                 name=line.split('\"summary-val\">')[1].split('</h1>')[0]
    #             if 'priority-val' in line:
    #                 pri = page[i+1].split('>')[-1]
    #                 break
    #         print '\t'.join([name, pri])
    #     except:
    #         print url2

