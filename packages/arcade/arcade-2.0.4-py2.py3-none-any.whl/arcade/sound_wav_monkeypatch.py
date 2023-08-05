# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2018 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

"""Simple Python-only RIFF reader, supports uncompressed WAV files.
"""

import pyglet

import wave

class WAVEFormatException(pyglet.media.exceptions.MediaFormatException):
    pass


class WaveSource(pyglet.media.StreamingSource):
    def __init__(self, filename, file=None):
        if file is None:
            file = open(filename, 'rb')

        self._file = file

        try:
            self._wave = wave.open(file)
        except wave.Error as e:
            raise WAVEFormatException(e)

        parameters = self._wave.getparams()

        self.audio_format = pyglet.media.codecs.base.AudioFormat(channels=parameters.nchannels,
                                                                 sample_size=parameters.sampwidth * 8,
                                                                 sample_rate=parameters.framerate)

        self._bytes_per_frame = parameters.nchannels * parameters.sampwidth
        self._duration = parameters.nframes / parameters.framerate
        self._duration_per_frame = self._duration / parameters.nframes
        self._num_frames = parameters.nframes

        self._wave.rewind()

    def __del__(self):
        self._file.close()

    def get_audio_data(self, num_bytes, compensation_time=0.0):
        num_frames = max(1, num_bytes // self._bytes_per_frame)

        data = self._wave.readframes(num_frames)
        if not data:
            return None

        timestamp = self._wave.tell() / self.audio_format.sample_rate
        duration = num_frames / self.audio_format.sample_rate
        return pyglet.media.codecs.base.AudioData(data, len(data), timestamp, duration, [])

    def seek(self, timestamp):
        timestamp = max(0.0, min(timestamp, self._duration))
        position = int(timestamp / self._duration_per_frame)
        self._wave.setpos(position)


#########################################
#   Decoder class:
#########################################

class WaveDecoder(object):

    def get_file_extensions(self):
        return ['.wav', '.wave', '.riff']

    def decode(self, file, filename, streaming):
        if streaming:
            return WaveSource(filename, file)
        else:
            return pyglet.media.codecs.base.StaticSource(WaveSource(filename, file))


def get_decoders():
    return [WaveDecoder()]


def get_encoders():
    return []
