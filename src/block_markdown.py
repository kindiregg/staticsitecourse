from inline_markdown import text_to_textnodes
from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
import re

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        if block == "":
            continue
        block = block.strip()
        blocks.append(block)
    return blocks
    

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
    
# returns ParentNode containing all markdown as children nodes    
def markdown_to_html_node(markdown):   
    markdown_blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in markdown_blocks:
        html_node = block_to_html_node(block)
        children_nodes.append(html_node)
    return ParentNode("div", children_nodes, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def paragraph_to_html_node(block):
    paragraph_content = " ".join(block.split("\n"))
    html_nodes = text_to_children(paragraph_content)
    return ParentNode("p", html_nodes)

def heading_to_html_node(block):
    header_tag ="h" + str(block.count("#"))
    header_content = block.lstrip("#").strip()
    html_nodes = text_to_children(header_content)
    return ParentNode(header_tag, html_nodes)

def code_to_html_node(block):
    code_content = block.lstrip("```").strip()
    text_node = TextNode(code_content, TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.lstrip(">").strip())
    quote_content = " ".join(cleaned_lines)
    html_nodes = text_to_children(quote_content)
    return ParentNode("blockquote", html_nodes)
    
def ulist_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines_nodes = []
    for line in lines:
        stripped_line = line[2:].strip()
        html_line = text_to_children(stripped_line)
        cleaned_lines_nodes.append(ParentNode("li", html_line))
    return ParentNode("ul", cleaned_lines_nodes)

def olist_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines_nodes = []
    for line in lines:
        stripped_line = re.sub(r'^\d+\.\s*', '', line)
        html_line = text_to_children(stripped_line)
        cleaned_lines_nodes.append(ParentNode("li", html_line))
    return ParentNode("ol", cleaned_lines_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    header = blocks[0]
    if header.count("#") > 1:
        raise Exception("Invalid markdown syntax")
    elif header.startswith("# "):
        return header.lstrip("#").strip()
    else:
        raise Exception("Missing header 1")
    
