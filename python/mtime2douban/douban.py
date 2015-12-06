# -*- coding:utf-8 -*-
import sys, time, os, re
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
import json
import math
import time

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

fp_log = open("douban_log.txt", "a")

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

# count for douban robot
count_robot = 0
num_robot_count = 80
time_robot_sleep = 60

def log(level, text):
    global num_log_error
    global num_log_waring

    print text
    if type(text) == type(u""):
        text = text.encode('utf-8')
    
    if level == LOG_NORMAL:
        fp_log.write("::" + text + "\n")
    elif level == LOG_WARNING:
        num_log_waring = num_log_waring + 1
        fp_log.write("--" + str(num_log_waring) + ":" + text + "\n")
    elif level == LOG_ERROR:
        num_log_error = num_log_error + 1
        fp_log.write("xx" + str(num_log_error) + ":" + text + "\n")

def search_movie(movie_name1, movie_name2, movie_year):
    global count_robot
    # search rule
    # 1 - title1 + year
    # 2 - title1
    # 3 - title2 + year
    # 4 - title2
    num_search_total = 4   
    num_search_count = 0
    
    tag_tables = None
    while num_search_count < num_search_total:
        num_search_count = num_search_count + 1
        url_movie_search = "http://movie.douban.com/subject_search?search_text="
        if num_search_count == 1:
            url_movie_search = url_movie_search + movie_name1 + "+" + str(movie_year)
        elif num_search_count == 2:
            url_movie_search = url_movie_search + movie_name1        
        elif num_search_count == 3:
            if movie_name2 == "":
                break
            else:
                url_movie_search = url_movie_search + movie_name2 + "+" + str(movie_year)
        elif num_search_count == 4:
            if movie_name2 == "":
                break
            else:
                url_movie_search = url_movie_search + movie_name2
        
        count_robot = count_robot + 1
        resp1 = opener.open(url_movie_search)
        html1 = resp1.read()
        resp1.close()

        soup1 = BeautifulSoup(html1, "html.parser")
        tag_content = soup1.find(id='content')
        if not tag_content:
            log(LOG_WARNING, "cant find content\t" + url_movie_search)
            break            
        tag_tables = tag_content.findAll('table')
        if len(tag_tables) > 0:
            return tag_tables
        else:
            log(LOG_WARNING, "cant search movie\t" + url_movie_search)

    return None

