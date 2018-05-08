import os, sys, fnmatch

maxfileload = 1000000
blksize = 1024 * 500

def copyfile(pathFrom, pathTo, maxfileload=maxfileload):
    if os.path.getsize(pathFrom) <= maxfileload:
        bytefrom = open(pathFrom, 'rb').read()
        open(pathTo,'wb').write(bytefrom)
    else:
        filefrom = open(pathFrom, 'rb')
        fileto = open(pathTo, 'wb')
        while True:
            bytefrom = filefrom.read(blksize)
            if not bytefrom: break
            fileto.write(bytefrom)


def copytree(dirFrom, dirTo, verbose=0):
    fcount = dcount = 0
    for filename in os.listdir(dirFrom):
        pathFrom = os.path.join(dirFrom, filename)
        pathTo = os.path.join(dirTo, filename)
        if not os.path.isdir(pathFrom):
            try:
                if verbose > 0: print('Copy file', pathFrom, 'to', pathTo)
                copyfile(pathFrom, pathTo)
                fcount += 1
            except:
                print('Error copying', pathFrom, 'to', pathTo, '--skipped')
                print(sys.exc_info()[0], sys.exc_info()[1])
        else:
            if verbose: print('copying dir', pathFrom, 'to', pathTo)
            try:
                os.mkdir(pathTo)
                below = copytree(pathFrom, pathTo)
                fcount += below[0]
                dcount += below[1]
                dcount += 1
            except:
                print('Error creating', pathTo, '--skipped')
                print(sys.exc_info()[0], sys.exc_info()[1])
    return(fcount, dcount)

def find(pattern, startdir=os.curdir):
    for (thisDir, subsHere, filesHere) in os.walk(startdir):
        for name in subsHere + filesHere:
            if fnmatch.fnmatch(name, pattern):
                fullpath = os.path.join(thisDir, name)
                yield fullpath

def findlist(pattern, startdir=os.curdir, dosort=False):
    matches = list(find(pattern, startdir))
    if dosort: matches.sort()
    return matches


def get_args():
    try:
        dirFrom, dirTo = sys.argv[:1]
    except:
        print('Call CH2036.py dirFrom dirTo')
    else:
        if not os.path.isdir(dirFrom):
            print('Error: The dirFrom is not dir')
        elif not os.path.exists(dirTo):
            os.mkdir(dirTo)
            print('Created the dirTo')
            return (dirFrom, dirTo)
        else:
            print('Warning: dirTo already exist')
            if hasattr(os.path, 'samefile'):
                same = os.path.samefile(dirFrom, dirTo)
            else:
                same = os.path.abspath(dirFrom) == os.path.abspath(dirTo)

            if same:
                print('Error: dirFrom is same as dirTo')
            else:
                return (dirFrom, dirTo)

if __name__ == '__main__':
    import time
    dirstuple = get_args()
    if dirstuple:
        print('Copying...')
        start = time.clock()
        fcount, dcount = copytree(*dirstuple)
        print('Copied', fcount, 'files', dcount, 'dirs', end=' ')
        print('In', time.clock()-start, 'seconds')


