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

import argparse
import copy
import os
import sys
import struct
import time
import threading
import json
import uuid
try:
    import queue
except:
    import Queue as queue
import logging
import math

import urwid

from editty.segment import *
from editty.program import *
import editty.source

PALETTE = [
    ('reversed', 'standout', ''),

    ('timeline-title', 'dark cyan', ''),
    ('selected-timeline-title', 'light cyan', ''),

    ('timeline-1-text', 'dark cyan', ''),
    ('timeline-1', 'black', 'dark cyan'),
    ('timeline-1-selection', 'black,standout', 'dark cyan'),
    ('selected-timeline-1-text', 'light cyan', ''),
    ('selected-timeline-1', 'black', 'light cyan'),
    ('selected-timeline-1-selection', 'black,standout', 'light cyan'),

    ('timeline-2-text', 'dark magenta', ''),
    ('timeline-2', 'black', 'dark magenta'),
    ('timeline-2-selection', 'black,standout', 'dark magenta'),
    ('selected-timeline-2-text', 'light magenta', ''),
    ('selected-timeline-2', 'black', 'light magenta'),
    ('selected-timeline-2-selection', 'black,standout', 'light magenta'),

    ('timeline-3-text', 'dark green', ''),
    ('timeline-3', 'black', 'dark green'),
    ('timeline-3-selection', 'black,standout', 'dark green'),
    ('selected-timeline-3-text', 'light green', ''),
    ('selected-timeline-3', 'black', 'light green'),
    ('selected-timeline-3-selection', 'black,standout', 'light green'),

    ('timeline-4-text', 'brown', ''),
    ('timeline-4', 'black', 'brown'),
    ('timeline-4-selection', 'black,standout', 'brown'),
    ('selected-timeline-4-text', 'yellow', ''),
    ('selected-timeline-4', 'black', 'yellow'),
    ('selected-timeline-4-selection', 'black,standout', 'yellow'),

    ('timeline-black-text', 'dark gray', ''),
    ('timeline-black', 'black', 'dark gray'),
    ('timeline-black-selection', 'black,standout', 'dark gray'),
    ('selected-timeline-black-text', 'light gray', ''),
    ('selected-timeline-black', 'black', 'light gray'),
    ('selected-timeline-black-selection', 'black,standout', 'light gray'),

    ('start-timecode', 'dark cyan', ''),
    ('selected-start-timecode', 'light cyan', ''),
    ('current-timecode', 'light red', ''),
    ('end-timecode', 'dark cyan', ''),
    ('selected-end-timecode', 'light cyan', ''),
]

FOCUS_MAP = {}
for x in PALETTE:
    name = x[0]
    if 'selected-'+name in [y[0] for y in PALETTE]:
        FOCUS_MAP[name]='selected-'+name

class Monitor(urwid.Widget):
    _selectable = False
    _sizing = frozenset([urwid.widget.FIXED])

    signals = ['closed', 'beep', 'leds', 'title']

    def __init__(self, editor, size):
        self.log = logging.getLogger('monitor')
        self.editor = editor
        self.size = size
        self.term_modes = urwid.TermModes()
        self.term = urwid.TermCanvas(size[0], size[1], self)
        self.term.modes.main_charset = urwid.vterm.CHARSET_UTF8
        self.off_canvas = urwid.TextCanvas(maxcol=size[0], text=[b'' for x in range(size[1])])
        self.off_canvas.cacheable = False
        self.off = False

    def render(self, size, focus=False):
        if self.off:
            return self.off_canvas
        else:
            return self.term

    def pack(self, size, focus=False):
        self.log.debug("pack")
        return self.size

    def rows(self, size, focus=False):
        return self.size[1]

    def keypress(self, size, key):
        return None

    def beep(self):
        self._emit('beep')

    def set_title(self, title):
        self._emit('title', title)

    def setFrame(self, frame):
        self.term.term = [line[:] for line in frame.content]
        self.term.set_term_cursor(frame.cursor[0], frame.cursor[1])
        self.editor.loop.draw_screen()

    def setTimecode(self, start, current, end):
        if start is not None:
            self._setTimecode(self.editor.screen.start_timecode,
                              'selected-start-timecode', start)
        else:
            self._setTimecode(self.editor.screen.start_timecode,
                              'start-timecode', 0.0)
        self._setTimecode(self.editor.screen.timecode,
                          'current-timecode', current)
        if end is not None:
            self._setTimecode(self.editor.screen.end_timecode,
                              'selected-end-timecode', end)
        else:
            self._setTimecode(self.editor.screen.end_timecode,
                              'end-timecode', 0.0)

    def _setTimecode(self, widget, attr, seconds):
        hours, seconds = divmod(seconds, 60*60)
        minutes, seconds = divmod(seconds, 60)
        tc = '%02i:%02i:%09.6f' % (hours, minutes, seconds)
        widget.set_text((attr, tc))

