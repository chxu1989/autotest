# encoding:utf-8
"""
@author = Monika
@create = 2019/10/12 13:25
"""
import mysql.connector
import Const
from comm import Const
import Define
import Logger

Const.CONNECT_SUCCESS = 0
Const.ERROR_CONNECT_FAIL = -1000            #数据库连接失败
Const.ERROR_INPUT_PARAMTER = -1001          #输入参数错误

class MySQL:

    def __init__(self, host, user, password, database, port=3306, charset='utf8'):
        '''
        初始化参数
        :param host: 主机
        :param user: 用户名
        :param password: 密码
        :param database: 数据库
        :param port: 端口号，默认是3306
        :param charset: 编码，默认是utf8
        '''
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password
        self.__charset = charset
        self.__conn = None
        self.__cur = None
        self.__logger = Logger.LoggerMgr(Define.Const.LOG_LEVEL)

    def __checkConnected(self):
        if self.__conn is None:
            self.__logger.info('Database not connect!')
            return False
        else:
            return True

    def connectDatabase(self):
        '''
        获取连接对象和执行对象
        :return: 无
        '''
        try:
            self.__conn = mysql.connector.connect(host=self.__host,
                                                user=self.__user,
                                                password=self.__password,
                                                database=self.__database,
                                                port=self.__port,
                                                charset=self.__charset)
            self.__cur = self.__conn.cursor()
        except Exception as ex:
            print(ex)

    def __fetchone(self, sql, params=None):
        '''
        根据sql和参数获取多行数据
        :param sql: sql语句
        :param params: sql语句对象的参数元组，默认值为None
        :return: 查询的多行数据
        '''
        ret = None
        try:
            count = self.__cur.execute(sql, params)
            ret = self.__cur.fetchone()
            if count is None or count == 0:
                self.__logger.info(f'Result is empty!')
                ret = None
        except Exception as ex:
            print(ex)

        return ret

    def __fetchall(self, sql, params=None):
        '''
        根据sql和参数获取数据
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 查询的一行数据
        '''
        ret = None
        try:
            count = self.__cur.execute(sql, params)
            ret = self.__cur.fetchall()
            if count is None or count == 0:
                self.__logger.info(f'Result is empty!')
                ret = None
        except Exception as ex:
            print(ex)

        return ret

    def queryByFormatter(self, table_name, cond_dict='', col_field='*', order=''):
        """
        example：
        Mysql.queryByFormatter（table）
        Mysql.queryByFormatter（table, col_field=['ID','name']）
        Mysql.queryByFormatter（table, con_dict={'id':1,'name':'sam'}, col_field=['ID','name']）
        Mysql.queryByFormatter（table, con_dict='id >1000 and name like '*xiao'', col_field='ID,name'
        Mysql.queryByFormatter（table, col_field=['ID','name'], order='order by id DESC'）
        Mysql.queryByFormatter（table, con_dict={'id':1,'name':'sam'}, col_field=['ID','name'], order='order by id DESC'）#此情况下
        order参数无效，可以理解为order=''
        
        args:
        :param table_name:表名
        :param cond_dict:查询条件，dict格式
        :param col_field: 显示的查询字段
        :param order: 排序条件
        :return: 查询结果，查询不到结果返回None,eg.[(6692, '108.00M', '324'), (6741, '108.00M', '324')}
        """

        ret = None
        query_cond = ''
        sql = ''

        if not self.__checkConnected():
            return Const.ERROR_CONNECT_FAIL

        if cond_dict != '':
            if isinstance(cond_dict, dict):
                for k, v in cond_dict.items():
                    if isinstance(v, str):
                        query_cond = query_cond + k + '=' + "'" + v + "'" + ' and '
                    else:
                        query_cond = query_cond + k + '=' + str(v) + ' and '
                query_cond = f'WHERE {query_cond}1=1 '
            elif isinstance(cond_dict, str):
                query_cond = f'WHERE {cond_dict} 1=1 '
            else:
                self.__logger.info('param type error, it must be dict or str!')
                return Const.ERROR_INPUT_PARAMTER

        if isinstance(col_field, list):
            sql = f'SELECT {",".join(col_field)} FROM {table_name} '
        elif isinstance(col_field, str):
            if col_field == '*':
                sql = f'SELECT * FROM {table_name} '
            else:
                sql = f'SELECT {col_field} FROM {table_name} '
        else:
            self.__logger.info('param type error, it must be list or str!')
            return Const.ERROR_INPUT_PARAMTER

        sql = sql + query_cond + order
        self.__logger.info(sql)

        try:
            count = self.__cur.execute(sql)
            ret = self.__cur.fetchall()
            if count == 0:
                self.__logger.info(f'{table_name} table is empty!')
                ret = None
        except Exception as ex:
            self.__logger.info(f'MySQL execute failed! Error:{ex}')

        return ret

    def __commitItem(self, sql, params=None):
        '''
        执行增删改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        '''
        ret = 0
        if not self.__checkConnected():
            return Const.ERROR_CONNECT_FAIL

        self.__logger.info(sql)
        try:
            if params is None:
                ret = self.__cur.execute(sql)
            else:
                ret = self.__cur.executemany(sql, params)
            self.__conn.commit()
        except Exception as ex:
            self.__logger.info(f'MySQL execute failed! Error:{ex}')
            self.__conn.rollback()

        return ret

    def updateBySql(self, sql, params=None):
        '''
        执行修改
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        '''
        return self.__commitItem(sql, params)

    def updateByFormatter(self, table_name, field_list, value_list, cond_dict=''):
        """
        example：
        field_list=['id','name']
        value_list=['ligang','xiaoming']
        con_dict={'id':1,'name':'sam'}
        MySQL.updateByFormatter(table,field_list,value_list,con_dict)

        args:
        :param table_name: 表名
        :param field_list: 字段名
        :param value_list: 值
        :param cond_dict:查询条件，dict格式
        :return: 影响行数
        """
        ret = 0
        if not self.__checkConnected():
            return Const.ERROR_CONNECT_FAIL

        if not isinstance(field_list, list) or not isinstance(value_list, list):
            return Const.ERROR_INPUT_PARAMTER

        if len(field_list) == 0 and len(field_list) != len(value_list):
            return Const.ERROR_INPUT_PARAMTER

        fields = ''
        query_cond = ''
        for i in range(0, len(field_list)):
            fields = fields + field_list[i] + '=%s'
            if i != len(field_list) - 1:
                fields += ','

        if cond_dict != '':
            if isinstance(cond_dict, dict):
                for k, v in cond_dict.items():
                    if isinstance(v, str):
                        query_cond = query_cond + k + '=' + "'" + v + "'" + ' and '
                    else:
                        query_cond = query_cond + k + '=' + str(v) + ' and '

                query_cond = f'WHERE {query_cond}1=1'
            elif isinstance(cond_dict, str):
                query_cond = f'WHERE {cond_dict} 1=1'
            else:
                self.__logger.info('param type error, it must be dict or str!')
                return Const.ERROR_INPUT_PARAMTER

        sql = 'UPDATE %s SET %s %s' % (table_name, fields, query_cond)
        ret = self.__commitItem(sql, value_list)
        return ret

    def insertBySql(self, sql, params=None):
        '''
        执行新增
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        '''
        return self.__commitItem(sql, params)

    def insertByFormatter(self, table_name, field_list, value_list):
        """
        example：
        field_list=['id','name']
        value_list=[[1,2],['ligang','xiaoming']]
        MySQL.insertByFormatter(table,field_list,value_list)
        
        args:
        :param table_name: 表名
        :param field_list: 字段名
        :param value_list: 值
        :return: 影响行数
        """
        ret = 0
        if not self.__checkConnected():
            return Const.ERROR_CONNECT_FAIL

        if not isinstance(field_list, list) or not isinstance(value_list, list):
            return Const.ERROR_INPUT_PARAMTER

        if len(field_list) == 0 and len(field_list) != len(value_list):
            return Const.ERROR_INPUT_PARAMTER

        param = []
        fields = '(' + ','.join(str(k) for k in field_list) + ')'
        for i in range(0, len(value_list)):
            param.append(value_list[i])
        values = '%s,' * (len(value_list) - 1) + '%s'
        sql = 'INSERT INTO %s %s VALUES(%s)' % (table_name, fields, values)
        ret = self.__commitItem(sql, param)
        return ret

    def deleteBySql(self, sql, params=None):
        '''
        执行删除
        :param sql: sql语句
        :param params: sql语句对象的参数列表，默认值为None
        :return: 受影响的行数
        '''
        return self.__commitItem(sql, params)

    def deleteByFormatter(self, table_name, cond_dict=''):
        """
        example：
        con_dict={'id':1,'name':'sam'}
        MySQL.queryByFormatter(table, con_dict)

        args:
        :param table_name: 表名
        :param cond_dict:查询条件，dict格式
        :return: 影响行数
        """
        ret = 0
        if not self.__checkConnected():
            return Const.ERROR_CONNECT_FAIL

        query_cond = ''
        if cond_dict != '':
            if isinstance(cond_dict, dict):
                for k, v in cond_dict.items():
                    if isinstance(v, str):
                        query_cond = query_cond + k + '=' + "'" + v + "'" + ' and '
                    else:
                        query_cond = query_cond + k + '=' + str(v) + ' and '
                query_cond = f'WHERE {query_cond}1=1'
            elif isinstance(cond_dict, str):
                query_cond = f'WHERE {cond_dict} 1=1'
            else:
                self.__logger.info('param type error, it must be dict or str!')
                return Const.ERROR_INPUT_PARAMTER

        sql = 'DELETE FROM %s %s' % (table_name, query_cond)
        ret = self.__commitItem(sql)
        return ret

    def closeDatabase(self):
        '''
        关闭执行工具和连接对象
        '''
        if self.__cur is not None:
            self.__cur.close()
        if self.__conn is not None:
            self.__conn.close()

