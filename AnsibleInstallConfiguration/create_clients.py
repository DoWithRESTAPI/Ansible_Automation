#!/bin/python
fo=open("exch_key.bh")
private_ips=fo.readlines()
del private_ips[0]
fc=open('clients_pv.txt','w')
for each in  private_ips:
  pvt=each.strip('\n').split('@')[-1]+'\n'
  fc.write(pvt)

fc.close()
fo.close()
