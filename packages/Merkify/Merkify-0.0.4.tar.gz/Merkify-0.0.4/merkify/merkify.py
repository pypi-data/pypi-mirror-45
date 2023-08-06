# Import packages
import hashlib

class Merkify():
    class Node(): # pylint: disable=too-few-public-methods
        '''
        Class for usage of Nodes. Node structure is used in the implmentation
        of the Merkle tree structure itself.
        '''
        def __init__(self, value: str or int):
            '''
                Docstring for __init__ and intialization. Will document
                within __init__ method rather than class level.

                Args:
                    value (str or int): Can be both string and integer value
                                        that is to-be-stored in the Merkle tree

                    hashvalue (str): Converts the value into a sha256 hashed value

                    left/right (str or int): initializing the left and right values
                                             of the node structure. Will be used
                                             later in the implementation.
            '''

            # Specific attributes of the node
            hashvalue = hashlib.sha256(value.encode('utf-8')).hexdigest()
            self.value = hashvalue
            self.left = None
            self.right = None

        def __add__(self, node):
            '''
            When summing two function in Python a + b, what really happens
            is a.__add__(b). This function allows us to add different instances
            that Python otherwise would not know how to add.

            Example:
                The 'build_tree' function where the following is added:
                parent = self.Node(items[i] + items[i + 1]). The addition of these
                items is possible due to the __add__ function.

            Args:
                node (Node): To be used in addtion, as seen above. The ability
                              to add the node instance is what it is aiming for.
            '''

            if type(node) == type(self):
                return self.value + node.value

            # Raising excpetion error if nodes are not being compared or
            # wrong usage of the add in combination with Node.
            raise Exception("Error. Nodes are not being compared.")


    def __init__(self, items: list):
        '''
        Initialization of the merkify class above. The order of items matter
        and is taken care of the order by hashlist.

        Args:
            items (list): Takes in a list of items to be added to the Merkle
                          tree

            hashlist (list): List will be put through node_hasify function
                             further down to be (1) hashed and (2) become
                             nodes that are added to the tree.

            self.root (nodes): Hashed items (effectively nodes) are brought through
                               the process of becoming trees. build_tree returns
                               very specifically "items[0], height" which is translated
                               to self.root being items[0], i.e. the first item.

            self.height (nodes): Similar to the idea above, self.height will effectively
                                 be the returned "height" from build_tree, reflecting
                                 the ability to quickly give us information on the
                                 tree height.
        '''

        self.hashlist = self.node_hashify(items)
        self.root, self.height = self.build_tree(self.hashlist)

    def node_hashify(self, items: list):
        '''
        From the initialization of the Node, the values will naturally
        be hashed with the sha-256 hash function.

        Example:
            For each respecitve item in the item list, it would go through
            the Node function, where it is translated to a hashed value.
            There will be a hashed value for each item in the form of a list.

        '''
        return [self.Node(item) for item in items]


    def build_tree(self, items, height=0):
        '''
        Building the binary tree in a bottom-up, recursive manner. The Merkle Tree
        is a binary tree and hence is reflective of the complexity of O(N log N).

        Args:
            items(list): A list of items that are already transformed into nodes
                         and hence, hashed with the sha256.

            height(int): Already initialized to be 0 from before as a given before
                         the tree is built.
        '''
        nodes = []
        last = None
        itemlength = len(items)

        if itemlength > 1:
            if itemlength % 2 == 1:
                last = items.pop()

            for i in range(0, len(items), 2):
                parent = self.Node(items[i] + items[i + 1])
                parent.left = items[i]
                parent.right = items[i + 1]
                nodes.append(parent)
            if last:
                parent = self.Node(last.value)
                parent.left = last
                nodes.append(parent)
                items.append(last) # put the last item back in
            return self.build_tree(nodes, height + 1)

        else:
            return items[0], height

    def add(self, values):
        '''
        Add allows us to add values to the Merkle tree after intialzation and
        build_tree. This can be strings or integers. The argument will, in specific
        take the given value, extend it to hashlist (which will hash our item) and
        then re-build the tree through self.build_tree for every time.

        Args:
            values(str/int): Will be added to the Merkle tree as hashed nodes.
        '''

        if type(values) != list:
            values = [values]

        self.hashlist.extend(self.node_hashify(values))
        self.root, self.height = self.build_tree(self.hashlist)


    def fetch_root_value(self):
        '''
        Returning the root value. This is enabled through the self.root in the
        __init__ function.
        '''

        return self.root.value


    def depth(self, values, depth, current):
        '''
        The depth is a traversing function in a top-down manner which
        is used in the fetch_depth_valye function.

        Args:
            values(list): Values are the list of items that are taken in as nodes.

            depth(int): Derived from the self.height in the build tree. The depth of
                        a given node in the tree is the length of the path from the
                        root of the tree to that given node.

            current(int): Current signfies a cursor as it is used in fetch_depth_value
                          and typically set to 0 for traversal purposes.
        '''

        depth_values = []
        for Node in values:
            depth_values.append(Node.left)
            if Node.right:
                depth_values.append(Node.right)

        current += 1
        if current == depth:
            return depth_values
        return self.depth(depth_values, depth, current)


    def fetch_depth_value(self, depth):
        '''
        The fetch depth value returns a lst of values at the target depth
        of the tree. This would be the hashed values, not the plain
        text values.

        In particular, if the depth is equal to the height, the code
        simply returns the leaf values. otherwise, the height should be
        larger than the depth as the depth of a node M in the tree is the
        length of the path from the root of the tree to M. In that case,
        it used the depth function previously made to return the values for
        a given depth.
        '''
        if depth == self.height:
            return self.get_leaf_values()
        elif depth < self.height:
            items = self.depth([self.root], depth, 0)
            return [item.value for item in items]

        # Raising exception if depth value is not existing
        raise Exception("Your target depth can not be over the tree height")


    def get_leaf_values(self):
        '''
        Return a list of all the node value at the bottom of the tree.
        '''
        return [item.value for item in self.hashlist]


    def fetch_height(self): # pylint: disable=too-few-public-methods
        '''
        Being able to fetch the height of the Merkle tree. Enabled by the
        self.height in the __init__ function.
        Additional comment regarding pyling added to avoid unnecessary styleguide
        error.
        '''
        return self.height
