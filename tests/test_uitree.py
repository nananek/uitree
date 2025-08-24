import unittest
from uitree.uitree import UITree


class TestUItree(unittest.TestCase):
    def setUp(self):
        self.tree = UITree(depth=1)  # テスト速度のため深さ1

    def test_xpath_returns_ui_elements(self):
        # ルート直下のControl要素をXPathで取得
        elements = self.tree.xpath('/Control/Control')
        self.assertIsInstance(elements, list)
        if elements:
            from uitree.uitree import UIElement
            self.assertIsInstance(elements[0], UIElement)

    def test_ui_element_control(self):
        # ルート直下のControl要素を取得し、control属性があることを確認
        elements = self.tree.xpath('/Control/Control')
        if elements:
            elem = elements[0]
            self.assertTrue(hasattr(elem, 'control'))
            runtime_id = elem.attrib.get('runtime_id', '')
            if not runtime_id:
                self.skipTest('runtime_idが空のためスキップ')
            self.assertIsNotNone(elem.control)

    def test_ui_element_attrib_and_tag(self):
        elements = self.tree.xpath('/Control/Control')
        if elements:
            elem = elements[0]
            self.assertTrue(isinstance(elem.attrib, dict))
            self.assertEqual(elem.tag, 'Control')

if __name__ == '__main__':
    unittest.main()