class Timeline(urwid.Text):
    _selectable = True

    def __init__(self):
        super(Timeline, self).__init__('')
        self.log = logging.getLogger('timeline')
        self.uuid = str(uuid.uuid4())
        self.set_text('AB'*60)
        self.log.debug("init")
        self.scale = 1.0  # one second per char
        self.hoffset = 0
        self.current_width = 0
        self.framecounts = []
        self.framecolors = []
        self.start_time = None
        self.end_time = None
        self.current_time = 0.0
        self.current_frame = None
        self.monitor = None
        self.play_queue = queue.Queue()
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon=True
        self._thread.start()
        self.playing = False
        self.color = 'timeline-black'

    def toJSON(self):
        if self.program:
            program = self.program.uuid
        else:
            program = None
        return dict(uuid=self.uuid,
                    color=self.color,
                    program=program)

    @classmethod
    def fromJSON(cls, data):
        t = Timeline()
        t.uuid = data['uuid']
        t.color = data['color']
        return t

    def setProgram(self, program):
        self.program = program
        self.setScale(self.scale)
        for fi in program:
            self.color = fi.frame.timeline_color
            break

    def setMonitor(self, monitor):
        self.monitor = monitor
        self.updateMonitor()

    def updateMonitor(self, update_frame=True):
        if not self.monitor:
            return
        if update_frame and self.current_frame:
            self.monitor.setFrame(self.current_frame.frame)
        self.monitor.setTimecode(self.start_time, self.current_time, self.end_time)
        screen = self.monitor.editor.screen
        if self.current_frame:
            screen.md_segment.set_text(str(self.current_frame.segment_index+1))
            screen.md_type.set_text(self.current_frame.segment.__class__.__name__)
            if hasattr(self.current_frame.segment, 'source'):
                screen.md_source.set_text(self.current_frame.segment.source.title)
            else:
                screen.md_source.set_text('')
            screen.md_segment_start.set_text('%0.6f' % (self.current_frame.segment.start))
            screen.md_segment_end.set_text('%0.6f' % (self.current_frame.segment.end))
            screen.md_segment_duration.set_text('%0.6f' % (self.current_frame.segment.duration))
            screen.md_frame.set_text(str(self.current_frame.frame_index+1))
            screen.md_cursor.set_text(self.current_frame.segment.visible_cursor and 'visible' or 'hidden')

    def setScale(self, scale):
        self.scale = scale
        count = int(math.ceil(self.program.length / self.scale))
        self.framecounts = [0 for x in range(count)]
        self.framecolors = ['' for x in range(count)]
        elapsed = 0.0
        for fi in self.program:
            pos = int(math.floor(fi.timecode / self.scale))
            self.framecounts[pos] += 1
            self.framecolors[pos] = fi.frame.timeline_color
        for i in range(len(self.framecolors)):
            if i and not self.framecolors[i]:
                self.framecolors[i] = self.framecolors[i-1]
        self.set_text('')

    def pack(self, size, focus=False):
        self.log.debug("pack %s %s", size, focus)

    def rows(self, size, focus=False):
        return 1

    def render(self, size, focus=False):
        title = '%-10s' % self.program.title[:10]
        title_len = len(title)
        text_attr = self.color + '-text'
        s = [(text_attr, title)]
        current_pos = int(math.floor(self.current_time / self.scale))
        start_pos = end_pos = current_pos

        range_points = 0
        if self.start_time is not None:
            start_pos = int(math.floor(self.start_time / self.scale))
            range_points += 1
        if self.end_time is not None:
            end_pos = int(math.floor(self.end_time / self.scale))
            range_points += 1
        selection_range = sorted([start_pos, end_pos])

        self.current_width = size[0]-title_len-2
        if current_pos > self.current_width+self.hoffset-1:
            self.hoffset = current_pos-self.current_width+1
        if current_pos < self.hoffset:
            self.hoffset = current_pos
        left_arrow = self.hoffset>0 and '<' or ' '
        right_arrow = self.hoffset+self.current_width<len(self.framecounts) and '>' or ' '
        s.append((text_attr, left_arrow))
        for i in range(self.hoffset, self.hoffset+self.current_width):
            if i < len(self.framecounts):
                if self.framecounts[i] > 1:
                    char = '•'  #▪▬■·•‧
                elif self.framecounts[i] > 0:
                    char = '‧'
                else:
                    char = ' '
                attr = self.framecolors[i] or self.color
            else:
                char = ' '
                attr = ''
            if selection_range[0] <= i < selection_range[1]:
                if range_points == 2 and i == current_pos:
                    pass
                else:
                    attr += '-selection'
            elif i == current_pos:
                attr += '-selection'
            s.append((attr, char))
        s.append((text_attr, right_arrow))
        self.set_text(s)
        return super(Timeline, self).render(size, focus)

    def updateCurrentFrame(self):
        pass

    def move(self, offset):
        self.log.debug('move %s time %s', offset, self.current_time)
        if abs(offset) >= 1:
            new_time = self.current_time + (offset * self.scale)
        else:
            new_time = self.current_time + offset
        new_time = max(0.0, min(self.program.length, new_time))
        if abs(offset) >= 1:
            new_time = math.floor(new_time / self.scale) * self.scale
        # Find the closest frame no later than the new time
        (prv, cur, nxt) = self.program.getFramesAtTimecode(new_time)
        self.log.debug('move %s %s %s', prv, cur, nxt)
        self.current_time = new_time
        if cur is None:
            if prv is None:
                self.current_frame = None
            else:
                self.current_frame = prv
        else:
            self.current_frame = cur
            # If our cell has at least one frame in it, jump ahead to the
            # first frame.
            if abs(offset) >= 1 and self.current_time > cur.timecode and nxt:
                if self.current_time + self.scale > nxt.timecode:
                    self.current_time = nxt.timecode
                    self.current_frame = nxt
        self.updateMonitor()
        self.set_text('')
        self.log.debug('move %s time %s', offset, self.current_time)

    def setStart(self):
        self.start_time = self.current_time
        self.set_text('')
        self.updateMonitor(update_frame=False)

    def setEnd(self):
        if self.current_time + self.scale > self.program.length:
            # If we're in the last cell, the user probably meant to go
            # to the end.
            self.end_time = self.program.length
        else:
            self.end_time = self.current_time
        self.set_text('')
        self.updateMonitor(update_frame=False)

    def clearSelection(self):
        self.start_time = None
        self.end_time = None
        self.set_text('')
        self.updateMonitor(update_frame=False)

    # Edit
    def cut(self):
        self.log.debug("cut")
        if self.start_time is None or self.end_time is None:
            return
        self.monitor.editor.saveUndo("Cut", (self.program,))
        saved = self.program.cut(self.start_time, self.end_time)
        self.monitor.editor.setClipboard(saved)
        if self.current_time > self.end_time:
            self.current_time -= (self.end_time - self.start_time)
        elif self.current_time > self.start_time:
            self.current_time = self.start_time
        self.clearSelection()
        self.setScale(self.scale)
        self.move(0)

    def insert(self):
        self.log.debug("insert")
        if self.monitor.editor.clipboard is None:
            return
        self.monitor.editor.saveUndo("Insert", (self.program,))
        self.program.insert(self.current_time, self.monitor.editor.clipboard)
        self.setScale(self.scale)
        self.move(0)

    def append(self):
        self.log.debug("append")
        if self.monitor.editor.clipboard is None:
            return
        self.monitor.editor.saveUndo("Append", (self.program,))
        self.program.append(self.monitor.editor.clipboard)
        self.setScale(self.scale)
        self.move(0)

    def toggleCursor(self):
        self.log.debug("cursor")
        self.monitor.editor.saveUndo("Toggle Cursor", (self.program,))
        self.current_frame.segment.visible_cursor = not self.current_frame.segment.visible_cursor
        self.move(0)

    # Playback
    def play(self):
        self.log.debug("play")
        self.playing = True
        if self.end_time is not None:
            end = self.end_time
        else:
            end = self.program.length
        if self.start_time is not None:
            start = self.start_time
        else:
            if self.current_time == end:
                start = 0.0
            else:
                start = self.current_time
        self.play_queue.put((start, end))

    def stop(self):
        self.log.debug("stop")
        self.playing = False

    # Playback thread
    def run(self):
        while True:
            item = self.play_queue.get()
            if item is None:
                return
            self._runPlay(item)
            self.playing = False

    def _runClock(self, start_wallclock_time, start_timecode, end_delay):
        while True:
            if not self.playing: return
            cur_wallclock_time = time.time()
            if cur_wallclock_time >= end_delay: break
            elapsed_wallclock_time = cur_wallclock_time - start_wallclock_time
            self.current_time = start_timecode + elapsed_wallclock_time
            self.updateMonitor(update_frame=False)
            self.set_text('')
            self.monitor.editor.loop.draw_screen()
            time.sleep(0)

    def _runPlay(self, item):
        start_timecode, end_timecode = item
        self.log.debug("play %s %s", start_timecode, end_timecode)
        self.current_time = start_timecode
        self.move(0)
        self.monitor.editor.loop.draw_screen()
        start_wallclock_time = time.time()
        first = True
        for fi in self.program.getFrames(start_timecode, end_timecode):
            end_delay = start_wallclock_time + fi.timecode - start_timecode
            self._runClock(start_wallclock_time, start_timecode, end_delay)
            if not self.playing: return
            self.current_frame = fi
            if not first:
                self.monitor.setFrame(self.current_frame.frame)
                self.monitor.editor.loop.draw_screen()
            else:
                first = False
        end_delay = start_wallclock_time + end_timecode - start_timecode
        self._runClock(start_wallclock_time, start_timecode, end_delay)
        if not self.playing: return
        self.current_time = end_timecode
        self.updateMonitor()
        self.monitor.editor.loop.draw_screen()
        self.log.debug("done play %s", self.current_time)

    def keypress(self, size, key):
        self.log.debug(repr(key))
        if self.playing and key != ' ':
            return None
        if key == (' '):
            if self.playing:
                self.stop()
            else:
                self.play()
        elif key == '[':
            self.setStart()
        elif key == ']':
            self.setEnd()
        elif key == 'esc':
            self.clearSelection()
        elif key == 'right':
            self.move(1)
        elif key == 'meta right':
            self.move(10)
        elif key == 'shift right':
            self.move(0.01)
        elif key == 'left':
            self.move(-1)
        elif key == 'meta left':
            self.move(-10)
        elif key == 'shift left':
            self.move(-0.01)
        elif key == '=':
            self.setScale(self.scale / 2)
        elif key == '-':
            self.setScale(self.scale * 2)
        elif key == 'x':
            self.cut()
        elif key == 'i':
            self.insert()
        elif key == 'a':
            self.append()
        elif key == 'C':
            self.toggleCursor()
        elif key == 'ctrl r':
            self.monitor.editor.render(self.program)
        return key

