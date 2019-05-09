# 分析一份影评，

参照文件：https://blog.csdn.net/lovecluo/article/details/84561706

# sqlite3的用法
	> 创建,建库，建表
		建库： sqlite3 databasaeName.db
		建表: create table database_name.table_name(
				fields_1 datatype primary key,
				fields_2 datatype,
			)
	> 数据类型
		null, integer, real, text, blob
	> 链接库
	> 插入数据、查询、修改、删除
	> 级联、存储、优化、分片、负载
	> 语法
		 SELECT、INSERT、UPDATE、DELETE、ALTER、DROP
		 ATTACH, BEGIN TRANSACTION, AND\OR, CREATE
		 COMMIT, COUNT, DETACH, DISTINCT,EXISTS,
		 EXPLAIN, GLOB, GROUP BY, HAVING,IN,LIKE
		 ORDER BY, PRAGMA,RELEASE, REINDEX, ROLLBACK,
		 SAVEPOINT,WHERE, VACUUM
	> 特点
		支持事务
	> id自增 (autoincrement)
		`
		cursor.execute('CREATE TABLE foo (
			id integer primary key autoincrement ,
            username varchar(50),
            password varchar(50))')
		`
# 图表

# python 模块
	1，import sqlite3
	2, import json
	3, import requests
		http://docs.python-requests.org/zh_CN/latest/user/advanced.html