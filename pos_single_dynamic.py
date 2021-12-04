# coding=utf-8
# !/usr/bin/env python
'''
 Program: pos_single_static
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/4
 '''
from crd_conv import xyz2enu
from read_pos import *
import matplotlib.pyplot as plt
from mymath import math_rms
from matplotlib import rcParams

def lim_text(list):
    a = max(list)
    b = min(list)
    nmax = a + (a - b) / 4
    nmin = b - (a - b) / 4
    ntext = nmax - (nmax - nmin) / 8
    return nmin, nmax, ntext


if __name__ == '__main__':
    # 单个动态接收机定位误差序列绘图
    # 输入： 一个pos文件 一个基准pos文件 一个图片保存路径
    pos_type = 2  # 设置pos文件的类型 [1:RTKLIB 2:GAMP 3:Net_Diff 4:IE]
    ref_pos_type = 3  # 设置pos文件的类型 [1:RTKLIB 2:GAMP 3:Net_Diff 4:IE]
    pos_file = r'C:\Users\LZ\Desktop\mobile2\result\spp_ele_15_GC\daynamic.21o.pos'
    ref_pos_file = r'C:\Users\LZ\Desktop\mobile2\Coor_2021280_base-rove.pos'
    png_file = r'C:\Users\LZ\Desktop\arlz2\result\harb2740.21o.png'

    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 10.5,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    enu = []
    list_pos = readpos(pos_file, pos_type)
    list_ref = readpos(ref_pos_file, ref_pos_type)

    ind1 = 0
    ind2 = 0
    while ind1 < len(list_pos) and ind2 < len(list_ref):
        if list_pos[ind1][3] == list_ref[ind2][3]:
            enu.append(xyz2enu(list_pos[ind1][0:3], list_ref[ind2][0:3]))
            ind1 += 1
            ind2 += 1
        elif list_pos[ind1][3] > list_ref[ind2][3]:
            ind2 += 1
        elif list_pos[ind1][3] < list_ref[ind2][3]:
            ind1 += 1

    e = []
    n = []
    u = []
    for i in range(len(enu)):
        e.append(enu[i][0])
        n.append(enu[i][1])
        u.append(enu[i][2])
    rms = math_rms(enu)

    ymin1, ymax1, ytext1 = lim_text(e)
    ymin2, ymax2, ytext2 = lim_text(n)
    ymin3, ymax3, ytext3 = lim_text(u)
    xtext = 15

    plt.figure(figsize=(8, 6))
    plt.subplot(3, 1, 1)
    plt.plot(e, lw=0.8, color='r')
    plt.ylim(ymin1, ymax1)
    plt.yticks(fontsize='x-large')
    plt.xticks([])
    plt.ylabel('E方向误差[m]', fontsize='x-large')
    plt.xlim(0, len(e))
    plt.text(xtext, ytext1, 'RMS = ' + str(rms[0]) + ' m', fontsize='x-large')

    plt.subplot(3, 1, 2)
    plt.plot(n, lw=0.8, color='r')
    plt.yticks(fontsize='x-large')
    plt.xticks([])
    plt.ylabel('N方向误差[m]', fontsize='x-large')
    plt.ylim(ymin2, ymax2)
    plt.xlim(0, len(e))
    plt.text(xtext, ytext2, 'RMS = ' + str(rms[1]) + ' m', fontsize='x-large')

    plt.subplot(3, 1, 3)
    plt.plot(u, lw=0.8, color='r')
    plt.yticks(fontsize='x-large')
    plt.ylabel('U方向误差[m]', fontsize='x-large')
    plt.ylim(ymin3, ymax3)
    plt.xlim(0, len(e))
    plt.xticks(fontsize='x-large')
    plt.text(xtext, ytext3, 'RMS = ' + str(rms[2]) + ' m', fontsize='x-large')

    plt.xlabel('历元', fontsize='x-large')
    plt.subplots_adjust(hspace=0)

    plt.savefig(png_file, dpi=600)
    plt.show()
    print("[INFO] Finish the paint")

