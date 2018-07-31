# General utilities for working with Micropython
# Author: Joseph G. Wezensky
# License: MIT License (https://opensource.org/licenses/MIT)

import os
import ure

def ls(path='/', filter="", recurse=False, output=''):

    endline = '\r\n'

    # create list of files and dirs sorted by name
    file_list = sorted(list(os.ilistdir(path)), key=lambda f: f[0])

    # only recurse through the dirs if needed
    if recurse:
        for f in file_list:
            if f[1] == 16384:
                ls(merged(path, f[0]), filter, recurse, output)

    r = ure.compile(filter)

    # print out the heading for the current dir
    if output != '':
        with open(output, 'a') as op:
            op.write(endline)
            op.write(path)
            op.write(endline)
    else:
        print('')
        print(path)
        print('')

    # if we are just listing this dir, go ahead and show the sub-directories
    if not recurse:
        for f in file_list:
            if f[1] == 16384:
                dirname = '<dir> {0}'.format(f[0])
                if output != '':
                    with open(output, 'a') as op:
                        op.write(dirname)
                        op.write(endline)
                else:
                    print(dirname)

    # now go through the actual files in the current directory
    sizetotal = 0
    filecount = 0
    for f in file_list:
        if f[1] == 32768:
            if filter == '' or r.match(f[0]):
                stat = '      {0}\t({1} bytes)'.format(f[0], f[3])
                if output != "":
                    with open(output, 'a') as op:
                        op.write(stat)
                        op.write(endline)
                else:
                    print(stat)
                sizetotal += f[3]
                filecount += 1

    # finally print a totals line
    final = '    {0} files {1} total bytes'.format(filecount, sizetotal)
    if output != '':
        with open(output, 'a') as op:
            op.write(final)
            op.write(endline)
    else:
        print(final)
        print('')


def find(target, path='/', filter='^.*\.py$', recurse=False, output=''):

    # create list of files
    file_list = list(os.ilistdir(path))

    # only recurse through the dirs if needed
    if recurse:
        for f in file_list:
            if f[1] == 16384:
                find(target, merged(path, f[0]), filter, recurse, output)

    r = ure.compile(filter)

    # scan the files
    for f in file_list:
        if f[1] == 32768:
            if filter == '' or r.match(f[0]):
                scanfile = merged(path, f[0])
                h = open(scanfile)
                linenumber = 1
                for line in h:
                    if target in line:
                        hit = '{0}:\t(Line {1})\t{2}'.format(scanfile, linenumber, line)
                        if output != '':
                            with open(output, 'a') as op:
                                op.write(hit)
                        else:
                            print(hit, end='')
                    linenumber += 1
                h.close()


def sed(filespec, target, replacement):
    if exists(filespec):
        tmpfile = "tmp.txt"
        fi = open(filespec)
        fo = open(tmpfile, 'w')
        for line in fi:
            if target in line:
                fo.write(line.replace(target, replacement))
            else:
                fo.write(line)
        fi.close()
        fo.close()
        os.remove(filespec)
        os.rename(tmpfile, filespec)
    else:
        print('Input file not found')

def cat(filespec):
    f = open(filespec)
    for line in f:
        print(line, end='')
    f.close()

def edit(filespec):
    from pye import pye
    r = pye(filespec)
    print('edit() done')

def df(path='/'):
    s = os.statvfs(path)
    print('{0}% free space ({1} bytes)'.format(s[3]/s[2]*100, s[3]*s[0]))

def mv(src, dst):
    os.rename(src, dst)

def mm():
    import micropython
    micropython.mem_info(1)

def id():
    import machine
    from ubinascii import hexlify
    return hexlify(machine.unique_id())

def mac():
    import network
    sta = network.WLAN(network.STA_IF)
    ma = ":".join(map(lambda x: "%02x" % x, sta.config('mac')))
    return ma

def local_time(offset=-5, pretty=True):
    import utime
    newtime = utime.time() + (60*60)*offset
    (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime(newtime)
    if pretty:
        timestr = '{0}-{1:02}-{2:02} {3}'.format(year, month, mday, pretty_time(hour, minute))
    else:
        timestr = '{0}-{1:02}-{2:02} {3:02}:{4:02}'.format(year, month, mday, hour, minute)
    return timestr

def man():
    print("""
Commands:
    cat(file) - Dump the contents of a file
    df([path]) - Disk free
    edit(file) - Edit file
    find(target, [path], [filter], [recurse], [output]) - Find string in file
    id() - Chip id
    local_time() - Time from RTC
    ls([path], [filter], [recurse], [output]) - List files
    mac() - MAC address
    mm() - Memory map
    mv(srcfile, dstfile) - Move file (rename)
    sed(file, target, replacement) - Replace string in file
""")

def merged(front, back):
    if front.endswith('/'):
        return front + back
    else:
        return front + '/' + back

def exists(file):
    try:
        s = os.stat(file)
        return True
    except:
        return False

def pretty_time(hour, minute):
    timestr = ''
    if hour > 12:
        timestr = str(hour - 12)
    elif hour == 0:
        timestr = '12'
    else:
        timestr = str(hour)
    timestr += ':{0:02}'.format(minute)
    timestr += ' am' if hour <= 11 else ' pm'
    return timestr
