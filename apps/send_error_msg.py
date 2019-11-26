# -*- encoding=utf-8 -*-
import requests
import os

"""
报警配置模板
"""
host_url="https://oapi.dingtalk.com/robot/send?access_token=0bc7fc7e022504edde7171dcdcdf9d02bd113d34339ee05cc0d2e04a3dace2c6"
text="爬虫错误日志"
url=host_url+text



# 检查是否出现error日志，若出现则钉钉报警出来~

# 先找到最新的error日志文件名
cmd1 = "ls /root/nanodata_crawling/logs/error/ -l | grep error | tail -n 1 | awk '{print $9}'"
res1 = os.popen(cmd1)
res1_1=res1.read()

cmd2="tail /root/nanodata_crawling/logs/%s" %res1_1
res2=os.popen(cmd2)
res2_1=res2.read()



# 如果有错误日志就报警出来
if len(res2_1)>0:
    # 发送钉钉报警
    content=requests.get(url).text


res1.close()
res2.close()
