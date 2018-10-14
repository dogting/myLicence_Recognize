# !/user/bin/env python
# -*- coding:utf-8 -*-
import MySQLdb
import video_track
class SQL_store():
    def __init__(self):
        pass

    def searchLiscence(self,TableName,carLiscence):
        try:
            self.conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="carinform", use_unicode=True,
                                        charset="utf8")

            self.cur = self.conn.cursor()
            try:
                sql = 'SELECT * FROM %s WHERE liscencePlate = "%s" '%(TableName,carLiscence)
                self.cur.execute(sql)
                results = self.cur.fetchall()
                if len(results) > 0:
                        string = "id = '%s';cameraID = '%s';liscencePlate = '%s';rect = '%s';beginTime='%s';endTime='%s';speed = '%s';filePath='%s'"%(results[0][:])
                else:
                    string = "no such car"
                video_track.video_track(self).find_car(string)
                return results
            except MySQLdb.Error as e:
                print(e)
            self.conn.commit()
            self.cur.close()
            self.conn.close()

        except MySQLdb.Error as e:
             print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


    def InsertData(self,TableName, dic,cameraID):
        try:
            self.conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="carinform", use_unicode=True,
                                        charset="utf8")

            self.cur = self.conn.cursor()
            results = ""

        # cur.execute("SELECT * FROM  %s" % (TableName))

        # 提取车辆信息中的内容 如：('京F28046',[123,123,123,123],'','')
            string = "'" + cameraID + "'"
            for key in dic:
                if isinstance(key, list):
                    key = str(key)
                string = string + ',' + "'" + key + "'"
            try:

                #判断是否已经有该车
                self.cur.execute('SELECT COUNT(*) FROM %s WHERE liscencePlate = "%s" and cameraID = "%s"'%(TableName,dic[0],cameraID))
                results = self.cur.fetchall()
                #存在该车，修改内容
                if results[0][0] > 0:
                    sql = "UPDATE %s SET rect='%s', speed='%s',endTime='%s' WHERE liscencePlate='%s'"%(TableName,dic[1],dic[4],dic[3],dic[0])
                else:
                    sql = "INSERT INTO %s (cameraID,liscencePlate,rect,beginTime,endTime,speed,filePath) VALUES (%s)" % (TableName, string)
                    # print(sql)
                #插入车辆信息
                self.cur.execute(sql)

            except MySQLdb.Error as e:
                sql = '	id INT AUTO_INCREMENT,' \
                      'cameraID VARCHAR(50),' \
                      'liscencePlate VARCHAR(50),' \
                      'rect VARCHAR(50),' \
                      'beginTime VARCHAR(50),' \
                      'endTime VARCHAR(50),' \
                      'speed VARCHAR(50),' \
                      'filePath VARCHAR(150),' \
                      'PRIMARY KEY(id)'

                self.cur.execute("CREATE TABLE %s (%s)" % (TableName,sql))
                self.cur.execute("INSERT INTO %s (cameraID,liscencePlate,rect,beginTime,endTime,speed,filePath) VALUES (%s)" % (TableName, string))

            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))




# if __name__ == '__main__':
#     dic = ('京6',[123,123,123,123],'20','')
#     SQL_store().InsertData('car', dic)