class Screen(urwid.WidgetWrap):
    def __init__(self, editor, size):
        super(Screen, self).__init__(urwid.Pile([]))
        self.log = logging.getLogger('screen')
        self.editor = editor
        self.size = size

        self.monitor = Monitor(editor, self.size)
        self.start_timecode = urwid.Text('00:00:00.000000', align='center')
        self.timecode = urwid.Text('00:00:00.000000', align='center')
        self.end_timecode = urwid.Text('00:00:00.000000', align='center')
        self.timecode_cols = urwid.Columns([
            ('weight', 1, urwid.Text(' ')),
            (15, self.start_timecode),
            (17, urwid.Text(' ')),
            (15, self.timecode),
            (17, urwid.Text(' ')),
            (15, self.end_timecode),
            ('weight', 1, urwid.Text(' ')),
            ])
        self.timeline = None
        self.md_segment = urwid.Text('')
        self.md_type = urwid.Text('')
        self.md_source = urwid.Text('')
        self.md_segment_start = urwid.Text('')
        self.md_segment_end = urwid.Text('')
        self.md_segment_duration = urwid.Text('')
        self.md_frame = urwid.Text('')
        self.md_cursor = urwid.Text('')
        metadata_pile = urwid.Pile([
            ('pack', urwid.Columns([(11, urwid.Text('Segment: ')),   ('weight', 1, self.md_segment)])),
            ('pack', urwid.Columns([(11, urwid.Text('Type: ')),     ('weight', 1, self.md_type)])),
            ('pack', urwid.Columns([(11, urwid.Text('Source: ')),   ('weight', 1, self.md_source)])),
            ('pack', urwid.Columns([(11, urwid.Text('Start: ')), ('weight', 1, self.md_segment_start)])),
            ('pack', urwid.Columns([(11, urwid.Text('End: ')), ('weight', 1, self.md_segment_end)])),
            ('pack', urwid.Columns([(11, urwid.Text('Duration: ')), ('weight', 1, self.md_segment_duration)])),
            ('pack', urwid.Columns([(11, urwid.Text('Frame: ')),     ('weight', 1, self.md_frame)])),
            ('pack', urwid.Columns([(11, urwid.Text('Cursor: ')),     ('weight', 1, self.md_cursor)])),
        ])
        program_box = urwid.LineBox(self.monitor, "Monitor")
        metadata_box = urwid.LineBox(metadata_pile)
        border = 2
        monitor_columns = urwid.Columns([
            #('weight', 1, urwid.Filler(urwid.Text(''))),
            (self.size[0]+border, program_box),
            metadata_box,
            #('weight', 1, urwid.Filler(urwid.Text(''))),
            ])
        lw = urwid.SimpleFocusListWalker([])
        self.timelines = urwid.ListBox(lw)
        urwid.connect_signal(lw, 'modified', self._updateFocus)
        self.main = urwid.Pile([])
        self.main.contents.append((monitor_columns, ('given', self.size[1]+border)))
        self.main.contents.append((self.timecode_cols, ('pack', None)))
        self.main.contents.append((self.timelines, ('weight', 1)))
        self.main.contents.append((urwid.Filler(urwid.Text(u'')), ('weight', 1)))
        self.main.set_focus(2)

        self._w.contents.append((self.main, ('weight', 1)))
        self._w.set_focus(0)

    def addTimeline(self, program, timeline=None):
        if timeline is None:
            timeline = Timeline()
        timeline.setProgram(program)
        timeline.setMonitor(self.monitor)
        w = urwid.AttrMap(timeline, None, focus_map=FOCUS_MAP)
        self.timelines.body.append(w)
        self.timeline = timeline
        self.timelines.set_focus(len(self.timelines.body)-1)

    def getTimelines(self):
        for w in self.timelines.body:
            yield w.original_widget

    def removeTimeline(self, timeline):
        if timeline == self.timeline:
            self.timeline = None
        for w in self.timelines.body:
            if w.original_widget == timeline:
                self.timelines.body.remove(w)
                return

    def _updateFocus(self):
        self.log.debug("update focus")
        if self.timeline:
            self.log.debug("clear monitor %s", self.timeline)
            self.timeline.setMonitor(None)
        if self.timelines.focus:
            self.timeline = self.timelines.focus.original_widget
            self.log.debug("set focus %s", self.timeline)
            self.timeline.setMonitor(self.monitor)
            self.log.debug("set monitor %s", self.timeline)
        else:
            self.log.debug("no timeline in focus")

    def keypress(self, size, key):
        self.log.debug(repr(key))
        if self.timeline and self.timeline.playing and key != ' ':
            return None
        if key == 'ctrl l':
            self.editor.load()
        elif key == 'ctrl o':
            self.editor.open()
        elif key == 'ctrl _':
            self.editor.undo()
        elif key == 'ctrl s':
            self.editor.save()
        return super(Screen, self).keypress(size, key)

