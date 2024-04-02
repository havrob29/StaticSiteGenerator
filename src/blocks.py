from htmlnode import (
    ParentNode
)

from textnode import(
    text_node_to_html_node,
)

from inlinemarkdown import(
    text_to_textnodes
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    listofblocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in listofblocks:
        if block == "":
            continue
        block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_blocktype(block):
    lines = block.split("\n")

    if (
        block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
        ):
        return block_type_heading
    
    if block.startswith("```") and block.endswith("```") and len(lines) > 1:
        return block_type_code
    
    quote_block = True
    unordered_list_block = True
    ordered_list_block = True
    for i in range(len(lines)):
        if lines[i].startswith(">") == False:
            quote_block = False
        if (lines[i].startswith("* ") or lines[i].startswith("- ")) == False:
            unordered_list_block = False
        index_plus_one = i+1
        if lines[i].startswith(f"{index_plus_one}. ") == False:
            ordered_list_block = False
    if quote_block:
        return block_type_quote
    if unordered_list_block:
        return block_type_unordered_list
    if ordered_list_block:
        return block_type_ordered_list
    return block_type_paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    childblocks = []
    for block in blocks:
        blocktype = block_to_blocktype(block)
        if blocktype == block_type_code:
            childblocks.append(code_block_to_html_node(block))
            continue
        if blocktype == block_type_quote:
            childblocks.append(quote_block_to_html_node(block))
            continue
        if blocktype == block_type_heading:
            childblocks.append(heading_to_html_node(block))
            continue
        if blocktype == block_type_paragraph:
            childblocks.append(paragraph_block_to_html_node(block))
            continue
        if blocktype == block_type_ordered_list:
            childblocks.append(ordered_list_block_to_html_node(block))
            continue
        if blocktype == block_type_unordered_list:
            childblocks.append(unordered_list_block_to_html_node(block))
            continue
        else:
            raise ValueError("Invalid block type")
    return ParentNode("div", childblocks, None)

def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def quote_block_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith(">") == False:
            raise Exception("Not a quote block")
        new_lines.append(line.lstrip(">").strip())
    joined = " ".join(new_lines)
    children = text_to_children(joined)
    return ParentNode("blockquote", children)

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    listnodes = []
    for line in lines:
        textchildren = text_to_children(line[2:])
        listnodes.append(ParentNode("li", textchildren))
    return ParentNode("ul", listnodes)

def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    listnodes = []
    for line in lines:
        children = text_to_children(line[3:])
        listnodes.append(ParentNode("li", children))
    return ParentNode("ol", listnodes)

def code_block_to_html_node(block):
    lines = block.split("\n")
    newlines = []
    for line in lines:
        if line.startswith("```"):
            cleaned = line.lstrip("```").strip()
            continue
        if line.endswith("```"):
            cleaned = line.rstrip("```").strip()
            continue
        newlines.append(line)
    cleanedblock = "\n".join(newlines)
    children = text_to_children(cleanedblock)
    prenode = ParentNode("code", children)
    return ParentNode("pre", [prenode])

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)