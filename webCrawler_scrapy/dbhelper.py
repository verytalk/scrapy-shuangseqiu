import MySQLdb
from scrapy.utils.project import get_project_settings

class DBHelper():
    
    def __init__(self):
        self.settings=get_project_settings()
        
        self.host=self.settings['MYSQL_HOST']
        self.port=self.settings['MYSQL_PORT']
        self.user=self.settings['MYSQL_USER']
        self.passwd=self.settings['MYSQL_PASSWD']
        self.db=self.settings['MYSQL_DBNAME']
    
    def connectMysql(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             charset='utf8')
        return conn
    def connectDatabase(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             db=self.db,
                             charset='utf8')
        return conn   
    
    def createDatabase(self):
        conn=self.connectMysql()
        
        sql="create database if not exists "+self.db
        cur=conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    def select_data(self,sql):
        conn= self.connectMysql()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        resultList = []
        for i in result:
            resultList.append(i)
        cursor.close()
        return resultList



    def createTable(self,sql):
        conn=self.connectDatabase()
        
        cur=conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()
    def insert(self,sql,*params):
        conn=self.connectDatabase()
        
        cur=conn.cursor()
        cur.execute(sql,params)
        conn.commit()
        cur.close()
        conn.close()
    def update(self,sql,*params):
        conn=self.connectDatabase()
        
        cur=conn.cursor()
        cur.execute(sql,params)
        conn.commit()
        cur.close()
        conn.close()
    
    def delete(self,sql,*params):
        conn=self.connectDatabase()
        
        cur=conn.cursor()
        cur.execute(sql,params)
        conn.commit()
        cur.close()
        conn.close()
        
        

class TestDBHelper():
    def __init__(self):
        self.dbHelper=DBHelper()
        self.testCreateTable()

    def testCreateDatebase(self):
        self.dbHelper.createDatabase()

    def testCreateTable(self):
        sql="CREATE TABLE `issues_list` ( `id` int(11) NOT NULL AUTO_INCREMENT, `open_date` varchar(20) COLLATE utf8_bin DEFAULT NULL, `issue_date` varchar(20) COLLATE utf8_bin DEFAULT NULL, `issue_no_1` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_no_2` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_no_3` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_no_4` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_no_5` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_no_6` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_no_blue` varchar(5) COLLATE utf8_bin DEFAULT NULL, `issue_amount_total` varchar(20) COLLATE utf8_bin DEFAULT NULL, `first_prize` varchar(20) COLLATE utf8_bin DEFAULT NULL, `second_prize` varchar(20) COLLATE utf8_bin DEFAULT NULL, `remark` int(255) DEFAULT NULL, PRIMARY KEY (`id`), UNIQUE KEY `idx_open_date` (`open_date`)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COLLATE=utf8_bin"
        self.dbHelper.createTable(sql)
        print "create table completed ."

if __name__=="__main__":
    testDBHelper=TestDBHelper()