class MainLoop(urwid.MainLoop):
    def __init__(self, *args, **kw):
        self._screen_lock = threading.RLock()
        super(MainLoop, self).__init__(*args, **kw)

    def draw_screen(self):
        with self._screen_lock:
            super(MainLoop, self).draw_screen()

class UndoRecord:
    def __init__(self, description, programs):
        self.description = description
        self.programs = programs

class FixedButton(urwid.Button):
    def sizing(self):
        return frozenset([urwid.FIXED])

    def pack(self, size, focus=False):
        return (len(self.get_label())+4, 1)

class LoadDialog(urwid.WidgetWrap):
    def __init__(self, editor):
        self.editor = editor
        self.ok = FixedButton("Load")
        self.cancel = FixedButton("Cancel")
        urwid.connect_signal(self.ok, 'click', editor._finishLoad, self)
        urwid.connect_signal(self.cancel, 'click', editor._clearPopup, self)

        file_types = []
        self.type_buttons = []
        self.button_types = {}
        for ft in editty.source.all_types:
            b = urwid.RadioButton(file_types, ft.name)
            self.type_buttons.append(b)
            self.button_types[b] = ft
        for b in self.type_buttons:
            urwid.connect_signal(b, 'postchange', self.setType)
        self.current_type = None

        buttons = urwid.Columns([
            ('pack', self.ok),
            ('pack', urwid.Text(' ')),
            ('pack', self.cancel),
            ])
        self.stream_file = urwid.Edit("")
        self.timing_file = urwid.Edit("Timing file: ")
        self.listbox = urwid.ListBox([
            urwid.Text('File type:'),
            ] + self.type_buttons + [
            urwid.Text(''),
            self.stream_file,
            urwid.Text(''),
            buttons,
            ])
        self.setType(self.current_type, self)
        super(LoadDialog, self).__init__(urwid.LineBox(self.listbox, 'Load'))

    def setType(self, button, dialog):
        # Only handle the second event
        selected = [b for b in self.type_buttons if b.state]
        if len(selected) > 1:
            return

        selected = selected[0]
        self.current_type = self.button_types[selected]

        if not self.current_type.timing:
            if self.timing_file in self.listbox.body:
                self.listbox.body.remove(self.timing_file)
        else:
            if self.timing_file not in self.listbox.body:
                loc = self.listbox.body.index(self.stream_file)
                self.listbox.body.insert(loc+1, self.timing_file)
        self.stream_file.set_caption('%s file: ' % self.current_type.name)

    def keypress(self, size, key):
        if key == 'esc':
            self.editor._clearPopup()
            return None
        if key == 'enter':
            if(self.current_type.timing and
               self.listbox.focus is self.stream_file):
                return self.keypress(size, 'down')
            if(self.listbox.focus is self.timing_file or
               self.listbox.focus is self.stream_file):
                return self.ok.keypress(size, key)
        return super(LoadDialog, self).keypress(size, key)

