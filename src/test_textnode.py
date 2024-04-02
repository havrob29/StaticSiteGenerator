import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq_same(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_different(self):
        node = TextNode("This is not a text node", "bold", "havrob.dev")
        node2 = TextNode("This is a text node", "bold")

        
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()