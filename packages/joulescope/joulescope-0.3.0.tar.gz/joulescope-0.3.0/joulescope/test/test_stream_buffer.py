# Copyright 2018 Jetperch LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test stream buffer
"""

import unittest
import numpy as np
import pyximport; pyximport.install(setup_args={'include_dirs': np.get_include()})
from joulescope.stream_buffer import StreamBuffer, usb_packet_factory

import logging
logging.basicConfig(level=logging.DEBUG)


SAMPLES_PER = 126


class TestStreamBuffer(unittest.TestCase):

    def test_init(self):
        b = StreamBuffer(1000, [10, 10])
        self.assertIsNotNone(b)
        del b

    def test_insert_process(self):
        b = StreamBuffer(1000000, [100, 100, 100])
        frame = usb_packet_factory(0, 1)
        self.assertEqual(0, b.status()['device_sample_id']['value'])
        b.insert(frame)
        self.assertEqual(126, b.status()['device_sample_id']['value'])
        self.assertEqual(0, b.status()['sample_id']['value'])
        b.process()
        self.assertEqual(126, b.status()['sample_id']['value'])
        data = b.raw_get(0, 126)
        expect = np.arange(126*2, dtype=np.uint16).reshape((126, 2))
        np.testing.assert_allclose(expect, np.right_shift(data, 2))
        np.testing.assert_allclose(expect, b.data_buffer[0:126*2].reshape((126, 2)))
        data = b.data_get(0, 126)
        np.testing.assert_allclose(expect[:, 0], data[:, 0, 0])

    def test_wrap_aligned(self):
        frame = usb_packet_factory(0, 4)
        b = StreamBuffer(2 * SAMPLES_PER, [])
        b.insert(frame)
        b.process()
        self.assertEqual((SAMPLES_PER * 2, SAMPLES_PER * 4), b.sample_id_range)
        data = b.raw_get(SAMPLES_PER * 2, SAMPLES_PER * 4)
        data = np.right_shift(data, 2)
        expect = np.arange(SAMPLES_PER * 4, SAMPLES_PER * 8, dtype=np.uint16).reshape((SAMPLES_PER * 2, 2))
        np.testing.assert_allclose(expect, data)
        np.testing.assert_allclose(expect[:, 0], b.data_buffer[::2])
        data = b.data_get(SAMPLES_PER * 2, SAMPLES_PER * 4)
        np.testing.assert_allclose(expect[:, 0], data[:, 0, 0])
        np.testing.assert_allclose(expect[:, 1], data[:, 1, 0])

    def test_wrap_unaligned(self):
        frame = usb_packet_factory(0, 4)
        b = StreamBuffer(2 * SAMPLES_PER + 2, [])
        b.insert(frame)
        b.process()
        self.assertEqual(SAMPLES_PER * 4, b.sample_id_range[1])
        data = np.right_shift(b.raw_get(SAMPLES_PER * 2, SAMPLES_PER * 4), 2)
        expect = np.arange(SAMPLES_PER * 4, SAMPLES_PER * 8, dtype=np.uint16).reshape((SAMPLES_PER * 2, 2))
        np.testing.assert_allclose(expect, data)

    def test_get_over_samples(self):
        b = StreamBuffer(2000, [10, 10])
        frame = usb_packet_factory(0, 1)
        b.insert(frame)
        b.process()
        data = b.data_get(0, 21, 5)
        self.assertEqual((4, 3, 4), data.shape)
        np.testing.assert_allclose(np.arange(10), b.data_buffer[0:10])  # processed correctly
        np.testing.assert_allclose([4.0, 14.0, 24.0, 34.0], data[:, 0, 0])
        np.testing.assert_allclose([4.0, 8.0, 0.0, 8.0], data[0, 0, :])
        np.testing.assert_allclose([5.0, 15.0, 25.0, 35.0], data[:, 1, 0])

    def test_get_over_reduction_direct(self):
        b = StreamBuffer(2000, [10, 10])
        frame = usb_packet_factory(0, 1)
        b.insert(frame)
        b.process()
        data = b.data_get(0, 20, 10)
        self.assertEqual((2, 3, 4), data.shape)
        np.testing.assert_allclose([9.0, 33.0, 0.0, 18.0], data[0, 0, :])
        np.testing.assert_allclose([29.0, 33.0, 20.0, 38.0], data[1, 0, :])
        np.testing.assert_allclose([10.0, 33.0, 1.0, 19.0], data[0, 1, :])
        np.testing.assert_allclose([30.0, 33.0, 21.0, 39.0], data[1, 1, :])

    def test_get_over_reduction(self):
        b = StreamBuffer(2000, [10, 10])
        frame = usb_packet_factory(0, 1)
        b.insert(frame)
        b.process()
        data = b.data_get(0, 40, 20)
        self.assertEqual((2, 3, 4), data.shape)
        np.testing.assert_allclose([19.0, 133.0, 0.0, 38.0], data[0, 0, :])
        np.testing.assert_allclose([20.0, 133.0, 1.0, 39.0], data[0, 1, :])
        np.testing.assert_allclose([59.0, 133.0, 40.0, 78.0], data[1, 0, :])

    def test_calibration(self):
        b = StreamBuffer(2000, [10, 10])
        b.calibration_set([-10.0] * 7, [2.0] * 7, [-2.0, 1.0], [4.0, 1.0])
        frame = usb_packet_factory(0, 1)
        b.insert(frame)
        b.process()
        data = b.data_get(0, 1, 1)
        self.assertEqual((1, 3, 4), data.shape)
        np.testing.assert_allclose([-20.0, -4.0, 80.0], data[0, :, 0])
