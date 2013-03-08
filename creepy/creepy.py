#coding=utf8

import urllib2
import re
from BeautifulSoup import *
import MySQLdb
import sys
"""
Login to Sina Weibo with cookie
"""
reload(sys)
sys.setdefaultencoding('utf8')  
COOKIE ='你的cookie'
HEADERS = {'cookie': COOKIE}
UID= COOKIE[COOKIE.find('uid')+4:COOKIE.find('uid')+14]
try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='weibodata',port=3309,charset='utf8',use_unicode=False)
    cur=conn.cursor()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def save_user(uuid,uid,name,common):
    fileHandle = open ( 'setup.ini','r+');
    now=int(fileHandle.readline())+1;
    point =int(fileHandle.readline())
    print now
    #print uuid,uid,name,common
    count=cur.execute('select * from relations where uid1=\''+str(uuid)+'\' and uid2=\''+str(uid)+'\'')
    if (count==0):
           
            cur.execute('insert into relations(uid1,uid2)values(\''+\
                        str(uuid)+'\',\''+str(uid)+'\')')
            conn.commit()

    count=cur.execute('select * from users where uid=\''+str(uid)+'\'')
    
    if (count==0):
            cs=common.encode('gbk', 'ignore').decode('gbk', 'ignore').encode('utf-8', 'ignore')
  
            #print cs
            cur.execute('insert into users(id,uid,name,common)values(\''+\
                        str(now)+'\',\''+str(uid)+'\',\''+str(name)+'\',\"'+\
                        cs +\
                        '\")')
            conn.commit()
            fileHandle.close()
            fileHandle = open ( 'setup.ini','w');
            fileHandle.write(str(now)+'\n'+str(point))
     
    fileHandle.close()

def creepy_myself():
    uid= COOKIE[COOKIE.find('uid')+4:COOKIE.find('uid')+14]
    url = 'http://weibo.com/'+str(uid)+'/myfollow?t=1&page=1'
    mainurl='http://weibo.com/'+str(uid)+'/myfollow?t=1&page='
    req = urllib2.Request(url, headers=HEADERS)
    text = urllib2.urlopen(req).read()
    mainSoup=BeautifulSoup(text)
    strs=str(mainSoup.find('div','lev2'));
    num=int(strs[strs.find('(')+1:strs.find(')')])

    lines=text.splitlines()  
    for line in lines:
         if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_relation_myf'):
            n = line.find('html":"')  
            if n > 0:  
                j = line[n + 7: -12].replace("\\", "")  
                soup =BeautifulSoup(j)
                follows=soup.findAll('div','myfollow_list S_line2 SW_fun')
                for follow in follows:
                    namess=follow.find('ul','info').find('a')['title']
                    temp_str=str(follow)
                    uiddd= temp_str[temp_str.find('uid')+4:temp_str.find('&')]
                    save_user(UID,uiddd,namess,follow.find('div','intro S_txt2').contents[0][6:])
                     
    for i in range(2,num/30+1):
        url = 'http://weibo.com/2421424850/myfollow?t=1&page='+str(i)
        req = urllib2.Request(url, headers=HEADERS)
        text = urllib2.urlopen(req).read()


        lines=text.splitlines()  
        for line in lines:
         if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_relation_myf'):
            n = line.find('html":"')  
            if n > 0:  
                j = line[n + 7: -12].replace("\\", "")  
                soup =BeautifulSoup(j)
                follows=soup.findAll('div','myfollow_list S_line2 SW_fun')
                for follow in follows:
                    namess=follow.find('ul','info').find('a')['title']
                    temp_str=str(follow)
                    uiddd =temp_str[temp_str.find('uid')+4:temp_str.find('&')]
                    save_user(UID,uiddd,namess,follow.find('div','intro S_txt2').contents[0][6:])

                    
                     
def creepy_others(uid):
    url="http://weibo.com/"+str(uid)+"/follow?page=";
    req = urllib2.Request(url, headers=HEADERS)
    text = urllib2.urlopen(req).read()

    
    mainSoup=BeautifulSoup(text.strip())
    lines=text.splitlines()
    num=1
    for line in lines:
         if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_relation_hisFollow'):
            n = line.find('html":"')
            if n > 0:  
                j = line[n + 7: -12].replace("\\n", "")
                j = j.replace("\\t","")
                j = j.replace("\\",'');
                soup=BeautifulSoup(j)
                strs=str(soup.find('div','patch_title'))
                num=int(strs[strs.find('关注了')+9:strs.find('人</div')]);
                follows=soup.findAll('li','clearfix S_line1')
                for follow in follows:
                    temp_str=str(follow)
                   # print temp_str
                    temp_uid=temp_str[temp_str.find('uid'):temp_str.find('&amp;')];
                    temp_soup=BeautifulSoup(temp_str);
                    temp_fnick=temp_soup.find('div').find('a')['title']
                    save_user(uid,temp_uid[4:],temp_fnick,str(temp_soup.find('div','info'))[18:-6]);

                #print num/20+2
                for i in range(2,num/20+1):
                     urls="http://weibo.com/"+str(uid)+"/follow?page="+str(i);
                     req = urllib2.Request(urls, headers=HEADERS)
                     text = urllib2.urlopen(req).read()
                     lines=text.splitlines()
                     for line in lines:
                        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_relation_hisFollow'):
                            n = line.find('html":"')
                            if n > 0:  
                                j = line[n + 7: -12].replace("\\n", "")
                                j = j.replace("\\t","")
                                j = j.replace("\\",'');
                                soup=BeautifulSoup(j)
                                strs=str(soup.find('div','patch_title'))
                                num=int(strs[strs.find('关注了')+9:strs.find('人</div')]);
                                follows=soup.findAll('li','clearfix S_line1')
                                for follow in follows:
                                    temp_str=str(follow)
                                   # print temp_str
                                    temp_uid=temp_str[temp_str.find('uid'):temp_str.find('&amp;')];
                                    temp_soup=BeautifulSoup(temp_str);
                                    temp_fnick=temp_soup.find('div').find('a')['title']
                                    save_user(uid,temp_uid[4:],temp_fnick,str(temp_soup.find('div','info'))[18:-6]);
                       
                                   

              
if __name__ == '__main__':
    #save_user('123','123','ads','212332231')
    #creepy_myself()
    
    while(1):
        fileHandle = open ( 'setup.ini','r+');
        now=int(fileHandle.readline());
        point =int(fileHandle.readline())+1;
        fileHandle.close()
        fileHandle = open ( 'setup.ini','w');
        fileHandle.write(str(now)+'\n'+str(point))
        fileHandle.close()
        cur.execute('select uid from users where id=\''+str(point)+'\'')
        uuid=cur.fetchone()[0];
        if len(uuid)==10:
            try:
                creepy_others(uuid)
            except Exception , e:
                pass
    
    cur.close()
    conn.close()
    
