# -*- Coding:utf-8 -*-

"""
################################################################################
全局共享的常量
################################################################################
"""

LOGIN_PORT=9999
PROCESSING_PORT=10000

DBNAME='bank.db'
PROCESSING_FILE='processing.py'

#crypt
SALT=b'salt'
ROUND=int(10e4)
HASH_NAME='sha256'

BK_FILE_NAME='.bk.p'#process's bakeup filename

#statue code
OK=1
InSufficientFound=-1
AccountNotExist=-2