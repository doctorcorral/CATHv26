import networkx as nx
import sys, os
from operator import itemgetter
from heapq import nlargest
from collections import defaultdict
from RCCpackage.RCCobject import *
import RCCpackage.RCCutils as rccu
import os.path

from parseCathDomall import *

RCCV1 = open('RCCVector1segmented.txt','r',buffering=0)
already_doms = set()
for l in RCCV1:
	l = l.strip().split(',')
	already_doms.add(l[0])
RCCV1.close()

RCCV1 = open('RCCVector1segmented.txt','a',buffering=0)
RCCV2 = open('RCCVector2segmented.txt','a',buffering=0)
MALOS = open('MALOSsegmented.txt','a',buffering=0)

def parseCathDomainList(CDLfilename):
	Cdict = defaultdict(set)
	CAdict = defaultdict(set)
	CATdict = defaultdict(set)
	CATHdict = defaultdict(set)

	CATHin = open(CDLfilename)

	for s in CATHin:
		if s[0] == '#':
			continue
		nombre, C, A, T, H = map(str,s.strip().split()[:5])
		CATHdict[C+'_'+A+'_'+T+'_'+H ].add(nombre.strip()) 
		CATdict[C+'_'+A+'_'+T].add(nombre.strip())
		CAdict[C+'_'+A].add(nombre.strip()) 
		Cdict[C].add(nombre.strip())
	return dict(CATH=CATHdict,CAT=CATdict,CA=CAdict,C=Cdict)


def main():

	if len(sys.argv)!=4:
		print 'usage: '+sys.argv[0]+' <path/to/dompdb/> <CathDomainList.v3.5.0.txt> <CathDomall.v3.5.0>'
		exit()

	dompdb = sys.argv[1]
	CDLfile = sys.argv[2]
	CDAfile = sys.argv[3]
	CDL = parseCathDomainList(CDLfile)
	_CDL = CDL['CATH']

	DomAllsegments = getParsedDomall(CDAfile)

	FGDR = open('UniProtCATHSeqs.txt','w',0)

	for key in  _CDL.iterkeys():
		for dom in _CDL[key]:
			if dom in already_doms: continue #SEE HERE
			#if not DomAllsegments.has_key(dom) : continue
			if not os.path.exists(os.path.join(dompdb,dom)):
				continue
			try:
				chain = 'A'#dom[4].replace('0','none')
                    #if dom[4] == '0':
				_P = RCC(os.path.join(dompdb,dom),chain,autochain=True,chain_segments=DomAllsegments.get(dom,[]))
                    #else:
                    #_P = RCC(os.path.join(dompdb,dom),chain,autochain=False,chain_segments=DomAllsegments.get(dom,[]))
                
				print dom,DomAllsegments.get(dom,[])
				#FGDR.write('%s,%s\n' % (dom,','.join(DomAllsegments.get(dom,[]) )))

				#_P.createR()
			except:
				MALOS.write('%s\n' % dom)
				continue
			print '%s,%s,%s' % (dom, ','.join(map(str,_P.RCCvector)), key)
			RCCV1.write('%s,%s,%s\n' % (dom, ','.join(map(str,_P.RCCvector)), key))
#RCCV2.write('%s,%s,%s\n' % (dom, ','.join(map(str,_P.RCCvector2)), key))

if __name__ == '__main__':
	main()

