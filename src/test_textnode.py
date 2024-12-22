import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()