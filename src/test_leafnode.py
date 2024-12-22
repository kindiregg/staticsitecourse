import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

    def test_leaf_node_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_node_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_leaf_node_repr(self):
        node = LeafNode('p', 'Hello!', {'class': 'greeting'})
        expected = "LeafNode(tag='p', value='Hello!', props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected)

if __name__ == '__main__':
    unittest.main()