import csv
import pymysql
import re
import logging
import argparse
from itertools import islice

class DatabaseLogin:
    
    def __init__(self, password, database, tablename, host="localhost", username="root"):
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self._tablename = tablename
        
    def login(self):
        db = None
        try:
            db = pymysql.connect(self._host,self._username,self._password, self._database)
        except Exception as e:
            print("Invalid username or password. Please try again.")
            exit(1)
        if db:
            return db
    def get_table_name(self):
        return self._tablename
    
    def get_database(self):
        return self._database
        
class DatabaseHandler:
    
    def __init__(self, csvfile, db):
        self._reader = csv.DictReader((open(csvfile, 'r', encoding="utf-8-sig")))
        self._header = self.process_headers()
        
        self._database = db # DatabaseLogin
        self._selected_database = db.login()
        try:
            self._selected_database.cursor().execute(self.create_table())
        except Exception as e:
            print("Table: {} already exists!".format(self._database.get_table_name()))
        self._sql_prefix = "INSERT INTO {} ".format(self._database.get_table_name())   
        
    def process_headers(self):
        headers = self._reader.fieldnames
        temp = ()
        for header in headers:
            temp += (header.rstrip(),)
        return temp
    
    def generate_line_data(self):
        for row in islice(self._reader, 1, None):
            line_data = ()
            for value in row.values():
                if not value:
                    value = ""
                line_data += ('"{}"'.format(value),)
            yield line_data
    
    def create_table(self):
        tablename = self._database.get_table_name()
        prefix = "CREATE TABLE {}(".format(tablename)
        for i in self._header:
            prefix += "{} text,".format(i)
        prefix = prefix.strip(",")
        prefix += ");"
        return prefix
      
    def process_sql(self, line):
        sql = ''
        sql += self._sql_prefix
        sql += "("
        for i in self._header:
            sql += "{},".format(i)
        sql = sql.strip(",")
        sql += ") VALUES ("
        for item in line:
            sql += item.rstrip()
            sql += ","
        sql = sql.strip(",")
        sql += ");"
        return sql
    
    def execute_sql(self, sql):
        cursor = self._selected_database.cursor()
        try:
            cursor.execute(sql)
            self._selected_database.commit()
        except Exception as e:
            print("[ERROR]: {}".format(sql))
            
        
def main():
    desc = """Help databases import csv files which could not be imported automatically. 
    Will automatically create a table in a database, and insert SQL queries to insert
    values.
    """
    parser = argparse.ArgumentParser(
        prog="python3 database_api.py",
        formatter_class=argparse.RawTextHelpFormatter,
        description=desc,
        epilog="Usage:\n        python3 database_api.py -p password -d database -f filename -t tablename"
    )
    parser.add_argument("-p", "--password", help="Password for MySQL")
    parser.add_argument("-d", "--database", help="Specific MySQL database to use")
    parser.add_argument("-f", "--filename", help="Specific csv file for SQL")
    parser.add_argument("-t", "--tablename", help="Which table to create in the database")
    args = parser.parse_args()
    password, database, filename, tablename = args.password, args.database, args.filename, args.tablename
    
    db = DatabaseLogin(password, database, tablename)
    handler = DatabaseHandler(filename, db)
    for line in handler.generate_line_data():
        sql = handler.process_sql(line)
        handler.execute_sql(sql)
        
if __name__ == '__main__':
    main()