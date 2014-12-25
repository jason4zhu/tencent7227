# encoding: utf-8
import subprocess

from loggingMngr import logger


######################################
#
# Function: shellCall()
#
######################################
def shellCall(cmd):
    process = subprocess.Popen(cmd, \
                           shell=True, \
                           stdout=subprocess.PIPE, \
                           stderr=subprocess.PIPE)
    out, err = process.communicate()   
    logger.info("output from shell:\n^---------\n"+out+"\n"+err+"\n$---------")
    

if __name__ == "__main__":
    shellCall("source ../test.sh \\'1\\',\\'2\\'")





