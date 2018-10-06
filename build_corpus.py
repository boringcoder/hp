#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import sys
import re
import random
import textwrap

replacement = {}

def init_data(path):
    list = os.listdir(path)
    for i in range(0,len(list)):
        file = os.path.join(path, list[i])
        if os.path.isfile(file):
            with open(file, 'rt') as f:
                lines = f.readlines()
                new_lines = []
                for line in lines:
                    line = line.replace('[', ' ').replace(']', ' ')
                    new_lines.append(line)
            replacement[list[i]] = new_lines
    #print (replacement)
    return replacement

def replace(line, replacement, num):
    if num == 'all':
        replace_all(line, replacement)
    else:
        num = int(num)
        replace_random(line, replacement, num)

def replace_all(line, replacement):
    temp = set([line])
    while len(temp) > 0:
        str = temp.pop()
        first = re.findall(r'\[(.+?)\]', str)[0]
        for i in range(0, len(replacement[first])):
            sentence = str.replace('['+first+']', replacement[first][i].strip())
            if (len(re.findall(r'\[(.+?)\]', sentence)) == 0):
                output.write(sentence+'\n')
            else:
                temp.update([sentence])

def replace_random(line, replacement, num):
    for x in range(0, num):
        temp = set([line])
        while len(temp) > 0:
            str = temp.pop()
            first = re.findall(r'\[(.+?)\]', str)[0]
            sentence = str.replace('['+first+']', replacement[first][random.randint(0, len(replacement[first]) - 1)].strip())
            if (len(re.findall(r'\[(.+?)\]', sentence)) == 0):
                output.write(sentence+'\n')
            else:
                temp.update([sentence])


if __name__ == '__main__':
    if (len(sys.argv) != 3) or (not os.path.isfile(sys.argv[1])) or (not os.path.exists(sys.argv[2])):
        print ('Usage: python %s template_file replacement_path'%sys.argv[0])
        sys.exit(1)
    template = sys.argv[1]
    path = sys.argv[2]
    
    print ('\ninit data ...')
    replacement = init_data(path)
    print ('''init data finished\n
以下将显示每一个句式及遍历时组成的句数,你可以输入一个数字以代表你想要随机生成的语料数或者输入"all"遍历生成语句\n''')
    output = open('result', 'w')
    log_out = open('log', 'w')
    with open(template, 'rt') as f:
        line = f.readline().strip()             
        while line:
            list = re.findall(r'\[(.+?)\]', line)
            max_num = eval('*'.join(str(len(replacement[list[i]])) for i in range(0, len(list))))
            print ('Template:'+line.strip())
            print ('Max Num:'+",".join(textwrap.wrap(str(max_num)[::-1], 3))[::-1])
            while True:
                num = raw_input('Enter your input: ')
                if num == 'all':
                    break
                else:
                    try:
                        num == int(num)
                        break
                    except (Exception):
                        print ('你必须输入一个数字或者"all"')
            log_out.write(line+'\t'+('all:'+str(max_num) if (num == 'all') else num)+'\n')
            replace(line, replacement, num)
            line = f.readline().strip()
            print ('\n')
    output.close()
