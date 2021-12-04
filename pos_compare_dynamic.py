# coding=utf-8
# !/usr/bin/env python
'''
 Program: pos_compare_dynamic
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/4
 '''
from crd_conv import xyz2enu
from read_pos import *
import matplotlib.pyplot as plt
from mymath import math_rms
from matplotlib import rcParams

def lim_text(list1, list2):
    a = max(max(list1), max(list2))
    b = min(min(list1), min(list2))
    nmax = a + (a - b) / 4
    nmin = b - (a - b) / 4
    ntext = nmax - (nmax - nmin) / 8
    return nmin, nmax, ntext


if __name__ == '__main__':
    # 两个动态接收机定位误差序列对比绘图
    # 输入： 两个对比pos文件 一个基准pos文件 一个图片保存路径
    pos_type = 2  # 设置pos文件的类型 [1:RTKLIB 2:GAMP 3:Net_Diff 4:IE]
    ref_pos_type = 3  # 设置ref_pos文件的类型 [1:RTKLIB 2:GAMP 3:Net_Diff 4:IE]
    pos_file1 = r'C:\Users\LZ\Desktop\mobile2\result\spp_snr_10_G\daynamic.21o.pos'
    pos_file2 = r'C:\Users\LZ\Desktop\mobile2\result\spp_snr_10_GC\daynamic.21o.pos'
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
    enu1 = []
    enu2 = []
    list1 = readpos(pos_file1, pos_type)
    list2 = readpos(pos_file2, pos_type)
    list_ref = readpos(ref_pos_file, ref_pos_type)

    ind1 = 0
    ind2 = 0
    while ind1 < len(list1) and ind2 < len(list_ref):
        if list1[ind1][3] == list_ref[ind2][3]:
            enu1.append(xyz2enu(list1[ind1][0:3], list_ref[ind2][0:3]))
            ind1 += 1
            ind2 += 1
        elif list1[ind1][3] > list_ref[ind2][3]:
            ind2 += 1
        elif list1[ind1][3] < list_ref[ind2][3]:
            ind1 += 1

    ind1 = 0
    ind2 = 0
    while ind1 < len(list2) and ind2 < len(list_ref):
        if list2[ind1][3] == list_ref[ind2][3]:
            enu2.append(xyz2enu(list2[ind1][0:3], list_ref[ind2][0:3]))
            ind1 += 1
            ind2 += 1
        elif list2[ind1][3] > list_ref[ind2][3]:
            ind2 += 1
        elif list2[ind1][3] < list_ref[ind2][3]:
            ind1 += 1

    # e n u 分组及统计RMS
    e1 = []
    n1 = []
    u1 = []
    e2 = []
    n2 = []
    u2 = []
    for i in range(len(enu1)):
        e1.append(enu1[i][0])
        n1.append(enu1[i][1])
        u1.append(enu1[i][2])
        e2.append(enu2[i][0])
        n2.append(enu2[i][1])
        u2.append(enu2[i][2])
    rms1 = math_rms(enu1)
    rms2 = math_rms(enu2)

    ymin1, ymax1, ytext1 = lim_text(e1, e2)
    ymin2, ymax2, ytext2 = lim_text(n1, n2)
    ymin3, ymax3, ytext3 = lim_text(u1, u2)
    xtext = 15

    plt.figure(figsize=(8,6))
    plt.subplot(3, 1, 1)
    plt.plot(e1, lw=0.8, color='r')
    plt.plot(e2, lw=0.8, color='b')
    plt.ylim(ymin1, ymax1)
    plt.yticks(fontsize='x-large')
    plt.xticks([])
    plt.ylabel('E方向误差[m]', fontsize='x-large')
    plt.xlim(0, len(e1))
    out_text = 'RMS1 = {:6.4f} m  RMS2 = {:6.4f} m'.format(rms1[0], rms2[0])
    plt.text(xtext, ytext1, out_text, fontsize='x-large')
    # plt.legend(['Helmert OFF', 'Helmert ON'], fontsize='large', loc='upper right')

    plt.subplot(3, 1, 2)
    plt.plot(n1, lw=0.8, color='r')
    plt.plot(n2, lw=0.8, color='b')
    plt.yticks(fontsize='x-large')
    plt.xticks([])
    plt.ylabel('N方向误差[m]', fontsize='x-large')
    plt.ylim(ymin2, ymax2)
    plt.xlim(0, len(e1))
    out_text = 'RMS1 = {:6.4f} m  RMS2 = {:6.4f} m'.format(rms1[1], rms2[1])
    plt.text(xtext, ytext2, out_text, fontsize='x-large')

    plt.subplot(3, 1, 3)
    plt.plot(u1, lw=0.8, color='r')
    plt.plot(u2, lw=0.8, color='b')
    plt.yticks(fontsize='x-large')
    plt.ylabel('U方向误差[m]', fontsize='x-large')
    plt.ylim(ymin3, ymax3)
    plt.xlim(0, len(e1))
    plt.xticks(fontsize='x-large')
    out_text = 'RMS1 = {:6.4f} m  RMS2 = {:6.4f} m'.format(rms1[2], rms2[2])
    plt.text(xtext, ytext3, out_text, fontsize='x-large')

    plt.xlabel('历元', fontsize='x-large')
    plt.subplots_adjust(hspace=0)

    plt.savefig(png_file, dpi=600)
    plt.show()
    print("[INFO] Finish the paint")

