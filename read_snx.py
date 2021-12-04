# coding=utf-8
# !/usr/bin/env python
'''
Program:
Author:LZ_CUMT
Version:1.0
Date:2021/10/10
'''

# 根据测站id在snx文件中查找测站精确坐标
def getcrd(siteid, sscfile):
    snxcrd = []
    if sscfile != '':
        f = open(sscfile, encoding='gb18030', errors='ignore')
        ln = f.readline()
        while ln:
            ln = f.readline()
            if not ln:
                print('[ERROR] Not find the siteid', siteid)
                break
            if ln[14:18] == siteid:
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                break
        if snxcrd:
            print('[INFO] The', siteid, 'sitecrd is', snxcrd)
        f.close()
    return snxcrd


def getsite(file):
    path = file.split('\\')
    return path[-1][0:4].upper()

