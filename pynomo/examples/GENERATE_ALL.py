import os, re, time

for root, dirs, files in os.walk('.'):
    if root=='.':
        filelist=files

filelist.remove('GENERATE_ALL.py')

tic_orig=time.time()
#print filelist
for filename in filelist:
    if not re.compile(".py").search(filename, 1)==None:
        tic=time.time()
        print "************************************"
        print "executing %s"%filename
        execfile(filename)
        toc=time.time()
        print '%3.1f s has elapsed for %s'%(toc-tic,filename)
        print "------------------------------------"
toc_orig=time.time()
print '%3.1f s has elapsed overall'%toc_orig-tic_orig
