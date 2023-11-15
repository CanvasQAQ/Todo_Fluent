
from PyQt5.QtGui import QFont
from qfluentwidgets import LineEdit, TextEdit, BodyLabel
from qfluentwidgets import FluentLabelBase
from qfluentwidgets import getFont


class self_LineEdit(LineEdit):
    def __init__(self, parent=None):
        super().__init__()
        font = QFont()
        font.setFamily("LXGW WenKai Mono")
        font.setPixelSize(16)
        self.setFont(font)

class self_TextEdit(TextEdit):
    def __init__(self, parent=None):
        super().__init__()
        font = QFont()
        font.setFamily("LXGW WenKai Mono")
        font.setPixelSize(16)
        self.setFont(font)

# class self_BodyLabel(BodyLabel):
#     def __init__(self, parent=None):
#         super().__init__()
#         font = QFont()
#         font.setFamily("LXGW WenKai Mono")
#         font.setPixelSize(16)
#         self.setFont(font)

class self_BodyLabel(FluentLabelBase):
    """ Body text label

    Constructors
    ------------
    * BodyLabel(`parent`: QWidget = None)
    * BodyLabel(`text`: str, `parent`: QWidget = None)
    """

    def getFont(self, weight=QFont.Normal):
        font = QFont()
        font.setFamily("LXGW WenKai Mono")
        font.setPixelSize(16)
        font.setWeight(weight)
        return font