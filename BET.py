from itertools import permutations, product


class BETNode:
    """Node for binary expression tree"""

    # Some class variables (no need to make a copy of these for every node)
    # access these with e.g. `BETNode.OPERATORS`
    OPERATORS = {'+', '-', '*', '/'}
    CARD_VAL_DICT = {'A': 1, '1': 1, '2': 2, '3': 3, '4': 4,
                     '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                     '10': 10, 'J': 11, 'Q': 12, 'K': 13}

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    # These are proficed for you - do not modify. They let you hash BETs (so they can be stored in sets)
    # and compare them (so you can write unittests more easily).
    def __eq__(self, other):
        """Two nodes are equal if their values are equal and their subtrees are (recursively) equal"""
        if other is None: return False
        return self.value == other.value and self.left == other.left and self.right == other.right

    def __hash__(self):
        """Hash the whole tree (value + left and right subtrees)"""
        return hash((self.value, self.left, self.right))

    # START HERE
    def add_left(self, node):
        self.left = node

    def add_right(self, node):
        self.right = node

    def evaluate(self):
        if self.value in self.OPERATORS:
            if self.value == '+':
                return self.left.evaluate() + self.right.evaluate()
            elif self.value == '-':
                return self.left.evaluate() - self.right.evaluate()
            elif self.value == '*':
                return self.left.evaluate() * self.right.evaluate()
            else:
                try:
                    return self.left.evaluate() / self.right.evaluate()
                except ZeroDivisionError:
                    return 0
        else:
            return self.convert_to_num(self.value)

    def __repr__(self):
        if self.value in self.OPERATORS:
            return f"({self.left.__repr__()}{self.value}{self.right.__repr__()})"
        else:
            return self.value

    def convert_to_num(self, string):
        return self.CARD_VAL_DICT.get(string)


def build_expression_tree(postfix_expression):
    stack = []

    operators = BETNode.OPERATORS

    for symbol in postfix_expression:
        if symbol not in operators:
            # Operand, push onto stack
            stack.append(BETNode(symbol))
        else:
            # Operator, pop two operands from stack
            right = stack.pop()
            left = stack.pop()
            # Create a new node for the operator
            node = BETNode(symbol, right=right, left=left)

            # Push the operator node back onto the stack
            stack.append(node)

    # The final item on the stack is the root of the tree
    return stack[0]


def create_trees(cards):
    # Generate all possible combinations of operands and operators
    operator_combinations = list(product(BETNode.OPERATORS, repeat=3))
    operand_permutations = list(permutations(cards))

    # Initialize an empty set to store unique trees
    tree_set = set()

    for op_combination in operator_combinations:
        for operand_permutation in operand_permutations:
            # Generate all possible expression trees for the given combination
            for tree in generate_trees(list(operand_permutation), list(op_combination)):
                tree_set.add(tree)

    return tree_set


def generate_trees(operands, operators):
    # Base case
    if len(operators) == 0:
        return [BETNode(operands[0])]

    trees = []
    for i in range(len(operators)):
        left_operands = operands[:i + 1]
        right_operands = operands[i + 1:]
        left_trees = generate_trees(left_operands, operators[:i])
        right_trees = generate_trees(right_operands, operators[i + 1:])

        for left_tree in left_trees:
            for right_tree in right_trees:
                tree = BETNode(operators[i], left=left_tree, right=right_tree)
                trees.append(tree)

    return trees


def find_solutions(cards):
    solutions = set()
    for tree in create_trees(cards):
        if tree.evaluate() == 24:
            solutions.add(tree)
    return solutions
