# -*- coding:utf-8 -*-
import sys, time, os, re
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
import json
import math

loginurl = 'https://www.douban.com/accounts/login'
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

fp_logininfo = open("info_login.txt", 'r')
line = fp_logininfo.readline()
while line:
    line = line.strip()
    print line
    if line == "[douban]":
        line = fp_logininfo.readline()
        str_email = line[line.find('=')+1:].strip()
        line = fp_logininfo.readline()
        str_password = line[line.find('=')+1:].strip()
        #
        break
    # next
    line = fp_logininfo.readline()

params = {
    "form_email" : "",
    "form_password" : "",
    "source": "index_nav"
}

response = opener.open(loginurl, urllib.urlencode(params))

if response.geturl() == "https://www.douban.com/accounts/login":
    html = response.read()
    response.close()
       
    #
    imgurl = re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
    if imgurl:
        url = imgurl.group(1)
        res = urllib.urlretrieve(url, 'vcode_douban.jpg')
        captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
        if captcha:
            vcode = raw_input('input douban vcode:')
            params["captcha-solution"] = vcode
            params["captcha-id"] = captcha.group(1)
            params["login"] = "登录"

            response = opener.open(loginurl, urllib.urlencode(params))
            if response.geturl() == "http://www.douban.com/":
                print "login success"
                p={"ck":""}
                c = [c.value for c in list(cookie) if c.name == 'ck']               
                if len(c) > 0:
                    p["ck"] = c[0].strip('"') 
                response.close()
                
                # read file
                fp_mtime_collect = open("mtime_collect.txt", 'r')
                line = fp_mtime_collect.readline()
                while line:
                    line = json.loads(line)
                    #url_movie_wish="http://movie.douban.com/mine?status=wish"
                    # movie_name = eval("u" + '"\u5927\u8bdd\u897f\u6e38"')
                    movie_name = line["title1"]
                    movie_name = urllib.quote(movie_name.encode('utf-8'))

                    movie_year = str(line["year"])
                    movie_rating = int(math.ceil(line["rating"] / 2.0))
                    if movie_rating > 5:
                        movie_rating = 5
                    movie_comment = line["comment"].encode('utf-8')
                    
                    url_movie_search = "http://movie.douban.com/subject_search?search_text=" + movie_name + "+" + movie_year
                    #params_search = {
                    #    "search_text" : "love",
                    #}
                    #resp1 = opener.open(url_movie_search, urllib.urlencode(params_search))
                    resp1 = opener.open(url_movie_search)
                    html1 = resp1.read()
                    resp1.close()
                    
                    soup1 = BeautifulSoup(html1, "html.parser")
                    tag_rets = soup1.find(id='content').findAll('table')
                    if len(tag_rets) >= 1:
                        tag_movie = tag_rets[0]
                        minfo = {}
                        tag_movie_info1 = tag_movie.find('a', attrs={"class":"nbg"})
                        minfo["title"] = tag_movie_info1["title"]
                        mhref = tag_movie_info1["href"]
                        minfo["id"] = mhref[mhref.find("subject/")+len("subject/"):-1]
                        
                        url_movie_interest = "http://movie.douban.com/j/subject/%s/interest" %minfo["id"]
                        params_interest = {
                            "ck" : p["ck"],
                            "rating" : str(movie_rating),
                            "comment" : movie_comment,
                            "interest" : "collect",
                            "tags" : "",
                            #"share-shuo" : "douban",
                            "foldcollect" : "U"
                        }
                        
                        resp2 = opener.open(url_movie_interest, urllib.urlencode(params_interest))
                        html2 = resp2.read()
                        if html2 and json.loads(html2)["r"] == 0:
                            print "--success--mtime/" + line["title1"] + "/" + line["year"] + "--" + minfo["id"] + "/" + minfo["title"]
                        else:
                            print "xxerror--mtime/" + line["title1"] + "/" + line["year"] + "--" + minfo["id"] + "/" + minfo["title"] 
                        resp2.close()                     
                    else:
                        print "xxnotfind--" + line["title1"] + "-" + line["year"]
                        
                    #
                    line = fp_mtime_collect.readline()
                                    

                """
                m = re.search('<li class="title"> <a href="(.+?)" class', html)

                m= re.search('<input type="hidden" name="topic_id" value="(.+?)">', html) 
                p["topic_id"] = m.group(1)
                m= re.search('<input type="hidden" name="topic_id_sig" value="(.+?)">', html) 
                p["topic_id_sig"] = m.group(1)
                p["rev_title"] = 'title'
                p["rev_text"] = 'send body'
                p["rev_submit"] = '好了，发言'

                request=urllib2.Request(addtopicurl)
                request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11")
                request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
                request.add_header("Origin", "http://www.douban.com")
                request.add_header("Referer", "http://www.douban.com/group/python/new_topic")
                opener.open(request, urllib.urlencode(p))
                """