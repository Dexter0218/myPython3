#!/usr/bin/env python

import os
import random
import string


def radom_generate():
	string = ''
	for n in range(1,9):
		number = int(random.uniform(0,9))
		string += str(number) 
	string += '\n'
	return	string 

def file_write(num=5):
    fp = open("result.txt",'w')
    for n in range(1,num+1):
        string = radom_generate()
        fp.write(string)  
    fp.close() 

forSelect = string.ascii_uppercase + string.digits

def generate_code(count=100, length=10):
    fp = open("result2.txt",'w')
    for x in range(count):
        Re = ""
        for y in range(length):
            Re += random.choice(forSelect)
            if ((y+1)< length) & ((y+1) % 4 == 0):
                Re += '-'
        print(Re)
        Re += '\n'
        fp.write(Re)
    fp.close() 
if __name__ == '__main__':
    file_write()
    generate_code(100,16)
