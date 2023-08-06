#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/05/05 11:25
# @Author  : niuliangtao
# @Site    : 
# @File    : temp.py
# @Software: PyCharm

import re
s = "感谢注册Tushare社区用户，验证码917601，5分钟内有效。"
pat = "验证码([0-9]{6})"
m = re.search(pat, s)
if m:
    print( m.group(1))
else:
    print( "没有找到数字")

