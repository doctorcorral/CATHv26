#This is gonna faccilitate CathDomall parsing

import os, sys
from collections import defaultdict


def getParsedDomall(CathDomallfile):
	fin = open(CathDomallfile,'r')
	domallDict = defaultdict(list)
	for l in fin:
		if l[0] == '#' : continue
		l = l.strip().split()
		#if l[2] != 'F00' : continue #No fragments are considered
		if l[1] == 'D01' and l[2] != 'F00': 
			domallDict[l[0]+'00'] = []
			continue
		domainname = l[0]
		D = l[3:]
		for dn in xrange(int(l[01][1:])):
			domainKey = '%s%02d' % (domainname , (dn+1))
			N = int(D[0])
			D = D[1:]
			for n in xrange(N):
				start = int(D[1])
				end = int(D[4])
				domallDict[domainKey].append((start,end))
				D = D[6:]
			
	return domallDict
		
def main():
	D = getParsedDomall(sys.argv[1])
	for k in D.iterkeys():
		print k, D[k]

if __name__ == '__main__':
	main()
	
