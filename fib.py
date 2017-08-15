#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys


def get_10(c):
    return ord(c) - ord('0')


def add_one_bit(n1, n2, n3=0):
    a = get_10(n1)
    b = get_10(n2)

    sum = a + b + n3

    yu = sum % 10
    shang = (sum - yu) / 10

    return str(yu), shang


def add(n1, n2):
    l1 = len(n1)
    l2 = len(n2)

    s1 = n1
    s2 = n2
    if l1 > l2:
        s1 = n2
        s2 = n1

    l1 = len(s1)
    l2 = len(s2)

    sum = []
    shang = 0
    for i in range(l1):
        c, shang = add_one_bit(s1[l1 - 1 - i], s2[l2 - 1 - i], shang)
        sum.append(c)

    for i in range(l1, l2):
        c, shang = add_one_bit('0', s2[l2 - 1 - i], shang)
        sum.append(c)
    if shang > 0:
        sum.append(str(shang))

    for i in range(len(sum) / 2):
        tmp = sum[i]
        sum[i] = sum[len(sum) - 1 - i]
        sum[len(sum) - 1 - i] = tmp
    return sum


def mul(n1, n2):
    l = len(n1)
    sum = []
    for i in range(l):
        v = get_10(n1[i])
        if v > 0:
            sum_tmp = n2
            for j in range(l - 1 - i):
                sum_tmp += "0"
            add_v = sum_tmp
            for j in range(1, v):
                sum_tmp = add(sum_tmp, add_v)
            if i == 0:
                sum = sum_tmp
            else:
                sum = add(sum, sum_tmp)
    return sum


def sub_one_bit(n1, n2, n3):
    a = get_10(n1)
    b = get_10(n2)

    sub = a - b - n3

    jie = 0
    while sub < 0:
        jie += 1
        sub += 10
    return str(sub), jie


def large(n1, n2):
    if len(n1) > len(n2):
        return True
    elif len(n1) < len(n2):
        return False
    else:
        for i in range(len(n1)):
            if ord(n1[i]) >= ord(n2[i]):
                return True
        return False


def sub(n1, n2):
    s1 = n1
    s2 = n2
    flag = False
    if not large(n1, n2):
        s1 = n2
        s2 = n1
        flag = True

    l1 = len(s1)
    l2 = len(s2)

    sub = []
    jie = 0
    for i in range(l2):
        c, jie = sub_one_bit(s1[l1 - 1 - i], s2[l2 - 1 - i], jie)
        sub.append(c)

    has_jie = 0
    if jie > 0:
        c, jie = sub_one_bit(n1[l2 - 1 - l1], str(jie), 0)
        sub.append(c)
        has_jie = 1

    while has_jie < l1 - l2:
        sub.append(s1[l1 - l2 - 1 - has_jie])
        has_jie += 1

    if flag:
        sub.append('-')

    for i in range(len(sub) / 2):
        tmp = sub[i]
        sub[i] = sub[len(sub) - 1 - i]
        sub[len(sub) - 1 - i] = tmp
    return sub


def div(n1, n2):
    return "Todo..."


def calc(n1, op, n2):
    if op == '+':
        return add(n1, n2)
    elif op == '-':
        return sub(n1, n2)
    elif op == '*':
        return mul(n1, n2)
    elif op == '/':
        return div(n1, n2)
    else:
        return "unsupported operation"


if __name__ == '__main__':
    length = 30
    x = [0] * length
    y = [0] * length
    for i in range(length):
        if i == 0:
            x[i] = 1
            y[i] = 1
        else:
            x[i] = 3 * x[i - 1] + 4 * y[i - 1]
            y[i] = 2 * x[i - 1] + 3 * y[i - 1]
    xx = [str(i * 10000000000) for i in x]
    a = [0] * length
    for i in range(length):
        a[i] = str(int((x[i] ** 0.5)*100000))
        temp = ''.join(mul(a[i],a[i]))
        while temp<xx[i]:
            print a[i],xx[i]
            a[i] = add(a[i],'1')
            temp = ''.join(mul(a[i], a[i]))
        if a[i][-5:]=='00000':
            a[i]=a[i][:-5]
        else:
            a[i]=a[i][:-5]+'.'+a[i][-5:]
        print a[i]
    print a
