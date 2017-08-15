# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Crypto.Cipher import AES

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

key = '2990E4BD95E99C35G711D37211143503CB08111610EE3D98AC0DE41E73E9BDE5'

key = key[:16]
print 'key: %s' % key

mode = AES.MODE_ECB

# key='[B@de0a01f'

mobile = range(23000000001, 23000300000)
texts = [unicode(i) for i in mobile]
# texts = ['10000074998']
# text+= '1472529221964'
# text += str(int(time()))

# print 'text: %s' % text
result = []
for text in texts:
    cipher = AES.new(key, mode)

    encrypted = cipher.encrypt(pad(text)).encode('hex')
    # result.append(encrypted)

    if encrypted == 'a829a5e4350e5bda09f04899af326242':
        print True
    cipher2 = AES.new(key, mode)
    decrypted = unpad(cipher2.decrypt(encrypted.decode('hex')))
    # print decrypted
    result.append(decrypted)
# print result
with open(r"mobile.txt", str('a')) as f:
    for x in result:
        f.write(str(x+str('\n')))
