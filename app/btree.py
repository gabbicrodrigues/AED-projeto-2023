import json
import csv

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

    def to_json(self):
        return {
            "leaf": self.leaf,
            "keys": self.keys,
            "values": self.values,
            "children": [child.to_json() if child else None for child in self.children]
        }

    @classmethod
    def from_json(cls, json_data):
        node = cls(leaf=json_data["leaf"])
        node.keys = json_data["keys"]
        node.values = json_data["values"]
        node.children = [cls.from_json(child) if child else None for child in json_data["children"]]
        return node

class BTree:
    def __init__(self, t):
        self.root = BTreeNode()
        self.t = t

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, i):
        t = self.t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        parent.values.insert(i, y.values[t - 1])
        z.keys = y.keys[t:(2 * t) - 1]
        z.values = y.values[t:(2 * t) - 1]
        y.keys = y.keys[0:t - 1]
        y.values = y.values[0:t - 1]
        if not y.leaf:
            z.children = y.children[t:2 * t]
            y.children = y.children[0:t - 1]
    
    def _find_key_index(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        return i

    def remove(self, key):
        root = self.root
        if not root.keys:
            print("B-tree is empty. Cannot remove from an empty tree.")
            return
        if len(root.keys) == 1 and not root.children:
            if key == root.keys[0]:
                self.root = BTreeNode()  # Resetting the root for an empty tree
            else:
                print(f"Key {key} not found in the B-tree.")
            return
        self._remove(root, key)

    def _remove(self, node, key):
        idx = self._find_key_index(node, key)
        if idx < len(node.keys) and key == node.keys[idx]:
            if node.leaf:
                self._remove_from_leaf(node, idx)
            else:
                self._remove_from_non_leaf(node, idx)
        else:
            if node.leaf:
                print(f"Key {key} not found in the B-tree.")
                return
            self._remove_from_subtree(node, idx, key)

    def _remove_from_leaf(self, node, idx):
        node.keys.pop(idx)
        node.values.pop(idx)

    def _remove_from_non_leaf(self, node, idx):
        key = node.keys[idx]
        if len(node.children[idx].keys) >= self.t:
            predecessor = self._get_predecessor(node.children[idx])
            node.keys[idx] = predecessor.keys[-1]
            node.values[idx] = predecessor.values[-1]
            self._remove(node.children[idx], predecessor.keys[-1])
        elif len(node.children[idx + 1].keys) >= self.t:
            successor = self._get_successor(node.children[idx + 1])
            node.keys[idx] = successor.keys[0]
            node.values[idx] = successor.values[0]
            self._remove(node.children[idx + 1], successor.keys[0])
        else:
            self._merge_children(node, idx)

    def _remove_from_subtree(self, node, idx, key):
        child = node.children[idx]
        if len(child.keys) == self.t - 1:
            self._fill(child, idx)
        if idx > len(node.keys):
            idx -= 1
        self._remove(node.children[idx], key)

    def _get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node

    def _get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node

    def _fill(self, node, idx):
        if idx != 0 and len(node.children[idx - 1].keys) >= self.t:
            self._borrow_from_prev(node, idx)
        elif idx != len(node.keys) and len(node.children[idx + 1].keys) >= self.t:
            self._borrow_from_next(node, idx)
        else:
            if idx != len(node.keys):
                self._merge_children(node, idx)
            else:
                self._merge_children(node, idx - 1)

    def _borrow_from_prev(self, node, idx):
        child = node.children[idx]
        sibling = node.children[idx - 1]
        child.keys.insert(0, node.keys[idx - 1])
        child.values.insert(0, node.values[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children[-1])
            sibling.children.pop(-1)
        node.keys[idx - 1] = sibling.keys[-1]

    def search(self, k, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return node, i
        if node.leaf:
            return None
        return self.search(k, node.children[i])

    @staticmethod
    def load_from_file(file_bytes):
        try:
            json_data = json.loads(file_bytes.decode('utf-8'))
            return BTree.from_json(json_data)
        except json.JSONDecodeError:
            print("Invalid JSON format.")
            return None

    def to_json(self):
        return {
            "root": self.root.to_json(),
            "t": self.t
        }

    @classmethod
    def from_json(cls, json_data):
        b_tree = cls(json_data["t"])
        b_tree.root = BTreeNode.from_json(json_data["root"])
        return b_tree
