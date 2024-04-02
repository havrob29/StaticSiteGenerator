import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "this paragraphs has a link", None, 
        {"href": "https://www.google.com", "target": "_blank"}
        ).props_to_html()
        string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node, string)

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.").to_html()
        string = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node, string)
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        string2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node2, string2)

class TestParentNode(unittest.TestCase):
    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ).to_html()
        string = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node, string)

        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Normal text2"),
                        LeafNode("b", "Bold text"),
                    ],
                ),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        ).to_html()
        string = "<p><b>Bold text</b><p>Normal text2<b>Bold text</b></p>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node2, string)

if __name__ == "__main__":
    unittest.main()