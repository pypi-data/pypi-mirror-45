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
import uuid

import urwid

class Segment(object):
    def __init__(self):
        super().__init__()
        self.visible_cursor = True

    def __repr__(self):
        return '<%s from %s to %s (%s seconds)>' % (self.__class__.__name__, self.start, self.end, self.duration)

    @classmethod
    def fromJSON(cls, data, sources):
        if data['type'] == 'clip':
            ret = Clip.fromJSON(data, sources)
        elif data['type'] == 'freeze-frame':
            ret = FreezeFrame.fromJSON(data, sources)
        elif data['type'] == 'black':
            ret = Black.fromJSON(data, sources)
        elif data['type'] == 'dissolve':
            ret = Dissolve.fromJSON(data, sources)
        else:
            raise Exception("Unknown segment type: %s" % data.get('type'))
        ret.visible_cursor = data.get('visible_cursor', True)
        return ret

    def toJSON(self):
        return dict(visible_cursor=self.visible_cursor)

    def updateCopy(self, copy):
        copy.visible_cursor = self.visible_cursor
        return copy

class Clip(Segment):
    def __init__(self, source, start, end, **kw):
        super().__init__(**kw)
        self.source = source
        self.start = start
        self.end = end

    def toJSON(self):
        d = super().toJSON()
        d.update(dict(type='clip',
                      source=self.source.uuid,
                      start=self.start,
                      end=self.end))
        return d

    @classmethod
    def fromJSON(cls, data, sources):
        return Clip(sources[data['source']],
                    data['start'],
                    data['end'])

    @property
    def duration(self):
        return self.end - self.start

    def copy(self):
        ret = Clip(self.source, self.start, self.end)
        return super().updateCopy(ret)

    def __iter__(self):
        for fi in self.source.getFrames(self.start, self.end):
            yield (fi[0]-self.start, fi[1])

class Still(Segment):
    def __init__(self, duration):
        super(Still, self).__init__()
        self.duration = duration

    @property
    def start(self):
        return 0.0

    @start.setter
    def start(self, start):
        self.duration -= start

    @property
    def end(self):
        return self.duration

    @end.setter
    def end(self, end):
        delta = end - self.duration
        self.duration -= delta

class FreezeFrame(Still):
    def __init__(self, source, timecode, duration):
        super(FreezeFrame, self).__init__(duration)
        self.source = source
        self.start = 0.0
        self.timecode = timecode
        self.end = duration

    def toJSON(self):
        return dict(type='freeze-frame',
                    source=self.source.uuid,
                    timecode=self.timecode,
                    duration=self.end)

    @classmethod
    def fromJSON(cls, data, sources):
        return FreezeFrame(sources[data['source']],
                           data['timecode'],
                           data['duration'])

    def copy(self):
        ret = FreezeFrame(self.source, self.timecode, self.duration)
        return super().updateCopy(ret)

class Black(Still):
    def __init__(self, duration):
        super(Black, self).__init__(duration)
        self.start = 0.0
        self.end = duration

    def toJSON(self):
        return dict(type='black',
                    duration=self.end)

    @classmethod
    def fromJSON(cls, data, sources):
        return Black(data['duration'])

    def copy(self):
        ret = Black(self.duration)
        return super().updateCopy(ret)

