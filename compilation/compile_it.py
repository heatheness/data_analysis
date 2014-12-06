# -*- coding: utf-8 -*-

__author__ = 'nyash myash'


# p = Program ('x+y+(1+2*z)')
# r = p.Run({'x'= 1, 'y'=4, 'z'=0})
# print r


# код можно представить в виде дерева

# начнем писать узлы

class Const():
    def __init__(self,value):
        self.value = value

    def run(self,context):
        return self.value


class Var():
    def __init__(self,name):
        self.name = name

    def run(self,context):
        return context[self.name]


class Add():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def run(self,context):
        return self.x.run(context) + self.y.run(context)


class Mul():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def run(self,context):
        return self.x.run(context) * self.y.run(context)


class Neg():
    def __init__(self,x):
        self.x = x

    def run(self,context):
        return - self.x.run(context)



class Sub():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def run(self,context):
        return self.x.run(context) - self.y.run(context)

# print Add(Const(1), Var('x')).run({'x':4})
# print Sub(Const(8), Var('x')).run({'x':4})

# лексемы:
# +-*()
# i идентификатор буква(буква или цифра)*
# c константа - цифра+

class TokenParser:
    def __init__(self,s):
        self.s = s
        self.curr = None

    def next(self):
        if self.curr:
            res = self.curr
            self.curr = None
            return res
        s = self.s.lstrip()
        if not s:
            res = ('', None)
            n = 1
        elif s[0] == '+':
            res = ('+', None)
            n = 1
        elif s[0] == '-':
            res = ('-', None)
            n = 1
        elif s[0] == '*':
            res = ('*', None)
            n = 1
        elif s[0] == '(':
            n = 1
            res = ('(', None)
        elif s[0] == ')':
            res = (')', None)
            n = 1
        elif s[0].isdigit():
            n = 1
            while n < len(s) and s[n].isdigit():
                n += 1
            res = ('c',int(s[:n]))
        elif s[0].isalpha():
            n = 1
            while n < len(s) and s[n].isalnum():
                n += 1
            res = ('i', s[:n])
        else:
            assert False
        self.s = s[n:]
        return res

    def putback(self,t):
        assert self.curr == None
        self.curr = t

p = TokenParser('1234 + -foo')
while True:
    t = p.next()
    print t
    if not t[0]:
        break


def pars_expr(p):
    res = pars_term(p)
    while True:
        t = p.next()
        if not t[0]:
            return res
        if t[0] == '+':
            res2 = pars_term(p)
            return Add(res,res2)
        if t[0] == '-':
            res2 = pars_term(p)
            return Sub(res,res2)
        assert False


def pars_unit(p):
    t = p.next()
    if t[0] == 'i':
        return Var(t[1])
    if t[0] == 'c':
        return Const(t[1])
    if t[0] == '(':
        res = pars_expr(p)
        assert p.next()[0] == ')'
        return res
    assert False

def pars_factor(p):
    t = p.next()
    if t[0] == '-':
        res = pars_unit(p)
        return Neg(res)
    p.putback(t)
    return pars_unit(p)

def pars_term(p):
    res = pars_factor(p)
    while True:
        t = p.next()
        if t[0] != '*':
            p.putback(t)
        return res
    res2 = pars_factor()
    res = Mul(res,res2)

p = TokenParser('1+2')
c = pars_expr(p)
print c.run({})