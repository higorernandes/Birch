from BaseNode import BaseNode
from Entry import Entry
from birch import Treshold, Branch, leaf_count, split_count


class Leaf(BaseNode):

    def __init__(self, *args, **kwargs):
        self.entries = []
        super(Leaf, self).__init__(*args, **kwargs)
        global leaf_count
        leaf_count += 1

    @property
    def childnodes(self):
        return self.entries

    @property
    def height(self):
        return self.calculate_height(self.entries)

    @property
    def depth(self):
        return self.calculate_depth(self.entries)

    def __str__(self):
        return '%LEAF %i (%i)->' % (self.indent(), hash(self), len(self.entries)) + ' '.join([str(c) for c in self.entries])

    def trickle(self, vector):
        """Gets a vector and stores it in the closest entry, checks for split afterwards."""

        closest = self.closest(vector, self.entries)

        if closest:
            closest.store_vector(vector)
            self.update_cf(vector)
        else:
            entry = Entry()
            entry.store_vector(vector)
            self.add_entry(entry)

    @classmethod
    def closest(cls, node, list, force = False):
        """Returns the closest match of the node list"""

        min_dist = 0
        min_item = None

        if not list:
            return

        for item in list:
            dist = item.distance(node)
            if not min_item:
                min_item = item
                min_dist = dist
            elif dist < min_dist:
                min_dist = dist
                min_item = item

        if min_item.test_radius(node) > Treshold:
            return

        return min_item

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

        self.update_cf(entry)
        if len(self.entries) > Branch:
            self.split_leaf()

    def split_leaf(self):
        global split_count
        split_count += 1

        entry1, entry2 = self.farthest_pair(self.entries)

        # Save to the old list.
        self.reset_cf()
        old_entries = self.entries
        self.entries = []

        old_entries.remove(entry1)
        old_entries.remove(entry2)

        # Two new leafs.
        leaf1 = self
        leaf2 = Leaf()
        leaf1.add_entry(entry1)
        leaf2.add_entry(entry2)

        while old_entries:
            e = old_entries.pop()
            if leaf1.distance(e) > leaf2.distance(e):
                leaf2.add_entry(e)
            else:
                leaf1.add_entry(e)

        # Create a new leaf and append it to our parent.
        self.parent.add_node(leaf2)