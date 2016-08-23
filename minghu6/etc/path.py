#!/usr/bin/env python3
# -*- Coding:utf-8 -*-
"""
################################################################################
About Path(File,Directory,Atty,Link etc)
################################################################################
"""

import os,sys
def get_cwd_presDir(n):
    '''
    get n level before cwd 's dir
    '''

    def get_pre_dir(path):
        '''
        get one level before path
        '''
        return os.path.split(path)[0]

    path=os.getcwd()
    for i in range(n):
        path=get_pre_dir(path)

    return path

def isempty_file(fn):
    with open(fn,'rb') as f:
        length=len(f.read(1))
    return length==0

def isempty_dir(fn):
    return os.listdir(fn).__len__()==0