class SaveDialog(urwid.WidgetWrap):
    def __init__(self, editor):
        self.editor = editor
        self.ok = FixedButton("Save")
        self.cancel = FixedButton("Cancel")
        urwid.connect_signal(self.ok, 'click', editor._finishSave, self)
        urwid.connect_signal(self.cancel, 'click', editor._clearPopup, self)
        buttons = urwid.Columns([
            ('pack', self.ok),
            ('pack', urwid.Text(' ')),
            ('pack', self.cancel),
            ])
        self.project_file = urwid.Edit("Project file: ")
        self.listbox = urwid.ListBox([
            self.project_file,
            urwid.Text(''),
            buttons,
            ])
        super(SaveDialog, self).__init__(urwid.LineBox(self.listbox, 'Save'))

    def keypress(self, size, key):
        if key == 'esc':
            self.editor._clearPopup()
            return None
        if key == 'enter':
            if(self.listbox.focus is self.project_file):
                return self.ok.keypress(size, key)
        return super(SaveDialog, self).keypress(size, key)

class OpenDialog(urwid.WidgetWrap):
    def __init__(self, editor):
        self.editor = editor
        self.ok = FixedButton("Open")
        self.cancel = FixedButton("Cancel")
        urwid.connect_signal(self.ok, 'click', editor._finishOpen, self)
        urwid.connect_signal(self.cancel, 'click', editor._clearPopup, self)
        buttons = urwid.Columns([
            ('pack', self.ok),
            ('pack', urwid.Text(' ')),
            ('pack', self.cancel),
            ])
        self.project_file = urwid.Edit("Project file: ")
        self.listbox = urwid.ListBox([
            self.project_file,
            urwid.Text(''),
            buttons,
            ])
        super(OpenDialog, self).__init__(urwid.LineBox(self.listbox, 'Open'))

    def keypress(self, size, key):
        if key == 'esc':
            self.editor._clearPopup()
            return None
        if key == 'enter':
            if(self.listbox.focus is self.project_file):
                return self.ok.keypress(size, key)
        return super(OpenDialog, self).keypress(size, key)

