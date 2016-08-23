# -*- Coding:utf-8 -*-
# !/usr/bin/env python3

"""
################################################################################
ATM 登陆界面的后台代码，实现了login_tk模块的主要功能调用
连接服务器，进行登录，如果登陆成功，则启动ATM 客户端(client)
并且开启一个监听线程，负责在必要的时候重启ATM 客户端
################################################################################
"""

import sys
# passwd input

import tkinter as tk
import time

import xmlrpc.client

from  xmlrpc.client import Binary

import subprocess
from subprocess import call

try:
    from .SharedNames import HOST,LOGIN_PORT,SALT,HASH_NAME,ROUND
except:
    from SharedNames import HOST,LOGIN_PORT,SALT,HASH_NAME,ROUND

CLIENT_FILE = 'client_tk.py'


def start_client(account_id):

    from minghu6.etc.launchmods import PortableLauncher as launch

    launcher=launch('client', ' '.join([CLIENT_FILE, account_id]))
    launcher()

    print('client pid ',launcher.popen.pid)
    return launcher.popen

class Result:
    def __init__(self):
        self.account_id = None
        self.passwd = None
        self.ok = False

    def __str__(self):
        return "username={} password={} ok={}".format(self.username,
                                                      self.password, self.ok)


class Login:
    def __init__(self, account_id, passwd):
        """
        连接服务器进行登录
        :param account_id:
        :param passwd:
        :return:
        """
        import hashlib
        if sys.version_info[:2] < (3, 3):
            ConnectionError = socket.error

        # print('hello',account_id,passwd)

        print(account_id,passwd)
        self.account_id = account_id
        self.passwd = hashlib.pbkdf2_hmac(HASH_NAME, passwd.encode('utf-8'), SALT, ROUND)

        self.normal_quit_state=True
        self.connect_server()

    def handle_error(self, err):
        '''
        if isinstance(err, xmlrpc.client.Fault):
            err = err.faultString
        messagebox.showinfo("Meter \u2014 Error",
                "{}\nIs the server still running?\n"
                "Try Quitting and restarting.".format(err), parent=self)
        '''
        print(err)

    def connect_server(self):
        """
        尝试连接服务器进行登陆，如果登陆成功开启监听线程，
        该线程保证在需要的时候进行ATM 客户端的重启
        :return:
        """
        try:

            self.manager = xmlrpc.client.ServerProxy("http://{}:{}"
                                                     .format(HOST,LOGIN_PORT,SALT,HASH_NAME,ROUND), allow_none=True)

            # print('hello',type(self.passwd),self.passwd)

            try:
                
                self.verified_account = self.manager.login_server(self.account_id,
                                                                  Binary(self.passwd))

                print(self.verified_account)

                if self.verified_account:
                    self.popen=start_client(self.account_id)

                    def start_listen_thread():
                        def listen_thread():

                            self.rebuild_connection()
                            while True:
                                if self.manager.need_restart_client():

                                    from tkinter.messagebox import showinfo
                                    showinfo('需要重启!',("很抱歉通知您\n"
                                                      "由于服务器端崩溃，所以客户端需要进行重启以重新建立连接\n"))

                                    self.normal_quit_state=False
                                    self.popen.terminate()

                                    self.popen=start_client(self.account_id)

                                time.sleep(3)

                        import threading
                        threading.Thread(target=listen_thread).start()

                    start_listen_thread()

                else:
                    from tkinter.messagebox import showerror
                    showerror('Login-Error', '账号或者密码错误')

            except Exception as ex:
                self.verified_account=None
                from tkinter.messagebox import showerror
                showerror('Error',ex.__repr__())

        except (ConnectionError, xmlrpc.client.Fault) as err:
            self.handle_error(err)
            return False

        pass

    def rebuild_connection(self):
        """
        不知道是XML-RPC这个版本的标准库有缺陷，还是使用方式不当，
        XML-RPC连接有时似乎断开连接，采用stackoverflow 上类似问题的说法
        重新建立XML-RPC连接
        :return:
        """
        self.manager=xmlrpc.client.ServerProxy("http://{}:{}".format(HOST,
                                                                     LOGIN_PORT,
                                                                     SALT,
                                                                     HASH_NAME,
                                                                     ROUND),
                                               allow_none=True)



    def normal_quit(self):# for login_tk
        """
        在login_tk中监听线程中调用的正常退出检测方法，
        在调用时如果判断是正常退出，则登出服务器logout()
        :return:
        """
        self.rebuild_connection()
        if self.normal_quit_state==True:

            def logout():
                self.manager.logout(self.account_id)

            logout()
            return True
        elif self.normal_quit_state==False:
            self.normal_quit_state=True
            return False



if __name__ == "__main__":
    if sys.stdout.isatty():#is tty
        def close(event):
            window.destroy()
            application.quit()


        application = tk.Tk()
        result = Result()
        from login_test import Window

        window = Window(application, result)

        application.bind("<Escape>", close)
        # application.mainloop()
    else:
        print("Loaded OK")
