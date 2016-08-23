# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
服务器端类似守护程序(daemon)。
处理客户端的登陆请求，并监测业务处理程序process(process.py)（当process崩溃时，负责进行重启和数据恢复的功能）

因此本程序对于整个ATM系统至关重要，除火山地震洪水海啸等不可抗力因素外，假定应该稳定运行。
（理论上，当本程序崩溃时，应该锁定整个银行业务处理的数据库，但这就不是我们这个程序该考虑的了）
################################################################################
"""


if __name__=='__main__':
    from SharedNames import LOGIN_PORT,PROCESSING_PORT
    from SharedNames import DBNAME,PROCESSING_FILE
    from SharedNames import SALT,ROUND,HASH_NAME

    import bakeup
else:
    from .SharedNames import LOGIN_PORT,PROCESSING_PORT
    from .SharedNames import DBNAME,PROCESSING_FILE
    from .SharedNames import SALT,ROUND,HASH_NAME
    from .SharedNames import WITHDRAW,DEPOSIT,TRANSFER
    from . import bakeup


from xmlrpc.server import SimpleXMLRPCServer as rpcServer
from xmlrpc.server import SimpleXMLRPCRequestHandler as rpcRequestHandler
import xmlrpc.client
import datetime

import sqlite3



class Server:


    def __init__(self,port=LOGIN_PORT):
        """
        1. 与账户存储数据库建立连接
        2. 启动业务处理子进程process
        3. 启动对业务处理子进程监听的线程listen_process_thread：
          3.1 负责对蹦溃子进程的恢复
          3.2 相关账户数据的恢复
          3.3 通知ATM客户端重启（避免长期客户端无响应）

        :param port:
        :return:
        """
        self.port=port

        self.login_dict=dict()

        self.conn=sqlite3.connect(DBNAME)
        self.cur=self.conn.cursor()

        global conn,cur

        conn,cur=self.conn,self.cur
        
        import urllib.request
        # Restrict to a particular path.
        class RequestHandler(rpcRequestHandler):
            #rpc_paths = ('.',)
            pass
        
        self.server=rpcServer(('127.0.0.1',port),requestHandler=RequestHandler,allow_none=True)
        self.client_need_restart=False

        def start_processing_process():
            from minghu6.etc.launchmods import PortableLauncher
            launcher=PortableLauncher(PROCESSING_FILE,PROCESSING_FILE)
            launcher()
            print('process.py pid:',launcher.popen.pid)
            return launcher.popen

        self.popen=start_processing_process()
        self.register()
        print('Listening on port {0:d}...'.format(port))

        def listen_process_thread():
            while True:
                bakeup.recover()
                self.popen.wait()
                print('recover the data')
                self.client_need_restart=True
                bakeup.recover()
                print('restart process')
                self.popen=start_processing_process()

        import threading
        thread=threading.Thread(target=listen_process_thread)
        thread.start()


    def mainloop(self):

        self.server.serve_forever()


    def login_server(self,account_id,passwd):
        """
        监听端口，如果有客户端login的登录请求，进行
           1.登录表检查（防止重复登录）
           2.密钥校验（相关API采用了 PKCS#5 基于密码的密钥导出函数，且采用 HMAC 作为伪随机函数）。、
        如果校验成功，允许启动ATM客户端,并设置其在登录表的登录状态。
        :param account_id: login account_id
        :param passwd: login passwd
        :return:
        """
        self.account_id=account_id
        self.passwd=passwd

        if account_id in self.login_dict and self.login_dict[account_id]==True:
            raise Exception('Your account have been logined')
            pass

        print('hi,here are server\n',account_id,passwd.data)
        cur.execute('select passwd from account where account_id=?',
                    (account_id,))


        fetched_set=cur.fetchone()
        if fetched_set == None:#account_id don't exist
            return False
        else:
            import hashlib

            #密钥导出函数
            voucher=hashlib.pbkdf2_hmac(HASH_NAME,
                                        fetched_set[0].encode('utf-8'),
                                        SALT,ROUND)

            #print(type(voucher),' : ',voucher)

            if voucher == passwd.data:
                self.login_dict[account_id]=True
                return True
            else:#Error Password
                return False


    def need_restart_client(self):
        """
        ATM login进程主动调用，检测是否需要重启client子进程
        :return: bool
        """
        if self.client_need_restart:
            self.client_need_restart=False#only one process at one time

            return True
        else:
            return False

    def logout(self,account_id):
        """
        ATM login进程退出时（包括正常退出以及不正常退出）调用，
        取消账户在登录表中的登录状态

        :param account_id:
        :return:
        """
        self.login_dict[account_id]=False


    def register(self):

        self.server.register_introspection_functions()
        
        self.server.register_function(self.login_server,'login_server')
        self.server.register_function(self.need_restart_client,'need_restart_client')
        self.server.register_function(self.logout,'logout')


if __name__ == "__main__":

    Server().mainloop()










