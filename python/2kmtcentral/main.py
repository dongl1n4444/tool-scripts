# -*- coding:utf-8 -*-

import sys
import urllib, urllib2
from bs4 import BeautifulSoup
from bs4 import element
import re
import xlsxwriter
import time
import datetime
import urllib
import lxml

allPlayerData = {}
allPlayerUrls = []

infoKeys = ['Name','Theme','Position','Team','Height','Weight','Age','From']
attrKeys = []
rankKeys = []
tendKeys = []

totalPlayerUrlNum = 0

def updateKeys(group, key):
    if group.count(key) == 0:
        group.append(key)

def filterAttrKey(val):
    for k in ['def.', 'Def.', 'attr.', 'Off.']:
        val = val.replace(k, '')
    tmp = val.find(' +')
    if tmp != -1:
        val = val[0:tmp]
    return val.strip()

def filterInfoVal(val):
    #return val.replace('\\', '')
    return val

def saveToExcel():
    try:
        outfile = 'output_' + datetime.datetime.now().strftime("%Y%m%d_%H%M") + '.xlsx'
        wbk = xlsxwriter.Workbook(outfile)
        sheet = wbk.add_worksheet("sheet 1")
        nrow = 0
        ncol = 0
        colKeys = ['Id', 'Url']
        #
        for kk in infoKeys:
            colKeys.append(kk)
        for kk in rankKeys:
            colKeys.append(kk)
        for kk in attrKeys:
            colKeys.append(kk)
        for kk in tendKeys:
            colKeys.append(kk)
        for kk in colKeys:
            sheet.write(nrow, ncol, kk)
            ncol = ncol + 1

        #
        idx = 0
        for url in allPlayerUrls:
            print 'x-' + "%.2f" % ((idx + 1) * 1.0 / totalPlayerUrlNum * 100) + '% save url: ' + url
            nrow = nrow + 1
            idx = idx + 1
            ncol = 0
            datPlayer = allPlayerData[url]
            for kk in colKeys:
                if kk == 'Id':
                    sheet.write(nrow, ncol, str(idx))
                elif kk == 'Url':
                    sheet.write(nrow, ncol, url)
                elif kk in datPlayer['info'].keys():
                    sheet.write(nrow, ncol, datPlayer['info'][kk])
                elif kk in datPlayer['attr'].keys():
                    sheet.write(nrow, ncol, datPlayer['attr'][kk])
                elif kk in datPlayer['rank'].keys():
                    sheet.write(nrow, ncol, datPlayer['rank'][kk])
                elif kk in datPlayer['tend'].keys():
                    sheet.write(nrow, ncol, datPlayer['tend'][kk])
                # else:
                #     sheet.write(nrow, ncol, 'N/A')
                ncol = ncol + 1

        #
        wbk.close()

    except Exception as err:
        print 'Error: ' + err

