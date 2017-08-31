import sys
import urllib, urllib2
from bs4 import BeautifulSoup
from bs4 import element

playerUrls = []
attrKeys = []

def updateAttrKey(key):
    if attrKeys.count(key) == 0:
        attrKeys.append(key)

def filterAttrVal(val):
    for k in ['def.', 'Def.', 'attr.', 'Off.']:
        val = val.replace(k, '')
    return val

def parsePlayerUrl(url):
    try:
        infos = {}

        rsp = urllib2.urlopen(url)
        html = rsp.read()

        soup = BeautifulSoup(html)

        tagPlayerView = soup.find('div', id='player-view')
        tagPlayerInfos = tagPlayerView.find('div', class_='col-xs-12 col-md-8')
        name = tagPlayerInfos.div.header.h1.text
        tagInfo = tagPlayerInfos.find('section', class_='infomation')

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
                    key, val = tagHeader.text.split(' ', 1)
                    val = filterAttrVal(val)
                    infos[key] = val
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
                        key, val = tagLi.text.split(' ', 1)
                        val = filterAttrVal(val)
                        infos[key] = val
                        updateAttrKey(key)



    except urllib2.HTTPError, e:
        print (e.code)
    except urllib2.URLError, e:
        print (e.args)

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