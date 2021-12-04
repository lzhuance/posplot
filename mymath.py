# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''
import math

# 计算enu矩阵的RMS值
def math_rms(enu):
 sump = [0, 0, 0]
 rms = []
 for i in range(len(enu[0])):
  for j in range(len(enu)):
   sump[i] += enu[j][i] * enu[j][i]
  rms.append(round(math.sqrt(sump[i] / len(enu)), 4))
 return rms