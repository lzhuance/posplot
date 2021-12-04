# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''
from time_conv import ymdhms2wksow
from crd_conv import llh2xyz

def read_RTKLIB_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[0] == '%':
            if "latitude(deg)" in ln:
                type = 'LLH'
                break
            elif "x-ecef(m)" in ln:
                type = 'XYZ'
                break
    ln = f.readline()
    while ln:
        if ln[0] != '%':
            if type == 'XYZ':
                x = float(ln[25:38])
                y = float(ln[40:53])
                z = float(ln[55:68])
                year = int(ln[0:4])
                mouth = int(ln[5:7])
                day = int(ln[8:10])
                hour = int(ln[11:13])
                mini = int(ln[14:16])
                sec = int(ln[17:19])
                week, t = ymdhms2wksow(year, mouth, day, hour, mini, sec)
                xyzlist.append([x, y, z, t])
            elif type == 'LLH':
                lat = float(ln[24:38])
                lon = float(ln[38:53])
                h = float(ln[53:64])
                xyz = llh2xyz([lat, lon, h])
                year = int(ln[0:4])
                mouth = int(ln[5:7])
                day = int(ln[8:10])
                hour = int(ln[11:13])
                mini = int(ln[14:16])
                sec = int(ln[17:19])
                week, t = ymdhms2wksow(year, mouth, day, hour, mini, sec)
                xyzlist.append([xyz[0], xyz[1], xyz[2], t])
        ln = f.readline()
    print("[INFO] Finish Reading the Net_Diff pos file")
    return xyzlist

def read_GAMP_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if len(ln) > 10:
            x = float(ln[36:49])
            y = float(ln[51:64])
            z = float(ln[66:79])
            t = int(ln[25:31])
            xyzlist.append([x, y, z, t])
        ln = f.readline()
    print("[INFO] Finish Reading the GAMP pos file")
    return xyzlist

def read_NetDiff_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if ln[0] != '%':
            x = float(ln[76:88])
            y = float(ln[91:103])
            z = float(ln[106:118])
            year = int(ln[0:4])
            mouth = int(ln[5:7])
            day = int(ln[8:10])
            hour = int(ln[11:13])
            mini = int(ln[14:16])
            sec = int(ln[17:19])
            week, t = ymdhms2wksow(year, mouth, day, hour, mini, sec)
            xyzlist.append([x, y, z, t])
        ln = f.readline()
    print("[INFO] Finish Reading the Net_Diff pos file")
    return xyzlist

def read_IE_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[3:10] == "(weeks)":
            break
    while ln:
        ln = f.readline()
        if not ln:
            break
        if ln[18:21] == "000":
            x = float(ln[22:36])
            y = float(ln[37:51])
            z = float(ln[52:66])
            t = int(ln[11:17])
            xyzlist.append([x, y, z, t])
    print("[INFO] Finish Reading the IE pos file")
    return xyzlist

# 读取POS文件 [1:RTKLIB 2:GAMP 3:Net_Diff 4:IE]
def readpos(file, type):
    if type == 1:
        xyzlist = read_RTKLIB_pos(file)
    elif type == 2:
        xyzlist = read_GAMP_pos(file)
    elif type == 3:
        xyzlist = read_NetDiff_pos(file)
    elif type == 4:
        xyzlist = read_IE_pos(file)
    else:
        print("[Error] Please cheak the input type!")
        xyzlist =[]
    return xyzlist

