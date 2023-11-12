# coding:utf-8
from datetime import datetime
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEvent
from PyQt5.QtGui import QDesktopServices, QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QTreeWidgetItem

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel, toggleTheme)

from qfluentwidgets import LineEdit, PrimaryPushButton, DateTimeEdit, IndeterminateProgressRing
from qfluentwidgets import FlowLayout
from ..common.style_sheet import StyleSheet
from ..view.self_widgets import self_LineEdit, self_TextEdit, self_BodyLabel
from ..view.tree_view import tree_view




class TodoUI(ScrollArea):

    def __init__(self, parent=None):
        super().__init__()
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
        self.initUI()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('todointerface')
        StyleSheet.TODO_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(10, 10, 10, 20)
        self.vBoxLayout.setSpacing(10)
        # self.vBoxLayout.setAlignment(Qt.AlignRight)
    
    def initUI(self):
        self.initAddTaskUI()
        self.initTreeviewUI()
        self.disableTaskInfo()

    def initAddTaskUI(self):
        self.add_task_layout = QVBoxLayout()
        self.task_input = self_LineEdit(self)
        self.task_input.setFixedWidth(250)

        self.add_task_button_layout = FlowLayout()
        self.add_button = PrimaryPushButton('Add Task')
        self.delete_button = PrimaryPushButton('Delete')
        self.add_task_button_layout.addWidget(self.add_button)
        self.add_task_button_layout.addWidget(self.delete_button)

        self.add_task_layout.addWidget(self.task_input)
        self.add_task_layout.addLayout(self.add_task_button_layout)

        self.vBoxLayout.addLayout(self.add_task_layout)
    
    def initTreeviewUI(self):
        self.tree_layout = QHBoxLayout()
        self.todo_list = tree_view(self)
        self.todo_list.setColumnCount(1)
        self.todo_list.setHeaderLabels(['TASK'])
        
        self.initTaskinfoUI()
        self.tree_layout.addWidget(self.todo_list)
        self.tree_layout.addLayout(self.task_Info_layout)

        self.vBoxLayout.addLayout(self.tree_layout)
        
    def initTaskinfoUI(self):
        self.task_Info_layout = QVBoxLayout()
        self.taskName_layout = FlowLayout()
        self.taskName_label = self_BodyLabel('Task Name:')
        self.taskName_ring = IndeterminateProgressRing(self)
        self.taskName_ring.setFixedSize(16, 16)
        self.taskName_ring.setStrokeWidth(3)
        self.taskName_ring.hide()
        self.taskName_layout.addWidget(self.taskName_label)
        self.taskName_layout.addWidget(self.taskName_ring)

        self.taskName = self_LineEdit()
        # self.taskName.setDisabled(True)

        self.task_startTime_label = self_BodyLabel('Start Time:')
        self.task_startTime = DateTimeEdit()
        # self.task_startTime.setDateTime(datetime.now())
        # self.task_startTime.setDateTime(QDateTime())
        self.task_startTime.setDisabled(True)
        self.task_startTime.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.task_completeTime_label = self_BodyLabel('Finished Time:')
        self.task_completeTime = DateTimeEdit()
        # self.task_completeTime.setDateTime(datetime.now())
        # self.task_startTime.clear()
        self.task_completeTime.setDisabled(True)
        self.task_completeTime.setDisplayFormat("yyyy-MM-dd HH:mm")


        self.task_description_layout = FlowLayout()

        self.description_ring = IndeterminateProgressRing(self)
        self.description_ring.setFixedSize(16, 16)
        self.description_ring.setStrokeWidth(3)
        self.description_ring.hide()
        # print( )

        self.task_description_label = self_BodyLabel('Description:')

        self.task_description_layout.addWidget(self.task_description_label)
        self.task_description_layout.addWidget(self.description_ring)
        self.task_description = self_TextEdit()
        


        self.task_TimeInfo_layout = QHBoxLayout()

        self.task_TimeInfo_layout_left = QVBoxLayout()
        self.task_TimeInfo_layout_left.addWidget(self.task_startTime_label)
        self.task_TimeInfo_layout_left.addWidget(self.task_startTime)
        
        self.task_TimeInfo_layout_right = QVBoxLayout()
        self.task_TimeInfo_layout_right.addWidget(self.task_completeTime_label)
        self.task_TimeInfo_layout_right.addWidget(self.task_completeTime)

        self.task_TimeInfo_layout.addLayout(self.task_TimeInfo_layout_left)
        self.task_TimeInfo_layout.addLayout(self.task_TimeInfo_layout_right)

        self.task_Info_layout.addLayout(self.taskName_layout)
        self.task_Info_layout.addWidget(self.taskName)
        self.task_Info_layout.addLayout(self.task_TimeInfo_layout)
        self.task_Info_layout.addLayout(self.task_description_layout)
        self.task_Info_layout.addWidget(self.task_description)
        # self.task_Info_layout.addWidget(self.ring)
    
    def disableTaskInfo(self):
        self.taskName.setDisabled(True)
        self.task_startTime.setDisabled(True)
        self.task_completeTime.setDisabled(True)
        self.task_description.setDisabled(True)
    
    def enableTaskInfo(self):
        self.taskName.setDisabled(False)
        self.task_startTime.setDisabled(False)
        self.task_completeTime.setDisabled(False)
        self.task_description.setDisabled(False)