class RenderDialog(urwid.WidgetWrap):
    def __init__(self, editor, program):
        self.editor = editor
        self.program = program
        self.ok = FixedButton("Render")
        self.cancel = FixedButton("Cancel")
        urwid.connect_signal(self.ok, 'click', editor._finishRender, self)
        urwid.connect_signal(self.cancel, 'click', editor._clearPopup, self)
        buttons = urwid.Columns([
            ('pack', self.ok),
            ('pack', urwid.Text(' ')),
            ('pack', self.cancel),
            ])
        self.ttyrec_file = urwid.Edit("Ttyrec file: ")
        self.listbox = urwid.ListBox([
            self.ttyrec_file,
            urwid.Text(''),
            buttons,
            ])
        super(RenderDialog, self).__init__(urwid.LineBox(self.listbox, 'Render'))

    def keypress(self, size, key):
        if key == 'esc':
            self.editor._clearPopup()
            return None
        if key == 'enter':
            if(self.listbox.focus is self.ttyrec_file):
                return self.ok.keypress(size, key)
        return super(RenderDialog, self).keypress(size, key)

class QuitDialog(urwid.WidgetWrap):
    def __init__(self, editor):
        self.editor = editor
        self.yes = FixedButton("Yes")
        self.no = FixedButton("No")
        urwid.connect_signal(self.yes, 'click', editor._quit, self)
        urwid.connect_signal(self.no, 'click', editor._clearPopup, self)
        buttons = urwid.Columns([
            ('pack', self.yes),
            ('pack', urwid.Text(' ')),
            ('pack', self.no),
            ])
        self.listbox = urwid.ListBox([
            urwid.Text('Are you sure you want to quit?\n'),
            buttons,
            ])
        super().__init__(urwid.LineBox(self.listbox, 'Quit'))

    def keypress(self, size, key):
        if key == 'esc':
            self.editor._clearPopup()
            return None
        return super().keypress(size, key)

class MessageDialog(urwid.WidgetWrap):
    def __init__(self, editor, title, message):
        self.editor = editor
        ok = FixedButton("OK")
        urwid.connect_signal(ok, 'click', editor._clearPopup, self)
        buttons = urwid.Columns([
            ('pack', ok),
            ])
        listbox = urwid.ListBox([
            urwid.Text(message),
            urwid.Text(''),
            buttons,
            ])
        super(MessageDialog, self).__init__(urwid.LineBox(listbox, title))

    def keypress(self, size, key):
        if key == 'esc':
            self.editor._clearPopup()
            return None
        return super().keypress(size, key)

