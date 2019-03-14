# -*- coding: utf-8 -*-
import commands
import os

base_path = os.getcwd()

file_list = [
    [base_path + '/sjtu.py', 'sjtu'],
    [base_path + '/fudan.py', 'fudan'],
    [base_path + '/nju.py', 'nju'],
    [base_path + '/newsmth.py', 'newsmth'],
    [base_path + '/picture.py', 'picture'],
]
for (file_name, school) in file_list:
    print "school:%s, file:%s" % (school, file_name)
    (status, output) = commands.getstatusoutput('python %s' % (file_name, ))
    print "status: %d" % (status, )
    print "output: %s" % (output, )
