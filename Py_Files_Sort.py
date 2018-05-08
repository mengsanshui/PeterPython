import os, sys, pprint
trace = 0 #1-dirs 2-files

visited = { }
allsizes = []

for srcdir in sys.path :
    for (thisdir, subdir, files) in os.walk(srcdir):
        if trace > 0: print(thisdir)
        thisdir = os.path.normpath(thisdir)
        fixcase = os.path.normcase(thisdir)
        if fixcase in visited:
            continue
        else:
            visited[fixcase] = True
        for filename in files:
            if filename.endswith('.py'):
                if trace > 1: print('...', filename)
                pypath = os.path.join(thisdir, filename)
                try:
                    pysize = os.path.getsize(filename)
                except os.error:
                    print('skipping', pypath, sys.exc_info()[0])
                else:
                    pylines = len(open(pypath, 'rb').readlines())
                    allsizes.append((pysize, pylines, pypath))

print('By size...')
allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])
print('By lines...')
allsizes.sort(key=lambda x: x[1])
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])
