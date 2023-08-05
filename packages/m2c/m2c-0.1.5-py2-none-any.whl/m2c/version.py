'''
0.0.8 add text search template
0.0.9 update service template url; auto check version
0.1.0 add go source file wathdog
0.1.1 add api version
0.1.2 fix page
0.1.3 add string type or/like template, fix without manager query bug
0.1.4 update watchgo/orm
0.1.5 update swagger
'''
name = 'm2c'
version = '0.1.5'

def check_version():
    import os
    from .conf import Color
    text = os.popen('pip search %s' % name).read()
    need_update = False
    for line in text.splitlines():
        print line
        line = line.strip()
        if line.startswith('LATEST:'):
            need_update = True
    if need_update:
        print Color.red('run: pip install -U %s, update it!' % name)
