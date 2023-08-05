
# -*- coding:UTF-8 -*-
r"""
author: boxueliu
version: 0.1.0
description: airflow analysis sql and create file
"""
import datetime
import os
import cx_Oracle
import traceback2 as traceback
import MySQLdb


class AirflowUtil:

    def __init__(self):
        self.flag = ''

    def flag_creat(self, **kwargs):
        file_path = kwargs['file_path']
        file_suffix = datetime.datetime.now().strftime('%Y%m%d')
        r"""
         cbb system to create success file flag
        :param file_path:
        :return:
        """
        flag_name = 'interface_' + file_suffix + '.flag'
        with open(os.path.join(file_path, flag_name), 'w') as file:
            file.write('')

    def get_cut_time(self, system_type, taskid, conn):
        r"""
        get daily cut time by taskid
        :param taskid:
        :param conn:
        :return:
        """
        try:
            if conn == '':
                return '1900-01-01 10:00:00', '2099-12-12 10:00:00'
            else:
                connnection = cx_Oracle.connect(conn)
                cursor = connnection.cursor()
                sql = "SELECT TO_CHAR(LAST_FIN_DAILY_DATE,'YYYY-MM-DD HH24:MI:SS')," \
                      "TO_CHAR(THIS_FIN_DAILY_DATE,'YYYY-MM-DD HH24:MI:SS') " \
                      "FROM K_ODS.FIN_DAILY_TABLE   WHERE SYSTEM_ID = '%s'  AND TASK_ID = '%s'   AND EFF_FLAG = '1'" \
                      % (str(system_type), str(taskid))
                cursor.execute(sql)
                connnection.commit()
                data = cursor.fetchall()
                return data[0][0], data[0][1]
        except Exception as e:
            print(e)

    # def spool_csv(self, **kwargs):
    def spool_csv(self, spool_path,data_path,data_type,sql_name,conn,daily_conn,system_type,database,ods_conn):
        r"""
        to analysis sql file and create csv file to export data
        :param kwargs:
        :return: csv file
        dataype must be attentionai
        SAP,RTL,ODSB,ODSB_CBB,WHS,CFL
        """
        # spool_path = kwargs['spool_path']
        # data_path = kwargs['data_path']
        # data_type = kwargs['data_type']
        # sql_name = kwargs['sql_name']
        # conn = kwargs['conn']
        # daily_conn = kwargs['daily_conn']
        # system_type = kwargs['system_type']
        # database = kwargs['database']
        # if kwargs['ods_conn']:
        #     ods_conn = kwargs['ods_conn']
        # else:
        #     ods_conn = ''
        """
            get daily time
        """
        if database == 'MYSQL':
            connect = self.mysql_connect(conn)
        else:
            connect = cx_Oracle.connect(conn, encoding='gb18030')
        daily_start_time = ''
        daily_end_time = ''
        if data_type == 'ODSB_CBB':
            pass
        else:
            daily_start_time, daily_end_time = self.get_cut_time(system_type, data_type, daily_conn)
        cursor = connect.cursor()

        """     
            to analysis sql
        """
        for file_ in os.listdir(spool_path):
            data_from = 0
            data_to = 0
            try:
                if file_ == sql_name:
                    print(spool_path+sql_name)
                    sql_dic = self.sql_parse(spool_path+sql_name)
                    sql_ = sql_dic['sql']
                    file_name = sql_dic['file'].replace('\n', '')
                    print(file_name)

                    if sql_.find('&2') != -1:
                        sql_ = sql_.replace('&2', daily_start_time)
                    if sql_.find('&3') != -1:
                        sql_ = sql_.replace('&3', daily_end_time)

                    print(sql_)
                    if database != 'MYSQL':
                        sql_ = sql_.replace(';', '')
                    try:
                        cursor.execute(sql_)
                    except Exception as ee:
                        print(ee)

                    if data_type == "ODSB_CBB":
                        with open(os.path.join(data_path, file_name), 'w', encoding='utf8') as f:
                            while True:
                                data = cursor.fetchmany(1000)
                                data_from += len(data)
                                if data:
                                    for x in data:
                                        f.write(x[0])
                                        f.write('\n')
                                        data_to += 1
                                else:
                                    break
                    else:
                        with open(os.path.join(data_path, file_name), 'w', encoding='gb18030') as f:
                            while True:
                                data = cursor.fetchmany(1000)
                                data_from += len(data)
                                if data:
                                    for x in data:
                                        f.write(str(x[0]))
                                        f.write('\n')
                                        data_to += 1
                                else:
                                    break
                        cursor.close()
                    print('==========从上游抽数该表 ' + file_name[:file_name.find('.csv')] + ' 获得数据为：' + str(data_from) + ' 条 ===============')
                    print('==========落成文件 ' + file_name + ' 的数据条数：' + str(data_to) + ' 条 =================')

                    sql_retail = "SELECT COUNT(1) FROM "
                    if file_name.find('ARCH') >= 0:
                        schema = 'DMT_ADMIN'
                    elif file_name.find('ODSB') >= 0:
                        schema = 'ODSB_ADMIN'
                    else:
                        schema = 'K_ODS'

                    sql = sql_retail + schema+'.'+file_name[:file_name.find('.csv')]
                    data_list = []
                    try:
                        ods_cursor = cx_Oracle.connect(ods_conn).cursor()
                        ods_cursor.execute(sql)
                        data_list = ods_cursor.fetchall()
                    except Exception as e:
                        print(e)
                    summary = 0
                    if data_list:
                        summary = data_list[0][0]

                    print('==============导入ods查询该表有 '+str(summary) + ' 条====================')

            except Exception as e:
                raise RuntimeError(e)

    def mysql_connect(self, conn):
        r"""
        mysql connect
        :param conn:
        :retur'ODSB_ADMIN/admin@10.20.201.99/DDMUATDB'n:
        """
        user = conn[:str(conn).find('/')]
        pwd = conn[str(conn).find('/')+1:str(conn).find('@')]

        if conn.find(':') >= 0:
            host = conn[str(conn).find('@')+1:str(conn).find(':')]
            port = int(conn[str(conn).find(':')+1:str(conn).rfind('/')])
        else:
            host = conn[str(conn).find('@')+1:str(conn).rfind('/')]
            port = 3306
        db = conn[str(conn).rfind('/')+1:]
        conn = MySQLdb.connect(host, user, pwd, db, port, charset='utf8')
        return conn

    def sql_parse(self, file_name):
        r"""
        解析sql
        :param file_name:
        :return:
        """
        _file = 0
        _sql = 0
        _file_str = ''
        _sql_str = ''

        with open(file_name, 'r') as fp:
            for line in fp:
                if line.strip().find('file:') == 0:
                    _file = 1
                    _sql = 0
                elif line.strip().find('sql:') == 0:
                    _sql = 1
                    _file = 0
                elif _file == 1:
                    _file_str = line
                elif _sql == 1:
                    _sql_str += line
        return {"file": _file_str, "sql": _sql_str}

