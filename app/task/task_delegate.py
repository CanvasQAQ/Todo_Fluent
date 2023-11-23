import pickle
import os
from .task import Task

class TaskDelegate():
    def __init__(self) -> None:
        self.data_path = 'data'
        self.pkl_file = 'task.pkl'
        self.task_dict = {} # type: dict
        self.treeview_list = [] # type: list
        self.init_root_task()
        
    def init_root_task(self):
        self.load_task()
        if not self.task_dict:
            self.task_dict[0] = Task("root")


    def get_treeview_list(self):
        '''
        init the treeview list
        the first list is the root task
        list like ["root",0,"start",["task1",1,"start",["task1-1",2,"start"]],[task2,3,"start"]]
        the first element is the task name, the second element is the task id, the third element is the task stats, the after fourth element is the childs task list
        if have no child, the fourth element is None, if have 3 child, 4-6 th element is the child task list
        each child task have same format
        '''
        # self.treeview_list = []
        self.refresh_task_status()
        temp_treeview_list=["root",0,"start"]
        temp_treeview_list = self.get_treeview_list_child(0,temp_treeview_list)
        self.treeview_list = temp_treeview_list
        return [self.treeview_list]

    def get_treeview_list_child(self, task_id, treeview_list):
        '''
        init the treeview list child
        '''
        for child_id in self.task_dict[task_id].getChildren():
            temp_list = [self.task_dict[child_id].getName(),child_id,self.task_dict[child_id].getStats()]
            self.get_treeview_list_child(child_id,temp_list)
            treeview_list.append(temp_list)
        
        return treeview_list
            

    def create_new_id(self):
        #create a new task id, the id is the 1 to max id
        #from 1 to max id, find the first id which is not used
        #return the new id
        new_id = 1
        while new_id in self.task_dict:
            new_id += 1
        return new_id
    
    def create_new_task(self, name, father_id=0):
        #create a new task, and return the task id
        new_id = self.create_new_id()
        self.task_dict[new_id] = Task(name)
        self.task_dict[father_id].addChild(new_id)
        return new_id
    
    def remove_task(self, task_id):
        #remove the task just means mark the task stats as 'waiver'
        #remove father task also means remove all the children task
        #find all task which child include the task_id, remove the task_id friom the child list,only remove the first one
        self.task_dict[task_id].setStats('waiver')
        for child_id in self.task_dict[task_id].getChildren():
            self.remove_task_child(child_id)
        for key in self.task_dict:
            if task_id in self.task_dict[key].getChildren():
                self.task_dict[key].removeChild(task_id)

    def remove_task_child(self, task_id):
        #for child task, just mark the stats as 'waiver'
        self.task_dict[task_id].setStats('waiver')
        for child_id in self.task_dict[task_id].getChildren():
            self.remove_task(child_id)
    
    def complete_task(self, task_id):
        #complete the task just means mark the task stats as 'complete'
        self.task_dict[task_id].setStats('complete')
        self.task_dict[task_id].setEndTime()
        for child_id in self.task_dict[task_id].getChildren():
            if self.task_dict[child_id].getStats() != 'complete':
                self.complete_task(child_id)
    
    def undo_task(self, task_id):
        #undo the task just means mark the task stats as 'start'
        self.task_dict[task_id].setStats('start')
        self.task_dict[task_id].setEndTime()
        # for child_id in self.task_dict[task_id].getChildren():
        #     self.undo_task(child_id)
    
    def save_task(self):
        #save the self.task_dict to the pkl file
        full_path = os.path.join(self.data_path, self.pkl_file)
        if not os.path.isdir(self.data_path):
            os.mkdir(self.data_path)
        with open(full_path, 'wb') as f:
            pickle.dump(self.task_dict, f, pickle.HIGHEST_PROTOCOL)
        

    def load_task(self):
        full_path = os.path.join(self.data_path, self.pkl_file)
        if os.path.isfile(full_path):
            #load the task from the pkl file
            with open(full_path, 'rb') as f:
                self.task_dict = pickle.load(f)
        #load the task from the file

    def judge_task_complete(self, task_id):
        #judge if the task is complete
        #if the task is complete, return True
        #if the task is not complete, return False
        #if the task is not complete, but all the child task is complete, then the task is complete
        if self.task_dict[task_id].getStats() == 'complete':
            if not self.task_dict[task_id].getChildren():
                return True
            else:
                for child_id in self.task_dict[task_id].getChildren():
                    if not self.judge_task_complete(child_id):
                        return False
                return True
        else:
            if not self.task_dict[task_id].getChildren():
                return False
            else:
                for child_id in self.task_dict[task_id].getChildren():
                    if not self.judge_task_complete(child_id):
                        return False
                return True
    
    def refresh_task_status(self):
        #refresh the task status, if the task is not complete, but all the child task is complete, then the task status should be complete
        #if the task is complete, but some child task is not complete, then the task status should be start
        for task_id in self.task_dict:
            if self.task_dict[task_id].getStats() != 'complete':
                if self.judge_task_complete(task_id):
                    self.task_dict[task_id].setStats('complete')
            elif self.task_dict[task_id].getStats() == 'complete':
                if not self.judge_task_complete(task_id):
                    self.task_dict[task_id].setStats('start')
