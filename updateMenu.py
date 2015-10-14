#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import requests
import getpass
from requests_ntlm import HttpNtlmAuth
import shutil
import json
import time
import datetime

if len(sys.argv)<2:
    print('Usage: auto script')
    exit(1)

class dish:
    def __init__(self, id, name, booth, ingredient, energy, price, mealTime, floor):
        self.id = id
        self.name = name
        self.booth = booth
        self.ingredient = ingredient
        self.energy = energy
        self.price = price
        self.mealTime = mealTime
        self.floor = floor

def parseDish(s, floor, lines, dishes, id2pic):
    id = 0
    pic = 0
    name = ''
    booth = ''
    ingredient = 0
    price = 0
    mealTime = ''
    lookupId = 0

    state = 0  # 0: before dishes, 1: in dishes, 2: in one dish
    for line in lines:
        if state == 0:
            if 'var WPQ2ListData' in line:
                state = 1
            continue
        if state == 1:
            if '"ID"' in line:
                state = 2
                id = int(line.split('": "')[1].split('",')[0])
            if 'FolderPermissions' in line:
                break
            continue
        if state == 2:
            if 'lookupValue' in line:
                lookupId = int(line.split('lookupId":')[1].split(',')[0])
                name = line.split('lookupValue":"')[1].split('",')[0].replace('"','')
            if 'Ingredients' in line:
                ingds = set()
                temp = line.split('title=\\"')
                for x in temp[1:]:
                    ingds.add(x.split('\\"')[0])
                ingredient = 0
                for i, x in enumerate(ingdLst):
                    if x in ingds:
                        ingredient += (1<<i)
            if 'Menu_x003a_Calory' in line:
                temp = line.split('Menu_x003a_Calory": "')[1].split('",')[0]
                if temp:
                    energy = int(temp)
                else:
                    energy = 0
            if 'Menu_x003a_Value' in line:
                temp = line.split('Menu_x003a_Value": "')[1].split('",')[0]
                if temp:
                    price = int(temp)
                else:
                    price = 0
            if 'Timezone' in line:
                mealTime = line.split('Timezone": "')[1].split('",')[0][0]
            if 'MenuTypeTitle' in line:
                booth = line.split('MenuTypeTitle": "')[1].split('",')[0]
                picid = getPic(s, floor, lookupId)
                if picid:
                    id2pic[id] = picid
                    dishes.append(dish(id, name, booth, ingredient, energy, price, mealTime, floor))
                state = 1
            continue

def getPic(s, floor, lookupId):
    retDish = s.get(urlDish % (floor, lookupId))
    picLines = retDish.text.replace('\r\n', '\n').split('\n')
    ret = 0
    for line in picLines:
        if 'Menu Image' in line:
            ret = int(line.split('-')[-1])
            break
    return ret

def downloadPics(s, dishes, id2pic):
    nowDir = os.getcwd()
    today = getToday()
    for x in dishes:
        picId = id2pic[x.id]
        pic = s.get(urlPic % (x.floor, picId), stream=True)
        meal = 'lunch'
        if x.mealTime == 'D':
            meal = 'dinner'
        os.chdir('%s/static/data/%s/%s%d/' % (nowDir, today, meal, x.floor))
        src = '../../../images/%s.jpg' % picId
        dst = '%d.jpg' % x.id
        with open(src, 'wb') as out_file:
            shutil.copyfileobj(pic.raw, out_file)
        del pic
        try:
            os.symlink(src, dst)
        except:
            os.unlink(dst)
            os.symlink(src, dst)

def getToday():
    ts = time.time();
    today = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d");
    return today

pw=getpass.getpass()

url01 = 'https://adfs.mail.rakuten.com/adfs/ls/auth/integrated/'
url02 = 'https://login.microsoftonline.com/login.srf'
url03 = 'https://portal.microsoftonline.com'
url04 = 'https://portal.office.com/landing.aspx?target=%2fdefault.aspx&wa=wsignin1.0'
url05 = 'https://officerakuten.sharepoint.com/_forms/default.aspx?apr=1&wa=wsignin1.0'

url9 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_9F/TodaysMenu.aspx'
url22 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_22F/TodaysMenu.aspx'

urlDish = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/Forms/DispForm.aspx?ID=%d'
# urlPic = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/%d.jpg'
urlPic = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/_w/%d_jpg.jpg'

