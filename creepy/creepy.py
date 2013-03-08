#coding=utf8

import urllib2
import re
from BeautifulSoup import *
import MySQLdb
import sys
"""
Login to Sina Weibo with cookie
setdefaultencoding 用于对中文编码的处理
"""
reload(sys)
sys.setdefaultencoding('utf8')  
COOKIE ='你的cookie'
HEADERS = {'cookie': COOKIE}
UID= COOKIE[COOKIE.find('uid')+4:COOKIE.find('uid')+14]

'''
    尝试连接数据库，以供保存诗句
'''
try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='weibodata',port=3309,charset='utf8',use_unicode=False)
    cur=conn.cursor()
except MySQLdb.Error,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])



def save_user(uuid,uid,name,common):
    '''
        save_user(uuid,uid,name,common)
        用于保存诗句，uuid->uid是用户关系，uuid关注uid
        uid,name,common是将要保存的用户信息
        setup.ini中保存有两个数字
        第一个是now我对当前用户的编号
        第二个point是当前正在扫描的用户的编号
        你可以把它们看作是一个队列的两个指针
    '''
    fileHandle = open ( 'setup.ini','r+');
    now=int(fileHandle.readline())+1;
    point =int(fileHandle.readline())
    print now
    #print uuid,uid,name,common
    #保存用户关系信息
    count=cur.execute('select * from relations where uid1=\''+str(uuid)+'\' and uid2=\''+str(uid)+'\'')
    if (count==0):
           
            cur.execute('insert into relations(uid1,uid2)values(\''+\
                        str(uuid)+'\',\''+str(uid)+'\')')
            conn.commit()

    count=cur.execute('select * from users where uid=\''+str(uid)+'\'')
    #保存用户信息
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
    '''
        这是用来扫描你自己的关注列表的
        我想着得有个开头，所以第一次使用时应调用这个函数为队列添加一些用户再作扩展
    '''
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
    '''
        扫描制定uid用户的信息
        和上面一样代码有冗余
        因为要先得到这个用户的关注人数，来计算一共有多少页数据
    '''
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
    '''
        虽然很谨慎地处理了中文编码，但每过一段时间还是会有一些问题
        于是抛掉了所有异常，防止程序中断
    '''
    while(1):
        '''
            首先取得队列的尾指针，也就是point
            根据point从数据库中找到uid，然后creepy_others(uuid)
        '''
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
    
