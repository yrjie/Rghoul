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
    'wresult': '<t:RequestSecurityTokenResponse xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><t:Lifetime><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-08T10:41:48.347Z</wsu:Created><wsu:Expires xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-08T11:41:48.347Z</wsu:Expires></t:Lifetime><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><t:RequestedSecurityToken><saml:Assertion MajorVersion="1" MinorVersion="1" AssertionID="_c682d868-1eb5-40bc-9b55-13f64bbcfa9e" Issuer="http://adfs.mail.rakuten.com/adfs/services/trust" IssueInstant="2015-10-08T10:41:48.355Z" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"><saml:Conditions NotBefore="2015-10-08T10:41:48.347Z" NotOnOrAfter="2015-10-08T11:41:48.347Z"><saml:AudienceRestrictionCondition><saml:Audience>urn:federation:MicrosoftOnline</saml:Audience></saml:AudienceRestrictionCondition></saml:Conditions><saml:AttributeStatement><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject><saml:Attribute AttributeName="UPN" AttributeNamespace="http://schemas.xmlsoap.org/claims"><saml:AttributeValue>ruijie.yang@rakuten.com</saml:AttributeValue></saml:Attribute><saml:Attribute AttributeName="ImmutableID" AttributeNamespace="http://schemas.microsoft.com/LiveID/Federation/2008/05"><saml:AttributeValue>JLX2E74/mk2m9Jf30wGM3Q==</saml:AttributeValue></saml:Attribute></saml:AttributeStatement><saml:AuthenticationStatement AuthenticationMethod="urn:federation:authentication:windows" AuthenticationInstant="2015-10-08T10:41:48.302Z"><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject></saml:AuthenticationStatement><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod><ds:Reference URI="#_c682d868-1eb5-40bc-9b55-13f64bbcfa9e"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod><ds:DigestValue>WdzPRXLtlOzeYz1Xf2ebLYi5ZRg=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>Jfb+l52fkVqJcPvlAajVvEpJfpNf+uvqFD9IzJCBXbcTIOmZdqqn+X6LGBDMafARYtuUOjwhkjICJhVqLygfc6OxaXVbTtgmamIuSSACnWhR3gJYE7i5sEqZ1pH8Nrhqqj3sQVTInaSUT+d98x1rImFKuoj/1ElUZw3CGe0YbNdE4IFNqoKhTjfBNU2V+WLhxK/yuIkbjvphVg2eOYy4u/SoRNMp7NX9brZsnWPJg4Psn1XUoGJ6je2ceJ0q3pBWrU1PzMDDvoow7Zgh9uo2B4ujFP9wFClAkqtroD94jBfpbQPSVzdFdn5Vw37dp2drZTO3T/VFVTFNwp2xw0ZGSA==</ds:SignatureValue><KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><X509Data><X509Certificate>MIIC6DCCAdCgAwIBAgIQJAvvkQTHvLhG964k1rqT8TANBgkqhkiG9w0BAQsFADAvMS0wKwYDVQQDEyRBREZTIFNpZ25pbmcgLSBhZGZzLm1haWwucmFrdXRlbi5jb20wIBcNMTMwMjE3MTUwMzM2WhgPMjExMzAxMjQxNTAzMzZaMC8xLTArBgNVBAMTJEFERlMgU2lnbmluZyAtIGFkZnMubWFpbC5yYWt1dGVuLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKPQX0FwxfkQ5PtGe7/kRoGzeOP65P94HkRAWJqZUbzX+/oSkab0hlawyOItAvmtzH1p/XRKdF8lIDO5jAGWZyUYPZYGRfJ6aMV82O+9nWEAO+NyWpv6qeYbmuwf7rDfjpE8gmV7TDAYIQTsVX4ZlQn0ifceeE7unES/R+uTi5klKiuIPuL4T8yJ/XaCxvGa7uAxwDJiK9tUGXXWh8l0i79zExc/QPmJHJiJjRXbt3j5w7UL1MCk5+WAQYx4PAYboCT7ifbwTlftYbB9HDSPXXpJ/6Zq5Iv7PvOp6s4wuAhidC/bH0Oi52LQHEtT95Z9X5n/+vKCxEh8RmIUWGrfGi0CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAdBHnjpqAjHrp2U0ZFHbRX2CQTWyg93NaKDBYgxZLPKfLuaOa4EJCEwODRzdYbxv+xrA937Oo55ysHr/Se8z4ro60IinYYRIw2BNow3CCTLfTRnzL9o5GA2qNcYEcXeOa+2cW8BMyb+ELFNHxV3K14MRTsbmc6nXTjjeOwRIM0FAq5EJdbm6/iWq+xi+xWjXb29hnMVZNZ2dH4/62OXtP7LFU1s10+pbqboq9n5CZWrHqdXMXtTfgugiosiHDLauXiahAH8rSWBUiztrZnaArxgJWPR6aqr+MXHkReRlierMoWFPQuO190VpkB+XJiRRamNbruPjpFCYsrrcmzehJyA==</X509Certificate></X509Data></KeyInfo></ds:Signature></saml:Assertion></t:RequestedSecurityToken><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType></t:RequestSecurityTokenResponse>',
    'wctx': 'estsredirect=2&estsrequest=rQIIAbNSzigpKSi20tcvyC8qSczRy09Ly0xO1UvOz9XLL0rPTAGxioS4BDaYSfw-UMvhvGkBR5DDLqbCVYxqOHXq5yTmpWTmpeslFhdUXGBk7GJiMTQwNt7ExOrr7OvkeYJpwlm5W0yC_kXpninhxW6pKalFiSWZ-XmPmHhDi1OL_PNyKkPys1PzJjHz5eSnZ-bFFxelxafl5JcDBYDGFyQml8SXZCZnp5bsYlYxMjZPMzFJTtFNMUlK1DVJtEzTTTRLMdO1TDQzTDU2N0gxTzI6wLIh5AKLwC5OW-LcbF-SWJSeWmKrapSWkpqWWJpTAhYGAA2'}
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
