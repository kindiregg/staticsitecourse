import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag = "img", props={"src": "image.jpg", "alt": "A smol dog", "class": "profile-picture"})
        self.assertEqual(node.props_to_html(), ' src="image.jpg" alt="A smol dog" class="profile-picture"')

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=p, value=What a strange world, children=None, props={'class': 'primary'})",
        )

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

class TestParentNode(unittest.TestCase):
    def test_parent_node_init(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_repr(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ]
        )
        expected = f"ParentNode(tag='p', children=[LeafNode(tag='b', value='Bold text', props=None), LeafNode(tag='None', value='Normal text', props=None)], props=None)"
        self.assertEqual(repr(node), expected)

    def test_parent_with_no_tag(self):
        node = ParentNode(
            "",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
            )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "tag is required")

    def test_parent_with_blank_children(self):
        node = ParentNode("div",[])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "children are required")    

    def test_parent_node_missing_children(self):
        with self.assertRaises(TypeError) as context:
            node = ParentNode("div")  # Oops, forgot children argument!
        self.assertEqual(
            str(context.exception),
            "ParentNode.__init__() missing 1 required positional argument: 'children'"
        )

    def test_parent_with_string_as_children(self):
        with self.assertRaises(TypeError) as context:
            node = ParentNode(
                "div",
                "this should be a list not a string",
            )
        self.assertEqual(str(context.exception), "children must be a list of nodes")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()