# coding:utf-8
from datetime import datetime
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEvent
from PyQt5.QtGui import QDesktopServices, QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QTreeWidgetItem
from PyQt5.QtCore import QTimer

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel, toggleTheme)

from qfluentwidgets import LineEdit, PrimaryPushButton, DateTimeEdit
from qfluentwidgets import FlowLayout
from ..common.style_sheet import StyleSheet
from ..ui.self_widgets import self_LineEdit, self_TextEdit, self_BodyLabel
from ..ui.tree_view import tree_view
from ..ui.todo_ui import TodoUI
from ..task.task_delegate import TaskDelegate






class TodoInterface(TodoUI):

    def __init__(self, parent=None):
        super().__init__()
        self.initTaskFunc()
        self.initTimer()
        self.initSignalToSlot()

    def initSignalToSlot(self):
        self.add_button.clicked.connect(self.addTask)
        self.delete_button.clicked.connect(self.deleteTask)
        self.todo_list.itemClicked.connect(self.itemClick)
        self.todo_list.nothingclicked.connect(self.setInfoToDefault)
        self.todo_list.itemChanged.connect(self.taskStatusChange)

    def initTaskFunc(self):
        self.taskFunc = TaskDelegate()
        self.updateTreeView()
    
    def initTimer(self):
        self.taskName_timer = QTimer(self)
        self.taskName_timer.setSingleShot(True)
        self.taskName_timer.timeout.connect(self.TaskNameChange)
        self.taskName.textChanged.connect(self.on_TaskNameChange)

        self.task_description_timer = QTimer(self)
        self.task_description_timer.setSingleShot(True)
        self.task_description_timer.timeout.connect(self.TaskDescriptionChange)
        self.task_description.textChanged.connect(self.on_TaskDescriptionChange)

    def addTask(self):
        self.tryDisconnectItemChanged()
        task_name = self.task_input.text()
        if task_name:
            if self.todo_list.selectedItems():
                current_task = self.todo_list.selectedItems()[0]
                # task = QTreeWidgetItem(current_task)
                task_id = current_task.data(0,Qt.UserRole)
            else:
                # task = QTreeWidgetItem(self.todo_list)
                task_id = 0
            self.taskFunc.create_new_task(task_name,task_id)
            self.taskFunc.save_task()
            self.updateTreeView()
            self.task_input.clear()
        self.ReConnectItemChanged()
    
    def deleteTask(self):
        self.tryDisconnectItemChanged()
        current_tasks = self.todo_list.selectedItems()
        if current_tasks:
            for task in current_tasks:
                task_id = task.data(0,Qt.UserRole)
                self.taskFunc.remove_task(task_id)
            self.taskFunc.save_task()
            self.updateTreeView()
        self.ReConnectItemChanged()


    def updateTreeView(self):
        treeview_list = self.taskFunc.get_treeview_list()
        self.todo_list.init_treeview_list(treeview_list)
        # self.todo_list.expandAll()


    def debug_temp(self):
        task = QTreeWidgetItem(self.todo_list)
        task.setText(0,"fuck")

    def itemClick(self,item):
        self.DisconnectInfo()
        current_task = item
        if not item:
            pass
        else:
            current_task_id = current_task.data(0,Qt.UserRole)
            if current_task_id in self.taskFunc.task_dict:
                task = self.taskFunc.task_dict[current_task_id]
                # self.info_taskname.textChanged.disconnect()
                self.taskName.setText(self.tr(task.task_name))
                # self.info_taskname.textChanged.connect(self.task_name_change)
                self.task_startTime.setDateTime(task.start_time)
                self.task_description.setHtml(task.description)
                if task.complete_time:
                    self.task_completeTime.setDateTime(task.complete_time)
                else:
                    self.task_completeTime.setDateTime(datetime.now())
                self.enableTaskInfo()
        self.ReConnectInfo()

    def setInfoToDefault(self):
        self.DisconnectInfo()
        self.taskName.setText(None)
        self.task_startTime.setDateTime(datetime.now())
        self.task_completeTime.setDateTime(datetime.now())
        self.task_description.setText(None)
        self.disableTaskInfo()
        self.ReConnectInfo()


    def on_TaskNameChange(self):
        self.taskName_timer.start(500)
        self.taskName_ring.show()
        self.todo_list.setDisabled(True)
        self.tryDisconnectItemChanged()
        self.tryDisconnectItemClicked()

    def TaskNameChange(self):
        text = self.taskName.text()
        if text:
            if len(self.todo_list.selectedItems()) != 0:
                current_task = self.todo_list.selectedItems()[0]
                current_task_id = current_task.data(0,Qt.UserRole)
                if current_task_id in self.taskFunc.task_dict:
                    task = self.taskFunc.task_dict[current_task_id]
                    task.setName(text)
                    self.todo_list.selectedItems()[0].setText(0,text)
                    self.taskFunc.save_task()
                    # self.updateTreeView()
        self.todo_list.itemClicked.connect(self.itemClick)
        self.todo_list.setDisabled(False)
        self.taskName_ring.hide()
        self.ReConnectItemChanged()
                    
    def on_TaskDescriptionChange(self):
        self.task_description_timer.start(500)
        self.description_ring.show()
        self.todo_list.setDisabled(True)
        self.tryDisconnectItemClicked()
    
    def TaskDescriptionChange(self):
        text = self.task_description.toHtml()
        if text:
            if len(self.todo_list.selectedItems()) != 0:
                current_task = self.todo_list.selectedItems()[0]
                current_task_id = current_task.data(0,Qt.UserRole)
                if current_task_id in self.taskFunc.task_dict:
                    task = self.taskFunc.task_dict[current_task_id]
                    task.setdescription(text)
                    self.taskFunc.save_task()
                    # self.updateTreeView()
        self.todo_list.itemClicked.connect(self.itemClick)
        self.todo_list.setDisabled(False)
        self.description_ring.hide()
    
    def tryDisconnectItemClicked(self):
        try:
            self.todo_list.itemClicked.disconnect()
        except:
            pass

    def tryDisconnectItemChanged(self):
        try:
            self.todo_list.itemChanged.disconnect()
        except:
            pass

    def ReConnectItemChanged(self):
        self.todo_list.reconnect_item_changed()
        self.todo_list.itemChanged.connect(self.taskStatusChange)
        

    def DisconnectInfo(self):
        self.taskName_timer.timeout.disconnect()
        self.taskName.textChanged.disconnect()
        self.task_description_timer.timeout.disconnect()
        self.task_description.textChanged.disconnect()

    def ReConnectInfo(self):
        self.taskName_timer.timeout.connect(self.TaskNameChange)
        self.taskName.textChanged.connect(self.on_TaskNameChange)
        self.task_description_timer.timeout.connect(self.TaskDescriptionChange)
        self.task_description.textChanged.connect(self.on_TaskDescriptionChange)

    def taskStatusChange(self, item, column):
        
        self.tryDisconnectItemClicked()
        # self.tryDisconnectItemChanged()
        self.todo_list.itemChanged.disconnect(self.taskStatusChange)
        if column == 0:  # 如果更改的是第一列
            current_task_id = item.data(0,Qt.UserRole)
            if item.checkState(column) == Qt.Checked :
                self.taskFunc.complete_task(current_task_id)
            else:
                self.taskFunc.undo_task(current_task_id)
            self.taskFunc.save_task()
            self.updateTreeView()
        # self.ReConnectItemChanged()
        self.todo_list.itemChanged.connect(self.taskStatusChange)
        self.todo_list.itemClicked.connect(self.itemClick)