class Editor(object):
    def __init__(self, args):
        self.size = (args.width, args.height)
        if args.debuglog:
            logfile = os.path.expanduser(args.debuglog)
            logging.basicConfig(filename=logfile, level=logging.DEBUG)
        self.log = logging.getLogger('editor')
        self.screen = Screen(self, self.size)
        self.loop = MainLoop(self.screen, palette=PALETTE,
                             unhandled_input=self.unhandledInput)
        self.loop.screen.tty_signal_keys(start='undefined', stop='undefined')
        self.loop.screen.set_terminal_properties(colors=256)
        self.loop.screen.start()
        self.clipboard = None
        self.programs = []
        self.undo_history = []
        self.timeline_color_generator = self._timelineColorGenerator()
        self.output_program = Program('Output')
        if args.project:
            self._open(args.project)

    def _timelineColorGenerator(self):
        while True:
            for i in range(1, 5):
                yield 'timeline-%i' % i

    def setSize(self, size):
        self.size = size
        self.screen = Screen(self, self.size)
        self.loop.widget = self.screen

    def help(self):
        msg = ('Use the arrow keys to move left and right in the timeline. '
               'Use meta-arrows to move longer distances and shift-arrows '
               'to move shorter distances.\n\n')
        for key, desc in [
                ('CTRL-l', 'Load terminal recording'),
                ('CTRL-o', 'Open Editty program file'),
                ('CTRL-s', 'Save Editty program file'),
                ('CTRL-r', 'Render'),
                ('CTRL-_', 'Undo'),
                ('CTRL-q', 'Quit'),
                ('SPACE', 'Play'),
                ('[',   'Set selection start'),
                (']',   'Set selection end'),
                ('ESC', 'Clear start/end points'),
                ('ARROW', 'Move left/right'),
                ('META-ARROW', 'Move 10x left/right'),
                ('SHIFT-ARROW', 'Move 0.01x left/right'),
                ('=',   'Zoom in timescale'),
                ('-',   'Zoom out timescale'),
                ('x',   'Cut selection to clipboard'),
                ('a',   'Append clipboard contents to end of timeline'),
                ('i',   'Insert clipboard contents to end of timeline'),
                ('C',   'Toggle whether cursor is visible in this segment'),
                ]:
            msg += '%-11s %s\n' % (key, desc)
        self.message("Help", msg, min_width=60, width=30, height=50)

    def unhandledInput(self, key):
        if key == 'f1':
            self.help()
        elif key == 'ctrl q':
            self.quit()

    def quit(self):
        dialog = QuitDialog(self)
        self.screen.monitor.off = True
        overlay = urwid.Overlay(dialog, self.screen,
                                'center', ('relative', 50),
                                'middle', ('relative', 25))
        self.loop.widget = overlay

    def _quit(self):
        raise urwid.ExitMainLoop()

    def saveUndo(self, description, programs):
        # Make an undo record, programs is a list of programs which
        # are about to change.
        saved_programs = []
        program_timelines = {}
        for timeline in self.screen.getTimelines():
            self.log.debug("save undo %s %s", timeline.program, timeline.uuid)
            if timeline.program:
                program_timelines[timeline.program] = timeline.uuid
        for p in self.programs:
            timeline_uuid = program_timelines.get(p)
            if p in programs:
                p = p.copy()
            saved_programs.append((p, timeline_uuid))
        ur = UndoRecord(description, saved_programs)
        self.undo_history.append(ur)

    def undo(self):
        undorecord = self.undo_history.pop()
        current_timelines = set(self.screen.getTimelines())
        self.programs = []
        self.log.debug("undo %s", undorecord.description)
        self.log.debug("undo %s", undorecord.programs)
        self.log.debug("current %s", current_timelines)
        for (program, timeline_uuid) in undorecord.programs:
            self.programs.append(program)
            for t in current_timelines:
                self.log.debug("undo %s %s", t.uuid, timeline_uuid)
                if t.uuid == timeline_uuid:
                    self.log.debug("found")
                    current_timelines.remove(t)
                    t.setProgram(program)
                    break
            else:
                self.log.debug("undo added new timeline for %s", program)
                self.screen.addTimeline(program)
        for t in current_timelines:
            self.log.debug("removed unused timeline %s", t)
            self.screen.removeTimeline(t)

    def setClipboard(self, program):
        self.clipboard = program

    def run(self):
        self.loop.run()

    def _clearPopup(self, *args, **kw):
        self.screen.monitor.off = False
        self.loop.widget = self.screen
        self.loop.draw_screen()

    def message(self, title, message, width=50, height=25,
                min_width=None, min_height=None):
        dialog = MessageDialog(self, title, message)
        self.screen.monitor.off = True
        overlay = urwid.Overlay(dialog, self.screen,
                                'center', ('relative', width),
                                'middle', ('relative', height),
                                min_width=min_width,
                                min_height=min_height)

        self.loop.widget = overlay

    def load(self):
        dialog = LoadDialog(self)
        self.screen.monitor.off = True
        overlay = urwid.Overlay(dialog, self.screen,
                                'center', ('relative', 50),
                                'middle', ('relative', 25))
        self.loop.widget = overlay

    def _load(self, file_type, stream_file, timing_file, program=None):
        color = next(self.timeline_color_generator)
        source = file_type.load(self.size, stream_file, timing_file, color)
        if program is None:
            program = Program(source.title)
        program.append(Clip(source, 0.0, source.length))
        self.saveUndo("Load %s" % stream_file, [])
        self.programs.append(program)
        self.screen.addTimeline(program)

    def _finishLoad(self, button, dialog):
        self._clearPopup()
        try:
            self._load(dialog.current_type,
                       dialog.stream_file.edit_text,
                       dialog.timing_file.edit_text)
        except Exception as e:
            self.message("Error", str(e))

    def save(self):
        dialog = SaveDialog(self)
        self.screen.monitor.off = True
        overlay = urwid.Overlay(dialog, self.screen,
                                'center', ('relative', 50),
                                'middle', ('relative', 25))
        self.loop.widget = overlay

    def _save(self, project_file):
        data = {'version': 1}
        data['size'] = self.size
        data['sources'] = []
        data['programs'] = []
        data['timelines'] = []
        sources = set()
        programs = set()
        for timeline in self.screen.getTimelines():
            data['timelines'].append(timeline.toJSON())
            if timeline.program:
                programs.add(timeline.program)
        for program in programs:
            data['programs'].append(program.toJSON())
            for segment in program.segments:
                if hasattr(segment, 'source'):
                    sources.add(segment.source)
        for source in sources:
            data['sources'].append(source.toJSON())
        with open(project_file, 'w') as f:
            f.write(json.dumps(data))

    def _finishSave(self, button, dialog):
        pf = dialog.project_file.edit_text
        self._clearPopup()
        self.log.debug("save %s", pf)
        try:
            self._save(pf)
        except Exception as e:
            self.message("Error", str(e))

    def open(self):
        dialog = OpenDialog(self)
        self.screen.monitor.off = True
        overlay = urwid.Overlay(dialog, self.screen,
                                'center', ('relative', 50),
                                'middle', ('relative', 25))
        self.loop.widget = overlay

    def _open(self, project_file):
        with open(project_file, 'r') as f:
            data = json.loads(f.read())

        for timeline in list(self.screen.getTimelines()):
            self.screen.removeTimeline(timeline)
        size = data['size']
        self.setSize(size)
        sources = {}
        for source in data['sources']:
            sc = editty.source.SourceClip.fromJSON(source)
            sources[sc.uuid] = sc
        programs = {}
        for program in data['programs']:
            p = Program.fromJSON(program, sources)
            programs[p.uuid] = p
            self.programs.append(p)
        for timeline in data['timelines']:
            t = Timeline.fromJSON(timeline)
            program = programs.get(timeline['program'])
            self.screen.addTimeline(program, timeline=t)

    def _finishOpen(self, button, dialog):
        pf = dialog.project_file.edit_text
        self._clearPopup()
        self.log.debug("open %s", pf)
        try:
            self._open(pf)
        except Exception as e:
            self.message("Error", str(e))

    def render(self, program):
        dialog = RenderDialog(self, program)
        self.screen.monitor.off = True
        overlay = urwid.Overlay(dialog, self.screen,
                                'center', ('relative', 50),
                                'middle', ('relative', 25))
        self.loop.widget = overlay

    def _render(self, ttyrec, program):
        program.render_ttyrec(self.size, ttyrec)

    def _finishRender(self, button, dialog):
        tf = dialog.ttyrec_file.edit_text
        program = dialog.program
        self._clearPopup()
        self.log.debug("render %s", tf)
        try:
            self._render(tf, program)
        except Exception as e:
            self.message("Error", str(e))

def main():
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('--width', type=int, default=80,
                        help='Screen width')
    parser.add_argument('--height', type=int, default=24,
                        help='Screen height')
    parser.add_argument('--debuglog',
                        help='Debug log file path')
    parser.add_argument('project', nargs='?',
                        help='project file')
    args = parser.parse_args()
    e = Editor(args)
    e.run()
