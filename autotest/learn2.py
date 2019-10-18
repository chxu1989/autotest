# -*- coding: utf-8 -*-

"""
@author = Monika
@create = 2019/8/5 &{TIME}
"""
import urllib.request,json
import schedule,time,random
import re,os
from urllib import request,parse

class dingding():

	def excute11(self):
		print( "I'm working....." )
		schedule.every().thursday.at('10:00').do(self.test3)
		schedule.every().friday.at( '10:00' ).do( self.test3 )
		while True:
			schedule.run_pending()
			time.sleep(1)



	def test3(self):

		url1='https://oapi.dingtalk.com/robot/send?access_token=3f8f31074adce540264fd4ffba049c577026ebfa618f5118b4aeba4962ce0b59'
		headers1={
			'Content-type': 'application/json;charset=UTF-8',
			"Cache-Control": "no-cache",
			"Connection": "Keep-Alive",}

		text=['记录机房日志啦','同学，赶紧记录机房日志','帅哥，靓女，看过来，快看看我的名字']
		nums=['13727025907','15970923025','13612231020']
		tt=random.choice(text)
		am=random.choice(nums)
		json1={"msgtype": "text","text": {"content": tt},"at": {"atMobiles": [am],"isAtAll": 'false'}}
		data1=json.dumps(json1)
		data1=bytes(data1,'utf8')
		req=urllib.request.Request(url=url1,data=data1,headers=headers1,method='POST')
		urllib.request.urlopen(req)
		#print(r.read())

def test1():
	'''
	sub(pattern, repl, string, count=0, flags=0)

	pattern为正则表达式，repl为替换的文本，string是被匹配的文本，count是替换次数，缺省为0，表示全部替换，flag是匹配规则，如是否区别大小写等，可省略。

	subn返回的结果是一个元组（替换后的字符串，替换次数）。

	sub仅返回替换后的字符串。
	:return:
	'''
	myBlogP = r'<div style="FONT-WEIGHT: bold">我的相关日志：</div>'
	subP = re.compile(myBlogP, re.I | re.S)
	print(f'sub={subP}')
	contentUni = subP.sub('bold', 'aa')
	print(contentUni)
def test2(value_list):
	# print(f'http://api.test.com.cn{url}')
	# print('http://'+'api.test.com.cn'+url)
	# print(str(int(time.time())))
	url = 'http://www.baidu.com/'
	headers = {
		'User-Agent': 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)',
		'Host': 'httpbin.org'
	}  # 定义头信

	#dict = {'name': 'germey'}
	#data = bytes( parse.urlencode( dict ), encoding='utf-8' )
	req = request.Request( url=url, data=None, headers=headers, method='GET' )
	# req.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 8.4; Windows NT') #也可以request的方法来添加
	response = request.urlopen( req )
	print( response.read() )
	for value in value_list:
		values = '('+ ','.join( i for i in value ) + ')'
		#for i in range(0,len(value_list)):
		

def test3():
	a = ['%'for i in range(10) if i >3]
	print(a)
	
	
test3()
# if __name__=='__main__':
# 	a=dingding()
# 	a.excute11()
# 	#a.test3()



