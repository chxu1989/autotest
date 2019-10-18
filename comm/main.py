# encoding:utf-8

from MySQL import MySQL

if __name__ == '__main__':
    info = {'host': '192.168.90.23', 'port': '3306', 'user': 'root', 'password': 'cjgame',
            'database': 'sysinfo', 'charset': 'utf8'}
    ms = MySQL(**info)
    ms.connectDatabase()
    # sql = 'select id,mem,handles from 5wheelstar0926  order by id'
    # params = ['12162','105']
    # data=ms.fetchall(sql)

    cond_dict = {'IP': '1'}
    params1 = ['id', 'mem', 'handles']
    ret= ms.queryByFormatter(table_name='5wheelstar0926',cond_dict=cond_dict,col_field=params1,order='order by id')
    # ret = ms.queryByFormatter(table_name='5wheelstar0926',
    #                              cond_dict='handles > 1000',
    #                              col_field='id,mem,handles',
    #                              order='order by id')
    # ret = ms.queryByFormatter( table_name='5wheelstar0926', col_field=params1, order='order by id' )

    # field_list = ['IP', 'processname']
    # value_list = [['100.0', 'aaa'],['200.0', 'bbb']]
    # ret = ms.insertByFormatter(table_name='5wheelstar0926', field_list=field_list, value_list=value_list)

    # field_list = ['IP', 'processname']
    # value_list = [['10000000', 'jerry']]
    # con_dict = {'IP': '1', 'processname': '2'}
    # ret = ms.updateByFormatter(table_name='5wheelstar0926', field_list=field_list, value_list=value_list, cond_dict=con_dict)

    # con_dict = {'IP': '200.0', 'processname': 'bbb'}
    # ret = ms.deleteByFormatter(table_name='5wheelstar0926', cond_dict=con_dict)
    print(ret)
    ms.closeDatabase()
