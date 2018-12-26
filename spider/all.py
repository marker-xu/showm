# -*- coding: utf-8 -*-
import commands


file_list = [
    ['/Users/baidu/www/app/ai/showx/test/sjtu.py', 'sjtu'],
    ['/Users/baidu/www/app/ai/showx/test/fudan.py', 'fudan'],
    ['/Users/baidu/www/app/ai/showx/test/nju.py', 'nju'],
    ['/Users/baidu/www/app/ai/showx/test/newsmth.py', 'newsmth'],
]
for (file_name, school) in file_list:
    print "school:%s, file:%s" % (school, file_name)
    (status, output) = commands.getstatusoutput('python %s' % (file_name, ))
    print "status: %d" % (status, )
    print "output: %s" % (output, )