def parsePlayerUrl(url):
    try:
        datPlayer = {}

        nurl = urllib.quote(url.encode('utf-8'), ':/')
        rsp = urllib2.urlopen(nurl)
        html = rsp.read()

        soup = BeautifulSoup(html, 'lxml')

        # infos
        infos = {}
        datPlayer['info'] = infos

        tagPlayerView = soup.find('div', id='player-view')
        tagPlayerInfos = tagPlayerView.find('div', class_='col-xs-12 col-md-8')
        name = tagPlayerInfos.div.header.h1.text
        infos['Name'] = filterInfoVal(name)

        tagInfos = tagPlayerInfos.find('section', class_='information')
        for tagInfo in tagInfos.find_all('div', class_=re.compile('^col-xs-')):
            if tagInfo.h6 and str(tagInfo.h6.text) in infoKeys:
                infoKey = str(tagInfo.h6.text)
                infos[infoKey] = filterInfoVal(tagInfo.span.text)

        # attrs
        attrs = {}
        datPlayer['attr'] = attrs

        tagAttrContainer = soup.find('div', class_='attributes-container')
        for tagDiv in tagAttrContainer.find_all('div'):
            # for tagSection in tagDiv.find_all('section', class_='total'):
            for tagSection in tagDiv.find_all('section'):
                # parse attr header
                tagHeader = tagSection.find('h4', class_='attribute-header')
                if tagHeader and len(tagHeader.contents) > 0:
                    #key = tagHeader.strong.get_text()
                    #val = tagHeader.find('span', class_='attribute-box').get_text()
                    #infos[key] = val
                    val, key = tagHeader.text.split(' ', 1)
                    key = filterAttrKey(key)
                    attrs[key] = val
                    updateKeys(attrKeys, key)

                # parse attr list
                tagList = tagSection.find('ul', class_='attribute-list')
                if tagList:
                    for tagLi in tagList.find_all('li', class_='attribute'):
                        # key = ""
                        # val = 0
                        # for cot in tagLi.contents:
                        #     if isinstance(cot, element.NavigableString):
                        #         key = key + cot
                        #     #elif type(cot) == type(BeautifulSoup.element.Tag):
                        #     else:
                        #         if cot['class'][0] == 'attribute-box':
                        #             val = cot.get_text()
                        #         else:
                        #             key = key + cot.get_text()
                        val, key = tagLi.text.split(' ', 1)
                        key = filterAttrKey(key)
                        attrs[key] = val
                        updateKeys(attrKeys, key)

        # ranking
        ranks = {}
        datPlayer['rank'] = ranks

        tagRanks = soup.find('section', class_='rankings')
        for tagRank in tagRanks.find_all('li', title=re.compile('^Top')):
            key = tagRank.span.text
            val = str(tagRank.contents[0])
            ranks[key] = val
            updateKeys(rankKeys, key)

        # tendencies
        tends = {}
        datPlayer['tend'] = tends

        rsp = urllib2.urlopen(nurl + "/tendencies")
        html = rsp.read()
        soup = BeautifulSoup(html, 'lxml')

        tagAttrContainer = soup.find('div', class_='attributes-container')
        for tagSection in tagAttrContainer.find_all('section'):
            # parse attr header
            # tagHeader = tagSection.find('h4', class_='attribute-header')
            # if tagHeader and len(tagHeader.contents) > 0:
            #     val, key = tagHeader.text.split(' ', 1)
            #     key = filterAttrKey(key)
            #     attrs[key] = val
            #     updateAttrKey(key)

            # parse attr list
            tagList = tagSection.find('ul', class_='attribute-list')
            if tagList:
                for tagLi in tagList.find_all('li', class_='attribute'):
                    val, key = tagLi.text.split(' ', 1)
                    key = filterAttrKey(key)
                    tends[key] = val
                    updateKeys(tendKeys, key)

        #
        allPlayerData[url] = datPlayer

    except urllib2.HTTPError, e:
        print 'http error: ' + e.code
    except urllib2.URLError, e:
        print 'url error: ' + e.args
    except Exception as err:
        print 'Error: ' + err

def parseAllUrl(fromIndex, toIndex):
    try:
        idxPage = fromIndex

        while toIndex == -1 or idxPage < toIndex:
            print "x- parse page: " + "http://2kmtcentral.com/17/players/page/" + str(idxPage)
            rsp = urllib2.urlopen("http://2kmtcentral.com/17/players/page/" + str(idxPage))
            html = rsp.read()

            soup = BeautifulSoup(html, 'lxml')
            tags = soup.find_all('tr', class_="box-click")

            if tags == None or len(tags) == 0:
                break

            for tag in tags:
                url = tag.a['href']
                allPlayerUrls.append(url)

            #
            idxPage = idxPage + 1

    except urllib2.HTTPError, e:
        print 'http error: ' + e.code
    except urllib2.URLError, e:
        print 'url error: ' + e.args
    except Exception as err:
        print 'Error: ' + err

if __name__ == '__main__':
    try:
        beginTime = time.time()
        print "-------------start parse all pages"
        parseAllUrl(0, -1)

        # test
        # u'http://2kmtcentral.com/17/players/20544/nenê'
        # u'http://2kmtcentral.com/17/players/8324/nenê'
        # u'http://2kmtcentral.com/17/players/907/nenê'
        #url = u'http://2kmtcentral.com/17/players/907/nenê'
        #allPlayerUrls = []
        #allPlayerUrls.append(url)

        print "-------------start parse player url"
        totalPlayerUrlNum = len(allPlayerUrls)
        for i in range(0, totalPlayerUrlNum):
            print "x-" + "%.2f"%((i+1)*1.0/totalPlayerUrlNum*100) + "% parse url: " + allPlayerUrls[i]
            parsePlayerUrl(allPlayerUrls[i])
        print "-------------start save to excel"
        #allPlayerUrls.append("http://2kmtcentral.com/17/players/8015/magic-johnson")
        #parsePlayerUrl("http://2kmtcentral.com/17/players/8015/magic-johnson")
        saveToExcel()

        #
        endTime = time.time()
        print "Total time: " + str(endTime - beginTime)


    except Exception as err:
        print 'Error: ' + err