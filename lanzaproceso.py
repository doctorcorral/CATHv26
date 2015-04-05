import os

for i in xrange(2000):
    print '\n\n*** RUNNING TRIAL ', i
    os.system("python createCATH_RCCsDB_parallel.py")
