#!/usr/bin/python
#salt-api
#wangpei
#20160215

import sys
import pycurl
import StringIO
import time

def api_login(url):
    ch = pycurl.Curl()
    ch.setopt(ch.URL,url + '/login')
    info = StringIO.StringIO()
    ch.setopt(ch.WRITEFUNCTION,info.write)
    ch.setopt(ch.POST,True)
    ch.setopt(ch.SSL_VERIFYPEER,0)
    ch.setopt(ch.SSL_VERIFYHOST,0)
    ch.setopt(ch.HTTPHEADER,['Accept: application/x-yaml'])
    ch.setopt(ch.POSTFIELDS,'username=saltapi&password=123456&eauth=pam')
    ch.setopt(ch.HEADER,False)
    ch.perform()
    html = info.getvalue()
    token = html.split('\n')[-3].replace('\n','')
    token = token.split(' ')[3]
    info.close()
    ch.close()
    #print html
    return token


def get_jid(url,token,*args):
    ch = pycurl.Curl()
    ch.setopt(ch.URL,url)
    info = StringIO.StringIO()
    ch.setopt(ch.WRITEFUNCTION,info.write)
    ch.setopt(ch.POST,True)
    ch.setopt(ch.SSL_VERIFYPEER,0)
    ch.setopt(ch.SSL_VERIFYHOST,0)
    ch.setopt(ch.HTTPHEADER,['Accept: application/x-yaml','X-Auth-Token: {0}'.format(token)])
    data = 'client=local_async&tgt={0}&expr_form=nodegroup&fun={1}'.format(args[1],args[2])
    if len(args) >= 3:
        for key in range(3,len(args)):
            data += '&arg={0}'.format(args[key])
    ch.setopt(ch.POSTFIELDS,data)
    ch.setopt(ch.HEADER,False)
    ch.perform()
    html = info.getvalue()
    jid = html.split('\n')[1].replace('\n','')
    jid = jid.split('\'')[1]
    info.close()
    ch.close()
    #print html
    return jid


def get_jobinfo(url,token,jid):
    ch = pycurl.Curl()
    ch.setopt(ch.URL,url)
    info = StringIO.StringIO()
    ch.setopt(ch.WRITEFUNCTION,info.write)
    ch.setopt(ch.POST,True)
    ch.setopt(ch.SSL_VERIFYPEER,0)
    ch.setopt(ch.SSL_VERIFYHOST,0)
    ch.setopt(ch.HTTPHEADER,['Accept: application/x-yaml','X-Auth-Token: {0}'.format(token)])
    data = 'client=runner&fun=jobs.lookup_jid&jid={0}'.format(jid)
    ch.setopt(ch.POSTFIELDS,data)
    ch.setopt(ch.HEADER,False)
    ch.perform()
    html = info.getvalue()
    info.close()
    ch.close()
    print html

if __name__ == '__main__':
    url = 'https://116.228.151.160:1238'
    args = sys.argv[:]
    if len(args) < 3:
        print 'input 2 arguments at least'
        sys.exit(1)
    token = api_login(url)
    jid = get_jid(url,token,*args)
    if 'jetty.signal' in args and 'start' in args:
        time.sleep(20)
    else:
        time.sleep(2)
    get_jobinfo(url,token,jid)
