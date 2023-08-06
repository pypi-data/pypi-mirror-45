#!/usr/bin/python2.7

class Foo(object):

    def __init__(self, x):
        self._x = x

    def __format__(self, format_spec):
        print format_spec
        l_format = '<Foo x={0:' + format_spec + '}>'
        print l_format
        a = l_format.format(self._x)
        print a
        return a


foo = Foo("fred")

# Pass "baz" as a format_spec
# print 'This is a foo: {0:baz}'.format(foo)
print 'aa {0:.4}'.format(foo)
print 'aa {0:.4} {1}'.format('bbbbbbbbbb', 'ccccccccccccc')
