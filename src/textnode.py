from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url):
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