url2 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/Forms/DispForm.aspx'
url3 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_9F/Forms/DispForm.aspx?ID=186'
urlIngd = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/%s.jpg'
urlUpdate = 'http://gcsd-id-mars-japan.cloudapp.net/thisisupdateSp/'

payload01 = {'username':'1@rakuten.com', 'wa':'wsignin1.0', 'wtrealm':'urn:federation:MicrosoftOnline', 'popupui':''}
payload02 = {'wa': 'wsignin1.0',
 # 'wresult': '<t:RequestSecurityTokenResponse xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><t:Lifetime><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-01T03:39:00.828Z</wsu:Created><wsu:Expires xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-01T04:39:00.828Z</wsu:Expires></t:Lifetime><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><t:RequestedSecurityToken><saml:Assertion MajorVersion="1" MinorVersion="1" AssertionID="_37744ddb-da73-40d2-ac2f-b4d7d72059a4" Issuer="http://adfs.mail.rakuten.com/adfs/services/trust" IssueInstant="2015-10-01T03:39:00.836Z" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"><saml:Conditions NotBefore="2015-10-01T03:39:00.828Z" NotOnOrAfter="2015-10-01T04:39:00.828Z"><saml:AudienceRestrictionCondition><saml:Audience>urn:federation:MicrosoftOnline</saml:Audience></saml:AudienceRestrictionCondition></saml:Conditions><saml:AttributeStatement><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject><saml:Attribute AttributeName="UPN" AttributeNamespace="http://schemas.xmlsoap.org/claims"><saml:AttributeValue>ruijie.yang@rakuten.com</saml:AttributeValue></saml:Attribute><saml:Attribute AttributeName="ImmutableID" AttributeNamespace="http://schemas.microsoft.com/LiveID/Federation/2008/05"><saml:AttributeValue>JLX2E74/mk2m9Jf30wGM3Q==</saml:AttributeValue></saml:Attribute></saml:AttributeStatement><saml:AuthenticationStatement AuthenticationMethod="urn:federation:authentication:windows" AuthenticationInstant="2015-10-01T03:39:00.796Z"><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject></saml:AuthenticationStatement><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod><ds:Reference URI="#_37744ddb-da73-40d2-ac2f-b4d7d72059a4"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod><ds:DigestValue>7H5ldKTIzneshJ7LmTm6uo0pnbc=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>LxaQqewRoCqEi375f0fsqYWzFZaDkx9jM8pi0shE2Vg1zzoGSmlNGxlx24hrdrniFN41S1eNGGGlP+6QdDo65UU48J1PSx8KkC37H0+MgfCvfNW+DyYscyFa/UL9bOFjwph2wpBoBsD4VgiYibUaSyPl3PN5ILpjl19gH1JWz0w5qJg8mYYAu0qNkj5SVmL6hpZn2LCViT7C/YppYSQg1u1G06UtSyAYbozudbuvdZdo6DE73Q2d4oSsfIPeTlsUe9h3q63Sc8CQnwo5Oqn2q32mg2dv5E9hDERK0E9jMJBkQYNTwE/45DA5hg4vkVi2M1piq/3/O5bpmw1BaCqJmw==</ds:SignatureValue><KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><X509Data><X509Certificate>MIIC6DCCAdCgAwIBAgIQJAvvkQTHvLhG964k1rqT8TANBgkqhkiG9w0BAQsFADAvMS0wKwYDVQQDEyRBREZTIFNpZ25pbmcgLSBhZGZzLm1haWwucmFrdXRlbi5jb20wIBcNMTMwMjE3MTUwMzM2WhgPMjExMzAxMjQxNTAzMzZaMC8xLTArBgNVBAMTJEFERlMgU2lnbmluZyAtIGFkZnMubWFpbC5yYWt1dGVuLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKPQX0FwxfkQ5PtGe7/kRoGzeOP65P94HkRAWJqZUbzX+/oSkab0hlawyOItAvmtzH1p/XRKdF8lIDO5jAGWZyUYPZYGRfJ6aMV82O+9nWEAO+NyWpv6qeYbmuwf7rDfjpE8gmV7TDAYIQTsVX4ZlQn0ifceeE7unES/R+uTi5klKiuIPuL4T8yJ/XaCxvGa7uAxwDJiK9tUGXXWh8l0i79zExc/QPmJHJiJjRXbt3j5w7UL1MCk5+WAQYx4PAYboCT7ifbwTlftYbB9HDSPXXpJ/6Zq5Iv7PvOp6s4wuAhidC/bH0Oi52LQHEtT95Z9X5n/+vKCxEh8RmIUWGrfGi0CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAdBHnjpqAjHrp2U0ZFHbRX2CQTWyg93NaKDBYgxZLPKfLuaOa4EJCEwODRzdYbxv+xrA937Oo55ysHr/Se8z4ro60IinYYRIw2BNow3CCTLfTRnzL9o5GA2qNcYEcXeOa+2cW8BMyb+ELFNHxV3K14MRTsbmc6nXTjjeOwRIM0FAq5EJdbm6/iWq+xi+xWjXb29hnMVZNZ2dH4/62OXtP7LFU1s10+pbqboq9n5CZWrHqdXMXtTfgugiosiHDLauXiahAH8rSWBUiztrZnaArxgJWPR6aqr+MXHkReRlierMoWFPQuO190VpkB+XJiRRamNbruPjpFCYsrrcmzehJyA==</X509Certificate></X509Data></KeyInfo></ds:Signature></saml:Assertion></t:RequestedSecurityToken><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType></t:RequestSecurityTokenResponse>',
 # 'wctx':'estsredirect=2&estsrequest=rQIIAbPSySgpKSi20tcvyC8qSczRy81MLsovzk8ryc_LycxL1UvOz9XLL0rPTAGxioS4BFqTvnQ9YPzotqT73dunE18rrGJUJmyE_gVGxheMjLeYBP2L0j1TwovdUlNSixJLMvPzHjHxhhanFvnn5VSG5Gen5k1i5svJT8_Miy8uSotPy8kvBwoATShITC6JL8lMzk4t2cWsYpZsmmhglGiia5KcDCQMzBJ1Ey0tTXSNjS1NzAxSTA0tkw0vsAgc4GQEAA2'}
    # 'wresult': '<t:RequestSecurityTokenResponse xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><t:Lifetime><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-01T07:31:06.939Z</wsu:Created><wsu:Expires xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-01T08:31:06.939Z</wsu:Expires></t:Lifetime><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><t:RequestedSecurityToken><saml:Assertion MajorVersion="1" MinorVersion="1" AssertionID="_b6097be0-3d41-4d75-a03e-bf75639aa9ce" Issuer="http://adfs.mail.rakuten.com/adfs/services/trust" IssueInstant="2015-10-01T07:31:06.947Z" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"><saml:Conditions NotBefore="2015-10-01T07:31:06.939Z" NotOnOrAfter="2015-10-01T08:31:06.939Z"><saml:AudienceRestrictionCondition><saml:Audience>urn:federation:MicrosoftOnline</saml:Audience></saml:AudienceRestrictionCondition></saml:Conditions><saml:AttributeStatement><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject><saml:Attribute AttributeName="UPN" AttributeNamespace="http://schemas.xmlsoap.org/claims"><saml:AttributeValue>ruijie.yang@rakuten.com</saml:AttributeValue></saml:Attribute><saml:Attribute AttributeName="ImmutableID" AttributeNamespace="http://schemas.microsoft.com/LiveID/Federation/2008/05"><saml:AttributeValue>JLX2E74/mk2m9Jf30wGM3Q==</saml:AttributeValue></saml:Attribute></saml:AttributeStatement><saml:AuthenticationStatement AuthenticationMethod="urn:federation:authentication:windows" AuthenticationInstant="2015-10-01T07:31:06.910Z"><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject></saml:AuthenticationStatement><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod><ds:Reference URI="#_b6097be0-3d41-4d75-a03e-bf75639aa9ce"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod><ds:DigestValue>KIGEKLnP10J7mqK5XZ3bKt+I5Q8=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>GqGLPiYl6hJAitsavG2Rl7qMYFftWuRqSrMFdYm1pny8pYZKd20OFkVUZOA+UenAbALBruHQ+EHMtWlcb2o7OG6qtbzmd+IypG+5PneP9IEG0f/JHu6CXOLloZ4kyBTIrACwzs1oi32J0fWKs6xhAPnqDv086rLYaTLph5D9X4qvnv3Ynd2MzcAs1xHG/lTirYxxxAV9daCRan61OO/1mXA9kptvxWsK20bjXKJcBp7y+9JXfVhq45f2uNdp8eC0HhnNP8ADn33VXJVIe0j6YHu+xNXk1td3QjQ/P+yonKvEKZ+iCMxJSuEWIkljsY14zfQS2l+JWbY1aR9MPLSuSw==</ds:SignatureValue><KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><X509Data><X509Certificate>MIIC6DCCAdCgAwIBAgIQJAvvkQTHvLhG964k1rqT8TANBgkqhkiG9w0BAQsFADAvMS0wKwYDVQQDEyRBREZTIFNpZ25pbmcgLSBhZGZzLm1haWwucmFrdXRlbi5jb20wIBcNMTMwMjE3MTUwMzM2WhgPMjExMzAxMjQxNTAzMzZaMC8xLTArBgNVBAMTJEFERlMgU2lnbmluZyAtIGFkZnMubWFpbC5yYWt1dGVuLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKPQX0FwxfkQ5PtGe7/kRoGzeOP65P94HkRAWJqZUbzX+/oSkab0hlawyOItAvmtzH1p/XRKdF8lIDO5jAGWZyUYPZYGRfJ6aMV82O+9nWEAO+NyWpv6qeYbmuwf7rDfjpE8gmV7TDAYIQTsVX4ZlQn0ifceeE7unES/R+uTi5klKiuIPuL4T8yJ/XaCxvGa7uAxwDJiK9tUGXXWh8l0i79zExc/QPmJHJiJjRXbt3j5w7UL1MCk5+WAQYx4PAYboCT7ifbwTlftYbB9HDSPXXpJ/6Zq5Iv7PvOp6s4wuAhidC/bH0Oi52LQHEtT95Z9X5n/+vKCxEh8RmIUWGrfGi0CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAdBHnjpqAjHrp2U0ZFHbRX2CQTWyg93NaKDBYgxZLPKfLuaOa4EJCEwODRzdYbxv+xrA937Oo55ysHr/Se8z4ro60IinYYRIw2BNow3CCTLfTRnzL9o5GA2qNcYEcXeOa+2cW8BMyb+ELFNHxV3K14MRTsbmc6nXTjjeOwRIM0FAq5EJdbm6/iWq+xi+xWjXb29hnMVZNZ2dH4/62OXtP7LFU1s10+pbqboq9n5CZWrHqdXMXtTfgugiosiHDLauXiahAH8rSWBUiztrZnaArxgJWPR6aqr+MXHkReRlierMoWFPQuO190VpkB+XJiRRamNbruPjpFCYsrrcmzehJyA==</X509Certificate></X509Data></KeyInfo></ds:Signature></saml:Assertion></t:RequestedSecurityToken><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType></t:RequestSecurityTokenResponse>',
    # 'wctx': 'estsredirect=2&estsrequest=rQIIAbPSySgpKSi20tcvyC8qSczRy81MLsovzk8ryc_LycxL1UvOz9XLL0rPTAGxioS4BBb7cm-dk__DpXGtzsMCazWbVYzKhI3Qv8DI-IKR8RaToH9RumdKeLFbakpqUWJJZn7eIybe0OLUIv-8nMqQ_OzUvEnMfDn56Zl58cVFafFpOfnlQAGgCQWJySXxJZnJ2aklu5hV0tKSUywsLMx1Lc0MU3RNUkxSdC0sky11LS0MTCxTEhMNE1PNL7AIHOBkBAA1'}
    # 'wresult': '<t:RequestSecurityTokenResponse xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><t:Lifetime><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-01T12:07:33.401Z</wsu:Created><wsu:Expires xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-01T13:07:33.401Z</wsu:Expires></t:Lifetime><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><t:RequestedSecurityToken><saml:Assertion MajorVersion="1" MinorVersion="1" AssertionID="_ed69f6dd-19d3-40f7-b34d-924a28f2451c" Issuer="http://adfs.mail.rakuten.com/adfs/services/trust" IssueInstant="2015-10-01T12:07:33.412Z" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"><saml:Conditions NotBefore="2015-10-01T12:07:33.401Z" NotOnOrAfter="2015-10-01T13:07:33.401Z"><saml:AudienceRestrictionCondition><saml:Audience>urn:federation:MicrosoftOnline</saml:Audience></saml:AudienceRestrictionCondition></saml:Conditions><saml:AttributeStatement><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject><saml:Attribute AttributeName="UPN" AttributeNamespace="http://schemas.xmlsoap.org/claims"><saml:AttributeValue>ruijie.yang@rakuten.com</saml:AttributeValue></saml:Attribute><saml:Attribute AttributeName="ImmutableID" AttributeNamespace="http://schemas.microsoft.com/LiveID/Federation/2008/05"><saml:AttributeValue>JLX2E74/mk2m9Jf30wGM3Q==</saml:AttributeValue></saml:Attribute></saml:AttributeStatement><saml:AuthenticationStatement AuthenticationMethod="urn:federation:authentication:windows" AuthenticationInstant="2015-10-01T12:07:33.355Z"><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject></saml:AuthenticationStatement><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod><ds:Reference URI="#_ed69f6dd-19d3-40f7-b34d-924a28f2451c"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></ds:Transform><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></ds:DigestMethod><ds:DigestValue>hdOFy1UDO4gSk96C2DhmNeQo2WI=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>PEMqcdqW8ZEnBANAkySWIMvDDPyA8PrQ1W928sN/Lb9sEUYIejkTJU2QJ+e9idREYr20fDb7MXx8lCyyoomWcbnqyVrzU00GhojV0Y8K0Zjc9CuGQe97YKCgkxXR8hIeILnntDUJzmulIL9jxCQueVmfFJltXQNbYw7B6jMHaI2NX/ouph+Db2xfaEz4ogUROQj54Jk0Fi8EbcJu5vCFtwKSsSE91cc4per5ekczX/FkkQjembPFS0bEtYIxMbgMluAqtXQXFGIK7KNsiLMSUzT6hvNjfnAmaTX05ESvhPvkC2SugZh4FrAUZgRcjdmMYv+ehuoR/SAU7Tk6fdzmvg==</ds:SignatureValue><KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><X509Data><X509Certificate>MIIC6DCCAdCgAwIBAgIQJAvvkQTHvLhG964k1rqT8TANBgkqhkiG9w0BAQsFADAvMS0wKwYDVQQDEyRBREZTIFNpZ25pbmcgLSBhZGZzLm1haWwucmFrdXRlbi5jb20wIBcNMTMwMjE3MTUwMzM2WhgPMjExMzAxMjQxNTAzMzZaMC8xLTArBgNVBAMTJEFERlMgU2lnbmluZyAtIGFkZnMubWFpbC5yYWt1dGVuLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKPQX0FwxfkQ5PtGe7/kRoGzeOP65P94HkRAWJqZUbzX+/oSkab0hlawyOItAvmtzH1p/XRKdF8lIDO5jAGWZyUYPZYGRfJ6aMV82O+9nWEAO+NyWpv6qeYbmuwf7rDfjpE8gmV7TDAYIQTsVX4ZlQn0ifceeE7unES/R+uTi5klKiuIPuL4T8yJ/XaCxvGa7uAxwDJiK9tUGXXWh8l0i79zExc/QPmJHJiJjRXbt3j5w7UL1MCk5+WAQYx4PAYboCT7ifbwTlftYbB9HDSPXXpJ/6Zq5Iv7PvOp6s4wuAhidC/bH0Oi52LQHEtT95Z9X5n/+vKCxEh8RmIUWGrfGi0CAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAdBHnjpqAjHrp2U0ZFHbRX2CQTWyg93NaKDBYgxZLPKfLuaOa4EJCEwODRzdYbxv+xrA937Oo55ysHr/Se8z4ro60IinYYRIw2BNow3CCTLfTRnzL9o5GA2qNcYEcXeOa+2cW8BMyb+ELFNHxV3K14MRTsbmc6nXTjjeOwRIM0FAq5EJdbm6/iWq+xi+xWjXb29hnMVZNZ2dH4/62OXtP7LFU1s10+pbqboq9n5CZWrHqdXMXtTfgugiosiHDLauXiahAH8rSWBUiztrZnaArxgJWPR6aqr+MXHkReRlierMoWFPQuO190VpkB+XJiRRamNbruPjpFCYsrrcmzehJyA==</X509Certificate></X509Data></KeyInfo></ds:Signature></saml:Assertion></t:RequestedSecurityToken><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType></t:RequestSecurityTokenResponse>',
    # 'wctx': 'estsredirect=2&estsrequest=rQIIAbPSySgpKSi20tcvyC8qSczRy81MLsovzk8ryc_LycxL1UvOz9XLL0rPTAGxioS4BPi9zWy3bGzz6ImK6YxXM56xilGZsBH6FxgZXzAy3mIS9C9K90wJL3ZLTUktSizJzM97xMQbWpxa5J-XUxmSn52aN4mZLyc_PTMvvrgoLT4tJ78cKAA0oSAxuSS-JDM5O7VkF7NKopmpqWGacZqugamFsa6JWZKxbpJpUopuorFxkoFlmoGJWWriBRaBA5yMAA2'}
    'wresult': '<t:RequestSecurityTokenResponse xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust"><t:Lifetime><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-14T02:00:15.869Z</wsu:Created><wsu:Expires xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2015-10-14T03:00:15.869Z</wsu:Expires></t:Lifetime><wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy"><wsa:EndpointReference xmlns:wsa="http://www.w3.org/2005/08/addressing"><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><t:RequestedSecurityToken><saml:Assertion MajorVersion="1" MinorVersion="1" AssertionID="_15bfb69d-8807-48c5-b609-e30ae79c2975" Issuer="http://rakuten.com/adfs/services/trust/" IssueInstant="2015-10-14T02:00:15.869Z" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion"><saml:Conditions NotBefore="2015-10-14T02:00:15.869Z" NotOnOrAfter="2015-10-14T03:00:15.869Z"><saml:AudienceRestrictionCondition><saml:Audience>urn:federation:MicrosoftOnline</saml:Audience></saml:AudienceRestrictionCondition></saml:Conditions><saml:AttributeStatement><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject><saml:Attribute AttributeName="UPN" AttributeNamespace="http://schemas.xmlsoap.org/claims"><saml:AttributeValue>ruijie.yang@rakuten.com</saml:AttributeValue></saml:Attribute><saml:Attribute AttributeName="ImmutableID" AttributeNamespace="http://schemas.microsoft.com/LiveID/Federation/2008/05"><saml:AttributeValue>JLX2E74/mk2m9Jf30wGM3Q==</saml:AttributeValue></saml:Attribute></saml:AttributeStatement><saml:AuthenticationStatement AuthenticationMethod="urn:federation:authentication:windows" AuthenticationInstant="2015-10-14T02:00:15.837Z"><saml:Subject><saml:NameIdentifier Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">JLX2E74/mk2m9Jf30wGM3Q==</saml:NameIdentifier><saml:SubjectConfirmation><saml:ConfirmationMethod>urn:oasis:names:tc:SAML:1.0:cm:bearer</saml:ConfirmationMethod></saml:SubjectConfirmation></saml:Subject></saml:AuthenticationStatement><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" /><ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" /><ds:Reference URI="#_15bfb69d-8807-48c5-b609-e30ae79c2975"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" /><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" /></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" /><ds:DigestValue>DHHTwxinEn0qqIXJBvhoDudEHcQ=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>Ca5nGm9jaJx1JRT6/nVrUzJyxNpMfvMOgKWejRrsV7xxltIyTk6h9Vw1i1DN56syFThHyr2m7GKT1oLCppQMEVK2tfjTAZa+K6GxcWNxenJMfH0ZlU+p2x2mzm0Q6etLgIRf0NHX6BS5almJDAtSbyxwT1D98J5SNhiBH8GZ+OMiWbXFFfe6UH/wyDocGbg501fMb9nLcmsBYBgd5O8HlAwIqa9g8BOV3QUFZOUDE+cIutvxd10INq7921WDC3/oTEhKXF7AiULd8zcvqbRwNtv8sI22C5ATvqdkUq+GlS5A3Q9QvCDIv+pHf6LUMK4c1e6yMFHk022yPnlvJ0E2Lw==</ds:SignatureValue><KeyInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><X509Data><X509Certificate>MIIC7DCCAdSgAwIBAgIQFlk90/Z2b5JIOgQMLajIajANBgkqhkiG9w0BAQsFADAxMS8wLQYDVQQDEyZBREZTIFNpZ25pbmcgLSBvMzY1LnNzby5yYWt1dGVuLWl0LmNvbTAgFw0xNTA5MTUwODIwMjJaGA8yMDY1MDkyMjA4MjAyMlowMTEvMC0GA1UEAxMmQURGUyBTaWduaW5nIC0gbzM2NS5zc28ucmFrdXRlbi1pdC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCpop7yLF0NeVCIedGTZGe0yUWWW0MKfZmYLcinc99qzOGI/lU+b1PG5xL1J7Wz+oY8aHIXwYrHRw8X3qu9QOrmyAGuRtGLpjoCY0/fDK4ldVGYGxFmeVdMpOTi41CAYAWX6Brr+dbnqNyFsCBSOZ65SOfviuTXQIPbASk95wb+6ZoycyMEiqh07ti9bOngMn2emH1HrNQHKsNNFjkK751MIGkCvDHF2sa4el1ZkosaINA31YadpLZ0XfDGDtADMkksyJ8HVip8VDormv2NReyk1chEwSmLPDWsaAeHEiuorSPprHM6Tbf1qOZntI4zP5PzQH4YwFhzPhkoxSBV6t4RAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAIYfyUlkldTQ0CpIghziEXAZBnz60EG6nv0bFYvDw0M3c296MEOtDCf5zlmQJZ+u3EW1C4I0R56kC+JERbIUexRDUN1+xOm0Ncon6b23Xwfq85hiErGzJAaxklxr7grpkRlvzpWMR3v7xjFUfsnSDchLtAS7/qPv0lYRvkPjPtYQKDGssHu+FHRSXy0uh18u2oPXXFsXnJRRpG8Z+0PpzBjmI1aWzjPC9B238h++0uoVSQWoglhuoQw2ghDO7KjAKSAnFD3cLK7eCrCjmJtspW4lyWnDMLNcz/A654CSyCPr2rPeJzOAXarxjtCPFj1CTNUTufW/pwH8a2g+bCXbSd0=</X509Certificate></X509Data></KeyInfo></ds:Signature></saml:Assertion></t:RequestedSecurityToken><t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType><t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType><t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType></t:RequestSecurityTokenResponse>',
    'wctx': 'estsredirect=2&estsrequest=rQIIAbNSzigpKSi20tcvyC8qSczRy09Ly0xO1UvOz9XLL0rPTAGxioS4BNbNnxM9V97DtZtdV3aOEE_bKkY1nDr1cxLzUjLz0vUSiwsqLjAydjGxGBoYG29iYvV19nXyPME04azcLSZB_6J0z5TwYrfUlNSixJLM_LxHTLyhxalF_nk5lSH52al5k5j5cvLTM_Pii4vS4tNy8suBAkDjCxKTS-JLMpOzU0t2MatYpBgkpqWZGuiaW5iY6pokmxjpJpoZm-gmG4LsNDUxTDJOPcCyIeQCi8AuTlvi3GxfkliUnlpiq2qUlpKalliaUwIWBgA1'}
payload03 = {'wa': 'wsignin1.0'}
payload04 = {}
payload05 = {}

ingdLst = ['ALCOHOL', 'BEEF', 'CHIKEN', 'FISH', 'HEALTHY', 'MUTTON', 'PORK']
dishes = []
id2pic = {}

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
    lines = ret9.text.replace('\r\n', '\n').split('\n')
    parseDish(s, 9, lines, dishes, id2pic)

    ret22 = s.get(url22)
    lines = ret22.text.replace('\r\n', '\n').split('\n')
    parseDish(s, 22, lines, dishes, id2pic)
    downloadPics(s, dishes, id2pic)
    # for x in ingdLst:
    #     ingdfile = s.get(urlIngd % x, stream=True)
    #     with open('static/images/%s.jpg' % x, 'wb') as out_file:
    #         shutil.copyfileobj(ingdfile.raw, out_file)
    #     del ingdfile
    
dishJson = json.dumps([vars(x) for x in dishes]).replace('\\', '').replace('u3000', ' ').replace('uff53', 'ｓ')
print(dishJson)
# print(id2pic)

ret = requests.post(urlUpdate, data=dishJson)
print(ret.text)
