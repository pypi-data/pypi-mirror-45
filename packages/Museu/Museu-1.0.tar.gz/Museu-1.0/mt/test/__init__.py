#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-18 11:25:53
# @Author  : Blackstone
# @to      :

import re

sqlstr="{fdsafad}"
fasf=re.findall(r"{.*?}", sqlstr)
print(fasf)