# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
About Import function, class
################################################################################
"""
import importlib
from importlib import import_module

from minghu6.etc.cmd import exec_cmd
from minghu6.etc.version import ispython2,ispython3

def check_module(module_name,install_name=''):
    try:
        import_module(module_name)

    except ImportError:
        print(module_name,'Not Exists')

        pip_name=''
        if ispython3():
            pip_name='pip3'
        elif ispython2():
            pip_name='pip'

        print('Now, try to install through {}'.format(pip_name))

        if install_name in ('',None):
            install_name=module_name

        lines=exec_cmd('{0} install {1}'.format(pip_name,install_name))
        print(''.join(lines))

if __name__ == '__main__':
    check_module('pbs','pbs')