import ws
import os
rootdir = '/wwwroot'
ws.routefile('/',rootdir+'/index.html')

def addfiles(path):
    for file in os.ilistdir(path):
        if file[1] == 16384:
            addfiles(path + '/' + file[0])
        else:
            rpath = path + '/' + file[0]
            rootlen = len(rootdir) + 1
            vpath = '/' + rpath[rootlen:]
            ws.routefile(vpath, rpath)
            print(vpath, rpath)

addfiles(rootdir)
ws.serve()