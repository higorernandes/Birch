from BaseNode import BaseNode
from Leaf import Leaf
from birch import Branch, node_count, split_count


class Node(BaseNode):

    def __init__(self, *args, **kwargs):
        self.children = []
        super(Node, self).__init__(*args, **kwargs)
        global node_count
        node_count += 1

    @property
    def childnodes(self):
        return self.children

    @property
    def height(self):
        return self.calculate_height(self.children)

    @property
    def depth(self):
        return self.calculate_depth(self.children)

    @property
    def __str__(self):
        return '%sNODE %i (%i)->' % (self.indent(), hash(self), len(self.children)) + ' '.join([str(c) for c in self.children])

    def trickle(self, vector):
        """Gets a vector and hands it down to the closest child, checks for split afterwards."""

        # Refresh CF vector.
        self.update_cf(vector)

        closest = self.closest(vector, self.children)

        if closest:
            closest.trickle(vector)
        else:
            leaf = Leaf()
            leaf.trickle(vector)
            self.add_node(leaf)

    def add_node(self, node, update=False):
        self.children.append(node)
        node.parent = self

        if update:
            self.update_cf(node)

        if len(self.children) > Branch:
            self.split_node()

    def split_node(self):
        global split_count
        split_count += 1

        child1, child2 = self.farthest_pair(self.children)

        # Saving the old list.
        self.reset_cf()
        old_children = self.children
        self.children = []

        # Two new leafs.
        if self.is_root:
            node1 = Node()
        else:
            node1 = self
        node2 = Node()

        # Add the farthest children to the new nodes.
        node1.add_node(child1, True)
        node2.add_node(child2, True)

        while old_children:
            child = old_children.pop()
            if node1.distance(child) > node2.distance(child):
                node2.add_node(child, True)
            else:
                node1.add_node(child, True)

        # Try to push down nodes if it only has one child.
        if len(node1.children) == 1:
            node1 = node1.children[0]
        if len(node2.children) == 1:
            node2 = node2.children[0]

        # Create a new leaf and append it to our parent.
        if self.is_root:
            self.add_node(node1, True)
            self.add_node(node2, True)
            # Try to re-merge node 1 or 2
        else:
            self.parent.add_node(node2)
