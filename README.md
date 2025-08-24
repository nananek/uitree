# UITree

Windows UI Automationのツリーをlxml.etreeでXML化し、XPathで検索・操作できるPythonモジュールです。

## 特徴
- uiautomationのUIツリーをlxmlのElementTreeとして構築
- 各ノードはコントロール種別名（例: Button, Edit, Window）でXML化
- XPathでUI要素を柔軟に検索
- 検索結果からUIElement経由で元のuiautomation.Controlにアクセス可能
- 各ノードには一意なUUIDが付与され、UIElement.controlでコントロール取得

## インストール
```
pip install -r requirements.txt
pip install .
```

## 使い方
```python
from uitree import UITree
from lxml import etree

# UIツリーを取得（デフォルトはデスクトップ直下3階層）
tree = UITree(depth=3)

# XMLとしてダンプ
xml_str = etree.tostring(tree.tree.getroot(), pretty_print=True, encoding='unicode')
print(xml_str)

# XPathでボタンを検索
buttons = tree.xpath('//Button')
for btn in buttons:
	print(btn.attrib)
	print(btn.control)  # uiautomation.Control
```

## クラス概要

### UITree
- `UITree(root_control=None, depth=3)`
	- UIツリーを構築。root_control未指定ならデスクトップ。
	- `xpath(expr)` ... XPathでUIElementリスト取得
	- `refresh()` ... ツリー再構築
	- `tree` ... lxmlのElementTree

### UIElement
- `attrib` ... XML属性(dict)
- `tag` ... コントロール種別名
- `control` ... uiautomation.Control
- `xpath(expr)` ... サブツリーにXPath検索

## ライセンス
MIT License