class Dissolve(Segment):
    def __init__(self, start_source, start_timecode, end_source, end_timecode, duration, **kw):
        super().__init__(**kw)
        self.log = logging.getLogger('program')
        self.start_source = start_source
        self.start_timecode = start_timecode
        self.end_source = end_source
        self.end_timecode = end_timecode
        self.duration = duration
        self._cache = []
        self._update()

    def copy(self):
        ret = Dissolve(self.start_source, self.start_timecode,
                       self.end_source, self.end_timecode, self.duration)
        return super().updateCopy(ret)

    @classmethod
    def fromJSON(cls, data, sources):
        return Dissolve(sources[data['start_source']],
                        data['start_timecode'],
                        sources[data['end_source']],
                        data['end_timecode'],
                        data['duration'])

    def toJSON(self):
        d = super().toJSON()
        d.update(dict(type='dissolve',
                      start_source=self.start_source.uuid,
                      start_timecode=self.start_timecode,
                      end_source=self.end_source.uuid,
                      end_timecode=self.end_timecode,
                      duration=self.duration))
        return d

    @property
    def start(self):
        return 0.0

    @start.setter
    def start(self, start):
        self.duration -= start
        self._update()

    @property
    def end(self):
        return self.duration

    @end.setter
    def end(self, end):
        delta = end - self.duration
        self.duration -= delta
        self._update()

    def __iter__(self):
        for x in self._cache:
            yield x

    def _update(self):
        start = list(self.start_source.getFrames(self.start_timecode, self.start_timecode))[0]
        end = list(self.end_source.getFrames(self.end_timecode, self.end_timecode))[0]
        self._cache = []
        num_frames = int(self.duration * 10)
        for tween_index in range(num_frames):
            tween_frame = self._render(start[1], end[1], tween_index / (self.duration*10.0))
            self._cache.append((self.start+(tween_index/10.0), tween_frame))

    def _fixrgb(self, rgb, background):
        ret = []
        for i in range(len(rgb)):
            if rgb[i] is None:
                ret.append(background[i])
            else:
                ret.append(rgb[i])
        return ret

    def _render(self, start, end, progress):
        line_list = []
        attr_list = []
        line_text = ''
        line_attrs = []
        current_attr = [None, 0]
        current_rgb = None
        current_props = None
        ret_content = []
        background = urwid.AttrSpec('light gray', 'black')
        for line_i in range(len(start.content)):
            ret_line = []
            for char_i in range(len(start.content[line_i])):
                if line_i == 1 and char_i == 0:
                    self.log.debug("tween %s %s", start.content[line_i][char_i], end.content[line_i][char_i])
                oldattr, oldcs, oldchar = start.content[line_i][char_i]
                newattr, newcs, newchar = end.content[line_i][char_i]
                if oldattr is None:
                    oldrgb = background.get_rgb_values()
                else:
                    oldrgb = oldattr.get_rgb_values()
                oldrgb = self._fixrgb(oldrgb, background.get_rgb_values())
                if newattr is None:
                    newrgb = background.get_rgb_values()
                else:
                    newrgb = newattr.get_rgb_values()
                newrgb = self._fixrgb(newrgb, background.get_rgb_values())
                if newchar == b' ' and oldchar != b' ':
                    char = oldchar
                    charattr = oldattr
                    newrgb = newrgb[3:]*2
                elif oldchar == b' ' and newchar != b' ':
                    char = newchar
                    charattr = newattr
                    oldrgb = oldrgb[3:]*2
                elif progress >= 0.5:
                    char = newchar
                    charattr = newattr
                else:
                    char = oldchar
                    charattr = oldattr
                rgb = []
                props = []
                if charattr and charattr.bold:
                    props.append('bold')
                if charattr and charattr.underline:
                    props.append('underline')
                if charattr and charattr.standout:
                    props.append('standout')
                if charattr and charattr.blink:
                    props.append('blink')
                for x in range(len(oldrgb)):
                    rgb.append(int(((newrgb[x]-oldrgb[x])*progress)+oldrgb[x])>>4)
                fg = ', '.join(props + ['#%x%x%x' % tuple(rgb[:3])])
                bg = '#%x%x%x' % tuple(rgb[3:])
                attr = urwid.AttrSpec(fg, bg)
                ret_line.append((attr, oldcs, char))
            ret_content.append(ret_line)
        if progress > 0.5:
            which = end
        else:
            which = start
        frame = Frame(None, which.timeline_color, content=ret_content, cursor=which.cursor)
        return frame
