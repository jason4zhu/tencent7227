#!/bin/sh

source /home/data12/supertool/yuchangliang/task7227/funcs.udf



taskid=7227
caid=$1
SPID_LIST=$2
starttime=$3
endtime=$4
hiveResultFileName=$5

hive -e "
$udf_define
set ca-meta=$caid;
set mapred.job.name=zhudi_tencent_task7227;
use logbase_db;

FROM(
FROM(
FROM logbase
    SELECT row_to_map(doc) AS row,dateid
    WHERE dateid >= $starttime AND dateid <=$endtime

)tmp
    SELECT row['plt'] plt,
        row['k'] caid,
        b10_to_b62(row['p']) spid,
        row['m6'] m6,
        row['m2'] m2,
        row['m5'] m5,
        row['tp'] tp,
        row['ip'] ip,
        row['uuid'] uuid,
        dateid
     WHERE row['p'] is not null
)tmp
    SELECT
        dateid,
        spid,
        m6,
        m2,
        m5,
        ip,
        tp
    WHERE
        spid IN ($SPID_LIST);


" | awk '{gsub(/\t/,"^",$0);print $0}' > $hiveResultFileName
