"""
Author: David Torpey

License: Apache 2.0

Redistribution Licensing:
- NumPy: https://www.numpy.org/license.html#

Module with unit tests for the BoW implementation.
"""

import unittest

import numpy as np

from theama.feature_encoding.vlad import VLAD


class VLADTests(unittest.TestCase):

    def setUp(self):
        self.K = 32
        self.vlad = VLAD(self.K)
        self.D = 128
        self.dummy_descriptors = np.random.random((100, self.D))

    def tearDown(self):
        pass

    def test_codebook_creation(self):
        self.vlad.learn_codebook(self.dummy_descriptors)

        self.assertTrue(self.vlad.codebook is not None)

    def test_compute_vlad_without_codebook_creation(self):
        with self.assertRaises(Exception) as context:
            self.vlad.compute_vlad_descriptor(self.dummy_descriptors)

        self.assertTrue('Please run learn_codebook method.' in context.exception)

    def test_compute_vlad_with_codebook_creation(self):
        self.vlad.learn_codebook(self.dummy_descriptors)

        vlad_descriptor = self.vlad.compute_vlad_descriptor(self.dummy_descriptors)
        vlad_descriptor_dimension = len(vlad_descriptor)

        self.assertEqual(vlad_descriptor_dimension, self.D * self.K)