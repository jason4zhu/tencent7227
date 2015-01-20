# -*- coding: utf-8 -*-
'''
Created on 2014年9月4日

@author: supertool
'''
import os

global statusFileName
statusFileName = '/home/data10/TencentTools/tools/main.status'

global STATUS_ONGOING
STATUS_ONGOING                      = (2, "正在进行中")
global STATUS_SUCCEED
STATUS_SUCCEED                      = (1, "执行成功")
global STATUS_FAIL_EXCEL_NOT_IN_FORMAT
STATUS_FAIL_EXCEL_NOT_IN_FORMAT     = (0, "excel格式不正确")
global STATUS_FAIL_TASK_7227
STATUS_FAIL_TASK_7227               = (0, "task7227执行失败")
global STATUS_FAIL_TASK_CONFLICT
STATUS_FAIL_TASK_CONFLICT           = (0, "已经存在正在执行中的task7227")

def __statusToLine(status):
    return str(status[0])+"\t"+str(status[1])

def __lineToStatus(line):
    line = line.strip()
    fields = line.split("\t")
    return (int(fields[0]), fields[1])

def writeStatus(status):
    """ 写状态
    """
    fw = open(statusFileName, 'w')
    fw.write(__statusToLine(status))
    fw.close()

def isOverlappedRunning():
    """ 是否已经有相同的脚本正在执行中
    """
    if not os.path.exists(statusFileName):
        fw = open(statusFileName, 'w')
        fw.write(__statusToLine(STATUS_ONGOING))
        fw.close()
        return False
    else:
        fr = open(statusFileName, 'r')
        line = fr.readline()
        status = __lineToStatus(line)
        if status[0] == STATUS_ONGOING[0]:
            return True
        else:
            return False
    
    
    
    
