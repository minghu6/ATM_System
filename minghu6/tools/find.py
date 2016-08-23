# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
Find
################################################################################
"""

from argparse import ArgumentParser
from pprint import pprint


from minghu6.etc.find import findlist

def shell_interactive():
    parser=ArgumentParser()

    parser.add_argument('-p','--path',dest='startdir',
                        help='find start from startdir(default os.curdir)')

    parser.add_argument('pattern',nargs='+',
                        help='such as *.c *.py')

    args=parser.parse_args()

    return args.__dict__

def main():
    args=shell_interactive()
    import os
    if args['startdir']==None:
        args['startdir']=os.curdir
    [pprint(findlist(pattern,args['startdir'])) for pattern in args['pattern']]


if __name__ == '__main__':
    main()