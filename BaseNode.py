from Vector import Vector
from birch import node_count


class BaseNode(object):

    @property
    def is_root(self):
        return not self.parent

    @property
    def level(self):
        count = 0
        r = self.parent
        while r:
            r = r.parent
            count += 1
        return count

    def __init__(self):
        global node_count
        node_count += 1

        self.n = 0
        self.ls = Vector()
        self.squared = 0

        self.parent = None

    def indent(self):
        indent = '\n'
        r = self.parent
        while r:
            r = r.parent
            indent += '       '
        return indent

    @classmethod
    def closest(cls, node, list, force=False):
        "Returns the closest match of node to list"
        min_dist = 0
        min_item = None

        for item in list:
            dist = item.distance(node)
            # if not force:
            #    print "d:",dist,len(node),len(list)

            if not min_item:
                min_item = item
                min_dist = dist
            elif dist < min_dist:
                min_dist = dist
                min_item = item

        return min_item

    def d0(self, other):
        res = 0.0
        for key, val in self.ls.items():
            if key in other.ls:
                res += (val / self.n - other.ls[key] / other.n) ** 2
            else:
                res += (val / self.n) ** 2
        for key, val in other.ls.items():
            if key not in self.ls:
                res += (val / other.n) ** 2
        return res

    def d2(self, other):
        # print "\n\nself%s %s\nn: %i other n: %i" % (hash(self), self, self.n,other.n)
        return (other.n * self.squared + self.n * other.squared - 2 * (self.ls % other.ls)) / (self.n * other.n)

    def d4(self, other):
        dot1, dot2, dot3 = 0.0, 0.0, 0.0
        for val in self.ls.values():
            dot1 += (val / self.n) ** 2
        for val in other.ls.values():
            dot2 += (val / other.n) ** 2

        for key, val in self.ls.items():
            if key in other.ls:
                dot3 += ((val + other.ls[key]) / (self.n + other.n)) ** 2
            else:
                dot3 += (val / (self.n + other.n)) ** 2
        for key, val in other.ls.items():
            if key not in self.ls:
                dot3 += (val / (self.n + other.n)) ** 2

        return self.n * dot1 + other.n * dot2 - (self.n + other.n) * dot3

    distance = d2

    @classmethod
    def farthest_pair(cls, list):

        max_dist = None
        max_pair = None
        for e1 in list:
            for e2 in list:
                if e1 == e2: continue

                dist = e1.distance(e2)
                if not max_pair:
                    max_pair = (e1, e2,)
                    max_dist = dist
                elif dist > max_dist:
                    max_pair = (e1, e2,)
                    max_dist = dist
        return max_pair

    @classmethod
    def closest_pair(cls, list):
        min_dist = None
        min_pair = None
        for e1 in list:
            for e2 in list:
                if e1 == e2: continue

                dist = e1.distance(e2)
                if not min_pair:
                    min_pair = (e1, e2,)
                    min_dist = dist
                elif dist < min_dist:
                    min_pair = (e1, e2,)
                    min_dist = dist
        return min_dist

    def reset_cf(self):
        self.n = 0
        self.ls = Vector()
        self.squared = 0

    def update_cf(self, data):
        self.n += data.n
        self.ls += data.ls
        self.squared += data.squared

    @classmethod
    def calculate_height(self, list):
        if not list:
            return 1
        else:
            cum = 0
            for x in list:
                cum += x.height
            return cum

    @classmethod
    def calculate_depth(self, list):
        if not list:
            return 0
        else:
            return max([(lambda x: x.depth)(x) for x in list])
