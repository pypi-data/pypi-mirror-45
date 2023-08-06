"""
Author: David Torpey

License: Apache 2.0

Redistribution Licensing:
- Scikit-Learn: https://github.com/scikit-learn/scikit-learn/blob/master/COPYING
- NumPy: https://www.numpy.org/license.html#

Module containing a Python implementation of the BOW
(bag-of-words) feature encoding algorithm.
"""

import numpy as np
from sklearn.cluster import MiniBatchKMeans, KMeans


class BOW(object):
    """
    Class for the implementation of the
    BoW feature encoding algorithm.
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
                ).fit(local_features)
        else:
            self.codebook = \
                KMeans(
                    n_clusters=self.codebook_size
                ).fit(local_features)

    def compute_bow_descriptor(self, local_features):
        """Function to compute the bag-of-words feature
        vector for a set of local feature vectors.

        Args:
            local_features: The data matrix to use to compute the
                            VLAD descriptor.

        Returns:
            BoW descriptor.
        """

        if self.codebook is None:
            raise Exception('Please run learn_codebook method.')

        cluster_assignments = self.codebook.predict(local_features)

        bow_descriptor = np.zeros((self.codebook_size,))
        for cluster_assignment in cluster_assignments:
            bow_descriptor[cluster_assignment] += 1.0

        return bow_descriptor / np.linalg.norm(bow_descriptor)
