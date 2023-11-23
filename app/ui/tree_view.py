from qfluentwidgets import TreeWidget
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEvent
from PyQt5.QtWidgets import QTreeWidgetItem
from ..common.style_sheet import StyleSheet

class tree_view(TreeWidget):
    nothingclicked = pyqtSignal()
    def __init__(self, parent=None):
        super(tree_view, self).__init__(parent)
        self.itemChanged.connect(self.handleItemChanged)  # 连接项目更改信号和处理函数
        StyleSheet.TREE_VIEW.apply(self)
        self.fontsize = 18
        
        # self.setItemDelegate(self_setfont_tree_delegate(self))

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            super(tree_view, self).mousePressEvent(event)
        else:
            self.clearSelection()  # 如果点击的位置没有项目，清除选择
            self.nothingclicked.emit()
        
    def handleItemChanged(self, item, column):
        if column == 0:  # 如果更改的是第一列
            self.auto_expand(item)
            font = item.font(column)
            if item.checkState(column) == Qt.Checked :
                font.setStrikeOut(True)
                #为每一个子项目设置选中状态
                for i in range(item.childCount()):
                    item.child(i).setCheckState(column,Qt.Checked)
            else:
                font.setStrikeOut(False)
                # for i in range(item.childCount()):
                #     item.child(i).setCheckState(column,Qt.Unchecked)
            item.setFont(column, font)  # 更新字体
            
    def auto_expand(self, item):
        if item.checkState(0) == Qt.Checked:
            self.collapseItem(item)
        else:
            self.expandItem(item)
        # parent = item.parent()
        # expand_flag = False #default is try to collapse
        # if parent:
        #     for i in range(parent.childCount()):
        #         if parent.child(i).checkState(0) == Qt.Unchecked:
        #             expand_flag = True
        #             break
        #     if expand_flag:
        #         self.only_unchecked(parent)
        #         self.expandItem(parent)
        #     else:
        #         self.only_checked(parent)
        #         self.collapseItem(parent)
                
    def auto_expand_all(self,item=None):
        if not item:
            item = self.invisibleRootItem()
        self.auto_expand(item)
        for i in range(item.childCount()):
            self.auto_expand_all(item.child(i))

    def only_unchecked(self, item):
        font = item.font(0)
        font.setStrikeOut(False)
        # self.itemChanged.disconnect(self.handleItemChanged)
        item.setCheckState(0,Qt.Unchecked)
        item.setFont(0, font)
        # self.itemChanged.connect(self.handleItemChanged)
    
    def only_checked(self, item):
        font = item.font(0)
        font.setStrikeOut(True)
        # self.itemChanged.disconnect(self.handleItemChanged)
        item.setCheckState(0,Qt.Checked)
        item.setFont(0, font)
        # self.itemChanged.connect(self.handleItemChanged)


    def init_treeview_list(self,treeview_list):
        root_item = self.invisibleRootItem()
        self.delete_all_item()
        root_item.setData(0,Qt.UserRole,0)
        self.load_item(root_item, treeview_list)
        self.auto_expand_all()
        
    def load_item(self,parent_item,data):
        for item_data in data:
            #id nor 0 means not root
            if item_data[1] != 0 :
                item = TreeWidgetItem(parent_item)
                item.setText(0,item_data[0])
                #set id
                item.setData(0,Qt.UserRole,item_data[1])
                if item_data[2] == "start" :
                    item.setCheckState(0,Qt.Unchecked)
                elif item_data[2] == 1 :
                    item.setCheckState(0,Qt.PartiallyChecked)
                elif item_data[2] == "complete" :
                    item.setCheckState(0,Qt.Checked)
            else:
                item = parent_item
            self.load_item(item, item_data[3:])
    
    def delete_all_item(self):
        root_item = self.invisibleRootItem()
        root_item.takeChildren()
    
    def reconnect_item_changed(self):
        # pass
        self.itemChanged.connect(self.handleItemChanged)

class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(TreeWidgetItem, self).__init__(parent)
        self.fontsize = 18
        # self.setCheckState(0,Qt.Unchecked)
        font = self.font(0)
        font.setFamily("LXGW WenKai Mono")
        font.setPixelSize(self.fontsize)
        self.setFont(0,font)
    