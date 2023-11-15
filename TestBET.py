import unittest
from BET import BETNode, create_trees, find_solutions, build_expression_tree


class TestBETNode(unittest.TestCase):
    def test_repr(self):
        r"""String representation
               *
              / \
             A   -
                / \
               2   +
                  / \
                 3   4
           
        """
        root = BETNode('*')
        root.add_left(BETNode('A'))
        root.add_right(BETNode('-'))
        root.right.add_left(BETNode('2'))
        root.right.add_right(BETNode('+'))
        root.right.right.add_left(BETNode('3'))
        root.right.right.add_right(BETNode('4'))
        expected_str = '(A*(2-(3+4)))'
        self.assertEqual(repr(root), expected_str)

    def test_evaluate_tree1(self):
        """
          /
        /   \
        5     *
           /  \
          K    +
             /  \
            3    2
        """
        root = build_expression_tree('K32+*5/')
        self.assertEqual(root.evaluate(), 13)

    def test_evaluate_tree2(self):
        """
              *
            /    \
           +      +
         /   \    /  \
         -    4   5   *
        /  \         /  \
        2   3        6   7
        """
        root = build_expression_tree('23-4+567*+*')
        self.assertEqual(root.evaluate(), 141)


class TestCreateTrees(unittest.TestCase):
    def test_hand1(self):
        result = create_trees(['A', '2', '3', '4'])
        self.assertEqual(7680, len(result))
        result = create_trees(['2', '5', 'K', '9'])
        self.assertEqual(7680, len(result))

    def test_hand2(self):
        result = create_trees(['2', '2', 'Q', '6'])
        self.assertEqual(7680//2, len(result))
        

class TestFindSolutions(unittest.TestCase):
    def test0sols(self):
        result = find_solutions(['A', 'A', 'A', 'A'])
        self.assertEqual(0, len(result))

    def test_A23Q(self):
        result = find_solutions(['A', '2', '3', 'Q'])
        self.assertEqual(33, len(result))


if __name__ == "__main__":
    unittest.main()