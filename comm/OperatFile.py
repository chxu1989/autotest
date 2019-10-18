#encoding:utf-8
"""
@author = Monika
@create = 2019/9/2
"""

import configparser
import sys
import os
from comm.PubFunctions import PubFunctions


class ReadFile():

	def readini(self,tagname):
		'''
		根据tagname读取固定路径的ini文件，返回字典
		:param tagname:ini文件中的标签名，eg[gameinfo]
		:return:字典，eg｛'host': '192.168.90.23','port': '3306'}
		'''
		try:
			
			config = configparser.ConfigParser()
			config.read(os.path.split(sys.argv[0])[0] + "/config.ini")
			#print(config.items(tagname))

			dict1={v[0]:v[1] for v in config.items(tagname) if v}
			#print( dict1 )
			return dict1
		except Exception as e:
			print('读取配置文件失败，请检查文件路径和配置：%s' % e)
			return None

	def readtxt(self,path,name='.txt'):
		"""
		1.输入路径，读取路径下的文件；
		2.未输入路径，读取当前路径下的所有.txt文件：
		  （1）如果前路径下只有1个,则返回文件内容的list
		  （2）如果前路径下有多个,则返回文件名的list
		:param path: 绝对路径,默认为空，eg.'D:\\CX\\test11'
		:param name: 默认'.txt'
		:return: list
		"""

		pf=PubFunctions()
		file_list=pf.getFilePath(path,name)#查找当前路径下名包含.txt的所有文件名
		if len(file_list)==1:
			with open(file_list[0]) as f:
				content=f.readlines() #读取txt文件所有内容，每一行做为一个元素写入list
				f.close()
				return content
		elif file_list:
			print(f'当前路径下，找不到txt文件')
		else:
			return file_list


if __name__=='__main__':
	rf=ReadFile()
	print(rf.readini('dbconfig'))
