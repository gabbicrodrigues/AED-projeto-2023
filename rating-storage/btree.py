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
            while i >= 0 and key < int(node.keys[i]):
                node.keys[i + 1] = int(node.keys[i])
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < int(node.keys[i]):
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if key > int(node.keys[i]):
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
        while i < len(node.keys) and key > int(node.keys[i]):
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
    
    def _merge_children(self, parent, idx):
        t = self.t
        child = parent.children[idx]
        sibling = parent.children[idx + 1]

        # Move a key from the parent to the child
        child.keys.append(parent.keys[idx])
        child.values.append(parent.values[idx])

        # Move keys and values from the sibling to the child
        child.keys += sibling.keys
        child.values += sibling.values

        # Move children from the sibling to the child (if not a leaf)
        if not child.leaf:
            child.children += sibling.children

        # Remove the key from the parent
        parent.keys.pop(idx)
        parent.values.pop(idx)

        # Remove the merged sibling
        parent.children.pop(idx + 1)

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
        while i < len(node.keys) and k > int(node.keys[i]):
            i += 1
        if i < len(node.keys) and k == int(node.keys[i]):
            return node, i
        if node.leaf:
            return None
        return self.search(k, node.children[i])
 
    def search_page(self, k, node=None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and k > int(node.keys[i]):
            i += 1
        
        if i < len(node.keys) and (k == int(node.keys[i])) :
            return node, i    

        if node.leaf:
            return node, i

        return self.search_page(k, node.children[i])

    def get_insert_page(self, key, node=None):
        if node is None:
            node = self.root

        # Encontrar a posição correta no nó atual

        i = 0
        while i < len(node.keys) and key > int(node.keys[i]):
            i += 1  

        # Se o nó é uma folha, estamos na posição correta
        if node.leaf and len(node.keys) < (2 * self.t) - 1:
            return node, i

        # Caso contrário, faça uma chamada recursiva para o filho apropriado
        return self.get_insert_page(key, node.children[i])
    
    def insert_page(self, init_key, new_page, node=None):
        if node is None:
            node = self.root

        # Encontrar a posição correta no nó atual
        i = 0
        while i < len(node.keys) and init_key > int(node.keys[i]):
            i += 1        

        if node.leaf and len(node.keys) < (2 * self.t) - 1:
            node.keys = new_page['keys']
            node.values = new_page['values']
            return

        # Caso contrário, faça uma chamada recursiva para o filho apropriado
        return self.insert_page(init_key, new_page, node.children[i])

    def save_to_file(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(), file)

    @staticmethod
    def load_root(self, json_data):
        if self.root is None:
            self.root = BTreeNode.from_json(json_data["root"])

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

def read_file_and_build_tree(file_name, order):
    with open(file_name, 'r', encoding= "utf-8", errors="replace") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    b_tree = BTree(order)  # Criando uma B-tree com ordem n-1
    for row in rows:
        key = row.get("id")
        # Inserir na árvore (aqui estamos usando key e value)
        b_tree.insert(int(key), row)

    return b_tree