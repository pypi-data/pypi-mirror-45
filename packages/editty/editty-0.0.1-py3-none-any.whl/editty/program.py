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

import logging
import tempfile
import struct
import uuid

from editty.segment import *

class FrameInfo:
    def __init__(self, **kw):
        self.__dict__.update(kw)

class Program:
    def __init__(self, title='Untitled'):
        self.log = logging.getLogger('program')
        self.title = title
        self.segments = []
        self.length = 0.0
        self.uuid = str(uuid.uuid4())

    def toJSON(self):
        return dict(uuid=self.uuid,
                    title=self.title,
                    segments=[x.toJSON() for x in self.segments])

    @classmethod
    def fromJSON(cls, data, sources):
        p = Program(data['title'])
        p.uuid = data['uuid']
        for segment in data['segments']:
            log = logging.getLogger('program')
            log.debug(segment)
            p.append(Segment.fromJSON(segment, sources))
        return p

    def copy(self):
        p = Program()
        p.title = self.title
        p.segments = [s.copy() for s in self.segments]
        p.length = self.length
        return p

    def cut(self, start, end):
        self.log.debug("cut %s %s", start, end)
        elapsed = 0.0
        cut_program = Program("Cut of %s" % self.title)
        for segment in self.segments[:]:
            segment_start = elapsed
            segment_end = segment_start + segment.duration
            segment_duration = segment.duration
            self.log.debug("consider segment %s %s %s", segment, segment_start, segment_end)
            #    [xxx]
            #[===========]
            if segment_start < start and segment_end > end:
                # The segment should be split and the middle removed
                self.log.debug("split and remove segment %s" % segment)
                # Save it for the clipboard
                clipboard_copy = segment.copy()
                clipboard_copy.start += start - segment_start
                clipboard_copy.end -= segment_end - end
                cut_program.append(clipboard_copy)
                # Make the cut
                segment_index = self.segments.index(segment)
                new_segment = segment.copy()
                self.segments.insert(segment_index+1, new_segment)
                segment.end -= segment_end - start
                new_segment.start += end - segment_start
                # No more segments apply
                break
            #    [xxxxxxxxxxx]
            #[-----][=====][-----]
            #       [xxxxx]
            #[-----][=====][-----]
            elif segment_start >= start and segment_end <= end:
                # The entire segment should be removed
                self.log.debug("remove segment %s" % segment)
                # Save it for the clipboard
                clipboard_copy = segment.copy()
                cut_program.append(clipboard_copy)
                # Make the cut
                self.segments.remove(segment)
            #           [xxxx]
            #[-----][=====][-----]
            #          [xx]
            #[-----][=====][-----]
            elif segment_start < start and segment_end >= start:
                # TODO: if segment_end == start, we may not need this segment in some cases
                # Move back the end of this segment
                delta = segment_end - start
                self.log.debug("move end of segment %s %s", segment, delta)
                # Save it for the clipboard
                clipboard_copy = segment.copy()
                clipboard_copy.start += start - segment_start
                cut_program.append(clipboard_copy)
                # Make the cut
                segment.end -= delta
            #    [xxxx]
            #[-----][=====][-----]
            #       [xx]
            #[-----][=====][-----]
            elif segment_end > end and segment_start <= end:
                # TODO: if segment_start == end, we may not need this segment in some cases
                # Move up the start of this segment
                delta = end - segment_start
                self.log.debug("move start of segment %s %s", segment, delta)
                # Save it for the clipboard
                clipboard_copy = segment.copy()
                clipboard_copy.end -= segment_end - end
                cut_program.append(clipboard_copy)
                # Make the cut
                segment.start += delta
            elapsed += segment_duration
        for segment in self.segments:
            self.log.debug("segment %s %s %s", segment, segment.start, segment.end)
        self.updateLength()
        return cut_program

    def insert(self, timecode, program):
        self.log.debug("insert %s %s", timecode, program)
        elapsed = 0.0
        for segment in self.segments[:]:
            segment_start = elapsed
            segment_end = segment_start + segment.duration
            self.log.debug("consider segment %s %s %s", segment, segment_start, segment_end)
            #        [xx]
            #[======]
            if timecode > segment_end:
                pass
            elif timecode < segment_start:
                pass
            #    [xxx]
            #[===========]
            elif segment_start < timecode < segment_end:
                # The segment should be split and the program inserted in the middle
                self.log.debug("split and insert program %s" % segment)
                segment_index = self.segments.index(segment)
                new_segment = segment.copy()
                segment.end -= segment_end - timecode
                new_segment.start += timecode - segment_start
                self.segments = (self.segments[:segment_index+1] +
                                 program.segments +
                                 [new_segment] +
                                 self.segments[segment_index+1:])
                # No more segments apply
                break
            #[xx]
            #[=====]
            elif segment_start == timecode:
                # The program should be inserted before the current segment
                self.log.debug("prepend segment %s" % segment)
                segment_index = self.segments.index(segment)
                self.segments = (self.segments[:segment_index] +
                                 program.segments +
                                 self.segments[segment_index:])
                # No more segments apply
                break
            #      [xx]
            #[=====]
            elif segment_end == timecode:
                # The program should be appended after the current segment
                self.log.debug("append segment %s", segment)
                segment_index = self.segments.index(segment)
                self.segments = (self.segments[:segment_index+1] +
                                 program.segments +
                                 self.segments[segment_index+1:])
                # No more segments apply
                break
            elapsed += segment.duration
        for segment in self.segments:
            self.log.debug("segment %s %s %s", segment, segment.start, segment.end)
        self.updateLength()

    def append(self, obj):
        if isinstance(obj, Segment):
            self.segments.append(obj)
        elif isinstance(obj, Program):
            self.segments.extend(obj.segments)
        else:
            raise Exception("Can not add %s to Program" % repr(obj))
        self.updateLength()

    def updateLength(self):
        self.length = 0.0
        for segment in self.segments:
            self.length += segment.duration

    def getFramesAtTimecode(self, timecode):
        # Return the frame before, at, and after the timecode
        prev_frame = None
        cur_frame = None
        next_frame = None
        for fi in self:
            if fi.timecode > timecode:
                next_frame = fi
                return (prev_frame, cur_frame, next_frame)
            prev_frame = cur_frame
            cur_frame = fi
        return (prev_frame, cur_frame, next_frame)

    def __iter__(self):
        previous_segment_duration = 0.0
        for si, segment in enumerate(self.segments):
            for (fi, (timecode, frame)) in enumerate(segment):
                yield FrameInfo(timecode=timecode + previous_segment_duration,
                                frame_index=fi,
                                segment_index=si,
                                segment=segment,
                                frame=frame)
            previous_segment_duration += segment.duration

    def getFrames(self, start, end):
        for fi in self:
            if end is not None and fi.timecode > end:
                return
            if start is not None and fi.timecode < start:
                continue
            start = None
            yield fi

    # TODO: this is currently unused
    def render_script(self, size, stream_fn, timing_fn):
        class LoadWidget(urwid.Widget):
            term_modes = urwid.TermModes()
            def beep(self): pass
            def set_title(self, title): pass
        class MyScreen(urwid.raw_display.Screen):
            def signal_init(self): pass
            def signal_restore(self): pass
        canv = urwid.TermCanvas(size[0], size[1], LoadWidget())
        canv.modes.main_charset = urwid.vterm.CHARSET_UTF8
        with tempfile.TemporaryFile() as screen_in:
            with open(stream_fn, 'w') as screen_out:
                with open(timing_fn, 'w') as timing_out:
                    screen_out.write("Rendered by Editty\n")
                    screen = MyScreen(screen_in, screen_out)
                    screen.start()
                    elapsed = 0.0
                    written = 0
                    for fi in self:
                        canv.term = [line[:] for line in fi.frame.content]
                        canv.set_term_cursor(fi.frame.cursor[0], fi.frame.cursor[1])
                        screen.draw_screen(size, canv)
                        screen._screen_buf_canvas=None
                        screen_out.flush()
                        current_pos = screen_out.tell()
                        delta_bytes = current_pos - written
                        delta_time = fi.timecode - elapsed
                        timing_out.write('%0.6f %i\n' % (delta_time, delta_bytes))
                        written = current_pos
                        elapsed = fi.timecode
                    screen.stop()
                    screen_out.write("\n\nRendered by Editty\n")

    # TODO: this is currently unused
    def render_asciicast(self, size, cast_fn):
        class LoadWidget(urwid.Widget):
            term_modes = urwid.TermModes()
            def beep(self): pass
            def set_title(self, title): pass
        class MyScreen(urwid.raw_display.Screen):
            def signal_init(self): pass
            def signal_restore(self): pass
        canv = urwid.TermCanvas(size[0], size[1], LoadWidget())
        canv.modes.main_charset = urwid.vterm.CHARSET_UTF8
        show_cursor_escape = urwid.escape.SHOW_CURSOR
        outdata = dict(version=1,
                       duration=self.length,
                       title="",
                       height=size[1],
                       width=size[0],
                       command=None,
                       stdout=[])
        stdout = outdata['stdout']
        with tempfile.TemporaryFile() as screen_in:
            with tempfile.TemporaryFile('w+') as screen_out:
                with open(cast_fn, 'w') as cast_out:
                    screen = MyScreen(screen_in, screen_out)
                    screen.start()
                    elapsed = 0.0
                    for fi in self:
                        canv.term = [line[:] for line in fi.frame.content]
                        canv.set_term_cursor(fi.frame.cursor[0], fi.frame.cursor[1])
                        if fi.segment.visible_cursor:
                            urwid.escape.SHOW_CURSOR = show_cursor_escape
                        else:
                            urwid.escape.SHOW_CURSOR = ''
                        screen.draw_screen(size, canv)
                        screen._screen_buf_canvas=None
                        screen_out.flush()
                        delta_bytes = screen_out.tell()
                        screen_out.seek(0)
                        data = screen_out.read()
                        self.log.debug("read %s chars %s bytes of %s" % (len(data), len(data.encode('utf8')), delta_bytes))
                        screen_out.seek(0)
                        screen_out.truncate()
                        if len(data.encode('utf8')) != delta_bytes:
                               raise Exception("Short read")
                        delta_time = fi.timecode - elapsed
                        stdout.append([delta_time, data])
                        self.log.debug("frame %s %s", delta_time, len(data))
                        elapsed = fi.timecode
                    cast_out.write(json.dumps(outdata))
                    screen.stop()
        urwid.escape.SHOW_CURSOR = show_cursor_escape

    def render_ttyrec(self, size, ttyrec_fn):
        class LoadWidget(urwid.Widget):
            term_modes = urwid.TermModes()
            def beep(self): pass
            def set_title(self, title): pass
        class MyScreen(urwid.raw_display.Screen):
            def signal_init(self): pass
            def signal_restore(self): pass
        canv = urwid.TermCanvas(size[0], size[1], LoadWidget())
        canv.modes.main_charset = urwid.vterm.CHARSET_UTF8
        show_cursor_escape = urwid.escape.SHOW_CURSOR
        with tempfile.TemporaryFile() as screen_in:
            with tempfile.TemporaryFile('w+') as screen_out:
                with open(ttyrec_fn, 'wb') as ttyrec_out:
                    screen = MyScreen(screen_in, screen_out)
                    screen.start()
                    first = True
                    for fi in self:
                        canv.term = [line[:] for line in fi.frame.content]
                        canv.set_term_cursor(fi.frame.cursor[0], fi.frame.cursor[1])
                        if fi.segment.visible_cursor:
                            urwid.escape.SHOW_CURSOR = show_cursor_escape
                        else:
                            urwid.escape.SHOW_CURSOR = ''
                        screen.draw_screen(size, canv)
                        screen._screen_buf_canvas=None
                        screen_out.flush()
                        delta_bytes = screen_out.tell()
                        screen_out.seek(0)
                        data = screen_out.read()
                        self.log.debug("read %s chars %s bytes of %s" % (len(data), len(data.encode('utf8')), delta_bytes))
                        screen_out.seek(0)
                        screen_out.truncate()
                        if len(data.encode('utf8')) != delta_bytes:
                               raise Exception("Short read")
                        if first:
                            prefix = '\x1b%%G\x1b[8;%s;%st' % (size[1], size[0])
                            data = prefix + data
                            first = False
                        tc_secs, tc_usecs = map(int, ('%0.6f' % fi.timecode).split('.'))
                        data = data.encode('utf8')
                        ttyrec_out.write(struct.pack('<III',
                                                     tc_secs, tc_usecs, len(data)))
                        ttyrec_out.write(data)
                        self.log.debug("frame %s %s %s", tc_secs, tc_usecs, len(data))
                        elapsed = fi.timecode
                    if elapsed < self.length:
                        data = '\x1b[1;1H'.encode('utf8')
                        tc_secs, tc_usecs = map(int, ('%0.6f' % self.length).split('.'))
                        ttyrec_out.write(struct.pack('<III',
                                                     tc_secs, tc_usecs, 0))
                    screen.stop()
        urwid.escape.SHOW_CURSOR = show_cursor_escape