if __name__ == '__main__':
    # def spool_csv(self, spool_path,data_path,data_type,sql_name,conn,daily_conn,system_type,database,ods_conn):
    #
    # op_kwargs = {'spool_path':'/Users/liuboxue/Documents/workspace/DWH_AIRFLOW_ODS_SQL/RETAIL/RTL/',
    #              'data_path':  '/Users/liuboxue/Documents/workspace/DWH_AIRFLOW_ODS_SQL/RETAIL/RTL/',
    #              'system_type': 'RTL',
    #              'data_type': 'RTL1',
    #              'sql_name': 'arch_city.sql',
    #              'conn': 'DMT2_RETAIL/D77EeKsM@10.20.31.17/RTLPRDDB',
    #              'daily_conn': 'k_ods/WrnN9Szg@10.20.201.216:1521/DDMUATDB',
    #              'ods_conn': 'k_ods/WrnN9Szg@10.20.201.216:1521/DDMUATDB',
    #              'database': 'ORACLE'
    #              }

    AirflowUtil = AirflowUtil()
    AirflowUtil.spool_csv('/Users/liuboxue/Documents/workspace/DWH_AIRFLOW_ODS_SQL/RETAIL/RTL/','/Users/liuboxue/Documents/workspace/DWH_AIRFLOW_ODS_SQL/RETAIL/RTL/',
                          'RTL1','arch_city.sql','DMT2_RETAIL/D77EeKsM@10.20.31.17/RTLPRDDB','k_ods/WrnN9Szg@10.20.201.216:1521/DDMUATDB','RTL','ORACLE','k_ods/WrnN9Szg@10.20.201.216:1521/DDMUATDB'
                          )