#-*- coding: utf-8 -*-

import os
import re
import sys
import wget

def inputs ():
    dirName = input('Input directory for save: ')
    address = input('Input ts File Address: ')
    concatedFileName = input('Output file name: ')
    return dirName, address, concatedFileName

def getTsFiles (address):
    return [ (re.sub(r'\-\d{6}\.ts', ('-' + ('%06d' % i) + '.ts'), address), ('%06d' % i) + '.ts') for i in range(0, 1000) ]

def downloadFiles (output, address):
    errorCount = 0
    for addr, name in address:
        try:
            wget.download(addr, out = name)
        except Exception as e:
            errorCount += 1
            print (e)
        if errorCount > 50:
            break

def concatFile (concatedFileName):
    stream = os.popen('cat * > ' + concatedFileName + '.ts')
    stream = os.popen('ffmpeg -i ' + concatedFileName + '.ts -acodec copy -vcodec copy ' + concatedFileName + '.mp4')
    output = stream.read()
    stream = os.popen('rm -rf *.ts')
    print (output)

if __name__ == '__main__':
    dirName, address, outputName = inputs()
    tsList = getTsFiles(address)
    downloadFiles(dirName, tsList)
    concatFile(outputName)
