import sys, time, os, re
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
import json
import math
import time

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

# error questions id list
# 2015/12/9
"""
qidlist_error = [4,23,51,72,75,79,84,86,90,121,122,130,152,156,159,185,211,214,226,227,236,238,244,246,247,248,\
                 250,259,260,266,267,269,271,266,267,269,271,279,280,293,295,306,315,316,317,319,321,328,329,335,\
                 349,355,356,360,382,425,461,468,469,480,489,493,498,500,501,543,549,552,554,564,590,597,604,611,\
                 620,635,639,645,649,665,669,682,689,692,699,703,710,715,729,732,738,749,763,765,769,771,774,796,798,\
                 801,802,804,806,812,822,828,831,853,864,890,892,899,946,958,980,1000,1002,1004,1013,1030,1043,1047,1080,1082,\
                 1086,1088,1106,1109,1112,1116,1127,1129,1134,1136,1145,1146,1158,1164,1180,1194,1222,1224]
"""
qidlist_error = [800300,802200,805000,807100,807400,807800,808300,808500,808900,812000,812100,812900,815100,815500,815800,818400,821000,821300,\
                 822500,822600,823500,823700,824300,824500,824600,824700,824900,825800,825900,826500,826600,826800,827000,827800,827900,829200,\
                 829400,830500,831400,831500,831600,831800,832000,832700,832800,833400,834800,835400,835500,835900,1093900,1119900,1123500,1124200,1124300,1125400,\
                 1126300,1126700,1127200,1127400,1127500,838700,839300,839600,839800,840800,843400,844100,844800,845500,846400,847900,848300,848900,849300,850900,\
                 851300,852600,853300,853600,854700,855400,855900,857300,857600,858200,859300,860700,860900,861300,861500,861800,864000,864200,864500,864600,864800,865000,\
                 865600,866600,867200,867500,869500,870600,873200,873400,874100,878800,880000,882200,884200,884400,884600,885500,1098500,1099800,1100200,1131000,1131200,1131600,\
                 1131800,1133600,1133900,1134200,1134600,887200,887400,887900,888100,889000,889100,890300,890900,892500,893900,896700,896900]

#url_test = "http://www.jiakaobaodian.com/mnks/exercise/0-c1-kemu1-chengdu.html?id="
url_question = "http://api2.jiakaobaodian.com/api/open/question/question-list.htm"

file_name = "ret_" + time.strftime("%Y%m%d") + ".md"
fp_output = open(file_name, "w")

def open_url_of_question(qid):
    try:
        shiti = {}
        
        """
        if qid < 1022:
            qid = 800000 + (qid - 1) * 100
        elif qid < 1065:
            qid = 1097700 + (qid - 1022) * 100
        else:
            qid = 1129500 + (qid - 1065) * 100
        """
        
        #url_question = url_test + str(qid)
        
        params = {
            "_r" : "19883872540018636094",
            "questionIds" : str(qid)
        }   
        
        #request=urllib2.Request(url_question)
        #request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11")
        #request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
        #request.add_header("Origin", "http://www.douban.com")
        #request.add_header("Referer", "http://www.douban.com/group/python/new_topic")       
        
        response = opener.open(url_question, urllib.urlencode(params))
        html = response.read()
        response.close() 
        
        kk = json.loads(html)
        #print kk["data"][0]["answer"]
        shiti = {}
        shiti["timu"] = kk["data"][0]["question"].encode('utf-8')
        
        shiti["daan"] = {}
        for i in ["optionA","optionB","optionC","optionD","optionE","optionF","optionG","optionH"]:
            if kk["data"][0][i] == None or kk["data"][0][i] == "":
                break
            shiti["daan"][i[-1:]] = kk["data"][0][i].encode('utf-8')
            print shiti["daan"][i[-1:]]
        
        if "mediaContent" in kk["data"][0].keys():
            shiti["img"] = kk["data"][0]["mediaContent"]
            
        if "explain" in kk["data"][0].keys():
            shiti["fenxi"] = kk["data"][0]["explain"].encode('utf-8')
            
        for i in range(4, 12):
            if kk["data"][0]["answer"] == (1 << i):
                shiti["answer"] = i - 4
        
        if shiti["answer"] >= len(shiti["daan"].keys()):
            raise "no answer"
        
        return shiti
        
        """
        soup = BeautifulSoup(html, "html.parser")
                                                    
        tag_shiti = soup.find('div', attrs={"class":"shiti-container"})
        if tag_shiti:
            shiti["timu"] = tag_shiti.find('p', attrs={"class":"shiti-content"}).get_text()
            shiti["daan"] = []
            
            tag_daan = tag_shiti.find('div', attrs={"data-item":"options-container"})
            if not tag_daan:
                raise "no danan item"
    
            for itm in tag_daan.findAll('p'):
                if not itm.find('span'):
                    raise "option no span"
                shiti["daan"].append(itm.find('span').get_text())
                
            opt_dui = tag_daan.find('p', attrs={"class":"dui"})
            shiti["dui"] = opt_dui
            
            tag_img = tag_shiti.find('div', attrs={"data-item":"media-container"})
            if tag_img:
                shiti["img"] = tag_img.find('img')["src"]
        else:
            raise "no shiti container"
        
        # fenxi
        tag_fenxi = soup.find('div', attrs={"class":"explain-container fenxi-container"})
        if not tag_fenxi:
            raise "no fenxi container"
        shiti["fenxi"] = tag_fenxi.find('p', attrs={"data-item":"explain-content"}).find('p').get_text()
        """
        
        
    except:
        print "error"

if __name__ == '__main__':
    try:
        if not os.path.exists("pic"):
            os.mkdir("pic")
        
        for qid in qidlist_error:
            shiti = open_url_of_question(qid)     
            #
            fp_output.write("###"+str(qid)+":"+shiti["timu"]+"\n\n")
            if "img" in shiti.keys():
                img_name = shiti["img"][shiti["img"].rfind('/')+1:]
                if not os.path.exists("pic/"+img_name):
                    res = urllib.urlretrieve(shiti["img"], "pic/"+img_name)
                #
                fp_output.write("![](pic/"+img_name+")\n\n")
            
            keys = sorted(shiti["daan"].keys())
            for k in keys:
                fp_output.write("####"+k+"."+shiti["daan"][k]+"\n\n")
            
            fp_output.write("###answer:" + ["A","B","C","D","E","F","G","H"][shiti["answer"]]+"\n\n")
            if "fenxi" in shiti.keys():
                fp_output.write("####explain:"+shiti["fenxi"]+"\n\n")
                
            fp_output.write("\n\n")
            
    finally:
        # clean
        fp_output.close()