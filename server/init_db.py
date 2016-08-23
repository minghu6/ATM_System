# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

import sqlite3


class AlreadyExists(Exception):
    pass

def init_db():

    conn=sqlite3.connect('bank.db')
    cur=conn.cursor()
    def create_db(conn):
        '''
        table account form are as follow(in MySQL form):

            account_id char(19) primary key
            passwd varchar(30) not null
            user_name varchar(30) not null
            user_id char(18) unique
            amount decimal default 0
            currency varchar(20) not null
            store_type varchar(20) default 'current_account')
            bank varchar(20) not null 所属银行
        '''
        try:
            with conn:
                conn.execute('''create table account(account_id text primary key,
                                                            passwd text,
                                                            user_name text not null,
                                                            user_id text unique,
                                                            amount real default 0,
                                                            currency text not null,
                                                            store_type text default 'currentt',
                                                            bank text not null);''')

        except sqlite3.OperationalError as err:
            raise AlreadyExists(err)

    def insert_data(conn):
        Users=[("b123456789123456789","123456","朱汉民","632875927425678921",10e8,"rmb","current_account","中国银行"),
              ("zh12345678912345678","654321","马云","143678142343647654",10e10,"rmb","fixed_102","超弦理论探索银行"),
              ("us123456789123456789","zxcvbn","Durex","171649872365873249",92345e3,"rmb","current","光大银行")]
        try:
            with conn:
                conn.executemany('insert into account values(?,?,?,?,?,?,?,?)',Users)
        except sqlite3.IntegrityError as err:
            raise AlreadyExists(err)

    try:
        create_db(conn)
    except AlreadyExists as err:
        print(err)

    try:
        insert_data(conn)
    except AlreadyExists as err:
        print(err)

    conn.commit()
    conn.close()



def drop_db():
    conn=sqlite3.connect('bank.db')
    conn.execute('drop table account')



if __name__ == "__main__":
    init_db()
    #drop_db()
