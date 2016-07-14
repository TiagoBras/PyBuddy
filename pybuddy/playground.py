# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import codecs

try:
    import sys, locale, os
    print(sys.stdout.encoding)
    print(sys.stdout.isatty())
    print(locale.getpreferredencoding())
    print(sys.getfilesystemencoding())
    print(os.environ["PYTHONIOENCODING"])
except Exception, e:
    pass

def sort_priority(values, group):
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    return sorted(values, key=helper)

A =[4, 2, 6, 8, 7, 1, 5, 9, 0, 3]
g = [3, 5, 8]

def foo(a, b, *, *args, **kwargs):
    pass
print(sort_priority(A, g))

# sys.stdout.write("António")
# from io import TextIOWrapper
# sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print(sys.version_info)

# if sys.version_info < (3, ):
# from builtins import bytes

def b(str_or_bytes):
    if sys.version_info < (3,):
        if isinstance(str_or_bytes, unicode):
            return str_or_bytes.encode('utf-8')
        else:
            return str_or_bytes
    else:
        if isinstance(str_or_bytes, str):
            return str_or_bytes.encode('utf-8')
        else:
            return str_or_bytes

def s(str_or_bytes):
    if sys.version_info < (3,):
        if isinstance(str_or_bytes, str):
            return str_or_bytes.decode('utf-8')
        else:
            return str_or_bytes
    else:
        if isinstance(str_or_bytes, bytes):
            return str_or_bytes.decode('utf-8')
        else:
            return str_or_bytes

import pprint 
# from collections import OrderedDict
# from configparser import SafeConfigParser

EX01 = "Olá {name}! こんに{lkfda}ちは！どこ行くの？ {email} {name}"
print(type(EX01))
print("%s" % EX01)

# def get_default(config, section, option, default):
#     if config.has_option(section, option):
#         return config.get(section, option)
#     else:
#         return default

def main():
    # pp = pprint.PrettyPrinter()
    # defs = {
    #     'create': {
    #         'author': 'ND',
    #         'email': 'ND',
    #         'version': '0.0.3',
    #     }
    # }
    # config = SafeConfigParser(OrderedDict(defs))
    # config.add_section('create')
    # config.set('create', 'author', '')
    # config.set('create', 'email', '')
    # config.set('create', 'version', '0.0.1')
    # config.read('pybuddy.ini')


    # pp.pprint(config.items('create'))

    print(render_string(EX01, name='António', email='james@gmail.com'))


def render_string(s, **kwargs):
    rendered_string = []

    it = iter(s)
    while True:
        try:
            c = next(it)

            if c == '{':
                token_name = []
                c = next(it)

                while c != '}':
                    token_name.append(c)
                    c = next(it)

                token = "".join(token_name)
                rendered_string.append(kwargs.get(token, ''))
            else:
                rendered_string.append(c)

        except StopIteration as e:
            break

    return "".join(rendered_string)

if __name__ == '__main__':
    main()