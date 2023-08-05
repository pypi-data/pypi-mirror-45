from airflow_util_dv import sql_pool
import unittest


class sql_pool_tests(unittest.TestCase):

    def setUp(self):
        self.file = 'E:\GAFCGIT\GAFC_DW_SQL\PARTY_FIN_DOC_TEXT_R_APP_COBORWINFO_COMPYNAME.sql'

    def test_sql_pool(self):
        with open(self.file, 'r', encoding='gbk') as fpo:
            sqls = sql_pool.modify_sql(fpo, need_chinese=True)
            for sql in sqls:
                print(sql)


if __name__ == '__main__':
    unittest.main()
