# This class manages the database for storing data, and calculates regressions and values with it
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from scipy.stats import linregress
from numpy import empty
import math
import datetime

class DataManager:
    def __init__(self):
        self.con = lite.connect('data.db')
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Data(Id INTEGER PRIMARY KEY, Time TEXT, Date TEXT, Bg INT, Carbs INT, Bolus INT, Notes Text)")
        cur.execute("CREATE TABLE IF NOT EXISTS CalibData(ADC INT, Actual INT)")

    def new_entry(self, time, date, bg, carbs, bolus, notes):
        self.con.execute("INSERT INTO data(Time, Date, Bg, Carbs, Bolus, Notes)  VALUES ('"+time+"','"+date+"',"+str(bg)+","+str(carbs)+","+str(bolus)+",'"+notes+"')")
        #print("INSERT INTO data(Time, Date, Bg, Carbs, Bolus, Notes)  VALUES ('"+time+"','"+date+"',"+str(bg)+","+str(carbs)+","+str(bolus)+",'"+notes+"')")
        self.con.commit()
    def delete_entry(self, rowid):
        self.con.execute("DELETE from Data where Id=" + str(rowid))
        self.con.commit()

        print 'deleted ' + str(rowid)

    def new_calib_entry(self, adc, actual):
        self.con.execute("INSERT INTO CalibData(ADC, Actual) VALUES ("+str(adc)+","+str(actual)+")")
        self.con.commit()
    def get_line(self):
        rows = self.get_whole_table("CalibData")
        x = empty([len(rows)])
        y = empty([len(rows)])
        index = 0
        for row in rows:
            x[index] = row["ADC"]
            y[index] = row["Actual"]
            index += 1
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        return lambda x: slope*x + intercept
    def get_whole_table(self, table):   # returns table in dict form
        with self.con:
            self.con.row_factory = lite.Row

            cur = self.con.cursor()
            cur.execute("SELECT * FROM " + table)

            return cur.fetchall()
    def delete_table(self, table):
        cur = self.con.cursor()
        cur.execute("DROP TABLE IF EXISTS " + table)
    def str_to_date(self, strdate):
        split_date = strdate.split('/')
        m = int(split_date[0])
        d = int(split_date[1])
        y = int(split_date[2])
        if y < 100:
            y = int('20' + str(y))
        return datetime.datetime(year=y, month=m, day=d)

if __name__ == "__main__":
    bgm = DataManager()
    rows = bgm.get_whole_table("Data")

    data = (
        ('10:34','9/1/16', 98, 36, 9, 'bg of 98'),
        ('12:34','9/1/16', 94, 24, 6, 'same notes'),
        ('6:40','9/4/16', 112, 26, 7, 'notes these are them'),
        ('8:19','9/6/16', 86, 13, 3, 'aeu'),
        ('1:30','9/6/16', 134, 6, 2, 'none'),
        ('2:45','9/7/16', 99, 6, 2, 'it was 99 today'),
        ('4:23','9/7/16', 109, 12, 3, 'tomorrow is 140'),
        ('3:33','9/8/16', 103, 140, 35, 'wow thats high'),
        ('2:29','9/15/16', 109, 60, 15, 'testing'),
        ('5:37','9/20/16', 94, 44, 11, '44, 11'),
        ('11:01','9/23/16', 117, 6, 2, 'notesnotesnotes'),
        ('11:01','10/4/16', 117, 6, 2, 'notesnotesnotes'),
        ('9:36','10/9/16', 111, 26, 7, ' '),
        ('11:01','10/11/16', 117, 6, 2, 'notesnotesnotes'),
        ('9:36','10/15/16', 111, 26, 7, ' '),
        ('9:36','10/17/16', 111, 26, 7, ' ')
    )

    bgm.delete_table('Data')
    bgm = DataManager()
    for point in data:
        bgm.new_entry(point[0],point[1],point[2],point[3], point[4], point[5])
    #for row in rows:
        #print "%s %s %s" % (row["Date"], row["Bg"], row["Carbs"])
        #print point[0]
    #bgm.delete_table('calibdata')
    #bgm.new_calib_entry(1, 1)
    #bgm.new_calib_entry(20, -100)
    #test = bgm.get_line()
    #print test(3700)






