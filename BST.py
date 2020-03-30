class node:
    # constructor
    def __init__(self, value=None):
        self.value = value
        # pointers to children
        self.left_child = None
        self.right_child = None
        # pointer to parent
        self.parent = None


class binary_search_tree:
    # constructor
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = node(value)
        else:
            # underscore signifies private function
            # _insert is recursive and the second input is the node we are looking at currently
            self._insert(value, self.root)

    def _insert(self, value, cur_node):
        if value < cur_node.value:
            if cur_node.left_child is None:
                cur_node.left_child = node(value)
                cur_node.left_child.parent = cur_node
            else:
                self._insert(value, cur_node.left_child)
        elif value > cur_node.value:
            if cur_node.right_child is None:
                cur_node.right_child = node(value)
                cur_node.right_child.parent = cur_node
            else:
                self._insert(value, cur_node.right_child)
        # value = cur_node value
        else:
            print('Value is already in the tree')

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, cur_node):
        if cur_node is not None:
            self._print_tree(cur_node.left_child)
            print(str(cur_node.value))
            self._print_tree(cur_node.right_child)

    def height(self):
        if self.root is not None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, cur_node, cur_height):
        # Once we hit a lead the cur_node will be none and we return the final height
        if cur_node is None:
            return cur_height
        left_height = self._height(cur_node.left_child, cur_height + 1)
        right_height = self._height(cur_node.right_child, cur_height + 1)
        return max(left_height, right_height)

    def search(self, value):
        if self.root is not None:
            return self._search(value, self.root)
        else:
            return False

    def _search(self, value, cur_node):
        if value == cur_node.value:
            return True
        elif value < cur_node.value and cur_node.left_child is not None:
            return self._search(value, cur_node.left_child)
        elif value > cur_node.value and cur_node.right_child is not None:
            return self._search(value, cur_node.right_child)
        else:
            return False

    def find(self, value):
        if self.root is not None:
            return self._find(value, self.root)
        else:
            return None

    def _find(self, value, cur_node):
        if value == cur_node.value:
            return cur_node
        elif value < cur_node.value and cur_node.left_child is not None:
            return self._find(value, cur_node.left_child)
        elif value > cur_node.value and cur_node.right_child is not None:
            return self._find(value, cur_node.right_child)

    def delete_value(self, value):
        return self.delete_node(self.find(value))

    def delete_node(self, node):

        if node is None or self.find(node.value) is None:
            print('Node to be deleted not found in the tree')
            return None

        # returns smallest element in tree
        def min_value_node(n):
            current = n
            while current.left_child is not None:
                current = current.left_child
            return current

        # returns number of children for a given node
        def num_children(n):
            num_children = 0
            if n.left_child is not None:
                num_children += 1
            if n.right_child is not None:
                num_children += 1
            return num_children

        # get the parent of the node to delete
        node_parent = node.parent
        # get the number of children of the node to delete
        node_children = num_children(node)
        if node_children == 0:
            if node_parent is not None:
                # then its a leaf node so just remove the parent child reference
                if node_parent.left_child == node:
                    node_parent.left_child = None
                else:
                    # can be a right child that is getting deleted
                    node_parent.right_child = None
            else:
                self.root = None
        if node_children == 1:
            # get the single child node
            if node.left_child is not None:
                child = node.left_child
            else:
                child = node.right_child
            if node_parent is not None:
                # replace the node to be deleted with its child
                if node_parent.left_child == node:
                    node_parent.left_child = child
                else:
                    node_parent.right_child = child
            else:
                self.root = child
            # correct the parent pointer in node
            child.parent = node_parent
        if node_children == 2:
            # get the inorder successor of the deleted node
            successor = min_value_node(node.right_child)

            # copy the inorder successor's value to the node formerly
            # holding the value we wished to delete
            node.value = successor.value

            # delete the inorder successor now that its value has been
            # copied into the other node
            self.delete_node(successor)

        return 'deleted'

def fill_tree(tree_object, num_elems=100, max_int=1000):
    from random import randint
    for _ in range(num_elems):
        cur_elem = randint(0, max_int)
        tree_object.insert(cur_elem)
    return tree_object
