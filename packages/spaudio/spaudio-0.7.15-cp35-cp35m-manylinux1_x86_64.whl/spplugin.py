# -*- coding: utf-8 -*-
"""
A python module for plugin-based audio file I/O based on `spPlugin
<http://www-ie.meijo-u.ac.jp/labs/rj001/spLibs/index.html>`_
which supports several sound formats including WAV, AIFF, MP3,
Ogg Vorbis, FLAC, ALAC, raw, and more.

Example:
    The following is the example plotting the waveform of an input audio file.
    ::

        import os
        import sys
        import spplugin
        import numpy as np
        import matplotlib.pyplot as plt


        def plotfilebyplugin(filename):
            with spplugin.open(filename, 'r') as pf:
                nchannels = pf.getnchannels()
                samprate = pf.getsamprate()
                sampbit = pf.getsampbit()
                nframes = pf.getnframes()
                duration = nframes / samprate

                y = pf.createndarray(nframes * nchannels)
                nread = pf.read(y)
                print('nread = %d' % nread)

                y.resize((nframes, nchannels))

                x = np.linspace(0.0, duration, nframes)
                for i in range(nchannels):
                    plt.plot(x, y[:,i])
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

"""


import sys
import os
import locale
import array
from collections import namedtuple
from _spplugin import spplugin_c as _spplugin_c


__version__ = '0.7.15'


_encoding = locale.getpreferredencoding()
_defaultdir = _spplugin_c.spGetDefaultDir()
if isinstance(_defaultdir, bytes):
    _ischarbinary = True
else:
    _ischarbinary = False


def _encodetocstr(pstr, encoding=None):
    if pstr is not None:
        global _ischarbinary
        if _ischarbinary:
            if encoding is None:
                global _encoding
                encoding = _encoding

            cstr = pstr.encode(encoding)
        else:
            cstr = pstr
    else:
        cstr = None
    return cstr


def _decodefromcstr(cstr, encoding=None):
    if cstr is None:
        return None

    global _ischarbinary
    if _ischarbinary:
        if encoding is None:
            global _encoding
            encoding = _encoding

        return cstr.decode(encoding)
    else:
        return cstr


_is_64bits = sys.maxsize > 2**32
_sysdirname = ''
_py_plugindir = ''

if sys.platform == 'win32':
    if _is_64bits:
        _sysdirname = 'win64'
    else:
        _sysdirname = 'win32'
elif sys.platform == 'darwin':
    _sysdirname = 'mac64'


def _listup_plugin_files():
    i = 0
    while True:
        cstr = _spplugin_c.spSearchPluginFile(i)
        if cstr is None:
            break
        print(_decodefromcstr(cstr))
        i += 1


if _sysdirname:
    # d = os.path.dirname(sys.modules['spplugin'].__file__)
    d = os.path.dirname(os.path.abspath(__file__))
    _py_plugindir = os.path.join(d, '_spplugins', _sysdirname)
    if os.path.isdir(_py_plugindir):
        _spplugin_c.spSetPluginSearchPath(_encodetocstr(_py_plugindir))
    else:
        _py_plugindir = ''


def getplugininfo(name):
    """Gets detailed information of the plugin which has a name specified."""
    cname = _encodetocstr(name)
    plugin = _spplugin_c.spLoadPlugin(cname)
    info = None
    if plugin is not None:
        info = _spplugin_c.spGetPluginInformation(plugin)
        if info is not None:
            info = _decodefromcstr(info)
        _spplugin_c.spFreePlugin(plugin)
    return info


def getplugindesc(name):
    """Gets short description of the plugin which has a name specified."""
    cname = _encodetocstr(name)
    plugin = _spplugin_c.spLoadPlugin(cname)
    desc = None
    if plugin is not None:
        desc = _spplugin_c.spGetPluginDescription(plugin)
        if desc is not None:
            desc = _decodefromcstr(desc)
        _spplugin_c.spFreePlugin(plugin)
    return desc


# https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
def _isnamedtupleinstance(x):
    t = type(x)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


class Error(Exception):
    """Base exception class for spplugin."""
    pass


class FileError(Error):
    """Exception raised by audio file problems."""
    pass


