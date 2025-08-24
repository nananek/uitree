

from __future__ import annotations
import uiautomation as auto
from lxml import etree
from typing import Any, Dict, List, Optional, Union
import uuid

class UIElement:
    def __init__(self, element: etree._Element, control_map: Dict[str, Any]):
        self._element = element
        self._control_map = control_map
        self._runtime_id = self._element.attrib.get('runtime_id', '')

    @property
    def attrib(self) -> Dict[str, str]:
        # lxmlのattribは特殊なMapping型なのでdictに変換
        return dict(self._element.attrib)

    @property
    def tag(self) -> str:
        return self._element.tag

    @property
    def control(self) -> Optional[Any]:
        # 常にuuidで紐付け
        return self._control_map.get(self._runtime_id)

    def xpath(self, expr: str) -> List['UIElement']:
        elements = self._element.xpath(expr)
        return [UIElement(e, self._control_map) for e in elements]

    def __str__(self):
        return f"<UIElement tag='{self.tag}' attrib={self.attrib}>"

    def __repr__(self):
        return self.__str__()

class UITree:
    def __init__(self, root_control: Optional[Any] = None, depth: Optional[int] = None):
        """
        root_control: uiautomation.Control オブジェクト。Noneならデスクトップ。
        depth: 再帰的に探索する深さ。Noneなら無制限。
        """
        self.root_control = root_control or auto.GetRootControl()
        self.depth = float('inf') if depth is None else depth
        self._control_map = {}  # runtime_id -> control
        self.xml_root = self._build_xml_tree(self.root_control, self.depth)
        self.tree = etree.ElementTree(self.xml_root)

    def _build_xml_tree(self, control: Any, depth: Union[int, float], parent_xml: Optional[etree._Element] = None) -> etree._Element:
        # runtime_idは常にuuidで生成
        runtime_id = str(uuid.uuid4())
        tag = control.ControlTypeName or 'Control'
        attrib = {
            'name': control.Name or '',
            'automation_id': control.AutomationId or '',
            'class': control.ClassName or '',
            'handle': str(control.NativeWindowHandle or ''),
            'runtime_id': runtime_id,
        }
        elem = etree.Element(tag, attrib=attrib)
        # Map runtime_id to control for reverse lookup
        self._control_map[runtime_id] = control

        if depth > 0:
            try:
                for child in control.GetChildren():
                    child_elem = self._build_xml_tree(child, depth-1, elem)
                    elem.append(child_elem)
            except Exception:
                pass  # 一部のコントロールで例外が出ることがある

        return elem

    def xpath(self, expr: str) -> List['UIElement']:
        """
        XPath式で要素を検索し、UIElementのリストを返す
        """
        elements = self.tree.xpath(expr)
        return [UIElement(elem, self._control_map) for elem in elements]

    def refresh(self, depth: Optional[int] = None) -> None:
        """
        UIツリーを再構築する。depthを指定した場合はその深さで再構築する。
        depth=None なら無制限。
        """
        if depth is None:
            self.depth = float('inf')
        else:
            self.depth = depth
        self._control_map.clear()
        self.xml_root = self._build_xml_tree(self.root_control, self.depth)

    def dumpxml(self, pretty_print: bool = True, encoding: str = 'unicode') -> str:
        """
        現在のUIツリーをXML文字列として返す。
        pretty_print=True で整形出力。
        encoding='unicode' でstr型、'utf-8' などでbytes型を返す。
        """
        return etree.tostring(self.xml_root, pretty_print=pretty_print, encoding=encoding)