import sqlite3
import traceback
import sys

class Mydatabase:
    def __init__(self):
        self.conn = sqlite3.connect('haojixing.db')
        self.cursor=self.conn.cursor()

        self.cursor.execute("create table if not exists user(id primary key,username,email,password,create_time,create_ip,verificated)")
        self.cursor.execute("create table if not exists articles(id primary key,title,content,create_time,author,public,hot,love,read_num)")
        self.cursor.execute("create table if not exists comments(content,article_id,sender,receiver,create_time,send_ip)")
        self.cursor.execute("create table if not exists recommends(id primary key,title,link,create_time,attribute)")
        self.cursor.execute("create table if not exists feedback(email,content,ip,create_time)")
        self.cursor.execute("create table if not exists files(id,name,attribute,create_time,type)")

    def insert(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception:
            print('发生了错误；',Exception)
            print(traceback.format_exc())
            self.conn.rollback()
            return False
        finally:
            self.conn.close()

    def fetchhone(self,sql):
        try:
            self.cursor.execute(sql)
            result=self.cursor.fetchone()
        except:
            traceback.print_exc()
            self.conn.rollback()
            result=None
        finally:
            self.conn.close()
        return result

    def fetchall(self,sql):
        try:
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
        except:
            info=sys.exc_info()
            print(info[0],',',info[1])
            self.conn.rollback()
            result = None
        finally:
            self.conn.close()
        return result

    def delete(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            f=open('\log.txt','a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            self.conn.rollback()
        finally:
            self.conn.close()

    def update(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except :
            self.conn.rollback()
            print(traceback.format_exc())
            return False
        finally:
            self.conn.close()

# Mydatabase=Mydatabase()