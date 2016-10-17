# -*- coding: utf-8 -*-
import MySQLdb
import settings

class db_operate:
    def mysql_command(self,conn,sql_cmd):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd)
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error,e:
            ret.append(e)

        return ret

    def select_table(self,conn,sql_cmd,parmas):
        try:
            ret = []
            conn=MySQLdb.connect(host=conn["host"],user=conn["user"],passwd=conn["password"],db=conn["database"],port=conn["port"],charset="utf8")
            cursor = conn.cursor()
            n = cursor.execute(sql_cmd,parmas)
            print n
            for row in cursor.fetchall():
                for i in row:
                    ret.append(i)
        except MySQLdb.Error,e:
            ret.append(e)

        return ret

#def main():
    #db = db_operate()
    #sql = 'select `return` from salt_returns where jid="20160722170818900450"'
    #result=db.mysql_command(settings.OPS_MYSQL,sql)
    #result=db.select_table(settings.OPS_MYSQL,sql,parmas)
    #print result

#if __name__ == '__main__':
#    main()
