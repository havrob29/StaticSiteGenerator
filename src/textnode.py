from htmlnode import LeafNode

text_type_text = "text"
text_type_code = "code"
text_type_italic = "italic"
text_type_bold = "bold"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        if self.url == None:
            return f'TextNode("{self.text}", "{self.text_type}")'
        
        return f'TextNode("{self.text}", "{self.text_type}", "{self.url}")'
    
def text_node_to_html_node(text_node):
    valid_types = ["text", "bold", "italic", "code", "link", "image"]
    if text_node.text_type not in valid_types:
        raise Exception(f"invalid text type for TextNode, valid types are {valid_types}")
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        props = {
            "href": text_node.url
        }
        return LeafNode("a", text_node.text, props)
    if text_node.text_type == "image":
        props = {
            "src": text_node.url,
            "alt": text_node.text
        }
        return LeafNode("img", "", props)

