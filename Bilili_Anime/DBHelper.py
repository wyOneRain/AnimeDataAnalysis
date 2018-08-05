import pymssql

class DBhelper:
    def __init__(self):
        self.__conn = pymssql.connect(user='sa', password='*******', host='.', port=1433, database='DataAnalysis', charset="utf8")
        self.__cur = self.__conn.cursor()

    #table_name：表名
    # data：字典，包含插入数据的字段和值
    def insert_data(self,table_name,dict_data):
        try:
            str1 = ""
            str2 = ""
            str1 = str1 + "Insert into " + table_name + " ("
            str2 = str2 + "("
            for key in dict_data.keys():
                str1 = str1 + key + ","
                str2 = str2 +"'" + str(dict_data[key]) + "',";
            str1 = str1 + ")"
            str2 = str2 + ")"
            sql = str1.replace(",)",") ") + "values " + str2.replace(",)",")")
            self.__cur.execute(sql)
            self.__conn.commit()
        except Exception:
            Logger.write_log(sql+"\n")

    def close_DB(self):
        self.__conn.close()


class Logger:
    def write_log(msg):
        with open("log.txt","a+",encoding='utf-8') as f:
            f.write(msg)