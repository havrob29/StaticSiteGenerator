import re

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    listofnodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            listofnodes.append(node)
            continue

        strlist = node.text.split(delimiter)
        if len(strlist) % 2 == 0:
            raise Exception("no closing delimiter")
        for i in range (0, len(strlist)):
            if strlist[i] == "":
                continue
            if i % 2 == 0:
                listofnodes.append(TextNode(strlist[i], text_type_text))
            if i % 2 == 1:
                listofnodes.append(TextNode(strlist[i], text_type))
    return listofnodes

def split_nodes_image(old_nodes):
    listofnodes = []
    for node in old_nodes:
        toextend = []
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            listofnodes.append(node)
            continue
        for image in images:
            firstnodeandrest = node.text.split(f"![{image[0]}]({image[1]})", 1)
            if firstnodeandrest[0] != "":
                toextend.append(TextNode(firstnodeandrest[0], text_type_text))  
            toextend.append(TextNode(image[0],text_type_image, image[1]))
            node.text = firstnodeandrest[1]
        if len(node.text) != 0:
            toextend.append(TextNode(node.text, text_type_text))
        listofnodes.extend(toextend)
    return listofnodes

def split_nodes_link(old_nodes):
    listofnodes = []
    for node in old_nodes:
        toextend = []
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            listofnodes.append(node)
            continue
        for link in links:
            firstnodeandrest = node.text.split(f"[{link[0]}]({link[1]})", 1)
            if firstnodeandrest[0] != "":
                toextend.append(TextNode(firstnodeandrest[0], text_type_text))  
            toextend.append(TextNode(link[0], text_type_link, link[1]))
            node.text = firstnodeandrest[1]
        if len(node.text) != 0:
            toextend.append(TextNode(node.text, text_type_text))
        listofnodes.extend(toextend)
    return listofnodes

def extract_markdown_images(text):
    list_to_return = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        list_to_return.append(match)
    return list_to_return

def extract_markdown_links(text):
    list_to_return = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        list_to_return.append(match)
    return list_to_return

def text_to_textnodes(text):
    first_node = [TextNode(text, text_type_text)]
    nodes1 = split_nodes_image(first_node)
    nodes2 = split_nodes_link(nodes1)
    nodes3 = split_nodes_delimiter(nodes2, "**", text_type_bold)
    nodes4 = split_nodes_delimiter(nodes3, "*", text_type_italic)
    nodes5 = split_nodes_delimiter(nodes4, "`", text_type_code)

    return nodes5
    
