import unittest

from textnode import TextNode, TextType, text_node_to_html
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "")
        node2 = TextNode("This is a text node", TextType.BOLD, "")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("", TextType.TEXT, "")
        node2 = TextNode("Words", TextType.TEXT, "")
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):  
        node = TextNode("Words", TextType.TEXT, "")
        node2 = TextNode("Words", TextType.BOLD, "")
        self.assertNotEqual(node, node2)

    def test_eq_image(self):
        node = TextNode("X the everything site!!!", TextType.IMAGE, "https://twitter.com")
        node2 = TextNode("X the everything site!!!", TextType.IMAGE, "https://twitter.com")
        self.assertEqual(node, node2)

    def test_eq_url_false(self):
        node = TextNode("X the everything site!!!", TextType.LINK, "https://twitter.com")
        node2 = TextNode("X the everything site!!!", TextType.LINK, "https://x.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestNodeToHtml(unittest.TestCase):
    def test_standard_types1(self):
        node = text_node_to_html(TextNode("Wow I sure love OOP", TextType.TEXT))
        self.assertEqual(node, LeafNode("", "Wow I sure love OOP"))

    def test_standard_types2(self):
        node = text_node_to_html(TextNode("Wow I sure love OOP", TextType.CODE))
        self.assertEqual(node, LeafNode("code", "Wow I sure love OOP"))

    def test_blank_text_type(self):
        text_node = TextNode("Wow I sure love OOP", TextType)
        with self.assertRaises(Exception) as context:
            text_node_to_html(text_node)

        self.assertTrue("invalid text type" in str(context.exception))

    def test_invalid_text_type(self):
        with self.assertRaises(AttributeError):
            # RICH is not supported
            text_node_to_html_node(TextNode("Wow I sure love OOP", TextType.RICH))

if __name__ == "__main__":
    unittest.main()