class WrongPluginError(Error):
    """Exception raised by a wrong plugin."""
    pass


class SuitableNotFoundError(Error):
    """Exception raised if no suitable plugin is found."""
    pass


class BogusFileError(Error):
    """Exception raised if the audio file is bogus."""
    pass


class FileTypeError(Error):
    """Exception raised if the specified file type is not accepted."""
    pass


class SampleRateError(Error):
    """Exception raised if the specified sample rate is not accepted."""
    pass


class SampleBitError(Error):
    """Exception raised if the specified bits/sample is not accepted."""
    pass


class NChannelsError(Error):
    """Exception raised if the specified number of channels is not accepted."""
    pass


class TotalLengthRequiredError(Error):
    """Exception raised if the total length is required to use the plugin."""
    pass


_standard_lib_params = namedtuple('_standard_lib_params',
                                  'nchannels sampwidth framerate nframes comptype compname')
_standard_lib_keys = ['nchannels', 'sampwidth', 'framerate',
                      'nframes', 'comptype', 'compname']

params_keys = ['nchannels', 'sampbit', 'samprate', 'length',
               'pluginid', 'filetype', 'filedesc', 'filefilter',
               'songinfo', 'sampwidth', 'framerate', 'nframes']

songinfo_keys_in_number = ['track', 'track_toral', 'disc',
                           'disc_total', 'tempo']
songinfo_keys_in_string = ['title', 'artist', 'album', 'genre', 'release',
                           'copyright', 'engineer', 'source', 'software',
                           'subject', 'comment', 'album_artist', 'composer',
                           'lyricist', 'producer', 'isrc']


