#!/usr/bin/env python3.10

from collections import namedtuple
from itertools import count
from sys import stdin

class Node:
    def __init__(self, parent):
        self.parent = parent
        self.right = self.left = self.value = None

    def __str__(self):
        if self.value is None:
            return "[" + str(self.left) + "," + str(self.right) + "]"
        return str(self.value)

    def magnitude(self):
        if self.value is None:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return self.value

class SnailfishNumber:

    def __init__(self, spec):
        self.root = Node(None)
        self.parse_spec(spec, self.root)

    def parse_spec(self, spec, root, offset=0):
        if spec[offset] == "[":
            root.left = Node(root)
            root.right = Node(root)
            offset = self.parse_spec(spec, root.left, offset + 1)
            assert(spec[offset] == ",")
            offset = self.parse_spec(spec, root.right, offset + 1)
            assert(spec[offset] == "]")
            return offset + 1
        else:
            for length in count(1):
                if not spec[offset:offset+length].isdigit():
                    root.value = int(spec[offset:offset+length-1])
                    return offset + length - 1
                assert(len(spec[offset:offset+length]) == length)

    def add(self, other):
        new_root = Node(None)
        new_root.left = self.root
        self.root.parent = new_root
        new_root.right = other.root
        other.root.parent = new_root
        self.root = new_root
        self.reduce_number()

    def reduce_number(self):
        while True:
            if self.explode_leftmost_nested_four():
                continue
            if self.split_leftmost_double_digit():
                continue
            break

    def explode_leftmost_nested_four(self):
        node = self.find_leftmost_nested_four(self.root)
        if node is None:
            return False
        self.explode(node)
        return True

    def split_leftmost_double_digit(self):
        node = self.find_leftmost_double_digit(self.root)
        if node is None:
            return False
        self.split(node)
        return True

    def find_leftmost_nested_four(self, root, depth=0):
        ret = None
        if root.left.value is not None and root.right.value is not None and depth >= 4:
            ret = root
        if ret is None and root.left.value is None:
            ret = self.find_leftmost_nested_four(root.left, depth+1)
        if ret is None and root.right.value is None:
            ret = self.find_leftmost_nested_four(root.right, depth+1)
        return ret

    def find_leftmost_double_digit(self, root):
        ret = None
        if root.value is not None and root.value > 9:
            ret = root
        if ret is None and root.left is not None:
            ret = self.find_leftmost_double_digit(root.left)
        if ret is None and root.right is not None:
            ret = self.find_leftmost_double_digit(root.right)
        return ret

    def explode(self, node):
        self.add_leftwards(node.left)
        self.add_rightwards(node.right)
        # Replace node with zero.
        new_node = Node(node.parent)
        new_node.value = 0
        if node.parent.left is node:
            node.parent.left = new_node
        else:
            node.parent.right = new_node

    def split(self, node):
        # The split is always on a literal node.
        new_node = Node(node.parent)
        new_node.left = Node(new_node)
        new_node.left.value = node.value // 2
        new_node.right = Node(new_node)
        new_node.right.value = node.value - new_node.left.value
        if node.parent.left is node:
            node.parent.left = new_node
        else:
            node.parent.right = new_node

    def add_leftwards(self, current):
        # Search upwards to find the first node of which we are the
        # right-hand child.
        to_add = current.value
        if current.parent is None:
            return
        while current is not current.parent.right:
            current = current.parent
            if current.parent is None:
                # No node to the left
                return
        # Now search down and to the right to find the left node.
        current = current.parent.left
        while current.value is None:
            current = current.right
        current.value += to_add

    def add_rightwards(self, current):
        # Search upwards to find the first node of which we are the
        # left-hand child.
        to_add = current.value
        if current.parent is None:
            return
        while current is not current.parent.left:
            current = current.parent
            if current.parent is None:
                # No node to the left
                return
        # Now search down and to the left to find the left node.
        current = current.parent.right
        while current.value is None:
            current = current.left
        current.value += to_add


result = SnailfishNumber(stdin.readline().strip())
for line in (i.strip() for i in stdin):
    result.add(SnailfishNumber(line))
print(str(result.root))
print(f"Magnitude={result.root.magnitude()}")
