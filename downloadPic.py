#!/usr/local/bin/python3

import sys, os
import requests
import getpass
from requests_ntlm import HttpNtlmAuth
import shutil
import json
import time
import datetime

if len(sys.argv)<2:
    print('Usage: infile')
    print('\ninfile format: floor picid')
    exit(1)

def downloadPic(s, floor, picId):
    picurl = urlPic % (floor, picId)
    print(picurl)
    pic = s.get(picurl, stream=True)
    src = 'static/images/%s.jpg' % picId
    with open(src, 'wb') as out_file:
        shutil.copyfileobj(pic.raw, out_file)
    del pic

pw=getpass.getpass()

url01 = 'https://adfs.mail.rakuten.com/adfs/ls/auth/integrated/'
url02 = 'https://login.microsoftonline.com/login.srf'
url03 = 'https://portal.microsoftonline.com'
url04 = 'https://portal.office.com/landing.aspx?target=%2fdefault.aspx&wa=wsignin1.0'
url05 = 'https://officerakuten.sharepoint.com/_forms/default.aspx?apr=1&wa=wsignin1.0'

urlPic = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/_w/%d_jpg.jpg'
url9 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_9F/TodaysMenu.aspx'

payload01 = {'username':'1@rakuten.com', 'wa':'wsignin1.0', 'wtrealm':'urn:federation:MicrosoftOnline', 'popupui':''}
payload02 = {'wa': 'wsignin1.0',
    'wresult': '<t:RequestSecurityTokenResponse xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><t:Lifetime><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-13T09:35:50.007Z</wsu:Created><wsu:Expires xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-13T10:35:50.007Z</wsu:Expires></t:Lifetime><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><t:RequestedSecurityToken><saml:Assertion MajorVersion="1" MinorVersion="1" AssertionID="_c42f988d-dc57-4965-b15f-36e6257a5544" Issuer="http://rakuten.com/adfs/services/trust/" IssueInstant="2015-10-13T09:35:50.007Z" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"><saml:Conditions NotBefore="2015-10-13T09:35:50.007Z" NotOnOrAfter="2015-10-13T10:35:50.007Z"><saml:AudienceRestrictionCondition><saml:Audience>urn:federation:MicrosoftOnline</saml:Audience></saml:AudienceRestrictionCondition></saml:Conditions><saml:AttributeStatement><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject><saml:Attribute AttributeName="UPN" AttributeNamespace="http://schemas.xmlsoap.org/claims"><saml:AttributeValue>ruijie.yang@rakuten.com</saml:AttributeValue></saml:Attribute><saml:Attribute AttributeName="ImmutableID" AttributeNamespace="http://schemas.microsoft.com/LiveID/Federation/2008/05"><saml:AttributeValue>JLX2E74/mk2m9Jf30wGM3Q==</saml:AttributeValue></saml:Attribute></saml:AttributeStatement><saml:AuthenticationStatement AuthenticationMethod="urn:federation:authentication:windows" AuthenticationInstant="2015-10-13T09:35:49.976Z"><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject></saml:AuthenticationStatement><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" /><ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" /><ds:Reference URI="#_c42f988d-dc57-4965-b15f-36e6257a5544"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" /><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" /></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" /><ds:DigestValue>dwzv8xDtZCxmZUdfA6naaUhGNUM=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>oMSoba/jETnVhR/tDUrYL1CfRdYv4YALYEEWTsBLAsIGdeSqYXPAoSg+fyDviTKpR81Yk+iBrRMJ2qQYKxmOWc1aOwnckAQ19oMIbVI4cId+8LLRMOuUAHrWBSMye4xcqvaTO6zUSj5kxjCN0YF2z+7m+yziUPFVwZcH/aoCdpkbUhd+XR2vneHxLbWWq7NTrp7eceiTDsW7umTfaHsGIZbzcJa4pnShzUd1KAHoxPrWvps2dPlbC/gu+8keb1qFQdsyBO4n3L+I10QB9/PRNt0TTfwb5y9xl4lLnpaN3VghCSM0eA97iVr/Q5rFQieo4wXVyoVaqpXeceoFQeR6PQ==</ds:SignatureValue><KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><X509Data><X509Certificate>MIIC7DCCAdSgAwIBAgIQFlk90/Z2b5JIOgQMLajIajANBgkqhkiG9w0BAQsFADAxMS8wLQYDVQQDEyZBREZTIFNpZ25pbmcgLSBvMzY1LnNzby5yYWt1dGVuLWl0LmNvbTAgFw0xNTA5MTUwODIwMjJaGA8yMDY1MDkyMjA4MjAyMlowMTEvMC0GA1UEAxMmQURGUyBTaWduaW5nIC0gbzM2NS5zc28ucmFrdXRlbi1pdC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCpop7yLF0NeVCIedGTZGe0yUWWW0MKfZmYLcinc99qzOGI/lU+b1PG5xL1J7Wz+oY8aHIXwYrHRw8X3qu9QOrmyAGuRtGLpjoCY0/fDK4ldVGYGxFmeVdMpOTi41CAYAWX6Brr+dbnqNyFsCBSOZ65SOfviuTXQIPbASk95wb+6ZoycyMEiqh07ti9bOngMn2emH1HrNQHKsNNFjkK751MIGkCvDHF2sa4el1ZkosaINA31YadpLZ0XfDGDtADMkksyJ8HVip8VDormv2NReyk1chEwSmLPDWsaAeHEiuorSPprHM6Tbf1qOZntI4zP5PzQH4YwFhzPhkoxSBV6t4RAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAIYfyUlkldTQ0CpIghziEXAZBnz60EG6nv0bFYvDw0M3c296MEOtDCf5zlmQJZ+u3EW1C4I0R56kC+JERbIUexRDUN1+xOm0Ncon6b23Xwfq85hiErGzJAaxklxr7grpkRlvzpWMR3v7xjFUfsnSDchLtAS7/qPv0lYRvkPjPtYQKDGssHu+FHRSXy0uh18u2oPXXFsXnJRRpG8Z+0PpzBjmI1aWzjPC9B238h++0uoVSQWoglhuoQw2ghDO7KjAKSAnFD3cLK7eCrCjmJtspW4lyWnDMLNcz/A654CSyCPr2rPeJzOAXarxjtCPFj1CTNUTufW/pwH8a2g+bCXbSd0=</X509Certificate></X509Data></KeyInfo></ds:Signature></saml:Assertion></t:RequestedSecurityToken><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType></t:RequestSecurityTokenResponse>',
    'wctx': 'estsredirect=2&estsrequest=rQIIAbNSzigpKSi20tcvyC8qSczRy09Ly0xO1UvOz9XLL0rPTAGxioS4BA4-viyccv-Hw6KzVS_sv-QkrmJUw6lTPycxLyUzL10vsbig4gIjYxcTi6GBsfEmJlZfZ18nzxNME87K3WIS9C9K90wJL3ZLTUktSizJzM97xMQbWpxa5J-XUxmSn52aN4mZLyc_PTMvvrgoLT4tJ78cKAA0viAxuSS-JDM5O7VkF7NKUpqZZaKhsaWuUaqRma6JeXKyrqWhgYWuUXKqRZpZWrKRmYHlAZYNIRdYBHZx2hLnZvuSxKL01BJbVaO0lNS0xNKcErAwAA2'}
