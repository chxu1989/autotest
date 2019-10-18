#encoding:utf-8
"""
@author = Monika
@create = 2019/9/2 &{TIME}
"""

import mysql.connector
from comm.OperatFile import ReadFile
import re

class MyDB:


	# 创建数据库连接
	def conne(self):
		rf=ReadFile()
		dbinfo = rf.readini( 'dbconfig' )
		self.tablename = rf.readini( 'gameinfo' )['gamename']
		try:
			self.conn=mysql.connector.connect(**dbinfo)
			self.cursor=None
			print( '\tSuccessful connection to MySQL DB！')
		except Exception as err:
			print( 'DB connection error：%s!'% err )

	# 获取数据库游标对象cursor
	def getcursor(self):

		# 建立连接
		self.conne()
		if self.cursor is None:
			self.cursor = self.conn.cursor()




	# 关闭连接
	def closeConn(self):

		# 关闭游标对象，关闭连接
		if self.cursor is not None:
			self.cursor.close()
		self.conn.close()

	def createtable(self):
		try:
			# 执行sql语句
			self.cursor.execute( "CREATE TABLE if not exists %s "
						 "(id int(11) auto_increment PRIMARY KEY, IP VARCHAR(50),processname VARCHAR(50),"
						 "datetime VARCHAR(100),mem VARCHAR(20),sysmem VARCHAR(100),cpu VARCHAR(20),"
						 "syscpu VARCHAR(100),handles VARCHAR(20),remark VARCHAR(20))" % self.tablename )
		except Exception as e:
			print( '创建表格失败：%s'% e )
			self.conn.rollback()
			pass


	def table_exists(self,tablename):
		tables=self.cursor.execute('show tables;')
		table_list = re.findall( '(\'.*?\')', str( tables ) )
		table_list = [re.sub( "'", '', each ) for each in table_list]
		if tablename in table_list:
			return 1
		else:
			return 0

	#插入操作
	def insert(self,tablename,**kwargs):

		fields = ','.join( '`' + str( k ) + '`' for k in kwargs["data"].keys() )
		values = ','.join( '"' + str( v ) + '"' for v in kwargs["data"].values() )
		sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (tablename, fields, values)

		try:
			self.cursor.execute( sql )
			insert_id = self.cursor.lastrowid
			self.conn.commit()
			#print(f'\t3.Successful to insert system parameter information in table{self.tablename}!')
			return insert_id
		except Exception as e:
			#print( 'Insertion data failed:%s'% e )
			self.conn.rollback()

	#更新操作
	def update(self,tablename,**kwargs):
		fields = ','.join( '`' + str( k ) + '`' for k in kwargs['data'].keys())
		values = ','.join( '"' + str( v ) + '"' for v in kwargs['data'].values())
		pass

	# 查询操作
	def query(self, sql):

		# 执行sql语句
		self.cursor.execute( sql )

		# 获取执行结果
		datalist = self.cursor.fetchall()

		# 关闭
		self.closeConn( self.cursor )

		return datalist