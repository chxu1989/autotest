#encoding:utf-8
"""
@author = Monika
@create = 2019/9/29 17:27
"""
import os
class PubFunctions:

	def getFolderPath(self,path=None):
		"""
		获取文件夹路径
		:param path: 文件夹路径，为None时，返回当前文件夹路径
		:return: str类型，文件夹路径
		"""
		if path:
			return os.path.split( path )[0]
		else:
			return os.getcwd()

	def getFilePath(self,path=None, name=None):
		"""
		获取文件绝对路径，通过name进行模糊查询，返回结果list
		:param path:文件夹路径，eg:   D:\\CX\\test11,当path为None时，默认为当前路径
		:param name:模糊查找文件或者文件夹名字中包含的字符串条件，，eg: '.txt'
		:return:查找到匹配文件的绝对路径的list，eg：['D:\\CX\\test11\\MoriDice_V1.0.0C_TCode1334_20190812_SN.txt'，
		D:\\CX\\test11\\test.txt']
		"""

		try:
			if path and name:
				file_list=[os.path.join(path,file) for file in os.listdir(path)]    #获取path下的所有文件的绝对路径
				search_result=[i for i in file_list if i.find( name ) != -1]   # 通过name模糊查询list并返回结果
				#print(path,'1',search_result)
				return search_result
	
			elif path is None and name:
				file_list=[os.path.join(os.getcwd(),file) for file in os.listdir()]#获取当前路径下所有文件的绝对路径
				search_result=[i for i in file_list if i.find( name ) != -1]   #通过name模糊查询list并返回结果
				#print( path, '2', search_result )
				return search_result
	
			else:
				print('调用方法缺少参数name！')
		except Exception as e:
			print(f'当前路径匹配不到{name}文件')
			pass


if __name__=='__main__':
	pf=PubFunctions()
	pf.getFilePath(name='.txt')
	pf.getFilePath(name='.rar')
	#pf.getFilePath(  )
