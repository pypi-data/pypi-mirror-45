"""
Author: David Torpey

License: Apache 2.0

Redistribution Licensing:
- Scikit-Learn: https://github.com/scikit-learn/scikit-learn/blob/master/COPYING
- NumPy: https://www.numpy.org/license.html#

Module containing a Python implementation of the VLAD
algorithm, as defined in the original paper, which can be
found at:

https://lear.inrialpes.fr/pubs/2010/JDSP10/jegou_compactimagerepresentation.pdf
"""

import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans


class VLAD(object):
    """
    Class implementing VLAD algorithm.
    """

    def __init__(self, codebook_size):
        self.codebook_size = codebook_size

        self.codebook = None

    def learn_codebook(self, local_features, mini_batch_kmeans=True):
        """Function to learn the codebook for VLAD by
        performing K-Means clustering. The mini-batch
        K-Means algorithm can be optionally chosen for
        speed improvement, but at the cost of less
        accurate centroid estimates.

        Args:
            local_features: The data matrix to use to learn the
                  codebook.
            mini_batch_kmeans: Boolean flag indicating
                               whether to use the
                               mini-batch K-Means
                               algorithm.
        """

        if mini_batch_kmeans:
            self.codebook = \
                MiniBatchKMeans(
                    n_clusters=self.codebook_size
                ).fit(local_features).cluster_centers_
        else:
            self.codebook = \
                KMeans(
                    n_clusters=self.codebook_size
                ).fit(local_features).cluster_centers_

    def compute_vlad_descriptor(self, local_features):
        """Function to compute VLAD descriptor using
        learned codebook.

        Args:
             local_features: The data matrix to use to compute the
                             VLAD descriptor.

        Returns:
            VLAD descriptor.
        """

        if self.codebook is None:
            raise Exception('Please run learn_codebook method.')

        cluster_feature_map = {i: [] for i in range(self.codebook_size)}

        for local_feature in local_features:
            closest_visual_word_index = np.linalg.norm(
                self.codebook - local_feature.reshape(1, -1),
                axis=1
            ).argmin()

            cluster_feature_map[closest_visual_word_index].append(local_feature)

        vlad_descriptor = []
        for visual_word_index, associated_local_features in cluster_feature_map.iteritems():
            visual_word = self.codebook[visual_word_index]

            sum_of_residuals = np.zeros_like(visual_word, dtype=np.float64)
            for local_feature in associated_local_features:
                residual = local_feature - visual_word
                sum_of_residuals += residual
            vlad_descriptor.append(sum_of_residuals)

        vlad_descriptor = np.array(vlad_descriptor)
        vlad_descriptor = vlad_descriptor.ravel()
        vlad_descriptor = vlad_descriptor / np.linalg.norm(vlad_descriptor)

        return vlad_descriptor
