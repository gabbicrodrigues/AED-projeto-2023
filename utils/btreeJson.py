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

    def save_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(), file)

    @staticmethod
    def load_from_file(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            return BTree.from_json(json_data)

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

def read_file_and_build_tree(file_name):
    with open(file_name, 'r', encoding= "utf-8", errors="replace") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    n = len(rows)
    print(rows[0])
    b_tree = BTree(t=n-1)  # Criando uma B-tree com ordem n-1
    for row in rows:
        key = row.get("id")
        # Inserir na árvore (aqui estamos usando key e value)
        b_tree.insert(key, row)

    return b_tree