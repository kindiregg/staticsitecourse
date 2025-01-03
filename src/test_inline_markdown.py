import unittest
from inline_markdown import (split_nodes_delimiter, 
                            extract_markdown_images, 
                            extract_markdown_links, 
                            split_nodes_image,
                            split_nodes_link,
                            text_to_textnodes)                           
from textnode import TextNode, TextType


class TestNodeDelimiter(unittest.TestCase):
    def test_standard_input(self):
        node = TextNode("I cant **believe** I am writing tests", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)  # Should have 3 nodes
        self.assertEqual(result[0].text, "I cant ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "believe")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_standard_input(self):
        node = TextNode("I cant believe I am writing tests", TextType.IMAGE)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].text, "I cant believe I am writing tests")
    
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

class TextExtractMarkdown(unittest.TestCase):
    
    def test_standard_case_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), result)

    def test_standard_case_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), result)

class TestSplitImageNode(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

class TestFullTextSplit(unittest.TestCase):
    def test_text_to_textnodes_types(self):
        text = "This is **text** with an *italic* word"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)

    def test_text_to_textnodes_comprehensive(self):
        text = "This is **bold** and *italic* and `code` with a ![image](http://image.jpg) and a [link](http://link.com)"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text_type, TextType.LINK)

        # Test URLs for image and link
        self.assertEqual(nodes[7].url, "http://image.jpg")
        self.assertEqual(nodes[9].url, "http://link.com")

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
        
if __name__ == "__main__":
    unittest.main()