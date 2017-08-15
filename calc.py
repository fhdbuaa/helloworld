# -*- coding: utf-8 -*-
import math


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


def sqr(n):
    if n == 1:
        return '1'
    temp = str(n)
    s = str(int(int(temp[:len(temp) % 2 + 2]) ** 0.5))
    m = len(temp) % 2 + 2
    while True:
        for i in range(9, -1, -1):
            cal = int(temp[:m+2])
            if m+2>len(temp):
                cal = n*10**(m+2-len(temp))
            if int(''.join(mul(s + str(i), s + str(i)))) < cal:
                s += str(i)
                m+=2
                break
        if len(s) > len(temp) / 2 + 10:
            break
    a = int((len(temp) + 1) / 2)
    return s[:a] + '.' + s[a:]


length = 1000
x = [0] * length
y = [0] * length
for i in range(length):
    if i == 0:
        x[i] = 1
        y[i] = 1
    else:
        x[i] = 3 * x[i - 1] + 4 * y[i - 1]
        y[i] = 2 * x[i - 1] + 3 * y[i - 1]
print sqr('1001047369445486500122677053453007')
with open('calcss.txt', 'a') as log:
    for i in x:
        temp = str(i) + ',' + sqr(i) + '\r\n'
        print temp
        log.write(temp)
