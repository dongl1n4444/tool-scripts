import sys, time, os, re
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
import json
import time

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

fp_log = open("mtime_log.txt", "w")

LOG_OUTPUT = -1
LOG_NORMAL = 0
LOG_WARNING = 1
LOG_ERROR = 2

num_collect_total = 0
num_collect_success = 0
num_wish_total = 0
num_wish_success = 0

num_log_error = 0
num_log_waring = 0

user_email = ""
user_password = ""

def log(level, text):
    global num_log_error
    global num_log_waring

    print text
    if level == LOG_NORMAL:
        fp_log.write("::" + text + "\n")
    elif level == LOG_WARNING:
        num_log_waring = num_log_waring + 1
        fp_log.write("--" + str(num_log_waring) + ":" + text + "\n")
    elif level == LOG_ERROR:
        num_log_error = num_log_error + 1
        fp_log.write("xx" + str(num_log_error) + ":" +text + "\n")

def do_collect(ck):
    global num_collect_total
    global num_collect_success

    fp_collect = open("mtime_collect.txt", "w")
    # had seen
    url_seen = "http://my.mtime.com/movie/seen"

    is_break = False
    num_test = 0
    while url_seen and num_test < 2:
        resp2 = opener.open(url_seen)
        html2 = resp2.read()
        resp2.close()

        soup2 = BeautifulSoup(html2, "html.parser")
        tag_region = soup2.find(id='seenMoviesRegion')
        if not tag_region:
            log(LOG_ERROR, "cant find seen movies region\t" + url_seen)
            break
        ret2 = tag_region.findAll('ul', attrs={"class":"col2 clearfix mt25"})
        if len(ret2) <= 0:
            log(LOG_WARNING, "no seen movies\t" + url_seen)
            break
        for tag_movie in ret2:
            num_collect_total = num_collect_total + 1
            #
            uminfo = {}
            # movie info
            tag_info = tag_movie.find('li').find('a', attrs={"class":"movie_75img"})
            murl = tag_info["href"]
            uminfo["id"] = murl[murl.find('com/')+len('com/'):-1]
            uminfo["url"] = murl
            mtitle = tag_info["title"]
            uminfo["title"] = mtitle
            # maybe not >2 name
            if mtitle.find('/') > 0:
                uminfo["title1"] = mtitle[0:mtitle.find('/')]
                uminfo["title2"] = mtitle[mtitle.find('/')+1:-6]                
            else:
                uminfo["title1"] = mtitle[0:-6]
                uminfo["title2"] = ""
            uminfo["year"] = mtitle[-5:-1]
            # comment auto create
            req_rating = 3
            while req_rating > 0:
                url_rating = "http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&Ajax_CallBackArgument0=" + uminfo["id"]
                resp3 = opener.open(url_rating)
                html3 = resp3.read()
                resp3.close()
                json3 = json.loads(html3[html3.find('{'):-1])
                if json3["value"]:
                    req_rating = -1
                    uminfo["rating"] = json3["value"]["userRating"]["Rating"]
                    uminfo["comment"] = json3["value"]["userLastComment"]
                else:
                    req_rating = req_rating - 1
            if 'rating' not in uminfo.keys():
                log(LOG_ERROR, "not get movie rating\t" + uminfo["id"] +"-" + uminfo["title1"])
            else:
                num_collect_success = num_collect_success + 1

            print uminfo["title1"] + "-" + uminfo["year"]
            fp_collect.write(json.dumps(uminfo))
            fp_collect.write('\n')

        # find next page
        tag_page = soup2.find(id="PageNavigator")
        if not tag_page:
            log(LOG_WARNING, "no page navigator\t" + url_wish)
            break        
        tag_next = tag_page.find('a', attrs={"class":"ml10 next"})
        if tag_next:
            url_seen = "http://my.mtime.com" + tag_next["href"]
        else:
            url_seen = None
            break

        #num_test = num_test + 1 
        #
        time.sleep(0.1)

    # clean
    fp_collect.close()

