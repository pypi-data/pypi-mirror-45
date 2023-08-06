#! /usr/bin/python3
# _*_ coding:utf-8 _*_

"""

@ File   :color.py
@ Author :LiuHeDong
@ Mail   :liuhedong135@163.com
@ Date   :2019-05-06 11:39:03

"""


class Color(object):

    def __init__(self, strings):
        self.strings = strings
        self.bground = 40
        self.fground = 37
        self.pattern = 0

    def excute(self):
        self.combine = "\033[{};{};{}m{}\033[0m".format(self.pattern, self.fground, self.bground, self.strings)
        return self.combine


class ForeColor(Color):

    def foreblack(self):
        self.fground = 30

    def forered(self):
        self.fground = 31

    def foregreen(self):
        self.fground = 32

    def foreyellow(self):
        self.fground =  33

    def foreblue(self):
        self.fground = 34

    def foremagenta(self):
        self.fground = 35

    def forecyan(self):
        self.fground = 36

    def forewhite(self):
        self.fground = 37

    def excute(self):
        self.combine = "\033[{};{};{}m{}\033[0m".format(self.pattern, self.fground, self.bground, self.strings)
        return self.combine

class BackColor(Color):

    def backblack(self):
        self.bground = 40

    def backred(self):
        self.bground = 41

    def backgreen(self):
        self.bground = 42

    def backyellow(self):
        self.bground = 43

    def backblue(self):
        self.bground = 44

    def backmagenta(self):
        self.bground = 45

    def backcyan(self):
        self.bground = 46

    def backwhite(self):
        self.bground = 47

    def excute(self):
        self.combine = "\033[{};{};{}m{}\033[0m".format(self.pattern, self.fground, self.bground, self.strings)
        return self.combine


class ModeColor(Color):

    def default(self):
        self.pattern = 0

    def highlight(self):
        self.pattern = 1

    def underline(self):
        self.pattern = 4

    def twinkle(self):
        self.pattern = 5

    def hide(self):
        self.pattern = 8

    def excute(self):
        self.combine = "\033[{};{};{}m{}\033[0m".format(self.pattern, self.fground, self.bground, self.strings)
        return self.combine

class Use(ForeColor, BackColor, ModeColor):
    pass

