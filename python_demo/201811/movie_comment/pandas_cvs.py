#!/usr/bin/python3

# 从sqlite3中获取数据并保存未 cvs文件

import sqlite3
import pandas
from sqlalchemy import create_engine

#sqlite3数据库中的tableName表,导出到csvDstPath为.csv格式,提供表名和目的路径
    # echo = True ，会显示在加载数据库所执行的SQL语句。
# engine = create_engine(r'sqlite:///'+'./movieComment.db', echo=True)
# table = pandas.read_sql_table(table_name= 'comment', con=engine)
# table.to_csv('./movie.csv')

# import pandas
#csv导入到sqlite中,提供路径和表名
def csv2sqlite(self, csvPath, csvTableName):
    df = pandas.read_csv(csvPath)
    df.to_sql(csvTableName, self.conn, if_exists='append', index=False)

#sqlite3数据库中的tableName表,导出到csvDstPath为.csv格式,提供表名和目的路径
def sqlite2csv(self,tableName, csvDstPath):
    # echo = True ，会显示在加载数据库所执行的SQL语句。
    engine = create_engine(r'sqlite:///'+dbPath, echo=True)
    table = pandas.read_sql_table(table_name= tableName, con=engine)
    table.to_csv(csvDstPath)