def do_wish(ck):
    global num_wish_total
    global num_wish_success

    fp_wish = open("mtime_wish.txt", "w")
    # wish
    url_wish = "http://my.mtime.com/movie/wish"
    #url_wish = "http://my.mtime.com/movie/wish?&pageIndex=33"

    is_break = False
    num_test = 0    
    while url_wish and num_test < 3:
        resp2 = opener.open(url_wish)
        html2 = resp2.read()
        resp2.close()

        soup2 = BeautifulSoup(html2, "html.parser")
        tag_region = soup2.find(id='wishMoviesRegion')
        if not tag_region:
            log(LOG_ERROR, "cant find wish movies region\t" + url_wish)
            break
        tag_wishs = tag_region.findAll('div', attrs={"class":"table"})
        if len(tag_wishs) <= 0:
            log(LOG_WARNING, "no wish movies\t" + url_wish)
            break
        for tag_movie in tag_wishs:
            num_wish_total = num_wish_total + 1
            #
            uminfo = {}
            # movie info
            minfo = tag_movie.find('a', attrs={"class":"bold px14"})
            murl = minfo["href"]
            uminfo["id"] = murl[murl.find('com/')+len('com/'):-1]
            uminfo["url"] = murl
            mtitle = minfo["title"]
            uminfo["title"] = mtitle
            # maybe not >2 name
            if mtitle.find('/') > 0:
                uminfo["title1"] = mtitle[0:mtitle.find('/')]
                uminfo["title2"] = mtitle[mtitle.find('/')+1:-6]                
            else:
                uminfo["title1"] = mtitle[0:-6]
                uminfo["title2"] = ""               
            uminfo["year"] = mtitle[-5:-1]

            print uminfo["title1"] + "-" + uminfo["year"]
            fp_wish.write(json.dumps(uminfo))
            fp_wish.write('\n')
            #
            num_wish_success = num_wish_success + 1

        # find next page
        tag_page = soup2.find(id="PageNavigator")
        if not tag_page:
            log(LOG_WARNING, "no page navigator\t" + url_wish)
            break
        tag_next = tag_page.find('a', attrs={"class":"ml10 next"})
        if tag_next:
            url_wish = "http://my.mtime.com" + tag_next["href"]
        else:
            url_wish = None
            break

        #num_test = num_test + 1 
        #
        time.sleep(0.1)        

    # clean
    fp_wish.close()

def login_mtime():
    url_login = 'http://passport.mtime.com'
    params = {
        "redirectUrl" : "http://my.mtime.com",
        "email" : user_email,
        "password" : user_password,
    }

    response = opener.open(url_login, urllib.urlencode(params))
    print response.geturl()
    if response.geturl() == "http://passport.mtime.com":
        html = response.read()
        response.close()

        # exist vcode
        if re.search('<input id="login_vcode"', html):
            resp2 = opener.open("http://passport.mtime.com/Passport.p?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Passport.Pages.PassportService&Ajax_CallBackMethod=RefreshVcode")
            json2 = json.loads(resp2.read())
            resp2.close()

            #resp2 = opener.open(str(url2))
            #html2 = resp2.read()
            res = urllib.urlretrieve(str(json2['value']['src']), 'vcode_mtime.jpg')
            vcode = raw_input('input mtime vcode:')
            params["vcode"] = vcode
            params["vcodeId"] = str(json2['value']['id'])

            response = opener.open("http://passport.mtime.com/Reg/RegisterAndLogin.p?", urllib.urlencode(params))
            if response.geturl() == "http://my.mtime.com/":
                response.close() 
                return True
            else:
                response.close() 
                return False
    elif response.geturl() == "http://my.mtime.com/":
        return True
    
    return False

if __name__ == '__main__':

    log(LOG_NORMAL, "-------start-------")
    log(LOG_NORMAL, time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # read user email and password
    fp_logininfo = open("info_login.txt", 'r')
    line = fp_logininfo.readline()
    while line:
        line = line.strip()
        if line == "[mtime]":
            line = fp_logininfo.readline()
            user_email = line[line.find('=')+1:].strip()
            line = fp_logininfo.readline()
            user_password = line[line.find('=')+1:].strip()
            #
            break
        # next
        line = fp_logininfo.readline() 
    fp_logininfo.close()

    # login in
    ret_login = login_mtime()
    if ret_login:
        print "login success"
        p={"ck":""}
        c = [c.value for c in list(cookie) if c.name == 'ck']               
        if len(c) > 0:
            p["ck"] = c[0].strip('"')

        # collect
        do_collect(p["ck"])

        # wish
        do_wish(p["ck"])
    else:
        log(LOG_ERROR, "login fail")

    log(LOG_NORMAL, "\n-------end-------")
    log(LOG_NORMAL, time.strftime("%Y-%m-%d %H:%M:%S"))
    log(LOG_NORMAL, "error:" + str(num_log_error) + "\t\t" + "waring:" + str(num_log_waring))
    log(LOG_NORMAL, "collect:" + str(num_collect_success) + "/" + str(num_collect_total))
    log(LOG_NORMAL, "wish:" + str(num_wish_success) + "/" + str(num_wish_total))

    # clean
    fp_log.close()