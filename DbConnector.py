# -*- coding: UTF-8 -*-
import mysql.connector

class DbConnector:
    def __init__(self):
        self.db = mysql.connector.connect(
                host = 'localhost',
                user = 'MNPS',
                passwd = '#Senha123')
        self.cursor = self.db.cursor()
        self.createDatabase('mnps')
        self.chooseDatabase('mnps')
        self.createTable()
    
    def execute(self,query):
        self.cursor.execute(query)
        self.db.commit()

    def createDatabase(self,dbName):
        self.execute('CREATE DATABASE if not exists ' + dbName)
    
    def createTable(self):
        query  = 'create table if not exists eventdata'
        query += '(eventdata_id integer primary key auto_increment,'
        query += 'measure double not null,'
        query += 'time_ timestamp not null default current_timestamp)'
        self.execute(query)

    def chooseDatabase(self,database):
        self.execute('use ' + database)

    def exit(self):
        self.db.close()

    def insert(self, data):
        query = ('insert into eventdata(measure) values (%f)'%(data))
        self.execute(query)