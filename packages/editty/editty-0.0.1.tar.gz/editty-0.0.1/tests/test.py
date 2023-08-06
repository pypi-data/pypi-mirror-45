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
import struct
import tempfile

import testtools
import fixtures

from editty.segment import *
from editty.program import *
import editty.source

class BaseTestCase(testtools.TestCase):
    def setUp(self):
        super().setUp()
        fs = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
        self.useFixture(fixtures.FakeLogger(level=logging.DEBUG,
                                            format=fs))
        self.log = logging.getLogger("test")

class FileTypeTests:
    def get_frames(self, source):
        ret = []
        for (timecode, frame) in source.getFrames(0, source.length):
            ret.append((timecode, b''.join([x[2] for x in frame.content[0]]).strip()))
        return ret

    def test_load(self):
        source = self.setup()
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (3.0, b'abc'), (4.0, b'abcd')],
            self.get_frames(source))

class TestScriptFile(BaseTestCase, FileTypeTests):
    def setup(self):
        size = (80, 24)
        with tempfile.NamedTemporaryFile() as stream:
            with tempfile.NamedTemporaryFile() as timing:
                stream.write(b"\nabcd")
                for x in range(4):
                    timing.write(b"1.0 1\n")
                stream.flush()
                timing.flush()
                source = editty.source.ScriptFile().load(
                    size, stream.name, timing.name, 'color')
        return source

class TestTtyrecFile(BaseTestCase, FileTypeTests):
    def setup(self):
        size = (80, 24)
        frames = [(1.0, b'a'), (2.0, b'b'), (3.0, b'c'), (4.0, b'd')]
        with tempfile.NamedTemporaryFile() as stream:
            for (timecode, data) in frames:
                tc_secs, tc_usecs = map(int, ('%0.6f' % timecode).split('.'))
                stream.write(struct.pack('<III',
                                             tc_secs, tc_usecs, len(data)))
                stream.write(data)
            stream.flush()
            source = editty.source.TtyrecFile().load(
                size, stream.name, None, 'color')
        return source

class TestProgram(BaseTestCase):
    size = (80, 24)

    def setup(self, color='1'):
        with tempfile.NamedTemporaryFile() as stream:
            with tempfile.NamedTemporaryFile() as timing:
                stream.write(b"\nabcd")
                for x in range(4):
                    timing.write(b"1.0 1\n")
                stream.flush()
                timing.flush()
                source = editty.source.ScriptFile().load(
                    self.size, stream.name, timing.name, color)
        program = Program(source.title)
        program.append(Clip(source, 0.0, source.length))
        return program

    def get_frames(self, program, start, end, color=False):
        ret = []
        for fi in program.getFrames(start, end):
            if color:
                ret.append((fi.timecode, b''.join([x[2] for x in fi.frame.content[0]]).strip(), fi.frame.timeline_color))
            else:
                ret.append((fi.timecode, b''.join([x[2] for x in fi.frame.content[0]]).strip()))
        return ret

    def test_playback(self):
        program = self.setup()
        frames = self.get_frames(program, 0, program.length)
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (3.0, b'abc'), (4.0, b'abcd')],
            frames)

    def test_cut(self):
        p1 = self.setup('1')
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (3.0, b'abc'), (4.0, b'abcd')],
            self.get_frames(p1, None, None))

        cut = p1.cut(2.0, 3.0)
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (2.0, b'abc'), (3.0, b'abcd')],
            self.get_frames(p1, None, None))
        self.assertEqual(
            [(0.0, b'ab'), (1.0, b'abc')],
            self.get_frames(cut, None, None))

        p2 = self.setup('2')
        p2.insert(2.5, cut)
        self.log.debug(self.get_frames(p2, None, None, True))

        cut = p2.cut(2.0, 4.0)
        p3 = self.setup('3')
        self.log.debug("cut")
        for s in cut.segments:
            self.log.debug(s)
        self.log.debug(self.get_frames(cut, None, None, True))
        self.assertEqual(
            [(0.0, b'ab', '2'), (0.5, b'ab',  '1'), (1.5, b'abc', '1'),
             (1.5, b'ab', '2'), (2.0, b'abc', '2')],
            self.get_frames(cut, None, None, True))
        p3.insert(2.5, cut)
        self.log.debug(self.get_frames(p3, None, None, True))
        self.assertEqual(
            [(1.0, b'a',  '3'), (2.0, b'ab',  '3'),
             (2.5, b'ab', '2'),
             (3.0, b'ab', '1'), (4.0, b'abc', '1'),
             (4.0, b'ab', '2'), (4.5, b'abc', '2'),
             (4.5, b'ab', '3'), (5.0, b'abc', '3'), (6.0, b'abcd', '3')],
            self.get_frames(p3, None, None, True))

    def test_repeated_cut(self):
        p1 = self.setup('1')
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (3.0, b'abc'), (4.0, b'abcd')],
            self.get_frames(p1, None, None))

        cut = p1.cut(2.0, 3.0)
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (2.0, b'abc'), (3.0, b'abcd')],
            self.get_frames(p1, None, None))
        self.assertEqual(
            [(0.0, b'ab'), (1.0, b'abc')],
            self.get_frames(cut, None, None))
        p2 = Program('2')
        self.log.debug('append')
        for s in cut.segments:
            self.log.debug(s)
        p2.append(cut)
        self.log.debug('appended')
        for s in p2.segments:
            self.log.debug(s)
        self.log.debug(self.get_frames(p2, None, None, True))

        cut = p1.cut(2.2, 2.7)  # 3.2 - 3.7
        self.log.debug(self.get_frames(p1, None, None))
        self.assertEqual(
            [(1.0, b'a'), (2.0, b'ab'), (2.0, b'abc'), (2.2, b'abc'), (2.5, b'abcd')],
            self.get_frames(p1, None, None))
        self.log.debug(self.get_frames(cut, None, None))
        self.assertEqual(
            [(0.0, b'abc')],
            self.get_frames(cut, None, None))
        self.log.debug('append')
        for s in cut.segments:
            self.log.debug(s)
        p2.append(cut)
        self.log.debug('appended')
        for s in p2.segments:
            self.log.debug(s)
        self.log.debug(self.get_frames(p2, None, None, True))
        self.assertEqual(
            [(0.0, b'ab', '1'), (1.0, b'abc', '1'), (1.0, b'abc', '1')],
            self.get_frames(p2, None, None, True))