class SpFilePlugin:
    """A class for audio file I/O. This class is similar to one provided by
        the standard libraries such as aifc, wave, or sunau. The important
        difference is that ``set*()`` functions must be called before
        :func:`~spplugin.SpFilePlugin.open` in this class. You can set
        parameters by using optional arguments of
        :func:`~spplugin.open` function.
    """
    def __init__(self):
        self._pluginname = None
        self._open_mode = ' '
        self._songinfo = {}
        self._plugin = None
        self._waveinfo_c = _spplugin_c.spWaveInfo()
        _spplugin_c.spInitWaveInfo(self._waveinfo_c)
        self._songinfo_c = _spplugin_c.spSongInfo()
        _spplugin_c.spInitSongInfo(self._songinfo_c)
        self._currentpos = 0
        self._setparams_pluginid = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def open(self, filename, mode, *, pluginname=None, samprate=0,
             sampbit=0, nchannels=0, filetype=None, songinfo=None, params=None):
        """Opens the file associated with the filename by using a plugin.

        Args:
            filename (str): The name of the file to open.
            mode (str): The opening mode. ``'r'`` means read mode, ``'w'`` means
                        write mode.
            pluginname (str): The name of the plugin used when this function
                              cannot find the suitable plugin.
            samprate (double): Sample rate.
            sampbit (int): Bits/sample.
            nchannels (int): The number of channels.
            filetype (str): File type string.
            songinfo (dict): Song information.
            params (dict): All above parameters in dict format.
        """
        if pluginname is not None:
            self._pluginname = pluginname
        if params is not None:
            self.setparams(params)
        if samprate != 0:
            self.setsamprate(samprate)
        if sampbit != 0:
            self.setsampbit(sampbit)
        if nchannels != 0:
            self.setnchannels(nchannels)
        if filetype:
            self.setfiletype(filetype)
        if songinfo:
            self.setsonginfo(songinfo)
            self._setsonginfo_toc()

        cpluginname = _encodetocstr(self._pluginname)
        cfilename = _encodetocstr(filename)
        cmode = _encodetocstr(mode, 'utf-8')
        self._plugin, errorcode \
            = _spplugin_c.spOpenFilePluginAuto_(cpluginname, cfilename, cmode,
                                                0,  # SP_PLUGIN_DEVICE_FILE
                                                self._waveinfo_c, self._songinfo_c)
        if self._setparams_pluginid and errorcode == -11:
            _spplugin_c.spFreePlugin(self._plugin)
            _spplugin_c.spSetWaveInfoFileType_(self._waveinfo_c, None)
            self._plugin, errorcode \
                = _spplugin_c.spOpenFilePluginAuto_(cpluginname, cfilename, cmode,
                                                    0,  # SP_PLUGIN_DEVICE_FILE
                                                    self._waveinfo_c, self._songinfo_c)
        self._procopenerror(errorcode)
        self._open_mode = mode
        self._currentpos = 0

    def close(self):
        """Closes the current audio file."""
        if self._plugin is not None:
            _spplugin_c.spCloseFilePlugin(self._plugin)
        self._plugin = None
        self._open_mode = ' '
        self._currentpos = 0
        self._songinfo = {}
        self._setparams_pluginid = None

    def _procopenerror(self, errorcode):
        if errorcode != 1:
            if errorcode == -1:
                raise WrongPluginError('wrong plugin')
            elif errorcode == -6:
                raise SuitableNotFoundError('no suitable plugin is found')
            elif errorcode == -10:
                raise BogusFileError('this audio file is bogus')
            elif errorcode == -11:
                raise FileTypeError('the file type is not accepted')
            elif errorcode == -12:
                raise SampleRateError('the sample rate is not accepted')
            elif errorcode == -13:
                raise SampleBitError('the bits/sample is not accepted')
            elif errorcode == -14:
                raise NChannelsError('the number of channels is not accepted')
            elif errorcode == -16:
                raise TotalLengthRequiredError('the total length is required')
            else:
                raise FileError('unknown file error')
            _spplugin_c.spFreePlugin(self._plugin)
            self._plugin = None

    def getpluginversion(self):
        """Gets the version of the plugin currently used."""
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        flag, version, revision = _spplugin_c.spGetPluginVersion(self._plugin)
        if not flag:
            raise RuntimeError('cannot get plugin version')
        return version, revision

    def getpluginname(self):
        """Gets the name of the plugin currently used."""
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        name = _spplugin_c.spGetPluginName(self._plugin)
        if name is not None:
            name = _decodefromcstr(name)
        return name

    def getpluginid(self):
        """Gets the ID of the plugin currently used."""
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        id = _spplugin_c.spGetPluginId(self._plugin)
        if id is not None:
            id = _decodefromcstr(id)
        return id

    def getplugininfo(self):
        """Gets the detailed information of the plugin currently used."""
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        info = _spplugin_c.spGetPluginInformation(self._plugin)
        if info is not None:
            info = _decodefromcstr(info)
        return info

    def getplugindesc(self):
        """Gets the short description of the plugin currently used."""
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        desc = _spplugin_c.spGetPluginDescription(self._plugin)
        if desc is not None:
            desc = _decodefromcstr(desc)
        return desc

    def _setsonginfo_toc(self):
        if self._songinfo:
            for key, value in self._songinfo.items():
                ckey = _encodetocstr(key, 'utf-8')
                if type(value) is str:
                    cvalue = _encodetocstr(value)
                    _spplugin_c.spUpdateSongInfoStringField_(self._songinfo_c,
                                                             ckey, cvalue)
                else:
                    _spplugin_c.spUpdateSongInfoNumberField_(self._songinfo_c,
                                                             ckey, value)

    def _getsonginfo_fromc(self):
        for index, key in enumerate(songinfo_keys_in_number):
            ckey = _encodetocstr(key, 'utf-8')
            number = _spplugin_c.spGetSongInfoNumberField_(self._songinfo_c, ckey)
            if number >= 0:
                self._songinfo[key] = number

        for index, key in enumerate(songinfo_keys_in_string):
            ckey = _encodetocstr(key, 'utf-8')
            cstring = _spplugin_c.xspGetSongInfoStringField_(self._songinfo_c, ckey)
            if (cstring is not None) and (len(cstring) > 0):
                self._songinfo[key] = _decodefromcstr(cstring)

    def setsonginfo(self, songinfo):
        """Sets song information to the file."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        self._songinfo = songinfo
        self._setsonginfo_toc()

    def appendsonginfo(self, songinfo):
        """Appends song information to the current internal information."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        # append dict of 'songinfo' arg to '_songinfo'
        self._songinfo = dict(self._songinfo, **songinfo)
        self._setsonginfo_toc()

    def getsonginfo(self):
        """Gets song information of the current file."""
        self._getsonginfo_fromc()
        return self._songinfo

    def setfiletype(self, filetype):
        """Sets file type to the file."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        cfiletype = _encodetocstr(filetype)
        _spplugin_c.spSetWaveInfoFileType_(self._waveinfo_c, cfiletype)

    def getfiletype(self):
        """Gets file type of the current file."""
        cfiletype = _spplugin_c.xspGetWaveInfoStringField_(self._waveinfo_c, 0)
        if cfiletype:
            filetype = _decodefromcstr(cfiletype)
        else:
            filetype = None
        return filetype

    def getfiledesc(self):
        """Gets file description of the current file."""
        cfiledesc = _spplugin_c.xspGetWaveInfoStringField_(self._waveinfo_c, 1)
        if cfiledesc:
            filedesc = _decodefromcstr(cfiledesc)
        else:
            filedesc = None
        return filedesc

    def getfilefilter(self):
        """Gets file filter (e.g. ``'*.wav'``) of the current file."""
        cfilefilter = _spplugin_c.xspGetWaveInfoStringField_(self._waveinfo_c, 2)
        if cfilefilter:
            filefilter = _decodefromcstr(cfilefilter)
        else:
            filefilter = None
        return filefilter

    def setsamprate(self, samprate):
        """Sets sample rate to the file."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        self._waveinfo_c.samp_rate = samprate

    def setframerate(self, samprate):
        """Sets sample rate to the file."""
        self.setsamprate(samprate)

    def getsamprate(self):
        """Gets sample rate of the current file."""
        return self._waveinfo_c.samp_rate

    def getframerate(self):
        """Gets sample rate of the current file."""
        return self.getsamprate()

    def setsampbit(self, sampbit):
        """Sets bits/sample to the file. sampbit = 33 means
        32bit float."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        if sampbit < 8:
            raise ValueError('sampbit >= 8 is required')
        self._waveinfo_c.samp_bit = sampbit

    def setsampwidth(self, sampwidth, floatflag=False):
        """Sets bytes/sample of the current file."""
        sampbit = sampwidth * 8
        if floatflag:
            sampbit += 1
        return self.setsampbit(sampbit)

    def getsampbit(self):
        """Gets bits/sample of the current file. sampbit = 33 means
        32bit float."""
        return self._waveinfo_c.samp_bit

    def getsampwidth(self):
        """Gets bytes/sample of the current file."""
        return self.getsampbit() // 8

    def getrawsampbit(self):
        """Gets the bits/sample for a raw buffer."""
        if self._waveinfo_c.samp_bit < 16:
            return 16
        elif ((self._waveinfo_c.samp_bit > 16)
              and (self._waveinfo_c.samp_bit < 32)):
            return 32
        else:
            return self.getsampwidth() * 8

    def getrawsampwidth(self):
        """Gets the bytes/sample for a raw buffer."""
        return self.getrawsampbit() // 8

    def setnchannels(self, nchannels):
        """Sets the number of channels to the file."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        if nchannels <= 0:
            raise ValueError('nchannels >= 1 is required')
        self._waveinfo_c.num_channel = nchannels

    def getnchannels(self):
        """Gets the number of channels of the current file."""
        return self._waveinfo_c.num_channel

    def setlength(self, length):
        """Sets the total length of the file."""
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        if length <= 0:
            raise ValueError('length >= 1 is required')
        self._waveinfo_c.length = length

    def setnframes(self, length):
        """Sets the total number of frames of the current file."""
        self.setlength(length)

    def getlength(self):
        """Gets the total length of the current file."""
        return self._waveinfo_c.length

    def getnframes(self):
        """Gets the total number of frames of the current file."""
        return self.getlength()

    def getcomptype(self, decodebytes=False):
        """Returns compression type. Currently, ``'NONE'`` (decodebytes = ``True``)
        or ``b'NONE'`` (decodebytes = ``False``) will be returned."""
        if decodebytes:
            return 'NONE'
        else:
            return b'NONE'

    def getcompname(self, decodebytes=False):
        """Returns human-readable name of compression type. Currently,
        ``'not compressed'`` (decodebytes = ``True``) or ``b'not compressed'``
        (decodebytes = ``False``) will be returned.
        """
        if decodebytes:
            return 'not compressed'
        else:
            return b'not compressed'

    def setcomptype(self, encodestr=True):
        """Sets compression type. Currently, this parameter is ignored."""
        pass

    def setparams(self, params):
        """Sets supported all parameters described in dict or
        namedtuple object to the file.

        Args:
            params (dict): a dict object of parameters whose keys are
                ``'nchannels'``, ``'sampbit'``, ``'samprate'``, ``'length'``,
                ``'filetype'``, or ``'songinfo'``.
                The namedtuple generated by standard libraries
                such as aifc, wave, or sunau is also acceptable.
        """
        if self._plugin is not None:
            raise RuntimeError('set before opening file')
        # if isinstance(params, namedtuple):
        if _isnamedtupleinstance(params):
            # some versions of Python include _asdist() bug.
            params = dict(zip(params._fields, params))
        elif isinstance(params, tuple):
            params = dict(zip(_standard_lib_keys, params))
        sampbit = 0
        pluginid = None
        self._setparams_pluginid = None
        for key, value in params.items():
            if key == 'sampwidth':
                if sampbit == 0:
                    sampbit = value * 8
            elif key == 'sampbit':
                sampbit = value
            elif key == 'nchannels':
                self.setnchannels(value)
            elif key == 'samprate' or key == 'framerate':
                self.setsamprate(value)
            elif key == 'length' or key == 'nframes':
                self.setlength(value)
            elif key == 'pluginid':
                pluginid = value
            elif key == 'filetype':
                self.setfiletype(value)
            elif key == 'songinfo':
                self.setsonginfo(value)
        if sampbit > 0:
            self.setsampbit(sampbit)
        if pluginid:
            self._setparams_pluginid = pluginid

    def getparams(self):
        """Gets supported all parameters of the current file in dict object.

        Returns:
            dict: A dict object including all parameters of the current file
            whose keys are ``'nchannels'``, ``'sampbit'``, ``'samprate'``,
            ``'length'``, ``'filetype'``, and ``'songinfo'``.
        """
        return dict(nchannels=self.getnchannels(), sampbit=self.getsampbit(),
                    samprate=self.getsamprate(), length=self.getlength(),
                    pluginid=self.getpluginid(), filetype=self.getfiletype(),
                    filedesc=self.getfiledesc(), filefilter=self.getfilefilter(),
                    songinfo=self.getsonginfo(), sampwidth=self.getrawsampwidth(),
                    framerate=self.getframerate(), nframes=self.getnframes())

    def getparamstuple(self, decodebytes=False):
        """Gets supported all parameters of the current file in namedtuple object.

        Args:
            decodebytes (bool): ``True`` decodes bytes objects into string objects
                obtained by :func:`~spplugin.SpFilePlugin.getcomptype`
                and :func:`~spplugin.SpFilePlugin.getcompname` .
                The standard libraries of wave and sunau expect a decoded string
                object while the standard aifc library expects a bytes object.

        Returns:
            namedtuple: A namedtuple object including all parameters of
            the current file whose entries are
            ``(nchannels, sampwidth, framerate, nframes, comptype, compname)`` .
            This object is compatible with the argument of ``setparams()``
            of standard libraries such as aifc, wave, or sunau.
        """
        return _standard_lib_params(self.getnchannels(), self.getsampwidth(),
                                    self.getframerate(), self.getnframes(),
                                    self.getcomptype(decodebytes),
                                    self.getcompname(decodebytes))

    def getrawarraytypecode(self):
        """Gets the type code for python array.

        Returns:
            char: A type code for the current settings.
        """
        sampbit = self.getrawsampbit()
        if sampbit >= 64:
            typecode = 'd'
        elif sampbit >= 33:
            typecode = 'f'
        elif sampbit > 16:  # sampbit >= 32
            typecode = 'l'
        else:
            typecode = 'h'
        return typecode

    def createrawarray(self, length, nframesflag=False):
        """Creates a raw array for the current file settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).
                    If you want to specify the number of frames,
                    the second argument must be ``True``.
            nframesflag (bool): ``True`` makes the first argument be
                                treated as the number of frames.

        Returns:
            array.array: An array class object for the current file settings.
        """
        if nframesflag:
            length = int(length) * self.getnchannels()
        size = int(length) * self.getrawsampwidth()
        buffer = bytearray(size)
        return array.array(self.getrawarraytypecode(), buffer)

    def getarraytypecode(self):
        """Gets the type code for python array to store double array.

        Returns:
            char: A type code of double array for the current settings.
        """
        return 'd'

    def createarray(self, length, nframesflag=False):
        """Creates a double array for the current file settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).
                    If you want to specify the number of frames,
                    the second argument must be ``True``.
            nframesflag (bool): ``True`` makes the first argument be
                                treated as the number of frames.

        Returns:
            array.array: An array class object for the current file settings.
        """
        if nframesflag:
            length = int(length) * self.getnchannels()
        size = int(length) * 8
        buffer = bytearray(size)
        return array.array(self.getarraytypecode(), buffer)

    def getrawndarraydtype(self):
        """Gets the dtype string for numpy ndarray.

        Returns:
            string: A dtype string for the current settings.
        """
        sampbit = self.getrawsampbit()
        if sampbit >= 64:
            dtypestr = 'f8'
        elif sampbit >= 33:
            dtypestr = 'f4'
        elif sampbit > 16:  # sampbit >= 32
            dtypestr = 'i4'
        else:
            dtypestr = 'i2'
        return dtypestr

    def createrawndarray(self, length, nframesflag=False):
        """Creates a raw numpy ndarray for the current file settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).
                    If you want to specify the number of frames,
                    the second argument must be ``True``.
            nframesflag (bool): ``True`` makes the first argument be
                                treated as the number of frames.

        Returns:
            numpy.ndarray: An ndarray class object for the current file settings.
        """
        import numpy as np
        if nframesflag:
            length = int(length) * self.getnchannels()
        size = int(length) * self.getrawsampwidth()
        buffer = bytearray(size)
        return np.frombuffer(buffer, dtype=self.getrawndarraydtype())

    def getndarraydtype(self):
        """Gets the dtype string for numpy ndarray to store double array.

        Returns:
            string: A dtype string for the current settings.
        """
        return 'f8'

    def createndarray(self, length, nframesflag=False):
        """Creates a numpy double array for the current file settings.

        Args:
            length: A length of the array. Note that this length is
                    not identical to the number of frames
                    (length = nframes * nchannels).
                    If you want to specify the number of frames,
                    the second argument must be ``True``.
            nframesflag (bool): ``True`` makes the first argument be
                                treated as the number of frames.

        Returns:
            numpy.ndarray: An ndarray class object for the current file settings.
        """
        import numpy as np
        if nframesflag:
            length = int(length) * self.getnchannels()
        size = int(length) * 8
        buffer = bytearray(size)
        return np.frombuffer(buffer, dtype=self.getndarraydtype())

    def setpos(self, pos):
        """Seeks to the specified position.

        Args:
            pos: a position to seek.
        """
        if pos < 0 or pos > self.getlength():
            raise ValueError('position not in range')
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        if self._open_mode[0] != 'r':
            raise RuntimeError('file must be opened with read mode')
        if not _spplugin_c.spSeekPlugin(self._plugin, pos):
            raise FileError('seek error')
        else:
            self._currentpos = pos

    def rewind(self):
        """Rewinds to the beginning of the file."""
        self.setpos(0)

    def tell(self):
        """Gets the current position in the file."""
        return self._currentpos

    def setmark(self, id, pos, name):
        """Does nothing (for compatibility with standard libraries
        such as aifc, wave, and sunau)."""
        raise Error('setmark() not supported')

    def getmark(self, id):
        """Does nothing (for compatibility with standard libraries
        such as aifc, wave, and sunau)."""
        raise Error('no marks')

    def getmarkers(self):
        """Does nothing (for compatibility with standard libraries
        such as aifc, wave, and sunau)."""
        return None

    def copyraw2array(self, rawdata, sampwidth, bigendian_or_signed8bit=False):
        """Copies raw bytes (bytearray) data contents to a new raw array (array.array).

        Args:
            rawdata (bytes or bytearray): Input bytes or bytearray object.
            sampwidth (int): bytes/sample of rawdata
            bigendian_or_signed8bit (bool): Specify ``True`` if endianness
                of rawdata is big endian (16- or 32-bit case) or data type
                of rawdata (8-bit case) is signed 8-bit.

        Returns:
            array.array: An array class object which contains converted data.
        """
        dest_bigendian = True if sys.byteorder == 'big' else False
        dest_sampwidth = self.getrawsampwidth()
        length = len(rawdata) // sampwidth
        outarray = self.createrawarray(length)
        _spplugin_c.spCopyBuffer_(memoryview(outarray), dest_sampwidth, dest_bigendian,
                                  rawdata, sampwidth, bigendian_or_signed8bit, 0)
        if sampwidth == 3:
            for n in range(length):
                outarray[n] //= 256
        return outarray

    def copyarray2raw(self, inarray, sampwidth, bigendian_or_signed8bit=False):
        """Copies raw array (array.array) contents to a new raw bytes
        (bytearray) data.

        Args:
            inarray (array.array): Input array object.
            sampwidth (int): bytes/sample of output data.
            bigendian_or_signed8bit (bool): Specify ``True`` if endianness
                of output data is big endian (16- or 32-bit case) or
                data type of output data is signed 8-bit (8-bit case).

        Returns:
            bytearray: A bytearray class object which contains converted data.
        """
        if not isinstance(inarray, array.array):
            raise RuntimeError('input type must be array.array')
        src_bigendian = True if sys.byteorder == 'big' else False
        src_sampwidth = self.getrawsampwidth()
        length = len(inarray)
        rawdata = bytearray(length * sampwidth)
        _spplugin_c.spCopyBuffer_(rawdata, sampwidth, bigendian_or_signed8bit,
                                  memoryview(inarray), src_sampwidth, src_bigendian,
                                  1 if self.getsampbit() == 24 else 0)
        return rawdata

    def readraw(self, data, offset=0, length=0):
        """Reads raw data from the audio file.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer to receive raw data from the audio file.
            offset (int): Optional offset location for the buffer.
            length (int): Optional read length for the buffer.

        Returns:
            int: The read size if successful, -1 otherwise.

        Note:
            The keyword arguments of `offset` and `length` were
            introduced in Version 0.7.5.
        """
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._open_mode[0] != 'r':
            raise RuntimeError('file must be opened with read mode')
        if isinstance(data, bytearray):
            buffer = data
        elif isinstance(data, array.array):
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')

        offsetbyte = int(offset) * self.getrawsampwidth() if offset > 0 else 0
        lengthbyte = int(length) * self.getrawsampwidth() if length > 0 else 0

        nread = _spplugin_c.spReadPluginInByte_(self._plugin, buffer,
                                                offsetbyte, lengthbyte)
        nread2 = nread // self.getrawsampwidth() if nread > 0 else nread
        if nread > 0:
            self._currentpos += nread2 // self._waveinfo_c.num_channel
        return nread2

    def read(self, data, weight=1.0, offset=0, length=0):
        """Reads data to double array from the audio file.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer of double array to receive data from the audio file.
            weight (double): A weighting factor multiplied to data after reading.
            offset (int): Optional offset location for the buffer.
            length (int): Optional read length for the buffer.

        Returns:
            int: The read size if successful, -1 otherwise.

        Note:
            The keyword arguments of `offset` and `length` were
            introduced in Version 0.7.5.
        """
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._open_mode[0] != 'r':
            raise RuntimeError('file must be opened with read mode')
        if isinstance(data, bytearray):
            buffer = data
        elif isinstance(data, array.array):
            if data.typecode != 'd':
                raise RuntimeError('the typecode must be \'d\'')
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            if not np.issubdtype('f8', data.dtype):
                raise RuntimeError('the dtype must be \'f8\' (\'float64\')')
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')
        nread = _spplugin_c.spReadPluginDoubleWeighted_(self._plugin, buffer,
                                                        weight, offset, length)
        if nread > 0:
            self._currentpos += nread // self._waveinfo_c.num_channel
        return nread

    def writeraw(self, data, offset=0, length=0):
        """Writes raw data to the audio file.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer to send raw data to the audio file.
            offset (int): Optional offset location for the buffer.
            length (int): Optional write length for the buffer.

        Returns:
            int: The written size if successful, -1 otherwise.

        Note:
            The keyword arguments of `offset` and `length` were
            introduced in Version 0.7.5.
        """
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._open_mode[0] != 'w':
            raise RuntimeError('file must be opened with write mode')
        if isinstance(data, bytearray) or isinstance(data, bytes):
            buffer = data
        elif isinstance(data, array.array):
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')

        offsetbyte = int(offset) * self.getrawsampwidth() if offset > 0 else 0
        lengthbyte = int(length) * self.getrawsampwidth() if length > 0 else 0

        nwrite = _spplugin_c.spWritePluginInByte_(self._plugin, buffer,
                                                  offsetbyte, lengthbyte)
        nwrite2 = nwrite // self.getrawsampwidth() if nwrite > 0 else nwrite
        if nwrite > 0:
            self._currentpos += nwrite2 // self._waveinfo_c.num_channel
        return nwrite2

    def write(self, data, weight=1.0, offset=0, length=0):
        """Writes data of double array to the audio file.

        Args:
            data (bytearray, array.array or numpy.ndarray):
                A buffer of double array to send data to the audio file.
            weight (double): A weighting factor multiplied to data before writing.
            offset (int): Optional offset location for the buffer.
            length (int): Optional write length for the buffer.

        Returns:
            int: The written size if successful, -1 otherwise.

        Note:
            The keyword arguments of `offset` and `length` were
            introduced in Version 0.7.5.
        """
        if self._plugin is None:
            raise RuntimeError('file must be opened')
        if data is None or len(data) <= 0:
            raise ValueError('a valid buffer must be specified')
        if self._open_mode[0] != 'w':
            raise RuntimeError('file must be opened with write mode')
        if isinstance(data, bytearray) or isinstance(data, bytes):
            buffer = data
        elif isinstance(data, array.array):
            if data.typecode != 'd':
                raise RuntimeError('the typecode must be \'d\'')
            buffer = memoryview(data)
        elif type(data).__name__ == 'ndarray':
            import numpy as np
            if not np.issubdtype('f8', data.dtype):
                raise RuntimeError('the dtype must be \'f8\' (\'float64\')')
            buffer = data.data
        else:
            raise RuntimeError('unsupported data type')
        nwrite = _spplugin_c.spWritePluginDoubleWeighted_(self._plugin, buffer,
                                                          weight, offset, length)
        if nwrite > 0:
            self._currentpos += nwrite // self._waveinfo_c.num_channel
        return nwrite


def open(filename, mode, *, pluginname=None, samprate=0,
         sampbit=0, nchannels=0, filetype=None, songinfo=None, params=None):
    """Opens the file associated with the filename by using a plugin.
    This function may be used in a ``with`` statement.

    Args:
        filename (str): The name of the file to open.
        mode (str): The opening mode. ``'r'`` means read mode, ``'w'`` means
                    write mode.
        pluginname (str): The name of the plugin used when this function
                          cannot find the suitable plugin.
        samprate (double): Sample rate.
        sampbit (int): Bits/sample.
        nchannels (int): The number of channels.
        filetype (str): File type string.
        songinfo (dict): Song information.
        params (dict): All above parameters in dict format.

    Returns:
        SpFilePlugin: A new instance of :class:`~spplugin.SpFilePlugin` class.
    """
    pf = SpFilePlugin()
    try:
        pf.open(filename, mode,
                pluginname=pluginname, samprate=samprate,
                sampbit=sampbit, nchannels=nchannels,
                filetype=filetype, songinfo=songinfo, params=params)
    except Exception as e:
        pf = None
        raise

    return pf
