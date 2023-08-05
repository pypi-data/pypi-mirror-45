#!/usr/bin/python2.7

class Test(object):

    def __init__(self, arg):
        self.arg1 = arg + 1
        self.arg2 = arg + 2
        self.arg3 = arg + 3
    def __iter__(self):
        # yield [self.arg1, self.arg2, self.arg3]
        return iter((self.arg1, self.arg2, self.arg3))

# for a, b, c in [Test(0), Test(1), Test(2)]:
# 	print a
# 	print b
# 	print c
#
t = Test(0)
for i in t:
    print i
a, b, c = t

class Test2(object):

    def __init__(self, arg):
        self.arg1 = arg + 1
        self.arg2 = arg + 2
        self.arg3 = arg + 3

    def __iter__2(self):
        # return iter((self.arg1, self.arg2, self.arg3))
        yield { 'k1': self.arg1}
        yield { 'k2': self.arg2}
        yield { 'k3': self.arg3}

    def __iter__(self):
        # return iter((self.arg1, self.arg2, self.arg3))
        return iter({
            'k1': self.arg1,
            'k2': self.arg2,
            'k3': self.arg3,
        })

print "----"
t = Test2(0)
for i in t:
    print i
a, b, c = t
print b
print 'aa {a:.4} {b} {c}'.format(a='bbbbbbbbbb', b='ccccccccccccc', c='eee')
# print 'aa {a:.4} {b} {c}'.format(**t)



print "----"

class D(object):
    def keys(self):
        return ['a', 'b']
    def __getitem__(self, key):
        return key.upper()

def f(**kwds):
    print kwds

f(**D())
