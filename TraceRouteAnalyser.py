#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:31:21 2018

@author: edw4r
"""

import numpy as np

#stores each ip, the hop # on which it occured, and the average ping time.
#The vars IPs hops and avgPing corresspond to rows in a table,
#each column is the same entry across each variable
IPs = []
hops = []
avgPing = []

routes = open("routes.txt", "r")

for line in routes:
	if line == "\n":
		continue
	strings = line.split("  ")
	if len(strings) == 1:
		continue
	if strings[1].split(' ')[0] == "*":
		continue
	if strings[0] == "traceroute":
		continue
	IP = strings[1].split(' ')
	IPs.append(IP[1].strip(')').strip('('))
	
	hops.append(strings[0])
	
	pings = []
	
	if strings[2].split(' ')[0] != '*':
		pings.append(strings[2].split(' ')[0])
	if strings[3].split(' ')[0] != '*':
		pings.append(strings[2].split(' ')[0])
	if strings[4].split(' ')[0] != '*':
		pings.append(strings[2].split(' ')[0])
	a = np.array(pings).astype(np.float)
	avgPing.append(np.mean(a))

hops = np.array(hops).astype(np.float)
avgPing = np.array(avgPing).astype(np.float)

#plot hops vs time
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
plt.scatter(hops, avgPing)
plt.xlabel("hops")
plt.ylabel("avgPing")
plt.show
print("The correlation coefficient for these hops vs avg ping is: " + str(pearsonr(hops, avgPing)))
#plot distance vs time
#plot hops vs distance
