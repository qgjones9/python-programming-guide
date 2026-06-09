import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting BST implementation")


class BSTNode:
    """A node in a binary search tree."""

    def __init__(self, key, value, left=None, right=None):
        logger.info(f"Creating BSTNode with key: {key}, value: {value}")
        self.key = key
        self.value = value
        self.left = left
        self.right = right


class BST:
    """Binary search tree mapping keys to values."""

    def __init__(self):
        logger.info("Creating BST")
        self.root = None
        self._size = 0
        logger.info(f"BST created with root: {self.root}, size: {self._size}")

    # --- Size and representation ---

    def __len__(self):
        """Return the number of nodes in the tree."""
        logger.info(f"Returning size: {self._size}")
        return self._size

    def __iter__(self):
        """Iterate keys in sorted (inorder) order."""
        logger.info("Iterating keys in sorted order")
        return self.inorder_iter()

    def __str__(self):
        """Return an inorder list string."""
        logger.info(f"Returning inorder list string: {self.to_list()}")
        return str(self.to_list())

    def __repr__(self):
        """Return a debug representation."""
        logger.info(f"Returning debug representation: {self.to_list()}")
        return f"BST({self.to_list()})"

    def __eq__(self, other):
        """Return True if inorder keys match another tree."""
        logger.info(f"Comparing equality to another BST: {self.to_list()} == {other.to_list()}")
        return self.to_list() == other.to_list()

    def __ne__(self, other):
        """Return True if inorder keys do not match another tree."""
        logger.info(f"Comparing inequality to another BST: {self.to_list()} != {other.to_list()}")
        return self.to_list() != other.to_list()

    def __lt__(self, other):
        """Return True if inorder keys are less than another tree."""
        logger.info(f"Comparing if less than another BST: {self.to_list()} < {other.to_list()}")
        return self.to_list() < other.to_list()

    def __gt__(self, other):
        """Return True if inorder keys are greater than another tree."""
        logger.info(f"Comparing if greater than another BST: {self.to_list()} > {other.to_list()}")
        return self.to_list() > other.to_list()

    def __le__(self, other):
        """Return True if inorder keys are less than or equal to another tree."""
        logger.info(f"Comparing if less than or equal to another BST: {self.to_list()} <= {other.to_list()}")
        return self.to_list() <= other.to_list()

    def __ge__(self, other):
        """Return True if inorder keys are greater than or equal to another tree."""
        logger.info(f"Comparing if greater than or equal to another BST: {self.to_list()} >= {other.to_list()}")
        return self.to_list() >= other.to_list()

    def __hash__(self):
        """Return the hash of the inorder keys."""
        h = hash(tuple(self.to_list()))
        logger.info(f"Hashing BST in-order keys as tuple: {h}")
        return h

    def is_empty(self):
        """Return True if the tree has no nodes."""
        empty = self.root is None
        logger.info(f"Checking if BST is empty: {empty}")
        return empty

    # --- Core operations ---

    def insert(self, key, value):
        """Insert key/value, or update value if key already exists."""
        logger.info(f"Inserting key: {key}, value: {value} into tree")
        if self.root is None:
            logger.info(f"Tree is empty, inserting new root node with key: {key}")
            self.root = BSTNode(key, value)
            self._size += 1
            logger.info(f"New node inserted as root, size is now {self._size}")
            return
        logger.info(f"Tree is not empty, searching for correct insertion point for key: {key}")
        cur = self.root
        while cur is not None:
            logger.info(f"Comparing with node key: {cur.key}")
            if key < cur.key:
                logger.info(f"Key {key} < {cur.key}, moving left")
                if cur.left is None:
                    logger.info(f"Left is None, inserting new node with key: {key}")
                    cur.left = BSTNode(key, value)
                    self._size += 1
                    logger.info(f"New node inserted to left, size is now {self._size}")
                    return
                cur = cur.left
            elif key > cur.key:
                logger.info(f"Key {key} > {cur.key}, moving right")
                if cur.right is None:
                    logger.info(f"Right is None, inserting new node with key: {key}")
                    cur.right = BSTNode(key, value)
                    self._size += 1
                    logger.info(f"New node inserted to right, size is now {self._size}")
                    return
                cur = cur.right
            else:
                logger.info(f"Key {key} == {cur.key}, updating value")
                cur.value = value
                logger.info(f"Key {key}'s value updated to {value}")
                return

    def search(self, key):
        """Return the node with key, or None if missing."""
        logger.info(f"Searching for key: {key}")
        cur = self.root
        while cur is not None:
            logger.info(f"At node with key: {cur.key}")
            if key == cur.key:
                logger.info(f"Found node with key: {key}")
                return cur
            elif key < cur.key:
                logger.info(f"Key {key} < {cur.key}, moving left")
                cur = cur.left
            else:
                logger.info(f"Key {key} > {cur.key}, moving right")
                cur = cur.right
        logger.info(f"Key {key} not found in BST")
        return None

    def contains(self, key):
        """Return True if key is in the tree."""
        logger.info(f"Checking containment for key: {key}")
        node = self.search(key)
        found = node is not None
        logger.info(f"Containment check for key {key}: {found}")
        return found

    def delete(self, key):
        """Remove key from the tree. Return True if a node was removed."""
        logger.info(f"Request to delete key: {key}")
        self.root, deleted = self._delete_rec(self.root, key)
        logger.info(f"Delete operation complete. Key deleted: {deleted}")
        if deleted:
            self._size -= 1
            logger.info(f"Decremented size to: {self._size}")
        return deleted

    def _delete_rec(self, node, key):
        logger.info(f"Recursive delete: node={node.key if node else None}, key={key}")
        if node is None:
            logger.info(f"Node is None during delete, key not found.")
            return None, False
        if key < node.key:
            logger.info(f"Key {key} < {node.key}, moving left")
            node.left, deleted = self._delete_rec(node.left, key)
            return node, deleted
        if key > node.key:
            logger.info(f"Key {key} > {node.key}, moving right")
            node.right, deleted = self._delete_rec(node.right, key)
            return node, deleted
        # Node to remove found
        logger.info(f"Node with key {key} found for deletion")
        if node.left is None:
            logger.info(f"Node has no left child, replacing node with right child")
            return node.right, True
        if node.right is None:
            logger.info(f"Node has no right child, replacing node with left child")
            return node.left, True
        # Two children: get inorder successor
        succ = self._min_node(node.right)
        logger.info(f"Replacing node with inorder successor key: {succ.key}")
        node.key = succ.key
        node.value = succ.value
        node.right, _ = self._delete_rec(node.right, succ.key)
        return node, True

    def clear(self):
        """Remove all nodes."""
        logger.info("Clearing entire BST")
        self.root = None
        self._size = 0
        logger.info("BST is cleared.")

    # --- Min / max ---

    def _min_node(self, node):
        logger.info("Finding minimum node in subtree")
        current = node
        if current is None:
            logger.info("Node is None, no minimum")
            return None
        while current.left is not None:
            logger.info(f"Moving left from node {current.key} to {current.left.key}")
            current = current.left
        logger.info(f"Min node found: {current.key}")
        return current

    def _max_node(self, node):
        logger.info("Finding maximum node in subtree")
        current = node
        if current is None:
            logger.info("Node is None, no maximum")
            return None
        while current.right is not None:
            logger.info(f"Moving right from node {current.key} to {current.right.key}")
            current = current.right
        logger.info(f"Max node found: {current.key}")
        return current

    def minimum(self):
        """Return the node with the smallest key, or None if empty."""
        logger.info("Looking up minimum node in BST")
        if self.root is None:
            logger.info("BST is empty, minimum is None")
            return None
        min_node = self._min_node(self.root)
        logger.info(f"Minimum node in BST: {min_node.key if min_node else None}")
        return min_node

    def maximum(self):
        """Return the node with the largest key, or None if empty."""
        logger.info("Looking up maximum node in BST")
        if self.root is None:
            logger.info("BST is empty, maximum is None")
            return None
        max_node = self._max_node(self.root)
        logger.info(f"Maximum node in BST: {max_node.key if max_node else None}")
        return max_node

    # --- Recursive traversals ---

    def inorder(self):
        """Return keys in sorted order."""
        logger.info("Performing recursive inorder traversal")
        out = []
        self._inorder_rec(self.root, out)
        logger.info(f"Recursive inorder traversal complete: {out}")
        return out

    def _inorder_rec(self, node, out):
        if node is None:
            return
        self._inorder_rec(node.left, out)
        logger.info(f"Visited node (inorder): {node.key}")
        out.append(node.key)
        self._inorder_rec(node.right, out)

    def preorder(self):
        """Return keys in preorder (root, left, right)."""
        logger.info("Performing recursive preorder traversal")
        out = []
        self._preorder_rec(self.root, out)
        logger.info(f"Recursive preorder traversal complete: {out}")
        return out

    def _preorder_rec(self, node, out):
        if node is None:
            return
        logger.info(f"Visited node (preorder): {node.key}")
        out.append(node.key)
        self._preorder_rec(node.left, out)
        self._preorder_rec(node.right, out)

    def postorder(self):
        """Return keys in postorder (left, right, root)."""
        logger.info("Performing recursive postorder traversal")
        out = []
        self._postorder_rec(self.root, out)
        logger.info(f"Recursive postorder traversal complete: {out}")
        return out

    def _postorder_rec(self, node, out):
        if node is None:
            return
        self._postorder_rec(node.left, out)
        self._postorder_rec(node.right, out)
        logger.info(f"Visited node (postorder): {node.key}")
        out.append(node.key)

    # --- Iterative traversals ---

    def inorder_iter(self):
        """Yield keys in sorted order without recursion."""
        logger.info("Beginning iterative inorder traversal")
        stack = []
        cur = self.root
        while stack or cur is not None:
            while cur is not None:
                logger.info(f"Pushing node {cur.key} to stack (inorder_iter)")
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            logger.info(f"Popped node {cur.key} from stack (inorder_iter)")
            yield cur.key
            cur = cur.right

    def preorder_iter(self):
        """Yield keys in preorder without recursion."""
        logger.info("Beginning iterative preorder traversal")
        if self.root is None:
            logger.info("BST is empty, ending preorder_iter")
            return
        stack = [self.root]
        while stack:
            node = stack.pop()
            logger.info(f"Yielding node {node.key} (preorder_iter)")
            yield node.key
            if node.right is not None:
                logger.info(f"Pushing node {node.right.key} to stack (preorder_iter)")
                stack.append(node.right)
            if node.left is not None:
                logger.info(f"Pushing node {node.left.key} to stack (preorder_iter)")
                stack.append(node.left)

    def postorder_iter(self):
        """Yield keys in postorder without recursion."""
        logger.info("Beginning iterative postorder traversal")
        if self.root is None:
            logger.info("BST is empty, ending postorder_iter")
            return
        stack = [self.root]
        reverse_out = []
        while stack:
            node = stack.pop()
            logger.info(f"Visiting node {node.key} (postorder_iter)")
            reverse_out.append(node.key)
            if node.left is not None:
                logger.info(
                    f"Pushing node {node.left.key} to stack (postorder_iter)"
                )
                stack.append(node.left)
            if node.right is not None:
                logger.info(
                    f"Pushing node {node.right.key} to stack (postorder_iter)"
                )
                stack.append(node.right)
        for key in reversed(reverse_out):
            logger.info(f"Yielding node {key} (postorder_iter)")
            yield key

    def level_order(self):
        """Yield keys level by level (breadth-first)."""
        logger.info("Beginning level-order (breadth-first) traversal")
        if self.root is None:
            logger.info("BST is empty, ending level_order traversal")
            return
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            logger.info(f"Yielding node {node.key} (level_order)")
            yield node.key
            if node.left is not None:
                logger.info(f"Appending node {node.left.key} to queue (level_order)")
                queue.append(node.left)
            if node.right is not None:
                logger.info(f"Appending node {node.right.key} to queue (level_order)")
                queue.append(node.right)

    def level_order_iter(self):
        """Alias for level_order."""
        logger.info("level_order_iter called (providing level_order generator)")
        return self.level_order()

    # --- Tree metrics ---

    def height(self):
        """Return edge count of the longest root-to-leaf path (-1 if empty)."""
        logger.info("Calculating height of BST")
        if self.root is None:
            logger.info("BST is empty, returning height -1")
            return -1
        h = self._height_rec(self.root)
        logger.info(f"BST height: {h}")
        return h

    def _height_rec(self, node):
        if node is None:
            return -1
        hl = self._height_rec(node.left)
        hr = self._height_rec(node.right)
        logger.info(f"Node {node.key} left height: {hl}, right height: {hr}")
        return 1 + max(hl, hr)

    def range_query(self, lo, hi):
        """Return keys in [lo, hi] in sorted order."""
        logger.info(f"Performing range query in [{lo}, {hi}]")
        out = []
        self._range_query_rec(self.root, lo, hi, out)
        logger.info(f"Range query result: {out}")
        return out

    def _range_query_rec(self, node, lo, hi, out):
        if node is None:
            return
        if lo < node.key:
            logger.info(f"Range query: {node.key} > lo={lo}, moving left")
            self._range_query_rec(node.left, lo, hi, out)
        if lo <= node.key <= hi:
            logger.info(f"Range query: {node.key} in [{lo}, {hi}], adding to output")
            out.append(node.key)
        if hi > node.key:
            logger.info(f"Range query: {node.key} < hi={hi}, moving right")
            self._range_query_rec(node.right, lo, hi, out)

    # --- Bulk helpers ---

    def to_list(self):
        """Return keys as a sorted list."""
        logger.info("Converting BST to sorted list")
        result = self.inorder()
        logger.info(f"BST as list: {result}")
        return result

    def from_list(self, lst):
        """Insert each list element as both key and value."""
        logger.info(f"Bulk inserting from list: {lst}")
        for key in lst:
            logger.info(f"Inserting {key} from list into BST")
            self.insert(key, key)
        logger.info("Bulk insertion from list complete")