#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import spplugin
import numpy as np
import matplotlib.pyplot as plt


def plotfilebyplugin(filename):
    with spplugin.open(filename, 'r') as pf:
        print('input plugin: %s (%s)' % (pf.getpluginid(), pf.getplugindesc()))
        print('plugin version: %d.%d' % pf.getpluginversion())

        nchannels = pf.getnchannels()
        samprate = pf.getsamprate()
        sampbit = pf.getsampbit()
        nframes = pf.getnframes()
        duration = nframes / samprate
        print('nchannels = %d, samprate = %d, sampbit = %d, nframes = %d, duration = %.2f'
              % (nchannels, samprate, sampbit, nframes, duration))

        y = pf.createndarray(nframes, True)
        nread = pf.read(y)
        print('nread = %d' % nread)

        y.resize((nframes, nchannels))

        x = np.linspace(0.0, duration, nframes)
        for i in range(nchannels):
            plt.plot(x, y[:, i])
        plt.xlim(0.0, duration)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude (normalized)')
        plt.show()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('usage: %s filename'
              % os.path.basename(sys.argv[0]), file=sys.stderr)
        quit()

    plotfilebyplugin(sys.argv[1])
