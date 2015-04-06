import RCCpackage.RCCobject as rcco
import RCCpackage.RCCutils as  rccu
import os
from random import randint

from multiprocessing import Pool
from threading import BoundedSemaphore


RCC_CATH_DB = "CATHvectors.txt"
DOMPDB_DIR = "dompdb"
CDLfile = "CathDomainList.v4.0.0"

pool_sema = BoundedSemaphore(value=1)


def parseCathDomainList(CDLfilename):
        
    CATHin = open(CDLfilename,'r')
    
    _D = dict()
        
    for s in CATHin:
        if s[0] == '#': continue
        nombre, C, A, T, H = map(str,s.strip().split()[:5])
        _D[nombre] = '_'.join([C,A,T,H])
    return _D



def calculateRCCandWrite(domclass_tuple):
    print ''
    print '*** domandclasstuple', domclass_tuple
    pdbname, cathclass = domclass_tuple
    domainname = os.path.basename(pdbname)#[:-4]
    
    print '*** Domain name: ', domainname
    
    rccs = rcco.RCC(pdbname,'A',autochain=True,chain_segments=[])
        
    print '*** RCC Vector: ', ','.join(map(str,rccs.RCCvector))
        
    print '*** CATH Classification: ', cathclass
    
    
    pool_sema.acquire()
    
    fout = open(RCC_CATH_DB,'a',0)
    fout.write("%s,%s,%s\n" % (domainname, ','.join(map(str,rccs.RCCvector)),cathclass ) )
    fout.close()
    
    pool_sema.release()


if __name__ == '__main__':

#D = parseClassesSCOP.getClassesDict(DIR_DES_SCOP_FN)
    D = parseCathDomainList(CDLfile)
    #Get domains already with a computed RCC vector on RCC_CATH_DB
    dns = set()
    fin = open(RCC_CATH_DB,'r',0)
    for l in fin:
        dn = l.strip().split(',')[0]
        dns.add(dn)
    fin.close()


    inputs = []

    for pdbname in rccu.iter_directory_files( DOMPDB_DIR ):
        
        domainname = os.path.basename(pdbname)#[:-4]
        
        if domainname in dns:
            print '\n*** Already ', domainname
            continue
        
        cathclass = D.get(domainname,None)
        if cathclass == None:
            print '\n*** No class found for ', domainname
            continue

        inputs.append((pdbname,cathclass))
    print '*** Already ', len(dns), ' domains'
    print '*** Going to process ', len(inputs) , ' domains'

    p = Pool(randint(2,4))
    p.map( calculateRCCandWrite, inputs )
    p.close()
    p.join()
