# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
import configparser
import cx_Oracle

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('conf/options.config')
    print config.items()
    db = cx_Oracle.connect('trade_hhj', 'huhuijun01', '192.168.121.15:1521/myldb')
    print db.version
    cursor = db.cursor()
    cursor.execute("SELECT * FROM JY_CPCNRESPONSERELATION ORDER BY ROWID")
    rows = cursor.fetchall()
    for i in rows:
        print i