def do_collect(ck):
    global num_collect_total
    global num_collect_success
    global count_robot
    # read file
    fp_mtime_collect = open("mtime_collect.txt", 'r')
    fp_douban_collect = None
    if os.path.exists("douban_collect.txt"):
        fp_douban_collect = open("douban_collect.txt", "r+")
    else:
        fp_douban_collect = open("douban_collect.txt", "w+")
    # num test when debug
    num_test = 2
    
    idx_line = 0
    line = fp_douban_collect.readline()
    if line:
        idx_line = int(line)
    
    try:
        lines = fp_mtime_collect.readlines()
        while idx_line < len(lines) and num_test > 0:
            #num_test = num_test - 1
            if count_robot >= num_robot_count:
                print "---sleep %d---"%time_robot_sleep
                count_robot = 0
                time.sleep(time_robot_sleep)
            #
            line = json.loads(lines[idx_line])
            idx_line = idx_line + 1
            #url_movie_wish="http://movie.douban.com/mine?status=wish"
            # movie_name = eval("u" + '"\u5927\u8bdd\u897f\u6e38"')
            movie_name1 = urllib.quote(line["title1"].encode('utf-8'))
            movie_name2 = urllib.quote(line["title2"].encode('utf-8'))
            movie_year = str(line["year"])
            # rating rule
            # 8.7 - 10 -> 5
            # 7.5 - 8.7 -> 4
            # 6.5 - 7.5 -> 3
            # 5 - 6.5 -> 2
            # 0 - 5 -> 1
            # movie_rating = int(math.ceil(line["rating"] / 2.0))
            movie_rating = line["rating"]
            if movie_rating >= 8.7:
                movie_rating = 5
            elif movie_rating >= 7.5:
                movie_rating = 4
            elif movie_rating >= 6.5:
                movie_rating = 3
            elif movie_rating >= 5:
                movie_rating = 2
            else:
                movie_rating = 1
            movie_comment = line["comment"].encode('utf-8')
    
            # search movie
            tag_tables = search_movie(movie_name1, movie_name2, movie_year)
            if tag_tables:
                num_collect_total = num_collect_total + 1
                # HARD CODE: find first search movie result
                tag_movie = tag_tables[0]
                
                minfo = {}
                tag_movie_info1 = tag_movie.find('a', attrs={"class":"nbg"})
                minfo["title"] = tag_movie_info1["title"]
                mhref = tag_movie_info1["href"]
                minfo["id"] = mhref[mhref.find("subject/")+len("subject/"):-1]
                
                # check whether had collected
                tag_gacts = tag_movie.find('span', attrs={"class":"gact"})
                if tag_gacts and len(tag_gacts) != 0:
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
        
                    count_robot = count_robot + 1
                    resp2 = opener.open(url_movie_interest, urllib.urlencode(params_interest))
                    html2 = resp2.read()
                    if html2 and json.loads(html2)["r"] == 0:
                        num_collect_success = num_collect_success + 1
                        log(LOG_NORMAL, "success collect\t" + line["id"] + "/" + line["title1"] + "-" + minfo["id"] + "/" + minfo["title"])
                    else:
                        log(LOG_ERROR, "fail collect\t" + line["id"] + "/" + line["title1"] + "-" + minfo["id"] + "/" + minfo["title"])
                    resp2.close()   
                else:
                    num_collect_success = num_collect_success + 1
                    log(LOG_WARNING, "had collect movie-" + line["id"] + "/" + line["title1"] + "-" + minfo["id"] + "/" + minfo["title"])
            else:
                log(LOG_ERROR, "cant find moive-" + line["id"] + "/" + line["title1"])
    
            #
            # line = fp_mtime_collect.readline()
            #
            time.sleep(0.1)  
    finally:
        print "count robot %d" %count_robot
        fp_mtime_collect.close()
        fp_douban_collect.seek(0)
        fp_douban_collect.write(str(idx_line - 2))
        fp_douban_collect.close()

