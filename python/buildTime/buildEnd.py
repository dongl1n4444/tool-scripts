#!/usr/bin/env python
#coding=utf-8

import os
import sys
import time
import traceback

def main():
	print "END LOG BUILD TIME"
	curTime = time.time()
	localTime = time.localtime(curTime)
	fileName = "/Users/xudong.zhu/Desktop/Shell/logBuildTime" + time.strftime("%Y%m%d", localTime) + ".txt"
	fp = open(fileName, "a+")
	strTime = time.strftime("%X", localTime)
	fp.write("END: " + strTime + " -" + str(int(curTime)) + "\n")
	fp.close()

# -------------- main --------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)