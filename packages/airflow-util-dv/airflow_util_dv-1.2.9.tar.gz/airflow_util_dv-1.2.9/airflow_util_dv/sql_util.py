
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

    def spool_csv(self, **kwargs):
        r"""
        to analysis sql file and create csv file to export data
        :param kwargs:
        :return: csv file
        dataype must be attentionai
        SAP,RTL,ODSB,ODSB_CBB,WHS,CFL
        """
        spool_path = kwargs['spool_path']
        data_path = kwargs['data_path']
        data_type = kwargs['data_type']
        sql_name = kwargs['sql_name']
        conn = kwargs['conn']
        daily_conn = kwargs['daily_conn']
        system_type = kwargs['system_type']
        if kwargs['ods_conn']:
            ods_conn = kwargs['daily_conn']
        else:
            ods_conn = ''
        """
            get daily time
        """
        daily_start_time = ''
        daily_end_time = ''
        if data_type == 'ODSB_CBB':
            pass
        else:
            daily_start_time, daily_end_time = self.get_cut_time(system_type, data_type, daily_conn)
        connect = cx_Oracle.connect(conn, encoding='gb18030')
        cursor = connect.cursor()

        """     
            to analysis sql
        """
        sql_ = ''
        file_name = ''
        for file_ in os.listdir(spool_path):
            data_from = 0
            data_to = 0
            try:
                if file_ == sql_name:
                    if data_type == 'ODSB_CBB':
                        with open(os.path.join(spool_path, file_), 'r') as fp:
                            for line in fp.readlines():
                                sql_ += line
                    else:
                        with open(os.path.join(spool_path, file_), 'r') as fp:
                            spool_source = fp.readlines()
                            file_flag = 0
                            sql_flag = 0
                            file_name = ''
                            sql_ = ''
                            for line_ in spool_source:
                                if (line_.find('spool ') >= 0) & (line_.find('set ') < 0) & (file_flag == 0):
                                    # find file path
                                    file_flag = 1
                                    try:
                                        file_name = line_.replace('\n', '').split(' ')[1].split('/')[-1].replace("'", '')
                                    except Exception:
                                        print('spool not formatted!')
                                        print(line_)
                                        print(traceback.format_exc())
                                elif (line_.upper().find('SELECT') >= 0) & (file_flag == 1) & (sql_flag == 0):
                                    sql_flag = 1
                                    sql_ += line_
                                elif line_.strip().find('spool off;') == 0:
                                    sql_flag = 0
                                elif line_.strip().find('quit;') == 0:
                                    sql_flag = 0
                                elif sql_flag == 1:
                                    sql_ += line_

                        if sql_.find('&2') != -1:
                            sql_ = sql_.replace('&2', daily_start_time)
                        if sql_.find('&3') != -1:
                            sql_ = sql_.replace('&3', daily_end_time)

                    print(sql_.replace(';', ''))
                    try:
                        cursor.execute(sql_.replace(';', ''))
                    except Exception as ee:
                        print(ee)

                    if data_type == "ODSB_CBB":
                        with open(os.path.join(data_path, file_.replace('.sql', '.csv')), 'w', encoding='utf8') as f:
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
                                        f.write(x[0])
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
                    else:
                        schema = 'K_ODS'
                    sql = sql_retail + schema+'.'+file_name[:file_name.find('.csv')]

                    ods_cursor = cx_Oracle.connect(ods_conn).cursor()
                    ods_cursor.execute(sql)
                    data_list = ods_cursor.fetchall()
                    if not data_list[0][0]:
                        data_list[0][0] = 0

                    print('==============导入ods查询该表有 '+str(data_list[0][0]) + ' 条====================')

            except Exception as e:
                raise RuntimeError(e)
