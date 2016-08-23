# -*- Coding:utf-8 -*-
# !/usr/bin/env python3

"""
################################################################################
负责处理交易清单相关功能的模块
main functions:
    bakeup
    undo_bakeup

    need_recorver
    recorver

    print_deal_list
################################################################################
"""

import pickle
import os



from SharedNames import BK_FILE_NAME

def bk_file_name(account_id):

    return str(account_id)+BK_FILE_NAME


def bakeup(account_id,msg):
    dump(account_id,msg)

def dump(account_id,msg):

    with open(bk_file_name(account_id),'wb') as f:
        obj=(account_id,msg)
        pickle.dump(obj,f)

def load(account_id):
    """
    Return 2-element tuple and delete the bakeup file
    :return:(account_id,amount)
    """
    bkfile_name=bk_file_name(account_id)
    assert os.path.exists(bkfile_name),'{0:s} Do not Exist'.format(bkfile_name)

    result=pickle.load(open(bkfile_name,'rb'))

    assert isinstance(result,tuple) and len(result)==2,'pickle.load Do not get 2-element tuple'

    return result

def recover(account_id):

    result=load(account_id)

    undo_bakeup(account_id)
    return result


def need_recorver(account_id):
    bakefile_name=bk_file_name(account_id)
    if os.path.exists(bakefile_name):
        return True

    else:
        return False

def undo_bakeup(account_id):

    try:
        os.remove(bk_file_name(account_id))
    except FileNotFoundError as e:
        print(e)

def print_deal_list(msg):
    from tkinter.messagebox import showinfo
    showinfo('交易清单',msg)


















