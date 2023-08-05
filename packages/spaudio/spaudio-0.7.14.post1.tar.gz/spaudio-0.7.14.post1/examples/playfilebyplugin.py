#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import spplugin
import spaudio


def playfilebyplugin(filename):
    with spplugin.open(filename, 'r') as pf:
        print('input plugin: %s (%s)' % (pf.getpluginid(), pf.getplugindesc()))
        print('plugin version: %d.%d' % pf.getpluginversion())

        nchannels = pf.getnchannels()
        samprate = pf.getsamprate()
        sampbit = pf.getsampbit()
        nframes = pf.getnframes()
        print('nchannels = %d, samprate = %d, sampbit = %d, nframes = %d'
              % (nchannels, samprate, sampbit, nframes))

        filetype = pf.getfiletype()
        filedesc = pf.getfiledesc()
        filefilter = pf.getfilefilter()
        if filetype:
            print('filetype = %s %s'
                  % (filetype, '(' + filedesc +
                     ('; ' + filefilter if filefilter else '') + ')' if filedesc else ''))
        songinfo = pf.getsonginfo()
        if songinfo:
            print('songinfo = ' + str(songinfo))

        a = spaudio.SpAudio()

        a.setnchannels(nchannels)
        a.setsamprate(samprate)
        a.setsampbit(sampbit)

        b = a.createarray(nframes, True)
        nread = pf.read(b)
        print('nread = %d' % nread)

        a.open('wo')

        nwrite = a.write(b)
        print('nwrite = %d' % nwrite)

        a.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('usage: %s filename'
              % os.path.basename(sys.argv[0]), file=sys.stderr)
        quit()

    playfilebyplugin(sys.argv[1])
