# This file is the implementation of the BIRCH Algorithm
# Created by Higor Ernandes on 04/16/2018, on a really tired monday night.
# Made based on this article: http://www.ques10.com/p/9298/explain-birch-algorithm-with-example/
# Code based on this git: https://github.com/janoberst/BIRCH/blob/master/birch.py
import random

from datetime import datetime
import Node
from Vector import Vector

# SETTINGS
Branch = 10                             # Limits the amout of children a node can have.
Treshold = 5000                         # Maximum size (Treshold) of a cluster before it has to be split.

# SAMPLE EXECUTION SETTINGS
sample_dimensions = 10                  # How many dimensions our tree has.
sample_vectors_fill_percentage = 50     # To which percentage are the vectors filled. At 50% and 10 dimensions our vectors will on average have a value in 5 dimensions. This simulates sparse vectors.
num_sample_points = 100                 # Tow many vectors to insert.

# STATISTICS
split_count = 0
node_count = 0
entry_count = 0
leaf_count = 0

# Phase 1: Loading data into memory
# Phase 2: Condense data
# Phase 3: Global clustering
# Phase 4: Cluster refining

if __name__ == '__main__':

    Branch = 10
    Treshold = 35
    sample_dimensions = 2
    sample_vectors_fill_percentage = 10
    num_sample_points = 100

    vectors = []
    print "Creating vectors... (%i-dimensional, %i%% filled, %i vectors, branch %i, treshold %i)" % \
          (sample_dimensions, sample_vectors_fill_percentage, num_sample_points, Branch, Treshold)

    # We'll produce random sample points
    # note that these points really are sparse vectors!
    # we're adding random values to random dimensions
    # so in the end only a few dimensions will have values!
    for x in range(num_sample_points):
        vector = Vector()
        hit = False
        while not hit:
            for x in range(sample_dimensions):
                if random.randint(0, 100 / sample_vectors_fill_percentage) == 0:
                    hit = True
                    vector[x] = random.randint(0, 100)
        vectors.append(vector)

    # Measuring computing time.
    start = datetime.now()
    print "Start clustering..."

    # Building the first node - root node.
    root = Node.Node()

    # Insert vector after vector
    for v in vectors:
        # Insert this vector to the tree's root.
        root.trickle(v)

    time = datetime.now() - start
    print "Took %s (%.2fms frames per point)" % (time, (time.seconds * 1000 + time.microseconds / 1000.0) / num_sample_points)