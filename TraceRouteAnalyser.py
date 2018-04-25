# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:31:21 2018
@author: edw4r
"""

import numpy as np

import math

"""
the two functions below come from:
    https://stackoverflow.com/questions/1502590/calculate-distance-between-two-points-in-google-maps-v3
I use them to calcultate the distance between the origin of the traceroute and the current location
"""

def rad(x):
     return x * math.pi / 180
 
def getDistance(lat1, long1, lat2, long2):
  R = 6378137
  dLat = rad(lat2 - lat1)
  dLong = rad(long2 - long1)
  a = (math.sin(dLat / 2) * math.sin(dLat / 2)) + math.cos(rad(lat1)) 
  a = a * math.cos(rad(lat2)) * math.sin(dLong / 2) * math.sin(dLong / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  d = R * c;
  return d

#stores each ip, the hop # on which it occured, and the average ping time.
#The vars IPs hops and avgPing corresspond to rows in a table,
#each column is the same entry across each variable
IPs = []
hops = []
avgPing = []
longitudes = []
latitudes = []
distances = []

routes = open("routes.txt", "r")


"""
parse routes.txt
"""

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

"""
get the location of all the IP addresses and handle errors
I use maxmind's database for this
"""

import pygeoip
gip = pygeoip.GeoIP('GeoLiteCity.dat')
for i in range(len(IPs)):
    rec = gip.record_by_addr(IPs[i])
    if IPs[i] == IPs[0]:
        longitudes.append(	-2.33067)
        latitudes.append(51.3804)
        continue
    longitudes.append(rec.get("longitude"))
    latitudes.append(rec.get("latitude"))
    
long1 = longitudes[0]
lat1 = latitudes[0]
for i in range(len(IPs)):
    distances.append(getDistance(lat1, long1, latitudes[i], longitudes[i]))
    
distances = np.array(distances).astype(np.float)

#plot hops vs time
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
plt.scatter(hops, avgPing)
plt.xlabel("hop number")
plt.ylabel("avgPing")
plt.show
print("Pearson regression analysis for hops vs avg ping is: " + str(pearsonr(hops, avgPing)))
#plot distance vs time
plt.scatter(distances, avgPing)
plt.xlabel("distances")
plt.ylabel("avgPing")
plt.show
print("Pearson regression analysis for distances vs avg ping is: " + str(pearsonr(distances, avgPing)))
#plot hops vs distance
plt.scatter(hops, distances)
plt.xlabel("hop number")
plt.ylabel("distance")
plt.show
print("Pearson regression analysis for hop number vs distance is: " + str(pearsonr(hops, distances)))
