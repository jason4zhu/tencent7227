# encoding: utf-8
import os
import logging
import thread
import datetime
import logging.handlers


# main logger
global logger

LogPath="./logs"
if not os.path.exists(LogPath):
    os.makedirs(LogPath)
curDate = (datetime.datetime.now()).strftime("%Y-%m-%d")

def setup_logger(logger_name, log_file_name, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(name)s %(asctime)s:[%(levelname)s]\t%(message)s')
    fileHandler = logging.FileHandler(LogPath+"/"+str(log_file_name)+"_"+str(curDate)+'.log', mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)  

    return logging.getLogger(logger_name)

logger = setup_logger('main', r'main')


# global logger
# 
# LogPath="./logs"
# if not os.path.exists(LogPath):
#     os.makedirs(LogPath)
# curDate = (datetime.datetime.now()).strftime("%Y-%m-%d")
# logging.basicConfig(filename=LogPath+"/main_"+curDate+'.log',
#                     filemode='a',
#                     format='%(name)s %(asctime)s:[%(levelname)s]\t%(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     level=logging.INFO)
# logger = logging.getLogger(os.path.split(os.path.abspath(__file__))[1])
# 
# # 根据当前thread_id返回对应的logger
# def InitLog(thread_id,logger):
#     LogPath="./logs"
#     if not os.path.exists(LogPath):
#         os.makedirs(LogPath)
#     curDate = (datetime.datetime.now()).strftime("%Y-%m-%d")
# 
#     LOG_FILENAME = LogPath+"/main_"+curDate+"_"+str(thread_id)+'.log'
#     handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,mode='a',maxBytes=10*1024*1024,backupCount=5)
#     #handler = logging.FileHandler(LOG_FILENAME)
#     formatter = logging.Formatter("[ %(asctime)s ][ %(levelname)s ] %(message)s\n")
#     handler.setFormatter(formatter)
#     #logger = logging.getLogger()
#     logger.addHandler(handler)
#     return logger
