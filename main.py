# -*- coding: utf-8 -*-
'''
Created on 2014年9月4日

@author: supertool
'''

import xlrd
import statusMngr
import sys
from loggingMngr import logger
import datetime
from shellCall import shellCall
from task7227 import task7227
import traceback
from statusMngr import isOverlappedRunning
import time


##################################
#
# script path: supertool@K1201.mzhen.cn:/home/data12/supertool/yuchangliang/task7227/tencentEntry
# ftp url: ftp://d15.mzhen.cn/task_7227/
#
##################################
if __name__ == "__main__":
    logger.info("""
###########################
# 
# TASK_7227
# datetime: %s
# 
###########################""" % (time.strftime('%Y-%m-%d %H:%M:%d',time.localtime(time.time())),))
    try:
        #-- 查看状态文件，如果已经有运行的脚本，直接返回；否则，标记状态为ONGOING --
        if isOverlappedRunning():
            logger.error("Another task7227 is undergoing.")
            sys.exit()
        statusMngr.writeStatus(statusMngr.STATUS_ONGOING)
        
        #-- 解析xls文件，获取信息 --
        data = xlrd.open_workbook(sys.argv[1])
        table = data.sheet_by_index(0)
        
        campaignid = table.cell(0, 0).value
        if type(campaignid) == float:
            campaignid = int(campaignid)
        campaignid  = str(campaignid).strip()
        if campaignid[:3] != 'ca_':
            campaignid = 'ca_' + campaignid
        
        start_time  = xlrd.xldate.xldate_as_datetime(table.cell(1, 0).value, 0)
        end_time    = xlrd.xldate.xldate_as_datetime(table.cell(1, 1).value, 0)
        if not campaignid or not start_time or type(start_time) != datetime.datetime or not end_time or type(end_time) != datetime.datetime:
            statusMngr.writeStatus(statusMngr.STATUS_FAIL_EXCEL_NOT_IN_FORMAT)
            logger.error("campaignid or start_time or end_time is not in format.")
            sys.exit()
        start_time = start_time.strftime('%Y%m%d')
        end_time = end_time.strftime('%Y%m%d')
        
        lines = []
        uniqueSpidSet = set()
        for i in range(3, table.nrows):
            if not str(table.cell(i,0).value).strip():
                continue
            
            gameid = table.cell(i,1).value
            if type(gameid) == float:
                gameid = int(gameid)
            gameid  = str(gameid).strip()
            
            platid = table.cell(i,2).value
            if type(platid) == float:
                platid = int(platid)
            platid  = str(platid).strip()
            
            mediaid = table.cell(i,3).value
            if type(mediaid) == float:
                mediaid = int(mediaid)
            mediaid = str(mediaid).strip()
            
            spid = table.cell(i,4).value
            if type(spid) == float:
                spid = int(spid)
            spid = str(spid).strip()
            
            if not gameid or not platid or not mediaid or not spid:
                statusMngr.writeStatus(statusMngr.STATUS_FAIL_EXCEL_NOT_IN_FORMAT)
                logger.error("cell is blank. row=["+str(i)+"]")
                sys.exit()
                
            line = spid + " " + gameid + " " + platid + " " + mediaid
            lines.append(line)
            
            uniqueSpidSet.add("\\'"+spid+"\\'")
        
        #-- 写task7227.cfg --
        cfgFileName = "task7227.cfg"
        linesStr = "\n".join(lines)
    
        try:
            fw = open(cfgFileName, 'w')
            fw.write("#spid gid pid mid\n")
            fw.write(linesStr)
        finally:
            fw.close()
        
        #-- 执行tencentHive.sh脚本 --
        hiveResultFileName = "tencentHive.output"
        spid_list = ",".join(uniqueSpidSet)
        cmd= "source tencentHive.sh %s %s %s %s %s" % (campaignid, spid_list, start_time, end_time, hiveResultFileName)
        logger.info("hive_cmd=["+str(cmd)+"]")
        shellCall(cmd)
        
        #-- 利用hive跑出的基础数据做相关计算，并打成.tar.gz压缩包 --
        print("cfgFileName=["+cfgFileName+"], hiveResultFileName=["+hiveResultFileName+"]")
        status = task7227(cfgFileName, hiveResultFileName, campaignid)
        statusMngr.writeStatus(status)
        
    except Exception as e:
        logger.error("When at main logic. errMsg=["+str(e)+"], traceback=[\n"+str(traceback.format_exc())+"]")
        statusMngr.writeStatus(statusMngr.STATUS_FAIL_TASK_7227)
        
