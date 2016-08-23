# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
业务处理进程，是由server启动的子进程。

提供：
    1.取款(withdraw)
	2.存款(deposit)
	3.转账(transfer)

    4.获取服务器时钟(today)
	5.获取账户所在银行(get_bank)
	6.查看当前账户余额(check_amount)

等功能
################################################################################
"""

if __name__=='__main__':
    from SharedNames import LOGIN_PORT,PROCESSING_PORT
    from SharedNames import DBNAME
    from SharedNames import BK_FILE_NAME

    import bakeup

else:
    from .SharedNames import LOGIN_PORT,PROCESSING_PORT
    from .SharedNames import DBNAME
    from .SharedNames import BK_FILE_NAME
    from . import bakeup
    from . import bakeup


from xmlrpc.server import SimpleXMLRPCServer as rpcServer
from xmlrpc.server import SimpleXMLRPCRequestHandler as rpcRequestHandler
import xmlrpc.client
import sqlite3

import time
from  threading import Thread

if __name__=='__main__':
    import SharedNames
else:
    from . import SharedNames

class Processing:
    """
    有点类似单例模式，不过直接用类而不是单实例来处理业务处理
    （如果是Java的话，还要单独搞一些奇奇怪怪的设计来迂回曲折地实现这种功能，
       （再次印证了在语法设计上，Java就是一把严谨的外形上很像一把刀的
       。。。大香蕉
       而python就是简单粗暴的手提电锯这一颠扑不破的真理））

    再次强调，这个类不需要，也不应有，准确说“不能有”实例！!
    """
    @classmethod
    def start(cls,port=PROCESSING_PORT):
        """
        这个类的初始化方法，类似于实例的__init__
        开启XML-RPC的服务器端监听进程
        :param port:
        :return:
        """

        cls.port=port
        cls.conn,cls.cur=Processing.create_database_obj()

        cls.server=rpcServer(('localhost',port),allow_none=True)
        cls.register()

        cls.commit=False
        cls.timeout=False
        print('Listening on port {0:d}...'.format(port))
        cls.server.serve_forever()

    @staticmethod
    def create_database_obj():
        """
        因为SQLite Object只能在创建它的线程中使用，因此对于其他线程，要用这个方法重新创建数据库对象
        :return:(database-connection,connection-cursor)
        """
        conn=sqlite3.connect(DBNAME)
        cur=conn.cursor()

        return conn,cur

    @classmethod
    def wait_confirm(cls,rounds=25,interval=0.2):
        """
        用于预防在取款、存款、转账时ATM 客户端崩溃的情形，
        只有当ATM 客户端完成了相应功能（比如取款时吐钱完毕）
        才会从ATM 客户端对commit进行了调用，会是函数返回True
        否则超时后返回False
        :param rounds: the number of rounds
        :param interval: sleep time every round
        :return: bool
        """
        for i in range(rounds):
            if cls.commit:
                cls.commit=False
                cls.timeout=False
                return True
            time.sleep(interval)

        cls.timeout=True
        cls.commit=False
        return False

    @staticmethod
    def today():
        import datetime
        today=datetime.datetime.today()
        return today.isoformat()

    @classmethod
    def get_bank(cls,account_id):
        cls.cur.execute('select bank from account where account_id=?',(account_id,))
        bank=cls.cur.fetchone()[0]

        return bank

    @classmethod
    def withdraw(cls,account_id,amount,delay=1.5,wait_confirm=True,create_new_conn=False):
        #print('withdraw :%d'%amount

        conn,cur=cls.conn,cls.cur
        if create_new_conn:
            conn,cur=cls.create_database_obj()

        cur.execute('select amount from account where account_id = ? ',(account_id,))
        cur_amount=cur.fetchone()[0]

        #make bakeup  file to protect loss of data from program crash

        bakeup.bakeup(account_id,cur_amount)

        time.sleep(delay)

        if cur_amount>=amount :


            def action():
                if not wait_confirm or (wait_confirm and Processing.wait_confirm(rounds=50)):

                    print('hi')
                    conn,cur=cls.create_database_obj()
                    cur.execute('update account set amount=? where account_id=? ',
                                (cur_amount - amount,account_id))

                    conn.commit()

            Thread(target=action).start()
            bakeup.undo_bakeup(account_id)#for process crash ,not for ATM client
            return cur_amount-amount,Processing.today()
        else:
            return (SharedNames.InSufficientFound,'\n\n\t余额不足\n\n\t交易失败')

        pass

    @classmethod
    def check_amount(cls,account_id):
        cls.cur.execute('select amount from account where account_id = ? ',(account_id,))
        cur_amount=cls.cur.fetchone()[0]
        print('cur_amount: ',cur_amount)

        return cur_amount

    @classmethod
    def deposit(cls,account_id,amount,delay=1.5,wait_confirm=True,create_new_conn=False):

        conn,cur=cls.conn,cls.cur
        if create_new_conn:
            conn,cur=cls.create_database_obj()
        cur.execute('select amount from account where account_id = ? ',(account_id,))
        cur_amount=cur.fetchone()[0]


        #make bakeup  file to protect loss of data from program crash

        bakeup.bakeup(account_id,cur_amount)

        time.sleep(delay)

        def action():
            if not wait_confirm or (wait_confirm and Processing.wait_confirm()):
                conn,cur=cls.create_database_obj()
                cur.execute('update account set amount=? where account_id=? ',
                            (cur_amount + amount,account_id))

                conn.commit()

        Thread(target=action).start()
        bakeup.undo_bakeup(account_id)
        return cur_amount+amount,Processing.today()

    @classmethod
    def transfer(cls,id_from,id_to,amount):

        time.sleep(1.5)

        cls.cur.execute('select amount from account where account_id = ? ',(id_from,))
        cur_amount=cls.cur.fetchone()[0]

        cls.cur.execute('select amount from account where account_id = ? ',(id_to,))
        if cls.cur.fetchone()==None:
            return (SharedNames.AccountNotExist,'\n\n\n\t输入的账号不存在')

        else:

            if cur_amount>=amount:
                def action():
                    if Processing.wait_confirm():

                        Processing.withdraw(id_from,amount,
                                            delay=0,wait_confirm=False,create_new_conn=True)
                        Processing.deposit(id_to,amount,
                                           delay=0,wait_confirm=False,create_new_conn=True)


                Thread(target=action).start()
                return cur_amount,Processing.today()

            else:
                return  (SharedNames.InSufficientFound,'\n\n\t余额不足\n\n\t交易失败')


    @classmethod
    def commit(cls):
        """
        ATM 客户端调用，在wait_confirm等待不超时的情况下，使之前的操作（取款、存款等）生效
        否则操作撤销
        :return:bool
        """
        if cls.timeout:
            cls.timeout=False
            cls.commit=False
            return False
        else:
            cls.commit=True
            cls.timeout=False
            return True

    @classmethod
    def register(cls):

        cls.server.register_introspection_functions()
        cls.server.register_function(Processing.withdraw,'withdraw')
        cls.server.register_function(Processing.check_amount,'check_amount')
        cls.server.register_function(Processing.deposit,'deposit')
        cls.server.register_function(Processing.transfer,'transfer')
        cls.server.register_function(Processing.get_bank,'get_bank')
        cls.server.register_function(Processing.commit,'commit')

if __name__=='__main__':
    import sys
    Processing.start().mainloop()