def do_wish(ck):
    global num_wish_total
    global num_wish_success
    global count_robot
    # read file
    fp_mtime_wish = open("mtime_wish.txt", 'r')
    fp_douban_wish = None
    if os.path.exists("douban_wish.txt"):
        fp_douban_wish = open("douban_wish.txt", "r+")
    else:
        fp_douban_wish = open("douban_wish.txt", "w+")
    # num test when debug
    num_test = 10
    
    idx_line = 0
    line = fp_douban_wish.readline()
    if line:
        idx_line = int(line)
    
    try:
        lines = fp_mtime_wish.readlines()
        while idx_line < len(lines) and num_test > 0:
            #num_test = num_test - 1
            if count_robot >= num_robot_count:
                print "---sleep %d---"%time_robot_sleep
                count_robot = 0
                time.sleep(time_robot_sleep)
            #
            line = json.loads(lines[idx_line])
            idx_line = idx_line + 1
            #url_movie_wish="http://movie.douban.com/mine?status=wish"
            # movie_name = eval("u" + '"\u5927\u8bdd\u897f\u6e38"')
            movie_name1 = urllib.quote(line["title1"].encode('utf-8'))
            movie_name2 = urllib.quote(line["title2"].encode('utf-8'))
            movie_year = str(line["year"])
    
            # search movie
            tag_tables = search_movie(movie_name1, movie_name2, movie_year)
            if tag_tables:
                num_wish_total = num_wish_total + 1
                # HARD CODE: find first search movie result
                tag_movie = tag_tables[0]
                
                minfo = {}
                tag_movie_info1 = tag_movie.find('a', attrs={"class":"nbg"})
                minfo["title"] = tag_movie_info1["title"]
                mhref = tag_movie_info1["href"]
                minfo["id"] = mhref[mhref.find("subject/")+len("subject/"):-1]
                
                # check whether had collected
                tag_gacts = tag_movie.findAll('span', attrs={"class":"gact"})
                if tag_gacts and len(tag_gacts) == 2:
                    url_movie_interest = "http://movie.douban.com/j/subject/%s/interest" %minfo["id"]
                    params_interest = {
                        "ck" : p["ck"],
                        "comment" : "",
                        "interest" : "wish",
                        "tags" : "",
                        #"share-shuo" : "douban",
                        "foldcollect" : "U"
                    }
        
                    count_robot = count_robot + 1
                    resp2 = opener.open(url_movie_interest, urllib.urlencode(params_interest))
                    html2 = resp2.read()
                    if html2 and json.loads(html2)["r"] == 0:
                        num_wish_success = num_wish_success + 1
                        log(LOG_NORMAL, "success wish\t" + line["id"] + "/" + line["title1"] + "-" + minfo["id"] + "/" + minfo["title"])
                    else:
                        log(LOG_ERROR, "fail wish\t" + line["id"] + "/" + line["title1"] + "-" + minfo["id"] + "/" + minfo["title"])
                    resp2.close()   
                else:
                    num_wish_success = num_wish_success + 1
                    log(LOG_WARNING, "had wish movie-" + line["id"] + "/" + line["title1"] + "-" + minfo["id"] + "/" + minfo["title"])
            else:
                log(LOG_ERROR, "cant find moive-" + line["id"] + "/" + line["title1"])
    
            #
            # line = fp_mtime_collect.readline()
            #
            time.sleep(0.1)  
    finally:
        print "count robot %d" %count_robot
        fp_mtime_wish.close()
        fp_douban_wish.seek(0)
        fp_douban_wish.write(str(idx_line - 2))
        fp_douban_wish.close()    

def login_douban():
    url_login = 'https://www.douban.com/accounts/login'
    params = {
        "form_email" : user_email,
        "form_password" : user_password,
        "source": "index_nav"
    }

    response = opener.open(url_login, urllib.urlencode(params))
    print response.geturl()
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

                response = opener.open(url_login, urllib.urlencode(params))
                if response.geturl() == "http://www.douban.com/":
                    response.close()
                    return True


    elif response.geturl() == "http://www.douban.com/":
        response.close()
        return True

    return False

if __name__ == '__main__':
    try:
        log(LOG_NORMAL, "-------start-------")
        log(LOG_NORMAL, time.strftime("%Y-%m-%d %H:%M:%S"))
    
        # read user email and password
        fp_logininfo = open("info_login.txt", 'r')
        line = fp_logininfo.readline()
        while line:
            line = line.strip()
            if line == "[douban]":
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
        ret_login = login_douban()
        if ret_login:
            print "login success"
            p={"ck":""}
            c = [c.value for c in list(cookie) if c.name == 'ck']               
            if len(c) > 0:
                p["ck"] = c[0].strip('"')
    
            # collect
            #do_collect(p["ck"])
            # wish
            do_wish(p["ck"])
            
        else:
            log(LOG_ERROR, "login fail")
    
        log(LOG_NORMAL, "\n-------end-------")
        log(LOG_NORMAL, time.strftime("%Y-%m-%d %H:%M:%S"))
        log(LOG_NORMAL, "error:" + str(num_log_error) + "\t\t" + "waring:" + str(num_log_waring))
        log(LOG_NORMAL, "collect:" + str(num_collect_success) + "/" + str(num_collect_total))
        log(LOG_NORMAL, "wish:" + str(num_wish_success) + "/" + str(num_wish_total))
        
    finally:
        # clean
        fp_log.close()