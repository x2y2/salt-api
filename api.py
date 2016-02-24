#!/usr/bin/python
#salt-api
#wangpei
#20160215

import sys
import pycurl
import StringIO
import time
import json

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
    #print token
    return token


def get_jid(url,token,*args):
    tgt = args[1]
    fun = args[2]
    ch = pycurl.Curl()
    ch.setopt(ch.URL,url)
    info = StringIO.StringIO()
    ch.setopt(ch.WRITEFUNCTION,info.write)
    ch.setopt(ch.POST,True)
    ch.setopt(ch.SSL_VERIFYPEER,0)
    ch.setopt(ch.SSL_VERIFYHOST,0)
    ch.setopt(ch.HTTPHEADER,['Accept: application/x-yaml','X-Auth-Token: {0}'.format(token)])
    data = 'client=local_async&tgt={0}&expr_form=nodegroup&fun={1}'.format(tgt,fun)
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
    #print jid
    return jid


def get_jobinfo(url,token,jid):
    ch = pycurl.Curl()
    #ch.setopt(ch.URL,url+'/jobs/{0}'.format(jid))
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

def job_state(url,token,jid):
    ch = pycurl.Curl()
    ch.setopt(ch.URL,url)
    info = StringIO.StringIO()
    ch.setopt(ch.WRITEFUNCTION,info.write)
    ch.setopt(ch.POST,True)
    ch.setopt(ch.SSL_VERIFYPEER,0)
    ch.setopt(ch.SSL_VERIFYHOST,0)
    ch.setopt(ch.HTTPHEADER,['Accept: application/json','X-Auth-Token: {0}'.format(token)])
    data = 'client=runner&fun=jobs.print_job&jid={0}'.format(jid)
    ch.setopt(ch.POSTFIELDS,data)
    ch.setopt(ch.HEADER,False)
    ch.perform()
    html = info.getvalue()
    ret = json.loads(html)
    target = ret['return'][0][jid]['Target'].split(',')
    ltarget = len(target)
    result = ret['return'][0][jid]['Result']
    lresult = len(result)
    info.close()
    ch.close()
    #print html
    #print target
    #print result
    if ltarget == lresult:
        return result
    else:
        return

if __name__ == '__main__':
    url = 'http://116.228.151.160:1238'
    args = sys.argv[:]
    if len(args) < 3:
        print 'input 2 arguments at least'
        sys.exit(1)
    token = api_login(url)
    jid = get_jid(url,token,*args)
    for timer in range(300):
        if timer < 300:
            state = job_state(url,token,jid)
            if state:
                get_jobinfo(url,token,jid)
                break
            else:
                time.sleep(1)
                timer = timer +1
                continue

