# encoding: utf-8
#!/usr/bin/env python2.6
# vim: set ts=4 sw=4 expandtab background=dark :

import sys
import os
import traceback
import statusMngr
from loggingMngr import logger
import time

output_path = "/home/data/ftp/tencent/task_7227"


def task7227(cfg, datafile, caid):
    print("cfg=["+str(cfg)+"], datafile=["+str(datafile)+"], caid=["+str(caid)+"]")
    try:
        # get config
        config = {}
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
        for line in open(cfg):
            if line.startswith("#"):
                continue
            (spid, gid, pid, mid) = line.rstrip().split()
            config[spid] = (spid, gid, pid, mid)
        
        output = {}
        validLineCount = 0
        for line in open(datafile, 'r'):
            if not line.strip():
                continue
            #line = line.rstrip().replace(" ", ",")
            #date p m6 m2 m5 ip type
            cols = line.rstrip().split("^")
            file = ''
            result = []
            if cols[-1] == "imp":
                file = "mz-views-%s-%s" % (caid, cols[0])
            elif cols[-1] == "clk":
                file = "mz-clicks-%s-%s" % (caid, cols[0])
            else:
                continue
            try:
                if os.path.exists(os.path.join(output_path, "%s.tar.gz" % file)):
                    os.remove(os.path.join(output_path, "%s.tar.gz" % file))
            except Exception as e:
                print(str(e))
                print("outpath=["+output_path+"], file=["+file+"]")
            if not output.has_key(file):
                output[file] = open(os.path.join(output_path, file), 'w')
    
            (spid, gid, pid, mid) = config[cols[1]]
            imei_ifa = ""
            if cols[3] and cols[3] != 'NULL':
                imei_ifa = cols[3]
            else:
                imei_ifa = cols[4]
            result.append(cols[0]) # date
            result.append(gid) # gameid
            result.append(pid) # platform id
            result.append(mid) # media id
            result.append(cols[2]) # MAC
            result.append(imei_ifa) # IMEI/IFA
            result.append(cols[-2]) # ip
    
            #print file, result
            print >> output[file], ",".join(result)
            validLineCount += 1
        logger.info("Generating ["+str(len(output.keys()))+"] file(s), namely ["+str(output.keys())+"]. ["+str(validLineCount)+"] lines have been processed.")
        
        for file in output.keys():
            output[file].close()
        
        for file in output.keys():
            path = os.path.join(output_path, file)
            cmd = "rm %s.tar.gz" % path
            os.system(cmd)
    
            cmd = "tar czf %s.tar.gz %s" % (path, path)
            os.system(cmd)
            time.sleep(10)
            cmd = "rm %s" % path
            os.system(cmd)
            os.system("ssh supertool@d15.mzhen.cn \"mkdir -p /home/data/ftp/tencent/task_7227/%s\"" % (caid,))
            os.system("rsync -azP --bwlimit=5120 %s.tar.gz supertool@d15.mzhen.cn:/home/data/ftp/tencent/task_7227/%s" % (path,caid,))
        
        os.system("rm -rf "+output_path)
        
        logger.info("task7227 is done.")
        return statusMngr.STATUS_SUCCEED
    except Exception as e:
        logger.error("When executing task7227.py. errMsg=["+str(e)+"], traceback=[\n"+str(traceback.format_exc())+"]")
        return statusMngr.STATUS_FAIL_TASK_7227
        

if __name__ == '__main__':
    rtn = task7227("task7227.cfg", "tencentHive.output", 'ccc')

