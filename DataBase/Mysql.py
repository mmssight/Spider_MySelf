# coding = 'utf8'
import pymysql,traceback


class MySql:
    def __init__(self):
        self.conn = self.to_connect()
        self.is_connected()
        self.cursor=self.conn.cursor()
    def __del__(self):
        self.conn.close()

    def to_connect(self):
        return pymysql.connect(host='127.0.0.1', user='root', password='root', database='myself', charset='utf8')

    def is_connected(self):
        """Check if the server is alive"""
        try:
            self.conn.ping(reconnect=True)
            print("db is connecting")
        except:
            traceback.print_exc()
            self.conn = self.to_connect()
            print("db reconnect")

    def Excute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            with open('MySql.sql','a') as f:
                f.write(sql)
                print(str(e))
    def Close(self):
        self.cursor.close()
        self.conn.close()
