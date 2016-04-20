#!/usr/bin/python2.6
#coding:utf-8
from pyleus.storm import SimpleBolt
import os,re,time
import logging
import MySQLdb
log = logging.getLogger('squid_rate')
class LogSquidBolt(SimpleBolt):
    def process_tuple(self, tup):
        if 'PURGE' in tup.values[0] or 'favicon.ico' in tup.values[0]:
            pass
        else:
            string_line = tup.values[0].strip()
            string_line = string_line.split()
            if '200' in string_line[8] or  '301' in string_line[8]:
                status=string_line[8].split('/')[0].strip()
                url_param=string_line[11].strip().split('/')
                yuming=url_param[2].strip()
                if "HIT" in status:
                    code_hit=1
                    code_miss=0
                elif "MISS" in status:
                    code_miss=1
                    code_hit=0
                else:
                    code_hit=0
                    code_miss=1
                if len(url_param) >= 5:
                    url=url_param[3].strip()
                else:
                    url="index"
                now=int(time.time())
                nowmin=now-now%60
                con=MySQLdb.connect(user='root',db='squid',passwd='yhd@123',host='10.4.225.152',charset='utf8')
                cur=con.cursor()
                insertformat="insert into squid_info(time,hit,miss,yuming,url) values(%d,%d,%d,'%s','%s');"
                insertvalue=(nowmin,code_hit,code_miss,yuming,url)
                insertcmd= insertformat % insertvalue
                cur.execute(insertcmd)
                log.debug(nowmin,insertcmd)
            else:
                pass
if __name__ == '__main__':
    if __name__ == '__main__':
            logging.basicConfig(
                level=logging.INFO,
                filename='/tmp/squid_results.log',
                format="%(message)s",
                filemode='a',
                )
            LogSquidBolt().run()


