from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self):
        type_string = self.text_type.value
        return f"TextNode({self.text}, {type_string}, {self.url})"
    
def text_node_to_html(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode("",text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b",text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i",text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code",text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a",text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img","", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("invalid text type")