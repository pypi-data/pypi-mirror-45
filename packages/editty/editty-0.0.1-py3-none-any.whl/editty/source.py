# -*- coding: utf-8 -*-
# Copyright (C) 2019 James E. Blair <corvus@gnu.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
import time
import struct
import uuid

import urwid

class Frame:
    def __init__(self, term, timeline_color, content=None, cursor=None):
        if content is not None:
            self.content = content
        else:
            self.content = [line[:] for line in term.content()]
        if cursor is not None:
            self.cursor = cursor
        else:
            self.cursor = term.term_cursor[:]
        self.timeline_color = timeline_color
        # TODO: cursor visibility, current color

class SourceClip:
    def __init__(self, size, title, stream_fn, timing_fn, timeline_color):
        self.title = 'Untitled'
        self.size = size
        self.frames = []
        self.times = []
        self.length = 0.0
        self.uuid = str(uuid.uuid4())
        self.timeline_color = timeline_color

    def addFrame(self, timecode, frame):
        self.frames.append(frame)
        self.times.append(timecode)
        self.length = timecode

    def toJSON(self):
        return dict(uuid=self.uuid,
                    size=self.size,
                    stream=self.stream_fn,
                    timing=self.timing_fn,
                    color=self.timeline_color)

    @classmethod
    def fromJSON(cls, data):
        ft = getFileType(data['type'])
        sc = ft.load(data['size'], data['stream'], data['timing'], data['color'])
        sc.uuid = data['uuid']
        return sc

    def getFrames(self, start, end):
        # In case we need to supply the frame before the start:
        prev = None
        yielded = False
        for fi in zip(self.times, self.frames):
            if end is not None and fi[0] > end:
                if not yielded and prev is not None:
                    yield (start, prev[1])
                return
            if start is not None:
                if fi[0] < start:
                    prev = fi
                    continue
                if prev is not None and fi[0] > start:
                    yield (start, prev[1])
                    yielded = True
            start = None
            yield fi
            yielded = True

class FileType:
    timing = False

    def __init__(self):
        self.log = logging.getLogger('file')

    def _loadCanvas(self, size, stream_fn, timing_fn, timeline_color):
        title = os.path.split(stream_fn)[-1]
        source_clip = SourceClip(size, title, stream_fn, timing_fn, timeline_color)
        class LoadWidget(urwid.Widget):
            term_modes = urwid.TermModes()
            def beep(self): pass
            def set_title(self, title): pass
        canv = urwid.TermCanvas(size[0], size[1], LoadWidget())
        canv.modes.main_charset = urwid.vterm.CHARSET_UTF8

        return (source_clip, canv)

class ScriptFile(FileType):
    name = 'Script'
    timing = True

    def load(self, size, stream_fn, timing_fn, timeline_color):
        self.log.debug('Loading %s %s', stream_fn, timing_fn)
        source_clip, canvas = self._loadCanvas(size, stream_fn, timing_fn, timeline_color)
        start = time.time()
        buffer_pos = 0
        timecode = 0.0
        with open(stream_fn, 'rb') as s:
            stream = s.read()
            i = stream.find(b'\n')
            stream = stream[i+1:]
        with open(timing_fn) as f:
            for i, line in enumerate(f):
                delay, count = line.strip().split(' ')
                delay = float(delay)
                count = int(count)
                timecode += delay
                data = stream[buffer_pos:buffer_pos+count]
                canvas.addstr(data)
                buffer_pos += count
                source_clip.addFrame(timecode, Frame(canvas, timeline_color))
        end = time.time()
        self.log.debug('Finished loading %s', end-start)
        return source_clip

class TtyrecFile(FileType):
    name = 'Ttyrec'

    def load(self, size, stream_fn, timing_fn, timeline_color):
        self.log.debug('Loading %s %s', stream_fn, timing_fn)
        source_clip, canvas = self._loadCanvas(size, stream_fn, timing_fn, timeline_color)
        with open(stream_fn, 'rb') as ttyrec_in:
            start_time = None
            while True:
                header = ttyrec_in.read(12)
                if not header:
                    self.log.debug("no header")
                    break
                tc_secs, tc_usecs, dlen = struct.unpack('<III', header)
                timecode = tc_secs + tc_usecs/1000000.0
                if start_time is None:
                    # If the first frame is less than a year from the
                    # epoch, assume we are 0-based, otherwise, assume
                    # it's epoch-based and use the first timecode as
                    # the basis.
                    if timecode > 365*24*60*60:
                        start_time = timecode
                    else:
                        start_time = 0.0
                data = ttyrec_in.read(dlen)
                if len(data) != dlen:
                    raise Exception("short read")
                canvas.addstr(data)
                self.log.debug("Frame %0.6f %i" % (timecode, dlen))
                source_clip.addFrame(timecode-start_time, Frame(canvas, timeline_color))
        return source_clip

all_types = [
    TtyrecFile(),
    ScriptFile(),
]

def getFileType(name):
    for ft in all_types:
        if ft.name == name:
            return ft