payload03 = {'wa': 'wsignin1.0'}
payload04 = {}
payload05 = {}

infile = sys.argv[1]
lines = open(infile).readlines()

with requests.session() as s:
    s.auth = HttpNtlmAuth('INTRA\\ruijie.yang', pw, s)
    s.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests':'1'
        })
    # ret01 = s.get(url02)
    # payload01['wctx'] = ret01.text.split('wctx=')[1].split('\\u0026')[0]
    ret01 = s.get(url01)
    payload01['wctx'] = 'estsredirect=2&estsrequest=rQIIAbPSySgpKSi20tcvyC8qSczRy81MLsovzk8ryc_LycxL1UvOz9XLL0rPTAGxioS4BBYVHnL4-T7Qcc-kppq1-SXbVjEqEzZC_wIj4wtGxltMgv5F6Z4p4cVuqSmpRYklmfl5j5h4Q4tTi_zzcipD8rNT8yYx8-Xkp2fmxRcXpcWn5eSXAwWAJhQkJpfEl2QmZ6eW7GJWSTYySDEwSkvSTTQ2T9M1MTU30LUwMjXXNUlLNrBINkhMTTZJu8AicICTEQA1'
    # payload02['wctx'] = payload01['wctx']
    ret01 = s.post(url01, data=payload01)
    # print(payload01)
    # print(ret01.text)
    # payload02['wresult'] = ret01.text.split('name="wresult" value="')[1].split('" />')[0]
    # payload02['wresult'] = ''
    ret02 = s.post(url02, data=payload02)
    # print(ret02.text)
    payload03['t'] = ret02.text.split('value="')[1].split('">')[0]
    ret03 = s.post(url03, data=payload03)
    payload04['t'] = ret03.text.split('value="')[1].split('">')[0]
    ret04 = s.post(url04, data=payload04)
    ret9 = s.get(url9)
    payload05['t'] = ret9.text.split('value="')[1].split('">')[0]
    
    ret9 = s.post(url05, data=payload05)
    for line in lines:
        line = line.strip()
        if len(line) < 1:
            continue
        [floor, picId] = [int(x) for x in line.split()]
        downloadPic(s, floor, picId)
