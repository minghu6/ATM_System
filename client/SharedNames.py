# -*- Coding:utf-8 -*-

"""
################################################################################
全局共享的常量
################################################################################
"""

HOST = 'localhost'
LOGIN_PORT = 9999
PROCESSING_PORT=10000

# crypt
SALT = b'salt'
ROUND = int(10e4)
HASH_NAME = 'sha256'

BK_FILE_NAME='.bk.p'#client_tk's deal_list bakeupfile

#statue code success >0 failed <0
OK=1
InSufficientFound=-1
AccountNotExist=-2