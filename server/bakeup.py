# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
Dealing Bakeup and Recover data For server and process

main functions:
    recorver :server recorver data

    bakeup :process bakeup data before operation
    undo_bakeup :process remove bakeup data after operation
################################################################################
"""
import pickle
import sqlite3
import os

from minghu6.etc import find

from SharedNames import BK_FILE_NAME
from SharedNames import DBNAME

def dump(account_id,amount):
    """

    :param account_id:
    :param amount:
    :return:
    """
    with open(str(account_id)+BK_FILE_NAME,'wb') as f:
        obj=(account_id,amount)
        pickle.dump(obj,f)


def load(bkfile_name):
    """
    Return 2-element tuple and delete the bakeup file
    :return:(account_id,amount)
    """
    assert os.path.exists(bkfile_name),'{0:s} Do not Exist'.format(bkfile_name)

    result=pickle.load(open(bkfile_name,'rb'))

    assert isinstance(result,tuple) and len(result)==2,'pickle.load Do not get 2-element tuple'

    return result

def recover():

    allfiles=find.findlist('*'+BK_FILE_NAME)
    results=[load(bkfile) for bkfile in allfiles]

    with sqlite3.connect(DBNAME) as conn:
        [conn.execute('update account set amount=? where account_id=?',result)
         for result in results]

    [undo_bakeup(result[0]) for result in results]


def bakeup(account_id,amount):
    dump(account_id,amount)

def undo_bakeup(account_id):
    try:
        os.remove(str(account_id)+BK_FILE_NAME)
    except FileNotFoundError as e:
        print(e)

























