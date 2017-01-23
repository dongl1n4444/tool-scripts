#!/usr/bin/env python
#coding=utf-8

import os
import sys
import time
import traceback

FLAG_START		"START:"
FLAG_END		"END:"

def parseLogFile(logFile):
	fp = open(logFile, "r")

	timeStart = 0
	timeEnd = 0
	for line in fp:
		if line.find("START")
	fp.close()

def main():
	# read all logs

# -------------- main --------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)