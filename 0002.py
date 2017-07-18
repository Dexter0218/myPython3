# -*- coding: utf-8 -*-
"""
第 0002 题：将 0001 题生成的 200 个激活码（或者优惠券）保存到 MySQL 关系型数据库中。
"""
import pymysql


def code2sql():
    f = open('result2.txt', 'r')
    conn = pymysql.connect(user='dexter0218', passwd='1234')
    cursor = conn.cursor()
    cursor.execute('create database if not exists accode')
    cursor.execute('use accode')
    cursor.execute('create table accode(id int auto_increment primary key, code varchar(20))')
    for line in f.readlines():
        cursor.execute('insert into accode (code) values (%s)', [line.strip()])
    try:       
        conn.commit()
    except:
        conn.rollback()
        print('Error happened when inserting data')
    finally:
        conn.close()
    f.close()
    cursor.close()


if __name__ == '__main__':
    code2sql()