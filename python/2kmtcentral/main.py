import sys
import urllib, urllib2
from bs4 import BeautifulSoup
from bs4 import element

playerUrls = []

def parsePlayerUrl(url):
    try:
        infos = {}

        rsp = urllib2.urlopen(url)
        html = rsp.read()

        soup = BeautifulSoup(html)

        tagAttrContainer = soup.find('div', class_='attributes-container')
        for tagDiv in tagAttrContainer.find_all('div'):
            for tagSection in tagDiv.find_all('section', class_='defending'):
                # parse attr header
                tagHeader = tagSection.find('h4', class_='attribute-header')
                if tagHeader:
                    key = tagHeader.strong.get_text()
                    val = tagHeader.find
                    infos[key] = val

                # parse attr list
                tagList = tagSection.find('ul', class_='attribute-list')
                if tagList:
                    for tagLi in tagList.find_all('li', class_='attribute'):
                        key = ""
                        val = 0
                        for cot in tagLi.contents:
                            if type(cot) == type(element.NavigableString):
                                key = key + cot
                            #elif type(cot) == type(BeautifulSoup.element.Tag):
                            else:
                                if cot['class'][0] == 'attribute-box':
                                    val = cot.get_text()
                                else:
                                    key = key + cot.get_text()
        pass


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