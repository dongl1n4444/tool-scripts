import sys
import urllib, urllib2
from bs4 import BeautifulSoup
from bs4 import element
import re

allPlayerData = {}
playerUrls = []
attrKeys = []

def updateAttrKey(key):
    if attrKeys.count(key) == 0:
        attrKeys.append(key)

def filterAttrKey(val):
    for k in ['def.', 'Def.', 'attr.', 'Off.']:
        val = val.replace(k, '')
    return val

def filterInfoVal(val):
    #return val.replace('\\', '')
    return val

def parsePlayerUrl(url):
    try:
        print "x- parse url: " + str(url)
        datPlayer = {}

        rsp = urllib2.urlopen(url)
        html = rsp.read()

        soup = BeautifulSoup(html)

        # infos
        infos = {
            'Name':'',
            'Theme':'',
            'Position':'',
            'Team':'',
            'Height':'',
            'Weight':'',
            'Age':'',
            'From':''
        }
        datPlayer['info'] = infos

        tagPlayerView = soup.find('div', id='player-view')
        tagPlayerInfos = tagPlayerView.find('div', class_='col-xs-12 col-md-8')
        name = tagPlayerInfos.div.header.h1.text
        infos['Name'] = filterInfoVal(name)

        tagInfos = tagPlayerInfos.find('section', class_='information')
        for tagInfo in tagInfos.find_all('div', class_=re.compile('^col-xs-')):
            if tagInfo.h6 and str(tagInfo.h6.text) in infos.keys():
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
                    updateAttrKey(key)

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
                        updateAttrKey(key)

        # ranking
        ranks = {}
        datPlayer['rank'] = ranks

        tagRanks = soup.find('section', class_='rankings')
        for tagRank in tagRanks.find_all('li', title=re.compile('^Top')):
            key = tagRank.span.text
            val = str(tagRank.contents[0])
            ranks[key] = val

        #

        #
        allPlayerData[url] = datPlayer

    except urllib2.HTTPError, e:
        print 'http err: ' + e.code
    except urllib2.URLError, e:
        print 'url err: ' + e.args
    except:
        print 'unknow err'

def main():
    try:
        idxPage = 0

        while idxPage < 1:
            rsp = urllib2.urlopen("http://2kmtcentral.com/17/players/page/" + str(idxPage))
            html = rsp.read()

            soup = BeautifulSoup(html)
            tags = soup.find_all('tr', class_="box-click")

            for tag in tags:
                url = tag.a['href']
                playerUrls.append(url)

            #
            idxPage = idxPage + 1

        for url in playerUrls:
            parsePlayerUrl(url)

    except urllib2.HTTPError, e:
        print (e.code)
    except urllib2.URLError, e:
        print (e.args)

if __name__ == '__main__':
    #main()
    parsePlayerUrl("http://2kmtcentral.com/17/players/8015/magic-johnson")