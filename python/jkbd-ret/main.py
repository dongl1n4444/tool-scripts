import sys, time, os, re
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
import json
import math
import time

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

# error questions id list
qidlist_error = [1,2,195]

#url_test = "http://www.jiakaobaodian.com/mnks/exercise/0-c1-kemu1-chengdu.html?id="
url_question = "http://api2.jiakaobaodian.com/api/open/question/question-list.htm"

file_name = "ret_" + time.strftime("%Y%m%d") + ".md"
fp_output = open(file_name, "w")

def open_url_of_question(qid):
    try:
        shiti = {}
        
        qid = 800000 + (qid - 1) * 100
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
            
        shiti["answer"] = kk["data"][0]["answer"] / 16 - 1
        
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