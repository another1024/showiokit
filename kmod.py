#!/usr/bin/python
#coding:utf-8

import lldb

class kmod:
    ci=None
    res=None
	
    def __init__(self):
        self.ci = lldb.debugger.GetCommandInterpreter()
        self.res = lldb.SBCommandReturnObject()
    def getsize(self,addr,size):
	
        if(size==4):
            c='w'
        elif(size==8):
            c='g'

        self.ci.HandleCommand('x/x'+c+' '+hex(addr),self.res)
        s=self.res.GetOutput()
        s=s.split(': ')[1]
        r=int(s[2:],16)
        return r
    def gets(self,addr):
        self.ci.HandleCommand('x/s '+hex(addr),self.res)
        r=self.res.GetOutput().split(': ')[1]
        return r
        
    def work(self,addr):
        addr=self.getsize(addr,8)
        addr+=4
        size=self.getsize(addr,4)
        addr+=4
        number=self.getsize(addr,4)
        addr+=0x8
        

        for i in range(0,number):
            r=self.gets(addr)
            addr+=0x50
            r+=hex(self.getsize(addr,8))
            print (r)
         
            addr+=size-0x50
# Super breakpoint
def getkmod(debugger, command, result, internal_dict):

    k = kmod()

    if not command:
        print  ('Please input the address!')
        return
    
    arg = command.split(' ')
    arg = [x for x in arg if x != '']
    print (arg)
    k=kmod()
    
    addr=int(arg[0],16)-int(arg[1],16)+int(arg[2],16)

    k.work(addr)
    

    
# And the initialization code to add your commands
def __lldb_init_module(debugger, internal_dict):

    debugger.HandleCommand('command script add kmod -f kmod.getkmod')
  
# 0xFFFFFF8000200000 0xFFFFFF8000E23260
