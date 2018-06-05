from BaseNode import BaseNode
from birch import entry_count


class Entry(BaseNode):
    # has Vectos
    is_entry = True

    def __init__(self, *args, **kwargs):
        self.vectors = []
        super(Entry, self).__init__(*args, **kwargs)

        global entry_count
        entry_count += 1
        self.radius = 0.0

    def testvolume(self, vector=None):
        if not self.vectors:
            return 0
        vecs = self.vectors[:]

        if vector:
            vecs.append(vector)

        n = len (vecs)

        dist = 0
        for v1 in vecs:
            for v2 in vecs:
                dist += v1.distance(v2)

        vol = (dist/(n*(n-1))) ** 0.5

        # print "vol: ", vol
        return vol
    volume = property(testvolume)

    def test_radius(self, vector):
        if self.n == 0:
            return 0

        new_n = self.n + 1
        new_ls = self.ls + vector.ls
        new_squared = self.squared + vector.squared

        testrad = self.radius + ((new_ls / new_n).distance(vector))
        # print "testrad: ", testrad
        return testrad

    @property
    def volume(self):
        return self.radius

    @property
    def refdist(self):
        dist = 0
        for v1 in self.vectors:
            for v2 in self.vectors:
                dist += v1.distance(v2)
            return dist

    @property
    def height(self):
        return len(self.vectors)

    @property
    def depth(self):
        return 1

    def store_vector(self, vector):
        "Stores a point in its list, this is the end! (I don't really know what this means)"
        self.vectors.append(vector)
        self.update_cf(vector)
        self.radius += (self.ls / self.n).distance(vector)